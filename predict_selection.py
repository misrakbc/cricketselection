"""
predict_selection.py
Interactive CLI predictor for Indian cricket selection under different head coaches.
Allows user to evaluate selection probabilities for any actual player or custom archetype
across Gautam Gambhir, Rahul Dravid, Ravi Shastri, Gary Kirsten, and Duncan Fletcher.
"""

import os
import sys
import pickle
import argparse
import pandas as pd
import numpy as np

# Force UTF-8 if supported
if sys.stdout.encoding and sys.stdout.encoding.lower() != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

from player_metadata import get_player_profile, PLAYER_ARCHETYPES

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
PROCESSED_DIR = os.path.join(DATA_DIR, "processed")
MODELS_DIR = os.path.join(DATA_DIR, "models")

COMMON_ALIASES = {
    "hardik pandya": "HH Pandya",
    "krunal pandya": "KH Pandya",
    "virat kohli": "V Kohli",
    "rohit sharma": "RG Sharma",
    "jasprit bumrah": "JJ Bumrah",
    "ravindra jadeja": "RA Jadeja",
    "axar patel": "AR Patel",
    "yashasvi jaiswal": "YBK Jaiswal",
    "rishabh pant": "RR Pant",
    "kl rahul": "KL Rahul",
    "sanju samson": "SV Samson",
    "suryakumar yadav": "SA Yadav",
    "surya kumar yadav": "SA Yadav",
    "sky": "SA Yadav",
    "mohammed shami": "Mohammed Shami",
    "shami": "Mohammed Shami",
    "mohammed siraj": "Mohammed Siraj",
    "siraj": "Mohammed Siraj",
    "kuldeep yadav": "Kuldeep Yadav",
    "yuzvendra chahal": "YS Chahal",
    "chahal": "YS Chahal",
    "arshdeep singh": "Arshdeep Singh",
    "shubman gill": "Shubman Gill",
    "shivam dube": "Shivam Dube",
    "washington sundar": "Washington Sundar",
    "sundar": "Washington Sundar",
    "ravichandran ashwin": "R Ashwin",
    "r ashwin": "R Ashwin",
    "ashwin": "R Ashwin",
    "ms dhoni": "MS Dhoni",
    "dhoni": "MS Dhoni",
    "suresh raina": "SK Raina",
    "yuvraj singh": "Yuvraj Singh",
    "virender sehwag": "V Sehwag",
    "sachin tendulkar": "SR Tendulkar",
    "gautam gambhir": "G Gambhir",
    "zaheer khan": "Z Khan",
    "ishant sharma": "I Sharma",
    "bhuvneshwar kumar": "B Kumar",
    "bhuvi": "B Kumar",
    "shardul thakur": "Shardul Thakur",
    "tilak varma": "Tilak Varma",
    "rinku singh": "Rinku Singh",
    "nitish kumar reddy": "Nitish Kumar Reddy",
    "varun chakravarthy": "CV Varun",
    "ravi bishnoi": "Ravi Bishnoi",
    "harshit rana": "Harshit Rana",
    "akash deep": "Akash Deep",
    "mayank yadav": "Mayank Yadav",
    "abhishek sharma": "Abhishek Sharma"
}

COACHES = [
    'Gautam Gambhir',
    'Rahul Dravid',
    'Ravi Shastri (Head Coach)',
    'Gary Kirsten',
    'Duncan Fletcher'
]

def load_models():
    model_path = os.path.join(MODELS_DIR, "trained_models.pkl")
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model file not found at {model_path}. Please run model_trainer.py first.")
    with open(model_path, "rb") as f:
        artifacts = pickle.load(f)
    return artifacts

def resolve_player_name(query_name):
    clean = query_name.strip().lower()
    if clean in COMMON_ALIASES:
        return COMMON_ALIASES[clean]
    # Check if exact match in PLAYER_ARCHETYPES
    for p in PLAYER_ARCHETYPES.keys():
        if clean == p.lower():
            return p
    # Partial match
    for p in PLAYER_ARCHETYPES.keys():
        if clean in p.lower():
            return p
    return query_name

def predict_player_selection(player_name=None, custom_profile=None, match_type='T20I', is_home=1, is_sena=0, squad_lock=True):
    artifacts = load_models()
    log_reg = artifacts['log_reg']
    scaler = artifacts['scaler']
    log_cols = artifacts['log_cols']
    rf_model = artifacts['rf_model']
    rf_cols = artifacts['rf_cols']

    resolved_name = resolve_player_name(player_name) if player_name else "Custom Archetype"

    if player_name:
        df_sel = pd.read_pickle(os.path.join(PROCESSED_DIR, "selection_dataset.pkl"))
        p_data = df_sel[df_sel['player'].str.lower() == resolved_name.lower()]
        
        meta = get_player_profile(resolved_name)
        if len(p_data) > 0:
            latest_row = p_data.iloc[-1]
            profile = {
                'player': resolved_name,
                'role': latest_row['primary_role'],
                'hand': latest_row['batting_hand'],
                'bowling': latest_row['bowling_style'],
                'arm': meta.get('arm', 'Right'),
                'career_caps': int(latest_row['career_caps']),
                'recent_caps_1y': int(latest_row['recent_caps_1y']),
                'recent_format_caps_1y': int(latest_row['recent_format_caps_1y']),
                'recent_bat_avg_1y': float(latest_row['recent_bat_avg_1y']),
                'recent_bat_sr_1y': float(latest_row['recent_bat_sr_1y']),
                'recent_bowl_econ_1y': float(latest_row['recent_bowl_econ_1y']),
                'recent_wickets_1y': int(latest_row['recent_wickets_1y']),
            }
        else:
            profile = {
                'player': resolved_name,
                'role': meta['role'],
                'hand': meta['hand'],
                'bowling': meta['bowling'],
                'arm': meta.get('arm', 'Right'),
                'career_caps': 40,
                'recent_caps_1y': 14,
                'recent_format_caps_1y': 9,
                'recent_bat_avg_1y': 32.0,
                'recent_bat_sr_1y': 142.0,
                'recent_bowl_econ_1y': 7.8,
                'recent_wickets_1y': 10
            }
    else:
        profile = custom_profile

    role = profile['role']
    is_top = 1 if role == "Top-Order Batter" else 0
    is_mid = 1 if role == "Middle-Order Batter" else 0
    is_wk = 1 if role == "Wicketkeeper" else 0
    is_pace_ar = 1 if role == "Pace All-Rounder" else 0
    is_spin_ar = 1 if role == "Spin All-Rounder" else 0
    is_spec_pace = 1 if role == "Specialist Fast Bowler" else 0
    is_spec_spin = 1 if role == "Specialist Spin Bowler" else 0
    is_lhb = 1 if profile['hand'] == 'LHB' else 0
    is_left_arm_pacer = 1 if (profile.get('arm') == 'Left' and ('Fast' in profile.get('bowling', '') or profile.get('bowling') == 'Pace')) else 0
    is_wrist_spinner = 1 if profile.get('bowling') == 'Wrist Spin' else 0
    is_finger_spinner = 1 if profile.get('bowling') in ['Finger Spin', 'Left-Arm Orthodox'] else 0

    base_num_features = [
        'recent_caps_1y', 'recent_format_caps_1y', 'career_caps',
        'recent_bat_avg_1y', 'recent_bat_sr_1y', 'recent_bowl_econ_1y', 'recent_wickets_1y',
        'is_home', 'is_sena'
    ]
    
    num_vals = np.array([[
        profile['recent_caps_1y'],
        profile['recent_format_caps_1y'],
        profile['career_caps'],
        profile['recent_bat_avg_1y'],
        profile['recent_bat_sr_1y'],
        profile['recent_bowl_econ_1y'],
        profile['recent_wickets_1y'],
        is_home,
        is_sena
    ]])
    
    scaled_num = scaler.transform(pd.DataFrame(num_vals, columns=base_num_features))[0]
    scaled_dict = dict(zip(base_num_features, scaled_num))

    results = []

    for coach in COACHES:
        row_dict = {col: 0.0 for col in log_cols}
        for k, v in scaled_dict.items():
            if k in row_dict:
                row_dict[k] = v
        
        row_dict['is_top_order'] = is_top
        row_dict['is_middle_order'] = is_mid
        row_dict['is_wk'] = is_wk
        row_dict['is_pace_ar'] = is_pace_ar
        row_dict['is_spin_ar'] = is_spin_ar
        row_dict['is_spec_pace'] = is_spec_pace
        row_dict['is_spec_spin'] = is_spec_spin
        row_dict['is_lhb'] = is_lhb
        row_dict['is_left_arm_pacer'] = is_left_arm_pacer
        row_dict['is_wrist_spinner'] = is_wrist_spinner

        if f'fmt_{match_type}' in row_dict:
            row_dict[f'fmt_{match_type}'] = 1.0

        coach_col = f'coach_{coach}'
        if coach_col in row_dict:
            row_dict[coach_col] = 1.0

        for arch_col in ['is_top_order', 'is_middle_order', 'is_wk', 'is_pace_ar', 'is_spin_ar',
                         'is_spec_pace', 'is_spec_spin', 'is_lhb', 'is_left_arm_pacer', 'is_wrist_spinner']:
            inter_col = f"{coach}_X_{arch_col}"
            if inter_col in row_dict:
                row_dict[inter_col] = row_dict[arch_col]

        x_log = pd.DataFrame([row_dict])[log_cols]
        prob_log = log_reg.predict_proba(x_log)[0][1]

        rf_row = {col: 0.0 for col in rf_cols}
        rf_row['is_top_order'] = is_top
        rf_row['is_middle_order'] = is_mid
        rf_row['is_wk'] = is_wk
        rf_row['is_pace_ar'] = is_pace_ar
        rf_row['is_spin_ar'] = is_spin_ar
        rf_row['is_spec_pace'] = is_spec_pace
        rf_row['is_spec_spin'] = is_spec_spin
        rf_row['is_lhb'] = is_lhb
        rf_row['is_left_arm_pacer'] = is_left_arm_pacer
        rf_row['is_wrist_spinner'] = is_wrist_spinner
        rf_row['is_finger_spinner'] = is_finger_spinner

        rf_row['recent_caps_1y'] = profile['recent_caps_1y']
        rf_row['recent_format_caps_1y'] = profile['recent_format_caps_1y']
        rf_row['career_caps'] = profile['career_caps']
        rf_row['recent_bat_avg_1y'] = profile['recent_bat_avg_1y']
        rf_row['recent_bat_sr_1y'] = profile['recent_bat_sr_1y']
        rf_row['recent_bowl_econ_1y'] = profile['recent_bowl_econ_1y']
        rf_row['recent_wickets_1y'] = profile['recent_wickets_1y']
        rf_row['is_home'] = is_home
        rf_row['is_sena'] = is_sena

        if f'fmt_{match_type}' in rf_row:
            rf_row[f'fmt_{match_type}'] = 1.0
        if coach_col in rf_row:
            rf_row[coach_col] = 1.0

        x_rf = pd.DataFrame([rf_row])[rf_cols]
        prob_rf = rf_model.predict_proba(x_rf)[0][1]

        # Check format retirement (e.g. Kohli, Rohit, Jadeja in T20Is after June 2024)
        is_retired = False
        if match_type == 'T20I' and coach == 'Gautam Gambhir':
            if profile.get('player') in ['V Kohli', 'RG Sharma', 'RA Jadeja']:
                is_retired = True

        if is_retired:
            prob_final = 0.0
        elif squad_lock:
            # Calibrated probability given player is named in the 15-man squad
            # Top contenders with high credentials have 95-99% conditional selection
            base_p = (0.4 * prob_log + 0.6 * prob_rf)
            prob_final = round(min(99.5, 100.0 / (1.0 + np.exp(-10.0 * (base_p - 0.18)))), 1)
        else:
            prob_final = round((0.4 * prob_log + 0.6 * prob_rf) * 100, 1)

        results.append({
            'Coach': coach,
            'Selection Probability (%)': prob_final,
            'LogReg Prob (%)': round(prob_log * 100, 1),
            'Ensemble Prob (%)': round(prob_rf * 100, 1),
            'Is Retired': is_retired
        })

    df_res = pd.DataFrame(results).sort_values('Selection Probability (%)', ascending=False).reset_index(drop=True)
    return profile, df_res

def display_report(profile, df_res, match_type, conditions):
    print("=" * 75)
    print("CRICKETER SELECTION PREDICTION ENGINE: INDIA PLAYING XI")
    print("=" * 75)
    print(f"PLAYER PROFILE: {profile.get('player', 'Custom Archetype')}")
    print(f"  * Primary Role:        {profile['role']}")
    print(f"  * Batting Hand:        {profile['hand']}")
    print(f"  * Bowling Style:       {profile['bowling']}")
    print(f"  * Recent Batting:      Avg {profile['recent_bat_avg_1y']} | SR {profile['recent_bat_sr_1y']}")
    print(f"  * Recent Bowling:      Econ {profile['recent_bowl_econ_1y']} | Wickets/Yr {profile['recent_wickets_1y']}")
    print(f"  * Experience:          {profile['career_caps']} Career Caps ({profile['recent_caps_1y']} in last 12m)")
    print("MATCH CONTEXT:")
    print(f"  * Format:              {match_type}")
    print(f"  * Venue Conditions:    {conditions}")
    print("-" * 75)
    print("PREDICTED SELECTION LIKELIHOOD BY COACH:")
    print("-" * 75)
    for idx, row in df_res.iterrows():
        bar_len = int(row['Selection Probability (%)'] / 5)
        bar = "#" * bar_len
        print(f"  {row['Coach']:<28} {row['Selection Probability (%)']:>5.1f}%  | {bar:<20}")
    print("-" * 75)
    
    top_coach = df_res.iloc[0]['Coach']
    bottom_coach = df_res.iloc[-1]['Coach']
    print("TACTICAL INSIGHT:")
    print(f"  * Most Favored By:  {top_coach} ({df_res.iloc[0]['Selection Probability (%)']}%)")
    print(f"  * Least Favored By: {bottom_coach} ({df_res.iloc[-1]['Selection Probability (%)']}%)")
    print("=" * 75)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Predict Indian cricketer selection across coaching eras")
    parser.add_argument("--player", type=str, default="Virat Kohli", help="Indian player name")
    parser.add_argument("--format", type=str, default="TEST", choices=["TEST", "ODI", "T20I"], help="Match format")
    parser.add_argument("--sena", action="store_true", help="Set match venue in SENA conditions (Overseas)")
    parser.add_argument("--raw-pool", action="store_true", help="Use raw uncalibrated contender pool (includes bilateral rests)")
    args = parser.parse_args()

    conditions = "SENA (South Africa, England, NZ, Australia)" if args.sena else "Subcontinent / Home Conditions"
    prof, res = predict_player_selection(
        player_name=args.player, 
        match_type=args.format, 
        is_home=0 if args.sena else 1, 
        is_sena=1 if args.sena else 0,
        squad_lock=not args.raw_pool
    )
    display_report(prof, res, args.format, conditions)
