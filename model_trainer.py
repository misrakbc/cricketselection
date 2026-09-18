"""
model_trainer.py
Trains predictive selection models and extracts coach archetype preference scorecards.
- Logistic Regression with Coach * Feature interaction effects (Odds Ratios)
- Random Forest Classifier for non-linear selection rules
- Empirical Coach Playing-XI Composition Scorecard
"""

import os
import pickle
import json
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import roc_auc_score, accuracy_score, classification_report, log_loss
from sklearn.model_selection import StratifiedKFold

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
PROCESSED_DIR = os.path.join(DATA_DIR, "processed")
MODELS_DIR = os.path.join(DATA_DIR, "models")

# Key modern coaches with sufficient sample size
MAJOR_COACHES = [
    'Gary Kirsten',
    'Duncan Fletcher',
    'Anil Kumble',
    'Ravi Shastri (Head Coach)',
    'Rahul Dravid',
    'Gautam Gambhir'
]

def load_data():
    df = pd.read_pickle(os.path.join(PROCESSED_DIR, "selection_dataset.pkl"))
    # Filter for major coaches or consolidate Shastri
    # Let's map Ravi Shastri (Team Director) and Ravi Shastri (Head Coach)
    df['coach_group'] = df['coach'].replace({
        'Ravi Shastri (Team Director)': 'Ravi Shastri',
        'Ravi Shastri (Head Coach)': 'Ravi Shastri'
    })
    return df

def analyze_empirical_compositions(df_matches, df_perfs):
    """
    Computes exact empirical Playing XI compositions for each coach:
    - Number of pace vs spin bowlers
    - Number of all-rounders
    - Number of Left-Hand Batters (LHBs)
    - Average experience (caps)
    - Home vs SENA tactical shifts
    """
    from player_metadata import get_player_profile, PLAYER_ARCHETYPES
    
    print("\n--- Computing Empirical Coach Playing-XI Compositions ---")
    
    # We can inspect df_matches with players in india_xi
    results = []
    
    for idx, row in df_matches.iterrows():
        coach = row['coach']
        m_type = row['match_type']
        is_home = row['is_home']
        is_sena = row['is_sena']
        xi = row['india_xi']
        
        profiles = [get_player_profile(p) for p in xi]
        
        num_lhb = sum(1 for p in profiles if p['hand'] == 'LHB')
        num_pace_ar = sum(1 for p in profiles if p['role'] == 'Pace All-Rounder')
        num_spin_ar = sum(1 for p in profiles if p['role'] == 'Spin All-Rounder')
        num_allrounders = num_pace_ar + num_spin_ar
        num_fast_bowlers = sum(1 for p in profiles if p['role'] == 'Specialist Fast Bowler')
        num_spin_bowlers = sum(1 for p in profiles if p['role'] == 'Specialist Spin Bowler')
        num_left_arm_pacers = sum(1 for p in profiles if p['arm'] == 'Left' and 'Fast' in p['bowling'] or p['bowling'] == 'Pace')
        num_wrist_spinners = sum(1 for p in profiles if p['bowling'] == 'Wrist Spin')
        num_finger_spinners = sum(1 for p in profiles if p['bowling'] in ['Finger Spin', 'Left-Arm Orthodox'])
        
        results.append({
            'coach': coach,
            'match_type': m_type,
            'is_home': is_home,
            'is_sena': is_sena,
            'num_lhb': num_lhb,
            'num_allrounders': num_allrounders,
            'num_pace_ar': num_pace_ar,
            'num_spin_ar': num_spin_ar,
            'num_fast_bowlers': num_fast_bowlers,
            'num_spin_bowlers': num_spin_bowlers,
            'num_left_arm_pacers': num_left_arm_pacers,
            'num_wrist_spinners': num_wrist_spinners,
            'num_finger_spinners': num_finger_spinners
        })
        
    df_comp = pd.DataFrame(results)
    
    # Filter for main coaching eras
    target_coaches = [
        'Gary Kirsten', 'Duncan Fletcher', 'Anil Kumble',
        'Ravi Shastri (Head Coach)', 'Rahul Dravid', 'Gautam Gambhir'
    ]
    df_comp_target = df_comp[df_comp['coach'].isin(target_coaches)]
    
    summary = df_comp_target.groupby('coach').agg({
        'num_allrounders': 'mean',
        'num_pace_ar': 'mean',
        'num_spin_ar': 'mean',
        'num_fast_bowlers': 'mean',
        'num_spin_bowlers': 'mean',
        'num_left_arm_pacers': 'mean',
        'num_wrist_spinners': 'mean',
        'num_finger_spinners': 'mean',
        'num_lhb': 'mean'
    }).round(2)
    
    print("\nEmpirical Average Team Composition per Match (Playing XI of 11):")
    print(summary.to_string())
    
    summary_path = os.path.join(PROCESSED_DIR, "coach_empirical_composition.csv")
    summary.to_csv(summary_path)
    return summary

def train_interaction_logistic_regression(df):
    """
    Fits Logistic Regression with Coach * Archetype Interaction terms.
    Extracts Odds Ratios for each coach's preference relative to baseline.
    """
    print("\n--- Training Coach-Interaction Logistic Regression Model ---")
    
    # Filter to main coaches for clean statistical inference
    coaches_to_use = [
        'Gary Kirsten',
        'Duncan Fletcher',
        'Ravi Shastri (Head Coach)',
        'Rahul Dravid',
        'Gautam Gambhir'
    ]
    df_sub = df[df['coach'].isin(coaches_to_use)].copy()
    
    # Features
    base_num_features = [
        'recent_caps_1y', 'recent_format_caps_1y', 'career_caps',
        'recent_bat_avg_1y', 'recent_bat_sr_1y', 'recent_bowl_econ_1y', 'recent_wickets_1y',
        'is_home', 'is_sena'
    ]
    
    archetype_features = [
        'is_top_order', 'is_middle_order', 'is_wk',
        'is_pace_ar', 'is_spin_ar', 'is_spec_pace', 'is_spec_spin',
        'is_lhb', 'is_left_arm_pacer', 'is_wrist_spinner'
    ]
    
    # Impute NaNs if any
    for col in base_num_features:
        df_sub[col] = df_sub[col].fillna(df_sub[col].median())
        
    scaler = StandardScaler()
    scaled_num = scaler.fit_transform(df_sub[base_num_features])
    df_scaled = pd.DataFrame(scaled_num, columns=base_num_features, index=df_sub.index)
    
    # One-hot encode coach and format
    coach_dummies = pd.get_dummies(df_sub['coach'], prefix='coach', drop_first=False, dtype=float)
    fmt_dummies = pd.get_dummies(df_sub['match_type'], prefix='fmt', drop_first=True, dtype=float)
    
    # Interaction terms: Coach * Archetype
    interaction_dfs = []
    for c_col in coach_dummies.columns:
        coach_name = c_col.replace('coach_', '')
        for arch in archetype_features:
            inter_col_name = f"{coach_name}_X_{arch}"
            inter_series = coach_dummies[c_col] * df_sub[arch]
            interaction_dfs.append(pd.Series(inter_series, name=inter_col_name))
            
    df_interactions = pd.concat(interaction_dfs, axis=1)
    
    # Full design matrix
    X = pd.concat([
        df_scaled,
        df_sub[archetype_features],
        fmt_dummies,
        coach_dummies,
        df_interactions
    ], axis=1)
    
    y = df_sub['selected'].values
    
    model = LogisticRegression(max_iter=1500, C=0.5, penalty='l2', solver='lbfgs')
    model.fit(X, y)
    
    preds_proba = model.predict_proba(X)[:, 1]
    auc = roc_auc_score(y, preds_proba)
    acc = accuracy_score(y, model.predict(X))
    print(f"Interaction Logistic Regression Fitted successfully!")
    print(f"Train AUC-ROC: {auc:.4f} | Accuracy: {acc:.4f} | Log-Loss: {log_loss(y, preds_proba):.4f}")
    
    # Extract coach-specific archetype coefficients
    coef_dict = dict(zip(X.columns, model.coef_[0]))
    
    coach_archetype_odds = {}
    for coach_name in coaches_to_use:
        coach_archetype_odds[coach_name] = {}
        for arch in archetype_features:
            inter_col = f"{coach_name}_X_{arch}"
            # Total log-odds contribution for this coach on this archetype:
            # base archetype coefficient + coach interaction coefficient
            log_odds = coef_dict.get(arch, 0.0) + coef_dict.get(inter_col, 0.0)
            odds_ratio = round(np.exp(log_odds), 2)
            coach_archetype_odds[coach_name][arch] = odds_ratio
            
    df_odds = pd.DataFrame(coach_archetype_odds).round(2)
    print("\nArchetype Selection Odds Multipliers across Coaches (Odds Ratio > 1.0 = Coach Favors):")
    print(df_odds.to_string())
    
    df_odds.to_csv(os.path.join(PROCESSED_DIR, "coach_archetype_odds_ratios.csv"))
    
    return model, scaler, X.columns.tolist(), df_odds

def train_gradient_boost_classifier(df):
    """
    Trains a Random Forest Classifier to evaluate non-linear selection dynamics.
    Calculates overall generalization AUC across cross-validation folds.
    """
    print("\n--- Training Non-Linear Ensemble Classifier (Random Forest) ---")
    
    target_coaches = [
        'Gary Kirsten', 'Duncan Fletcher', 'Anil Kumble',
        'Ravi Shastri (Head Coach)', 'Rahul Dravid', 'Gautam Gambhir'
    ]
    df_sub = df[df['coach'].isin(target_coaches)].copy()
    
    features = [
        'is_top_order', 'is_middle_order', 'is_wk',
        'is_pace_ar', 'is_spin_ar', 'is_spec_pace', 'is_spec_spin',
        'is_lhb', 'is_left_arm_pacer', 'is_wrist_spinner', 'is_finger_spinner',
        'recent_caps_1y', 'recent_format_caps_1y', 'career_caps',
        'recent_bat_avg_1y', 'recent_bat_sr_1y', 'recent_bowl_econ_1y', 'recent_wickets_1y',
        'is_home', 'is_sena'
    ]
    
    for col in features:
        df_sub[col] = df_sub[col].fillna(df_sub[col].median())
        
    # Categoricals
    coach_enc = pd.get_dummies(df_sub['coach'], prefix='coach', dtype=float)
    fmt_enc = pd.get_dummies(df_sub['match_type'], prefix='fmt', dtype=float)
    
    X = pd.concat([df_sub[features], coach_enc, fmt_enc], axis=1)
    y = df_sub['selected'].values
    
    # 5-Fold Stratified Cross-Validation
    skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    cv_scores = []
    
    for train_idx, val_idx in skf.split(X, y):
        X_tr, X_val = X.iloc[train_idx], X.iloc[val_idx]
        y_tr, y_val = y[train_idx], y[val_idx]
        
        clf = RandomForestClassifier(n_estimators=150, max_depth=10, min_samples_leaf=5, random_state=42, n_jobs=-1)
        clf.fit(X_tr, y_tr)
        val_proba = clf.predict_proba(X_val)[:, 1]
        cv_scores.append(roc_auc_score(y_val, val_proba))
        
    print(f"5-Fold Cross-Validation AUC-ROC: {np.mean(cv_scores):.4f} +/- {np.std(cv_scores):.4f}")
    
    # Fit full model
    final_rf = RandomForestClassifier(n_estimators=200, max_depth=12, min_samples_leaf=5, random_state=42, n_jobs=-1)
    final_rf.fit(X, y)
    
    feat_imp = pd.Series(final_rf.feature_importances_, index=X.columns).sort_values(ascending=False)
    print("\nTop 15 Feature Importances in Selection:")
    print(feat_imp.head(15).round(4).to_string())
    
    feat_imp.to_csv(os.path.join(PROCESSED_DIR, "feature_importances.csv"))
    
    return final_rf, X.columns.tolist()

def save_artifacts(log_reg, scaler, log_cols, rf_model, rf_cols):
    os.makedirs(MODELS_DIR, exist_ok=True)
    
    artifacts = {
        'log_reg': log_reg,
        'scaler': scaler,
        'log_cols': log_cols,
        'rf_model': rf_model,
        'rf_cols': rf_cols
    }
    with open(os.path.join(MODELS_DIR, "trained_models.pkl"), "wb") as f:
        pickle.dump(artifacts, f)
        
    print(f"\nAll models and scalers successfully saved to {os.path.join(MODELS_DIR, 'trained_models.pkl')}")

if __name__ == "__main__":
    from feature_builder import assign_coach
    df_sel = load_data()
    df_matches = pd.read_pickle(os.path.join(PROCESSED_DIR, "matches.pkl"))
    df_perfs = pd.read_pickle(os.path.join(PROCESSED_DIR, "player_performances.pkl"))
    df_matches['coach'] = df_matches['date'].apply(assign_coach)
    
    # 1. Empirical composition breakdown
    analyze_empirical_compositions(df_matches, df_perfs)
    
    # 2. Logistic regression with interaction terms
    log_reg, scaler, log_cols, df_odds = train_interaction_logistic_regression(df_sel)
    
    # 3. Random Forest non-linear classifier
    rf_model, rf_cols = train_gradient_boost_classifier(df_sel)
    
    # 4. Save artifacts
    save_artifacts(log_reg, scaler, log_cols, rf_model, rf_cols)
    print("\nModel training and scorecard evaluation complete!")
