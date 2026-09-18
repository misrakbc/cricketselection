"""
feature_builder.py
Constructs the player selection modeling dataset across Indian coaching eras.
Avoids lookahead bias by strictly computing rolling stats using data strictly prior to each match date.
"""

import os
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from player_metadata import get_player_profile, PLAYER_ARCHETYPES

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
PROCESSED_DIR = os.path.join(DATA_DIR, "processed")

def assign_coach(date_val):
    d = pd.to_datetime(date_val)
    if d < pd.Timestamp('2005-05-01'):
        return 'John Wright'
    elif d < pd.Timestamp('2007-04-01'):
        return 'Greg Chappell'
    elif d < pd.Timestamp('2008-03-01'):
        return 'Lalchand Rajput (Interim)'
    elif d <= pd.Timestamp('2011-04-02'):
        return 'Gary Kirsten'
    elif d < pd.Timestamp('2014-08-15'):
        return 'Duncan Fletcher'
    elif d < pd.Timestamp('2016-04-15'):
        return 'Ravi Shastri (Team Director)'
    elif d < pd.Timestamp('2016-06-23'):
        return 'Sanjay Bangar (Interim)'
    elif d <= pd.Timestamp('2017-06-20'):
        return 'Anil Kumble'
    elif d <= pd.Timestamp('2021-11-10'):
        return 'Ravi Shastri (Head Coach)'
    elif d <= pd.Timestamp('2024-06-30'):
        return 'Rahul Dravid'
    else:
        return 'Gautam Gambhir'

def build_selection_dataset(lookback_days=540):
    """
    Constructs observations (match m, player p in pool).
    Target: selected in Playing XI (1) vs active contender on bench/rested (0).
    """
    print("Loading processed matches and player performances...")
    df_matches = pd.read_pickle(os.path.join(PROCESSED_DIR, "matches.pkl"))
    df_perfs = pd.read_pickle(os.path.join(PROCESSED_DIR, "player_performances.pkl"))

    df_matches['date'] = pd.to_datetime(df_matches['date'])
    df_perfs['date'] = pd.to_datetime(df_perfs['date'])
    df_matches['coach'] = df_matches['date'].apply(assign_coach)

    # Sort chronologically
    df_matches = df_matches.sort_values('date').reset_index(drop=True)
    df_perfs = df_perfs.sort_values('date').reset_index(drop=True)

    records = []
    
    # Pre-cache player profiles
    player_profiles = {}
    for p in df_perfs['player'].unique():
        player_profiles[p] = get_player_profile(p)

    print(f"Building candidate selection pools across {len(df_matches)} matches...")

    # We start after an initial burn-in period of 365 days to establish reliable player history
    min_date = df_matches['date'].min() + pd.Timedelta(days=365)
    valid_matches = df_matches[df_matches['date'] >= min_date].reset_index(drop=True)

    for idx, match in valid_matches.iterrows():
        match_id = match['match_id']
        m_date = match['date']
        m_type = match['match_type']
        coach = match['coach']
        is_home = match['is_home']
        is_sena = match['is_sena']
        playing_xi = set(match['india_xi'])

        # Candidate pool: playing XI + any player who played for India in previous lookback_days
        window_start = m_date - pd.Timedelta(days=lookback_days)
        recent_perfs_all = df_perfs[(df_perfs['date'] >= window_start) & (df_perfs['date'] < m_date)]
        contenders = set(recent_perfs_all['player'].unique()).union(playing_xi)

        # Skip if contender pool is unrealistically small (< 11)
        if len(contenders) < 11:
            continue

        # Calculate historical stats for all contenders strictly before m_date
        past_perfs = df_perfs[df_perfs['date'] < m_date]
        past_perfs_1y = df_perfs[(df_perfs['date'] >= m_date - pd.Timedelta(days=365)) & (df_perfs['date'] < m_date)]
        past_perfs_format_1y = past_perfs_1y[past_perfs_1y['match_type'] == m_type]

        for player in contenders:
            selected = 1 if player in playing_xi else 0
            profile = player_profiles.get(player, get_player_profile(player))

            # Career stats before this match
            p_past = past_perfs[past_perfs['player'] == player]
            career_caps = len(p_past)
            career_runs = p_past['runs_scored'].sum()
            career_balls = p_past['balls_faced'].sum()
            career_outs = p_past['out'].sum()
            career_bat_avg = round(career_runs / max(1, career_outs), 2)
            career_bat_sr = round((career_runs / max(1, career_balls)) * 100, 2)
            career_wickets = p_past['wickets_taken'].sum()
            career_balls_bowled = p_past['balls_bowled'].sum()
            career_runs_conceded = p_past['runs_conceded'].sum()
            career_bowl_econ = round((career_runs_conceded / max(1, career_balls_bowled / 6)), 2)

            # Rolling 1-year stats before this match
            p_1y = past_perfs_1y[past_perfs_1y['player'] == player]
            recent_caps_1y = len(p_1y)
            recent_runs_1y = p_1y['runs_scored'].sum()
            recent_balls_1y = p_1y['balls_faced'].sum()
            recent_outs_1y = p_1y['out'].sum()
            recent_bat_avg_1y = round(recent_runs_1y / max(1, recent_outs_1y), 2) if recent_caps_1y > 0 else career_bat_avg
            recent_bat_sr_1y = round((recent_runs_1y / max(1, recent_balls_1y)) * 100, 2) if recent_balls_1y > 10 else career_bat_sr
            recent_wickets_1y = p_1y['wickets_taken'].sum()
            recent_balls_bowled_1y = p_1y['balls_bowled'].sum()
            recent_runs_conceded_1y = p_1y['runs_conceded'].sum()
            recent_bowl_econ_1y = round((recent_runs_conceded_1y / max(1, recent_balls_bowled_1y / 6)), 2) if recent_balls_bowled_1y > 30 else career_bowl_econ

            # Format-specific caps in last year
            p_fmt_1y = past_perfs_format_1y[past_perfs_format_1y['player'] == player]
            recent_format_caps_1y = len(p_fmt_1y)

            # Role booleans
            role = profile['role']
            is_top_order = 1 if role == "Top-Order Batter" else 0
            is_middle_order = 1 if role == "Middle-Order Batter" else 0
            is_wk = 1 if role == "Wicketkeeper" else 0
            is_pace_ar = 1 if role == "Pace All-Rounder" else 0
            is_spin_ar = 1 if role == "Spin All-Rounder" else 0
            is_spec_pace = 1 if role == "Specialist Fast Bowler" else 0
            is_spec_spin = 1 if role == "Specialist Spin Bowler" else 0
            is_all_rounder = 1 if (is_pace_ar or is_spin_ar) else 0

            is_lhb = 1 if profile['hand'] == 'LHB' else 0
            is_left_arm_pacer = 1 if (profile['arm'] == 'Left' and profile['bowling'] in ['Pace', 'Left-Arm Fast']) else 0
            is_wrist_spinner = 1 if profile['bowling'] == 'Wrist Spin' else 0
            is_finger_spinner = 1 if profile['bowling'] == 'Finger Spin' or profile['bowling'] == 'Left-Arm Orthodox' else 0

            records.append({
                'match_id': match_id,
                'date': m_date,
                'year': m_date.year,
                'match_type': m_type,
                'coach': coach,
                'is_home': is_home,
                'is_sena': is_sena,
                'player': player,
                'selected': selected,
                'primary_role': role,
                'batting_hand': profile['hand'],
                'bowling_style': profile['bowling'],
                'career_caps': career_caps,
                'career_bat_avg': career_bat_avg,
                'career_bat_sr': career_bat_sr,
                'career_wickets': career_wickets,
                'career_bowl_econ': career_bowl_econ,
                'recent_caps_1y': recent_caps_1y,
                'recent_format_caps_1y': recent_format_caps_1y,
                'recent_bat_avg_1y': recent_bat_avg_1y,
                'recent_bat_sr_1y': recent_bat_sr_1y,
                'recent_wickets_1y': recent_wickets_1y,
                'recent_bowl_econ_1y': recent_bowl_econ_1y,
                'is_top_order': is_top_order,
                'is_middle_order': is_middle_order,
                'is_wk': is_wk,
                'is_pace_ar': is_pace_ar,
                'is_spin_ar': is_spin_ar,
                'is_all_rounder': is_all_rounder,
                'is_spec_pace': is_spec_pace,
                'is_spec_spin': is_spec_spin,
                'is_lhb': is_lhb,
                'is_left_arm_pacer': is_left_arm_pacer,
                'is_wrist_spinner': is_wrist_spinner,
                'is_finger_spinner': is_finger_spinner
            })

    df_selection = pd.DataFrame(records)
    print(f"Generated selection dataset with {len(df_selection)} rows.")
    print(f"Positive selections (selected=1): {(df_selection['selected']==1).sum()}")
    print(f"Bench / Non-selections (selected=0): {(df_selection['selected']==0).sum()}")

    output_path = os.path.join(PROCESSED_DIR, "selection_dataset.pkl")
    df_selection.to_pickle(output_path)
    df_selection.to_csv(os.path.join(PROCESSED_DIR, "selection_dataset.csv"), index=False)
    print(f"Saved selection dataset to {output_path}")

    return df_selection

if __name__ == "__main__":
    df_sel = build_selection_dataset()
