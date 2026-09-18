"""
data_loader.py
Downloads and parses Cricsheet data for Indian Men's cricket matches.
URL: https://cricsheet.org/downloads/india_male_json.zip
Registry: https://cricsheet.org/register/people.csv
"""

import os
import io
import json
import zipfile
import urllib.request
import pandas as pd
from datetime import datetime

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
RAW_DIR = os.path.join(DATA_DIR, "raw")
PROCESSED_DIR = os.path.join(DATA_DIR, "processed")

MATCHES_ZIP_URL = "https://cricsheet.org/downloads/india_male_json.zip"
PEOPLE_CSV_URL = "https://cricsheet.org/register/people.csv"

def setup_directories():
    os.makedirs(RAW_DIR, exist_ok=True)
    os.makedirs(PROCESSED_DIR, exist_ok=True)

def download_data():
    setup_directories()
    zip_path = os.path.join(RAW_DIR, "india_male_json.zip")
    people_path = os.path.join(RAW_DIR, "people.csv")

    if not os.path.exists(zip_path):
        print(f"Downloading India matches dataset from {MATCHES_ZIP_URL}...")
        urllib.request.urlretrieve(MATCHES_ZIP_URL, zip_path)
        print(f"Downloaded to {zip_path} ({os.path.getsize(zip_path) / (1024*1024):.2f} MB)")
    else:
        print(f"Found cached zip at {zip_path}")

    if not os.path.exists(people_path):
        print(f"Downloading player registry from {PEOPLE_CSV_URL}...")
        urllib.request.urlretrieve(PEOPLE_CSV_URL, people_path)
        print(f"Downloaded to {people_path}")
    else:
        print(f"Found cached people registry at {people_path}")

    return zip_path, people_path

def load_people_registry(people_path):
    df_people = pd.read_csv(people_path, low_memory=False)
    id_to_name = dict(zip(df_people['identifier'], df_people['unique_name']))
    return df_people, id_to_name

def parse_matches(zip_path):
    print("Parsing match JSONs from zip...")
    matches_list = []
    player_performances = []

    with zipfile.ZipFile(zip_path, 'r') as z:
        filenames = [f for f in z.namelist() if f.endswith('.json')]
        print(f"Found {len(filenames)} match JSON files in archive.")

        for idx, fname in enumerate(filenames):
            match_id = fname.replace('.json', '')
            try:
                content = json.loads(z.read(fname).decode('utf-8'))
            except Exception as e:
                print(f"Skipping corrupt file {fname}: {e}")
                continue

            info = content.get('info', {})
            teams = info.get('teams', [])
            if 'India' not in teams:
                continue

            opponent = [t for t in teams if t != 'India']
            opponent = opponent[0] if opponent else 'Unknown'

            dates = info.get('dates', [])
            match_date = dates[0] if dates else '2000-01-01'
            raw_match_type = info.get('match_type', 'Unknown')
            if raw_match_type.lower() in ['test', 'mdm']:
                match_type = 'TEST'
            elif raw_match_type.lower() in ['odi', 'odm']:
                match_type = 'ODI'
            elif raw_match_type.lower() in ['t20', 'it20']:
                match_type = 'T20I'
            else:
                match_type = raw_match_type.upper()

            venue = info.get('venue', 'Unknown')
            city = info.get('city', 'Unknown')
            toss = info.get('toss', {})
            outcome = info.get('outcome', {})
            winner = outcome.get('winner', 'Draw/Tie/No Result')
            india_won = 1 if winner == 'India' else (0 if winner in teams else -1)

            players_map = info.get('players', {})
            india_xi = players_map.get('India', [])
            opp_xi = players_map.get(opponent, [])

            if len(india_xi) < 7:
                continue

            venue_lower = (venue + " " + city).lower()
            is_home = 1 if any(ind_city in venue_lower for ind_city in [
                'india', 'delhi', 'mumbai', 'kolkata', 'chennai', 'bengaluru', 'bangalore',
                'hyderabad', 'ahmedabad', 'pune', 'nagpur', 'kanpur', 'mohali', 'dharamsala',
                'cuttack', 'indore', 'rajkot', 'ranchi', 'lucknow', 'guwahati', 'thiruvananthapuram',
                'visakhapatnam', 'jaipur'
            ]) else 0

            is_sena = 1 if any(sena_term in venue_lower for sena_term in [
                'australia', 'melbourne', 'sydney', 'brisbane', 'adelaide', 'perth', 'hobart',
                'england', 'lord\'s', 'oval', 'edgbaston', 'headingley', 'trent bridge', 'manchester',
                'south africa', 'johannesburg', 'cape town', 'centurion', 'durban', 'port elizabeth',
                'new zealand', 'auckland', 'wellington', 'christchurch', 'hamilton', 'mount maunganui'
            ]) else 0

            matches_list.append({
                'match_id': match_id,
                'date': match_date,
                'match_type': match_type,
                'venue': venue,
                'city': city,
                'opponent': opponent,
                'is_home': is_home,
                'is_sena': is_sena,
                'india_won': india_won,
                'toss_winner': toss.get('winner'),
                'toss_decision': toss.get('decision'),
                'india_xi': india_xi,
                'num_india_players': len(india_xi)
            })

            innings_list = content.get('innings', [])
            match_batter_stats = {}
            match_bowler_stats = {}

            for inn in innings_list:
                team_batting = inn.get('team')
                overs = inn.get('overs', [])
                for over_data in overs:
                    deliveries = over_data.get('deliveries', [])
                    for deliv in deliveries:
                        batter = deliv.get('batter')
                        bowler = deliv.get('bowler')
                        runs = deliv.get('runs', {})
                        batter_runs = runs.get('batter', 0)
                        total_runs = runs.get('total', 0)
                        extras = deliv.get('extras', {})
                        is_wide = 'wides' in extras
                        is_noball = 'noballs' in extras

                        if batter:
                            if batter not in match_batter_stats:
                                match_batter_stats[batter] = {'team': team_batting, 'runs': 0, 'balls': 0, 'fours': 0, 'sixes': 0, 'out': 0}
                            match_batter_stats[batter]['runs'] += batter_runs
                            if not is_wide:
                                match_batter_stats[batter]['balls'] += 1
                            if batter_runs == 4:
                                match_batter_stats[batter]['fours'] += 1
                            elif batter_runs == 6:
                                match_batter_stats[batter]['sixes'] += 1

                        if bowler:
                            if bowler not in match_bowler_stats:
                                match_bowler_stats[bowler] = {'team': 'Opp' if team_batting == 'India' else 'India', 'balls': 0, 'runs_conceded': 0, 'wickets': 0}
                            if not is_wide and not is_noball:
                                match_bowler_stats[bowler]['balls'] += 1
                            conceded = batter_runs + extras.get('wides', 0) + extras.get('noballs', 0)
                            match_bowler_stats[bowler]['runs_conceded'] += conceded

                        wickets = deliv.get('wickets', [])
                        for w in wickets:
                            player_out = w.get('player_out')
                            kind = w.get('kind', '')
                            if player_out and player_out in match_batter_stats:
                                match_batter_stats[player_out]['out'] += 1
                            if bowler and kind not in ['run out', 'retired hurt', 'retired out', 'obstructing the field']:
                                if bowler in match_bowler_stats:
                                    match_bowler_stats[bowler]['wickets'] += 1

            for p in india_xi:
                b_stat = match_batter_stats.get(p, {'runs': 0, 'balls': 0, 'fours': 0, 'sixes': 0, 'out': 0})
                bowl_stat = match_bowler_stats.get(p, {'balls': 0, 'runs_conceded': 0, 'wickets': 0})
                player_performances.append({
                    'match_id': match_id,
                    'date': match_date,
                    'match_type': match_type,
                    'player': p,
                    'runs_scored': b_stat['runs'],
                    'balls_faced': b_stat['balls'],
                    'fours': b_stat['fours'],
                    'sixes': b_stat['sixes'],
                    'out': b_stat['out'],
                    'balls_bowled': bowl_stat['balls'],
                    'runs_conceded': bowl_stat['runs_conceded'],
                    'wickets_taken': bowl_stat['wickets']
                })

    df_matches = pd.DataFrame(matches_list)
    df_matches['date'] = pd.to_datetime(df_matches['date'])
    df_matches = df_matches.sort_values('date').reset_index(drop=True)

    df_perfs = pd.DataFrame(player_performances)
    df_perfs['date'] = pd.to_datetime(df_perfs['date'])
    df_perfs = df_perfs.sort_values('date').reset_index(drop=True)

    print(f"Parsed {len(df_matches)} valid matches for India.")
    print(f"Recorded {len(df_perfs)} player-match performance records.")

    df_matches.to_pickle(os.path.join(PROCESSED_DIR, "matches.pkl"))
    df_perfs.to_pickle(os.path.join(PROCESSED_DIR, "player_performances.pkl"))
    df_matches.to_csv(os.path.join(PROCESSED_DIR, "matches.csv"), index=False)

    return df_matches, df_perfs

if __name__ == "__main__":
    zip_p, people_p = download_data()
    df_m, df_p = parse_matches(zip_p)
    print("Data extraction complete!")
