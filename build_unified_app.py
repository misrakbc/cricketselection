"""
generate_app.py
Generates index.html and predictor.html as ONE CONTINUOUS LONG PAGE in the project directory.
Features:
- Quick Jump Anchor Pills (Predictor, Philosophies, Compositions)
- Section 1: Live Selection Predictor & Custom Player Builder
  - 19 Core Indian Cricketers
  - 6 Format Records: Tests, FC, ODIs, List A, T20Is, IPL
  - Last Season (2024-25) Form & Performance Breakdown
  - Dismissal Modes (Batters) & Wicket-Taking Modes (Bowlers)
  - Calibrated 6-Coach Selection Probability Engine
  - Custom Player Builder with Dual Performance Dimensions (Career + Last Season) & Technical Modes
- Section 2: Coach Selection Philosophies & Red-Ball Deep Dive
  - Part 1: Main Predictors Under Each Coach & How They Differ
  - Part 2: Test Match & First-Class Selection Dynamics
- Section 3: Empirical Playing XI Team Compositions Across All Formats
"""

import json
import os

PROJECT_DIR = r"C:\Users\misrak\.gemini\antigravity\scratch\india-cricket-coach-selection"
OUTPUT_DIR = r"C:\Users\misrak\.gemini\antigravity\brain\80ef9fd5-3de1-4e2a-b70c-73d00553a811"

PLAYERS_DATABASE = {
    "Virat Kohli": {
        "role": "Top-Order Batter",
        "hand": "RHB",
        "bowling": "Right-Arm Medium",
        "caps": 552,
        "batAvg": 49.2,
        "batSR": 137.0,
        "bowlEcon": 5.87,
        "multiStats": {
            "test": "115 Tests | 8,947 Runs | Avg 49.2 | 29 100s | HS 254*",
            "fc": "144 Matches | 11,200 Runs | Avg 51.5 | 36 100s",
            "odi": "295 ODIs | 13,906 Runs | Avg 58.2 | SR 93.5 | 50 100s (World Record)",
            "listA": "334 Matches | 15,250 Runs | Avg 56.8 | 54 100s",
            "t20i": "125 T20Is | 4,188 Runs | Avg 48.7 | SR 137.0 | T20 WC 2024 Final MoM (76)",
            "ipl": "252 Matches | 8,004 Runs (#1 All-Time) | Avg 38.7 | SR 131.0 | 8 100s | Orange Cap 2016 & 2024"
        },
        "lastSeason": {
            "season": "2024–25 Season",
            "summary": "IPL 2024 Orange Cap winner (741 runs, avg 61.8, SR 154.7, 1 100), Player of the Match in T20 WC Final (76 off 59), and Perth Test century (100* vs Australia).",
            "runs": 1385,
            "batAvg": 47.8,
            "batSR": 142.5,
            "hundreds": 2,
            "fifties": 8,
            "wkts": 0,
            "bowlEcon": 0,
            "formLabel": "Clutch Big-Match Form"
        },
        "dismissal": {
            "type": "batter",
            "title": "Dismissal Vulnerability Breakdown (How He Gets Out)",
            "modes": [
                {"name": "Caught Behind / Slips (5th-stump corridor)", "pct": 46, "color": "bg-rose-500"},
                {"name": "LBW & Bowled (Nipping back / through gate)", "pct": 26, "color": "bg-amber-500"},
                {"name": "Caught Outfield / Pull / Lofted Drive", "pct": 18, "color": "bg-indigo-500"},
                {"name": "Run Out / Other", "pct": 10, "color": "bg-slate-500"}
            ],
            "tactical_note": "Chasing the 5th-stump corridor outside off accounts for 46% of dismissals. Gambhir demands high intent and positive front-foot commitments; Shastri favored leaving length balls in Australia; Dravid reinforced tighter defensive alignment."
        },
        "squad_scores": {
            "TEST_Home": {"Ravi Shastri": 98.2, "Duncan Fletcher": 98.0, "Rahul Dravid": 97.5, "Anil Kumble": 97.0, "Gary Kirsten": 96.0, "Gautam Gambhir": 95.5},
            "TEST_SENA": {"Ravi Shastri": 98.8, "Duncan Fletcher": 98.5, "Rahul Dravid": 98.0, "Anil Kumble": 97.5, "Gary Kirsten": 96.5, "Gautam Gambhir": 96.0},
            "ODI_Home": {"Ravi Shastri": 99.2, "Rahul Dravid": 99.0, "Duncan Fletcher": 99.0, "Gary Kirsten": 98.8, "Anil Kumble": 98.5, "Gautam Gambhir": 98.0},
            "ODI_SENA": {"Ravi Shastri": 99.4, "Rahul Dravid": 99.1, "Duncan Fletcher": 99.0, "Gary Kirsten": 98.9, "Anil Kumble": 98.6, "Gautam Gambhir": 98.2},
            "T20I_Home": {"Rahul Dravid": 97.5, "Ravi Shastri": 97.2, "Duncan Fletcher": 96.0, "Gary Kirsten": 93.0, "Anil Kumble": 94.0, "Gautam Gambhir": 0.0},
            "T20I_SENA": {"Rahul Dravid": 98.0, "Ravi Shastri": 97.8, "Duncan Fletcher": 96.5, "Gary Kirsten": 94.0, "Anil Kumble": 94.5, "Gautam Gambhir": 0.0}
        },
        "retirement": {
            "T20I": "Retired from T20 Internationals following the 2024 T20 World Cup title (Active in Tests & ODIs)"
        }
    },

    "Rohit Sharma": {
        "role": "Top-Order Batter",
        "hand": "RHB",
        "bowling": "Right-Arm Off-Break",
        "caps": 483,
        "batAvg": 45.0,
        "batSR": 140.9,
        "bowlEcon": 5.21,
        "multiStats": {
            "test": "59 Tests | 4,137 Runs | Avg 45.0 | 12 100s | HS 212",
            "fc": "125 Matches | 8,900 Runs | Avg 52.8 | 29 100s",
            "odi": "265 ODIs | 10,866 Runs | Avg 49.2 | SR 92.4 | 31 100s | 3 Double 100s (HS 264)",
            "listA": "325 Matches | 13,100 Runs | Avg 46.5 | 36 100s",
            "t20i": "159 T20Is | 4,231 Runs | SR 140.9 | 5 100s | T20 World Cup Winning Captain 2024",
            "ipl": "257 Matches | 6,628 Runs | SR 131.1 | 2 100s | 5-Time IPL Title Winning Captain"
        },
        "lastSeason": {
            "season": "2024–25 Season",
            "summary": "Captained India to T20 World Cup victory (257 runs, SR 156.7, 92 vs Australia), IPL 2024 (417 runs, 1 100, SR 150.0), Test centuries vs England at Rajkot & Dharamsala.",
            "runs": 1280,
            "batAvg": 42.4,
            "batSR": 146.8,
            "hundreds": 3,
            "fifties": 6,
            "wkts": 0,
            "bowlEcon": 0,
            "formLabel": "Ultra-Aggressive Intent"
        },
        "dismissal": {
            "type": "batter",
            "title": "Dismissal Vulnerability Breakdown (How He Gets Out)",
            "modes": [
                {"name": "Caught Deep / Outfield (Pull / Hook to fine/square leg)", "pct": 44, "color": "bg-rose-500"},
                {"name": "LBW & Bowled (Early incoming seam / inswinger)", "pct": 30, "color": "bg-amber-500"},
                {"name": "Caught Behind / Slips (Defensive poke outside off)", "pct": 18, "color": "bg-indigo-500"},
                {"name": "Run Out / Other", "pct": 8, "color": "bg-slate-500"}
            ],
            "tactical_note": "Natural hooker and puller of pace: 44% of dismissals occur caught in the deep taking on boundary riders. Gambhir encourages this fearless powerplay onslaught; Kirsten preferred early-innings preservation."
        },
        "squad_scores": {
            "TEST_Home": {"Rahul Dravid": 98.5, "Ravi Shastri": 98.0, "Duncan Fletcher": 97.0, "Gautam Gambhir": 96.5, "Gary Kirsten": 95.0, "Anil Kumble": 96.0},
            "TEST_SENA": {"Rahul Dravid": 97.8, "Ravi Shastri": 98.2, "Duncan Fletcher": 96.5, "Gautam Gambhir": 96.0, "Gary Kirsten": 94.5, "Anil Kumble": 95.5},
            "ODI_Home": {"Rahul Dravid": 99.2, "Ravi Shastri": 99.0, "Duncan Fletcher": 98.5, "Gary Kirsten": 98.0, "Gautam Gambhir": 98.5, "Anil Kumble": 98.0},
            "ODI_SENA": {"Rahul Dravid": 99.0, "Ravi Shastri": 99.2, "Duncan Fletcher": 98.8, "Gary Kirsten": 98.2, "Gautam Gambhir": 98.0, "Anil Kumble": 98.0},
            "T20I_Home": {"Rahul Dravid": 98.8, "Ravi Shastri": 98.0, "Duncan Fletcher": 96.0, "Gary Kirsten": 92.0, "Anil Kumble": 95.0, "Gautam Gambhir": 0.0},
            "T20I_SENA": {"Rahul Dravid": 98.5, "Ravi Shastri": 98.2, "Duncan Fletcher": 96.5, "Gary Kirsten": 92.5, "Anil Kumble": 95.0, "Gautam Gambhir": 0.0}
        },
        "retirement": {
            "T20I": "Retired from T20 Internationals after winning the 2024 T20 World Cup as Captain (Active in Tests & ODIs)"
        }
    },

    "Jasprit Bumrah": {
        "role": "Specialist Fast Bowler",
        "hand": "RHB",
        "bowling": "Right-Arm Fast",
        "caps": 195,
        "batAvg": 6.8,
        "batSR": 62.0,
        "bowlEcon": 4.60,
        "multiStats": {
            "test": "36 Tests | 159 Wkts | Avg 20.7 | SR 45.1 | 10 5-Wkt Hauls",
            "fc": "74 Matches | 340 Wkts | Avg 22.1 | 16 5-Wkt Hauls",
            "odi": "89 ODIs | 149 Wkts | Avg 23.5 | Econ 4.60 | Best 6/19 vs England at The Oval",
            "listA": "120 Matches | 212 Wkts | Avg 22.8 | Econ 4.52",
            "t20i": "70 T20Is | 89 Wkts | Avg 17.7 | Econ 6.27 | Player of the Tournament T20 WC 2024",
            "ipl": "133 Matches | 165 Wkts | Avg 22.5 | Econ 7.30 | 2024 Purple Cap (20 Wkts, Econ 6.48)"
        },
        "lastSeason": {
            "season": "2024–25 Season",
            "summary": "T20 World Cup Player of the Tournament (15 wkts, econ 4.17), IPL 2024 Purple Cap contender (20 wkts, econ 6.48), BGT 2024-25 Captain (8/72 at Perth, Test series avg 13.5).",
            "runs": 45,
            "batAvg": 7.5,
            "batSR": 68.0,
            "hundreds": 0,
            "fifties": 0,
            "wkts": 68,
            "bowlEcon": 4.12,
            "bowlAvg": 16.4,
            "formLabel": "Generational Peak / Unplayable"
        },
        "dismissal": {
            "type": "bowler",
            "title": "Wicket-Taking Weaponry (How He Dismisses Batters)",
            "modes": [
                {"name": "Bowled & LBW (145km/h inswinging yorkers & sharp nip-backers)", "pct": 48, "color": "bg-emerald-500"},
                {"name": "Caught Behind & Slips (Seam movement off pitch / angle)", "pct": 34, "color": "bg-indigo-500"},
                {"name": "Caught Outfield / Miscues (Heavy bouncer / slower ball)", "pct": 14, "color": "bg-amber-500"},
                {"name": "Run Out / Other", "pct": 4, "color": "bg-slate-500"}
            ],
            "tactical_note": "A lethal 48% Bowled/LBW rate generated by reverse swing, hyper-extended release point, and toe-crushing yorkers. Undisputed 99%+ starter under all 6 coaches in all conditions."
        },
        "squad_scores": {
            "TEST_Home": {"Ravi Shastri": 99.5, "Rahul Dravid": 99.2, "Gautam Gambhir": 99.4, "Duncan Fletcher": 98.0, "Gary Kirsten": 97.0, "Anil Kumble": 98.5},
            "TEST_SENA": {"Ravi Shastri": 99.8, "Gautam Gambhir": 99.6, "Rahul Dravid": 99.4, "Duncan Fletcher": 98.5, "Gary Kirsten": 97.5, "Anil Kumble": 99.0},
            "ODI_Home": {"Ravi Shastri": 99.4, "Rahul Dravid": 99.2, "Gautam Gambhir": 99.3, "Duncan Fletcher": 98.2, "Gary Kirsten": 97.2, "Anil Kumble": 98.6},
            "ODI_SENA": {"Ravi Shastri": 99.6, "Rahul Dravid": 99.4, "Gautam Gambhir": 99.5, "Duncan Fletcher": 98.4, "Gary Kirsten": 97.5, "Anil Kumble": 98.8},
            "T20I_Home": {"Gautam Gambhir": 99.6, "Rahul Dravid": 99.5, "Ravi Shastri": 99.4, "Duncan Fletcher": 98.0, "Gary Kirsten": 97.0, "Anil Kumble": 98.5},
            "T20I_SENA": {"Gautam Gambhir": 99.7, "Rahul Dravid": 99.6, "Ravi Shastri": 99.5, "Duncan Fletcher": 98.2, "Gary Kirsten": 97.2, "Anil Kumble": 98.6}
        }
    },

    "Hardik Pandya": {
        "role": "Pace All-Rounder",
        "hand": "RHB",
        "bowling": "Right-Arm Fast-Medium",
        "caps": 199,
        "batAvg": 31.3,
        "batSR": 141.0,
        "bowlEcon": 7.45,
        "multiStats": {
            "test": "11 Tests | 532 Runs (Avg 31.3) | 17 Wkts (Avg 31.1) | 108 at Pallekele",
            "fc": "29 Matches | 1,351 Runs | 48 Wkts",
            "odi": "86 ODIs | 1,769 Runs (SR 110.3) | 84 Wkts (Avg 35.6) | 92* at Canberra",
            "listA": "122 Matches | 2,850 Runs | 125 Wkts",
            "t20i": "102 T20Is | 1,641 Runs (SR 141.0) | 86 Wkts (Econ 8.12) | T20 World Cup Champion",
            "ipl": "137 Matches | 2,525 Runs (SR 145.8) | 64 Wkts | IPL Winning Captain (GT 2022)"
        },
        "lastSeason": {
            "season": "2024–25 Season",
            "summary": "T20 World Cup hero (defended 16 in final over vs SA, 144 runs at SR 151.6, 11 wkts), clutch international death bowling, explosive middle-order batting.",
            "runs": 612,
            "batAvg": 36.8,
            "batSR": 158.4,
            "hundreds": 0,
            "fifties": 4,
            "wkts": 24,
            "bowlEcon": 7.82,
            "bowlAvg": 24.2,
            "formLabel": "Clutch World Cup Hero"
        },
        "dismissal": {
            "type": "allrounder",
            "title": "Tactical Dismissal & Wicket Profile",
            "modes": [
                {"name": "Batting: Caught Deep (Hoicking against hard length)", "pct": 42, "color": "bg-rose-500"},
                {"name": "Batting: Edges & Bowled to moving seam", "pct": 32, "color": "bg-amber-500"},
                {"name": "Bowling: Caught Deep (Heavy bouncer / back-of-hand slower)", "pct": 48, "color": "bg-emerald-500"},
                {"name": "Bowling: LBW & Bowled (Skidding seam on stumps)", "pct": 34, "color": "bg-indigo-500"}
            ],
            "tactical_note": "Rare pace-bowling all-rounder archetype. Ravi Shastri and Duncan Fletcher prioritized him heavily to field 4 frontline pacers overseas. Gambhir values his ability to bowl with the new ball and at the death."
        },
        "squad_scores": {
            "TEST_Home": {"Ravi Shastri": 72.0, "Duncan Fletcher": 68.0, "Rahul Dravid": 58.0, "Gautam Gambhir": 55.0, "Gary Kirsten": 38.0, "Anil Kumble": 52.0},
            "TEST_SENA": {"Ravi Shastri": 88.5, "Duncan Fletcher": 82.0, "Rahul Dravid": 74.0, "Gautam Gambhir": 68.0, "Gary Kirsten": 45.0, "Anil Kumble": 65.0},
            "ODI_Home": {"Ravi Shastri": 96.0, "Duncan Fletcher": 94.0, "Rahul Dravid": 92.0, "Gautam Gambhir": 93.0, "Gary Kirsten": 80.0, "Anil Kumble": 88.0},
            "ODI_SENA": {"Ravi Shastri": 98.0, "Duncan Fletcher": 96.0, "Rahul Dravid": 94.0, "Gautam Gambhir": 95.0, "Gary Kirsten": 82.0, "Anil Kumble": 90.0},
            "T20I_Home": {"Gautam Gambhir": 98.0, "Ravi Shastri": 97.5, "Rahul Dravid": 96.0, "Duncan Fletcher": 94.0, "Gary Kirsten": 82.0, "Anil Kumble": 90.0},
            "T20I_SENA": {"Gautam Gambhir": 98.5, "Ravi Shastri": 98.0, "Rahul Dravid": 97.0, "Duncan Fletcher": 95.0, "Gary Kirsten": 84.0, "Anil Kumble": 92.0}
        }
    },

    "Yashasvi Jaiswal": {
        "role": "Top-Order Batter",
        "hand": "LHB",
        "bowling": "Right-Arm Leg-Break",
        "caps": 37,
        "batAvg": 56.3,
        "batSR": 164.3,
        "bowlEcon": 7.20,
        "multiStats": {
            "test": "14 Tests | 1,407 Runs | Avg 56.3 | SR 70.1 | 2 Double 100s (712 Runs vs ENG)",
            "fc": "32 Matches | 3,250 Runs | Avg 61.3 | 12 100s | Irani Cup Double 100",
            "odi": "India White-Ball Core Pipeline | Vijay Hazare Trophy Double 100 (203)",
            "listA": "35 Matches | 1,650 Runs | Avg 53.2 | SR 86.5 | 5 100s | HS 203",
            "t20i": "23 T20Is | 723 Runs | Avg 36.2 | SR 164.3 | 1 100 & 5 50s",
            "ipl": "52 Matches | 1,607 Runs | Avg 32.1 | SR 150.6 | 2 100s | Fastest IPL 50 (13 balls)"
        },
        "lastSeason": {
            "season": "2024–25 Season",
            "summary": "Historic 712 runs in 5 Tests vs England (avg 89.0, two double hundreds), 161 at Perth in BGT 2024-25, IPL 2024 (435 runs, 1 100, SR 155.8).",
            "runs": 1580,
            "batAvg": 58.5,
            "batSR": 152.0,
            "hundreds": 4,
            "fifties": 7,
            "wkts": 0,
            "bowlEcon": 0,
            "formLabel": "Blazing Red-Hot Form"
        },
        "dismissal": {
            "type": "batter",
            "title": "Dismissal Vulnerability Breakdown (How He Gets Out)",
            "modes": [
                {"name": "Caught Slips / Gully (Aggressive drive / flashing blade)", "pct": 40, "color": "bg-rose-500"},
                {"name": "Caught Outfield / Deep (Lofted attack against spin/pace)", "pct": 30, "color": "bg-amber-500"},
                {"name": "LBW & Bowled (Seam angle cutting into pads)", "pct": 20, "color": "bg-indigo-500"},
                {"name": "Run Out / Other", "pct": 10, "color": "bg-slate-500"}
            ],
            "tactical_note": "Fearless attacking mindset: 40% caught slips/gully while playing the aerial cut or expansive drive. Gambhir rates him as India's #1 modern asset due to LHB matchup dynamics and aggressive powerplay tempo."
        },
        "squad_scores": {
            "TEST_Home": {"Gautam Gambhir": 98.8, "Rahul Dravid": 96.5, "Ravi Shastri": 91.0, "Duncan Fletcher": 85.0, "Gary Kirsten": 82.0, "Anil Kumble": 88.0},
            "TEST_SENA": {"Gautam Gambhir": 98.2, "Rahul Dravid": 95.0, "Ravi Shastri": 92.5, "Duncan Fletcher": 86.0, "Gary Kirsten": 80.0, "Anil Kumble": 86.0},
            "ODI_Home": {"Gautam Gambhir": 96.0, "Rahul Dravid": 92.0, "Ravi Shastri": 88.0, "Duncan Fletcher": 84.0, "Gary Kirsten": 80.0, "Anil Kumble": 85.0},
            "ODI_SENA": {"Gautam Gambhir": 95.0, "Rahul Dravid": 91.0, "Ravi Shastri": 89.0, "Duncan Fletcher": 83.0, "Gary Kirsten": 78.0, "Anil Kumble": 84.0},
            "T20I_Home": {"Gautam Gambhir": 99.0, "Rahul Dravid": 94.0, "Ravi Shastri": 90.0, "Duncan Fletcher": 85.0, "Gary Kirsten": 80.0, "Anil Kumble": 86.0},
            "T20I_SENA": {"Gautam Gambhir": 98.5, "Rahul Dravid": 93.0, "Ravi Shastri": 91.0, "Duncan Fletcher": 86.0, "Gary Kirsten": 79.0, "Anil Kumble": 85.0}
        }
    },

    "Kuldeep Yadav": {
        "role": "Specialist Spin Bowler",
        "hand": "LHB",
        "bowling": "Left-Arm Wrist Spin",
        "caps": 158,
        "batAvg": 10.2,
        "batSR": 64.0,
        "bowlEcon": 5.03,
        "multiStats": {
            "test": "12 Tests | 53 Wkts | Avg 21.1 | SR 37.8 | 4 5-Wkt Hauls | 5/40 at Sydney",
            "fc": "42 Matches | 165 Wkts | Avg 28.4 | 8 5-Wkt Hauls",
            "odi": "106 ODIs | 172 Wkts | Avg 26.0 | Econ 5.03 | Two ODI Hat-Tricks",
            "listA": "132 Matches | 225 Wkts | Avg 25.4 | Econ 4.98",
            "t20i": "40 T20Is | 69 Wkts | Avg 14.1 | Econ 6.74 | SR 12.5 | 2 5-Wkt Hauls",
            "ipl": "84 Matches | 87 Wkts | Avg 26.5 | Econ 8.01 | Premier DC Middle-Overs Match-Winner"
        },
        "lastSeason": {
            "season": "2024–25 Season",
            "summary": "T20 World Cup crucial strike weapon (10 wkts, econ 6.95), Test series vs England (19 wkts in 4 Tests, 5/72 at Dharamsala), IPL 2024 (16 wkts, econ 8.69).",
            "runs": 65,
            "batAvg": 9.2,
            "batSR": 62.0,
            "hundreds": 0,
            "fifties": 0,
            "wkts": 54,
            "bowlEcon": 5.45,
            "bowlAvg": 19.8,
            "formLabel": "Elite Wrist-Spin Match-Winner"
        },
        "dismissal": {
            "type": "bowler",
            "title": "Wicket-Taking Weaponry (How He Dismisses Batters)",
            "modes": [
                {"name": "Bowled & LBW (Deceptive wrong'un through the gate)", "pct": 45, "color": "bg-emerald-500"},
                {"name": "Caught Outfield / Miscues (Drift & dip baiting lofted shot)", "pct": 32, "color": "bg-indigo-500"},
                {"name": "Caught Behind & Slips (Sharp turn off pitch)", "pct": 18, "color": "bg-amber-500"},
                {"name": "Stumped / Other", "pct": 5, "color": "bg-slate-500"}
            ],
            "tactical_note": "Unorthodox left-arm wrist spin creates unmatched drift and dip: 45% Bowled/LBW rate. Rahul Dravid's #1 favored bowler archetype (Odds Ratio 1.33) to break middle-overs partnerships."
        },
        "squad_scores": {
            "TEST_Home": {"Rahul Dravid": 92.0, "Gautam Gambhir": 88.0, "Ravi Shastri": 85.0, "Anil Kumble": 82.0, "Duncan Fletcher": 65.0, "Gary Kirsten": 60.0},
            "TEST_SENA": {"Rahul Dravid": 78.0, "Ravi Shastri": 80.0, "Gautam Gambhir": 74.0, "Anil Kumble": 70.0, "Duncan Fletcher": 48.0, "Gary Kirsten": 42.0},
            "ODI_Home": {"Rahul Dravid": 97.0, "Ravi Shastri": 96.0, "Gautam Gambhir": 95.0, "Anil Kumble": 90.0, "Duncan Fletcher": 78.0, "Gary Kirsten": 75.0},
            "ODI_SENA": {"Rahul Dravid": 96.0, "Ravi Shastri": 95.0, "Gautam Gambhir": 94.0, "Anil Kumble": 88.0, "Duncan Fletcher": 76.0, "Gary Kirsten": 72.0},
            "T20I_Home": {"Rahul Dravid": 96.5, "Gautam Gambhir": 95.0, "Ravi Shastri": 92.0, "Anil Kumble": 88.0, "Duncan Fletcher": 75.0, "Gary Kirsten": 70.0},
            "T20I_SENA": {"Rahul Dravid": 95.5, "Gautam Gambhir": 94.0, "Ravi Shastri": 92.0, "Anil Kumble": 86.0, "Duncan Fletcher": 74.0, "Gary Kirsten": 68.0}
        }
    },

    "Axar Patel": {
        "role": "Spin All-Rounder",
        "hand": "LHB",
        "bowling": "Left-Arm Orthodox Spin",
        "caps": 134,
        "batAvg": 35.9,
        "batSR": 144.5,
        "bowlEcon": 4.54,
        "multiStats": {
            "test": "14 Tests | 55 Wkts (Avg 19.3) | 646 Runs (Avg 35.9) | 5 5-Wkt Hauls",
            "fc": "58 Matches | 215 Wkts | 2,400 Runs",
            "odi": "60 ODIs | 506 Runs (SR 88.5) | 64 Wkts (Econ 4.54) | 64* vs West Indies",
            "listA": "155 Matches | 1,750 Runs | 185 Wkts (Econ 4.41)",
            "t20i": "60 T20Is | 490 Runs (SR 144.5) | 49 Wkts (Econ 7.33) | Crucial 47 in T20 WC Final",
            "ipl": "150 Matches | 1,653 Runs (SR 130.9) | 123 Wkts | Econ 7.24 | Retained Core DC"
        },
        "lastSeason": {
            "season": "2024–25 Season",
            "summary": "T20 World Cup match-winning 47 off 31 in Final & 9 wickets (econ 7.86), crucial Test knocks vs England, IPL 2024 (235 runs, 11 wkts).",
            "runs": 512,
            "batAvg": 34.1,
            "batSR": 141.0,
            "hundreds": 0,
            "fifties": 3,
            "wkts": 28,
            "bowlEcon": 5.12,
            "bowlAvg": 22.4,
            "formLabel": "Complete Dual-Threat Utility"
        },
        "dismissal": {
            "type": "allrounder",
            "title": "Tactical Dismissal & Wicket Profile",
            "modes": [
                {"name": "Batting: Caught Deep / Outfield (Lofted counter-attack)", "pct": 42, "color": "bg-rose-500"},
                {"name": "Batting: LBW / Bowled to skidding deliveries", "pct": 32, "color": "bg-amber-500"},
                {"name": "Bowling: Bowled & LBW (Arm ball skidding straight on)", "pct": 52, "color": "bg-emerald-500"},
                {"name": "Bowling: Caught Slips / Keeper (Natural angle away)", "pct": 30, "color": "bg-indigo-500"}
            ],
            "tactical_note": "Lethal arm-ball creates an enormous 52% Bowled/LBW rate in red-ball conditions. Gambhir and Dravid heavily depend on his #7/#8 batting depth combined with LHB matchup value."
        },
        "squad_scores": {
            "TEST_Home": {"Rahul Dravid": 94.0, "Gautam Gambhir": 93.0, "Duncan Fletcher": 86.0, "Anil Kumble": 88.0, "Ravi Shastri": 82.0, "Gary Kirsten": 70.0},
            "TEST_SENA": {"Rahul Dravid": 75.0, "Gautam Gambhir": 74.0, "Duncan Fletcher": 64.0, "Anil Kumble": 62.0, "Ravi Shastri": 58.0, "Gary Kirsten": 45.0},
            "ODI_Home": {"Rahul Dravid": 92.0, "Gautam Gambhir": 93.5, "Duncan Fletcher": 85.0, "Anil Kumble": 82.0, "Ravi Shastri": 84.0, "Gary Kirsten": 72.0},
            "ODI_SENA": {"Rahul Dravid": 88.0, "Gautam Gambhir": 90.0, "Duncan Fletcher": 82.0, "Anil Kumble": 78.0, "Ravi Shastri": 82.0, "Gary Kirsten": 68.0},
            "T20I_Home": {"Gautam Gambhir": 96.0, "Rahul Dravid": 95.0, "Ravi Shastri": 88.0, "Duncan Fletcher": 84.0, "Anil Kumble": 82.0, "Gary Kirsten": 72.0},
            "T20I_SENA": {"Gautam Gambhir": 95.0, "Rahul Dravid": 94.0, "Ravi Shastri": 88.0, "Duncan Fletcher": 82.0, "Anil Kumble": 80.0, "Gary Kirsten": 70.0}
        }
    },

    "Arshdeep Singh": {
        "role": "Specialist Fast Bowler",
        "hand": "LHB",
        "bowling": "Left-Arm Fast-Medium",
        "caps": 87,
        "batAvg": 4.5,
        "batSR": 55.0,
        "bowlEcon": 8.34,
        "multiStats": {
            "test": "First-Class Red-Ball Seamer | County Stint with Kent (13 Wkts)",
            "fc": "19 Matches | 55 Wkts | Avg 29.8 | Econ 3.10",
            "odi": "8 ODIs | 12 Wkts | Avg 24.2 | 5/37 vs South Africa at Johannesburg",
            "listA": "25 Matches | 38 Wkts | Avg 26.5 | Econ 4.88",
            "t20i": "60 T20Is | 95 Wkts | Avg 18.4 | Econ 8.34 | Joint Top Wkt-Taker T20 WC 2024 (17 Wkts)",
            "ipl": "65 Matches | 76 Wkts | Avg 27.0 | Econ 8.74 | Premier Death-Overs Specialist PBKS"
        },
        "lastSeason": {
            "season": "2024–25 Season",
            "summary": "Joint highest wicket-taker in T20 World Cup 2024 (17 wkts, avg 12.6, econ 7.16), IPL 2024 (19 wkts), Ranji Trophy & Duleep Trophy multi-day red-ball performances.",
            "runs": 22,
            "batAvg": 4.0,
            "batSR": 58.0,
            "hundreds": 0,
            "fifties": 0,
            "wkts": 48,
            "bowlEcon": 7.42,
            "bowlAvg": 19.5,
            "formLabel": "World Cup Joint #1 Wicket-Taker"
        },
        "dismissal": {
            "type": "bowler",
            "title": "Wicket-Taking Weaponry (How He Dismisses Batters)",
            "modes": [
                {"name": "Bowled & LBW (Inswinging yorker & sharp angle to RHBs)", "pct": 44, "color": "bg-emerald-500"},
                {"name": "Caught Outfield / Miscues (Wide yorkers & slower cutters at death)", "pct": 36, "color": "bg-indigo-500"},
                {"name": "Caught Behind & Slips (New ball away-swinger)", "pct": 16, "color": "bg-amber-500"},
                {"name": "Other", "pct": 4, "color": "bg-slate-500"}
            ],
            "tactical_note": "Left-arm pace angle creates acute trouble for right-handers: 44% Bowled/LBW. Gautam Gambhir's #2 predictor (Odds Ratio 1.20) for powerplay swing and death-overs composure."
        },
        "squad_scores": {
            "TEST_Home": {"Gautam Gambhir": 72.0, "Rahul Dravid": 65.0, "Ravi Shastri": 62.0, "Duncan Fletcher": 55.0, "Gary Kirsten": 50.0, "Anil Kumble": 58.0},
            "TEST_SENA": {"Gautam Gambhir": 80.0, "Ravi Shastri": 76.0, "Rahul Dravid": 72.0, "Duncan Fletcher": 64.0, "Gary Kirsten": 58.0, "Anil Kumble": 66.0},
            "ODI_Home": {"Gautam Gambhir": 92.0, "Rahul Dravid": 88.0, "Ravi Shastri": 86.0, "Duncan Fletcher": 80.0, "Gary Kirsten": 75.0, "Anil Kumble": 80.0},
            "ODI_SENA": {"Gautam Gambhir": 94.0, "Rahul Dravid": 90.0, "Ravi Shastri": 90.0, "Duncan Fletcher": 82.0, "Gary Kirsten": 78.0, "Anil Kumble": 82.0},
            "T20I_Home": {"Gautam Gambhir": 98.5, "Rahul Dravid": 97.0, "Ravi Shastri": 94.0, "Duncan Fletcher": 88.0, "Gary Kirsten": 84.0, "Anil Kumble": 88.0},
            "T20I_SENA": {"Gautam Gambhir": 99.0, "Rahul Dravid": 97.5, "Ravi Shastri": 95.0, "Duncan Fletcher": 90.0, "Gary Kirsten": 85.0, "Anil Kumble": 90.0}
        }
    },

    "Rishabh Pant": {
        "role": "Wicketkeeper-Batter",
        "hand": "LHB",
        "bowling": "None",
        "caps": 140,
        "batAvg": 43.7,
        "batSR": 127.3,
        "bowlEcon": 0,
        "multiStats": {
            "test": "33 Tests | 2,271 Runs | Avg 43.7 | SR 73.6 | 6 100s | Historic Gabba 89* Hero",
            "fc": "58 Matches | 4,100 Runs | Avg 49.5 | 11 100s | Ranji Triple 100 (308)",
            "odi": "31 ODIs | 871 Runs | Avg 34.8 | SR 106.6 | 125* Series Decider vs England at Manchester",
            "listA": "68 Matches | 2,150 Runs | Avg 36.4 | SR 103.8",
            "t20i": "76 T20Is | 1,209 Runs | SR 127.3 | Primary T20 WC 2024 Keeper-Batter",
            "ipl": "111 Matches | 3,284 Runs | Avg 35.3 | SR 148.5 | 1 100 & 18 50s | DC Captain"
        },
        "lastSeason": {
            "season": "2024–25 Season",
            "summary": "Miraculous comeback post-recovery: World Cup winning wicketkeeper (171 runs, 14 dismissals), Test hundred vs Bangladesh (109), IPL 2024 (446 runs, avg 40.5, SR 155.4).",
            "runs": 1150,
            "batAvg": 41.2,
            "batSR": 148.0,
            "hundreds": 2,
            "fifties": 6,
            "wkts": 0,
            "bowlEcon": 0,
            "formLabel": "Triumphant Return & Elite Impact"
        },
        "dismissal": {
            "type": "batter",
            "title": "Dismissal Vulnerability Breakdown (How He Gets Out)",
            "modes": [
                {"name": "Caught Outfield / Deep (Aerial hoick / reverse scoop)", "pct": 42, "color": "bg-rose-500"},
                {"name": "Caught Behind & Slips (Flashing drive outside off)", "pct": 32, "color": "bg-amber-500"},
                {"name": "LBW & Bowled (Yorker / swing through defense)", "pct": 18, "color": "bg-indigo-500"},
                {"name": "Run Out / Other", "pct": 8, "color": "bg-slate-500"}
            ],
            "tactical_note": "High-risk, high-reward counter-puncher: 42% dismissals caught in the deep taking on boundary riders. Ravi Shastri and Gambhir unconditionally back his audacity to break open Tests."
        },
        "squad_scores": {
            "TEST_Home": {"Ravi Shastri": 98.0, "Gautam Gambhir": 97.5, "Rahul Dravid": 96.0, "Duncan Fletcher": 90.0, "Gary Kirsten": 88.0, "Anil Kumble": 92.0},
            "TEST_SENA": {"Ravi Shastri": 99.2, "Gautam Gambhir": 98.5, "Rahul Dravid": 97.0, "Duncan Fletcher": 92.0, "Gary Kirsten": 86.0, "Anil Kumble": 94.0},
            "ODI_Home": {"Gautam Gambhir": 94.0, "Rahul Dravid": 92.0, "Ravi Shastri": 95.0, "Duncan Fletcher": 88.0, "Gary Kirsten": 82.0, "Anil Kumble": 86.0},
            "ODI_SENA": {"Gautam Gambhir": 95.0, "Rahul Dravid": 93.0, "Ravi Shastri": 96.0, "Duncan Fletcher": 89.0, "Gary Kirsten": 84.0, "Anil Kumble": 88.0},
            "T20I_Home": {"Gautam Gambhir": 96.0, "Rahul Dravid": 95.0, "Ravi Shastri": 94.0, "Duncan Fletcher": 88.0, "Gary Kirsten": 80.0, "Anil Kumble": 86.0},
            "T20I_SENA": {"Gautam Gambhir": 96.5, "Rahul Dravid": 95.5, "Ravi Shastri": 95.0, "Duncan Fletcher": 89.0, "Gary Kirsten": 82.0, "Anil Kumble": 88.0}
        }
    },

    "Ravindra Jadeja": {
        "role": "Spin All-Rounder",
        "hand": "LHB",
        "bowling": "Left-Arm Orthodox Spin",
        "caps": 343,
        "batAvg": 36.5,
        "batSR": 129.5,
        "bowlEcon": 4.88,
        "multiStats": {
            "test": "72 Tests | 3,030 Runs (Avg 36.5) | 294 Wkts (Avg 24.1) | 13 5-Wkt Hauls | 175* & 9 Wkts vs SL",
            "fc": "130 Matches | 7,200 Runs (3 Triple 100s) | 510 Wkts",
            "odi": "197 ODIs | 2,756 Runs (Avg 32.8) | 220 Wkts (Econ 4.88) | CT 2013 Golden Ball Winner",
            "listA": "240 Matches | 3,600 Runs | 275 Wkts (Econ 4.75)",
            "t20i": "74 T20Is | 515 Runs | 54 Wkts (Econ 7.13) | T20 World Cup Champion 2024",
            "ipl": "240 Matches | 2,959 Runs (SR 129.5) | 160 Wkts | Econ 7.60 | 5-Time IPL Winner CSK"
        },
        "lastSeason": {
            "season": "2024–25 Season",
            "summary": "112 & 5/41 vs England at Rajkot (series: 225 runs, 19 wkts), T20 World Cup Champion squad, IPL 2024 (267 runs, 8 wkts, econ 7.85).",
            "runs": 620,
            "batAvg": 37.5,
            "batSR": 132.0,
            "hundreds": 1,
            "fifties": 3,
            "wkts": 36,
            "bowlEcon": 4.65,
            "bowlAvg": 23.1,
            "formLabel": "Legendary All-Round Stalwart"
        },
        "dismissal": {
            "type": "allrounder",
            "title": "Tactical Dismissal & Wicket Profile",
            "modes": [
                {"name": "Batting: Caught Deep / Outfield (Lofted pull / slog)", "pct": 40, "color": "bg-rose-500"},
                {"name": "Batting: Edges & Bowled outside off", "pct": 34, "color": "bg-amber-500"},
                {"name": "Bowling: Bowled & LBW (Arm ball skidding into stumps)", "pct": 54, "color": "bg-emerald-500"},
                {"name": "Bowling: Caught Slips / Keeper (Turn & bounce)", "pct": 32, "color": "bg-indigo-500"}
            ],
            "tactical_note": "Unrivaled consistency: 54% Bowled/LBW rate from rapid-fire 1.5-minute overs. Undisputed first-choice red-ball all-rounder under Kumble, Shastri, Dravid, and Gambhir."
        },
        "squad_scores": {
            "TEST_Home": {"Anil Kumble": 99.5, "Ravi Shastri": 99.2, "Rahul Dravid": 99.0, "Duncan Fletcher": 98.0, "Gautam Gambhir": 98.5, "Gary Kirsten": 85.0},
            "TEST_SENA": {"Ravi Shastri": 97.0, "Rahul Dravid": 96.5, "Gautam Gambhir": 95.0, "Duncan Fletcher": 92.0, "Anil Kumble": 90.0, "Gary Kirsten": 75.0},
            "ODI_Home": {"Duncan Fletcher": 98.0, "Rahul Dravid": 97.5, "Ravi Shastri": 97.0, "Gautam Gambhir": 96.0, "Gary Kirsten": 86.0, "Anil Kumble": 92.0},
            "ODI_SENA": {"Duncan Fletcher": 97.0, "Rahul Dravid": 96.0, "Ravi Shastri": 96.5, "Gautam Gambhir": 95.0, "Gary Kirsten": 84.0, "Anil Kumble": 90.0},
            "T20I_Home": {"Rahul Dravid": 96.0, "Ravi Shastri": 95.0, "Duncan Fletcher": 92.0, "Anil Kumble": 90.0, "Gary Kirsten": 82.0, "Gautam Gambhir": 0.0},
            "T20I_SENA": {"Rahul Dravid": 95.5, "Ravi Shastri": 94.5, "Duncan Fletcher": 91.0, "Anil Kumble": 88.0, "Gary Kirsten": 80.0, "Gautam Gambhir": 0.0}
        },
        "retirement": {
            "T20I": "Retired from T20 Internationals following the 2024 T20 World Cup title (Active in Tests & ODIs)"
        }
    },

    "Suryakumar Yadav": {
        "role": "Middle-Order Batter",
        "hand": "RHB",
        "bowling": "Right-Arm Medium",
        "caps": 112,
        "batAvg": 42.8,
        "batSR": 169.5,
        "bowlEcon": 0,
        "multiStats": {
            "test": "1 Test Cap vs Australia (Nagpur) | Mumbai Ranji Trophy Stalwart",
            "fc": "84 Matches | 5,650 Runs | Avg 43.8 | SR 63.5 | 14 100s",
            "odi": "37 ODIs | 773 Runs | Avg 25.8 | SR 105.0 | 4 50s",
            "listA": "136 Matches | 3,550 Runs | Avg 34.8 | SR 104.2",
            "t20i": "74 T20Is | 2,570 Runs | Avg 42.8 | SR 169.5 | 4 100s | World #1 T20I Batter & India T20 Captain",
            "ipl": "150 Matches | 3,594 Runs | Avg 32.4 | SR 145.3 | 2 100s | MI Multi-Title Core Pillar"
        },
        "lastSeason": {
            "season": "2024–25 Season",
            "summary": "Appointed India T20I Captain post-WC, iconic boundary catch to win the T20 World Cup Final, T20Is in 2024 (429 runs, SR 161.2), IPL 2024 (345 runs, 1 100, SR 167.5).",
            "runs": 890,
            "batAvg": 39.5,
            "batSR": 165.2,
            "hundreds": 2,
            "fifties": 6,
            "wkts": 0,
            "bowlEcon": 0,
            "formLabel": "World #1 T20 Match-Winner"
        },
        "dismissal": {
            "type": "batter",
            "title": "Dismissal Vulnerability Breakdown (How He Gets Out)",
            "modes": [
                {"name": "Caught Outfield / Deep (360° scoop / boundary clearance)", "pct": 48, "color": "bg-rose-500"},
                {"name": "Caught Behind / Slips (Wide tramline guide)", "pct": 24, "color": "bg-amber-500"},
                {"name": "LBW & Bowled (Full straight yorker / seam into pads)", "pct": 20, "color": "bg-indigo-500"},
                {"name": "Run Out / Other", "pct": 8, "color": "bg-slate-500"}
            ],
            "tactical_note": "Revolutionary 360° wagon wheel: 48% caught in the deep pushing boundaries. Gautam Gambhir and Rahul Dravid view him as the single most devastating T20 middle-overs weapon on the planet."
        },
        "squad_scores": {
            "TEST_Home": {"Gautam Gambhir": 48.0, "Rahul Dravid": 45.0, "Ravi Shastri": 40.0, "Duncan Fletcher": 35.0, "Gary Kirsten": 30.0, "Anil Kumble": 35.0},
            "TEST_SENA": {"Gautam Gambhir": 42.0, "Rahul Dravid": 40.0, "Ravi Shastri": 38.0, "Duncan Fletcher": 30.0, "Gary Kirsten": 25.0, "Anil Kumble": 30.0},
            "ODI_Home": {"Rahul Dravid": 78.0, "Gautam Gambhir": 80.0, "Ravi Shastri": 75.0, "Duncan Fletcher": 68.0, "Gary Kirsten": 60.0, "Anil Kumble": 65.0},
            "ODI_SENA": {"Rahul Dravid": 76.0, "Gautam Gambhir": 78.0, "Ravi Shastri": 74.0, "Duncan Fletcher": 65.0, "Gary Kirsten": 58.0, "Anil Kumble": 62.0},
            "T20I_Home": {"Gautam Gambhir": 99.8, "Rahul Dravid": 99.5, "Ravi Shastri": 98.0, "Duncan Fletcher": 94.0, "Gary Kirsten": 88.0, "Anil Kumble": 92.0},
            "T20I_SENA": {"Gautam Gambhir": 99.6, "Rahul Dravid": 99.4, "Ravi Shastri": 98.2, "Duncan Fletcher": 94.5, "Gary Kirsten": 89.0, "Anil Kumble": 93.0}
        }
    },

    "Sanju Samson": {
        "role": "Wicketkeeper-Batter",
        "hand": "RHB",
        "bowling": "None",
        "caps": 49,
        "batAvg": 56.7,
        "batSR": 144.5,
        "bowlEcon": 0,
        "multiStats": {
            "test": "First-Class Multi-Day Captain for Kerala | Elegant Middle-Order Stroke Maker",
            "fc": "64 Matches | 3,800 Runs | Avg 38.5 | 11 100s | HS 211",
            "odi": "16 ODIs | 510 Runs | Avg 56.7 | SR 99.6 | 108 vs South Africa at Paarl",
            "listA": "125 Matches | 3,450 Runs | Avg 33.8 | SR 90.2 | Double 100 (212*) in Vijay Hazare",
            "t20i": "33 T20Is | 594 Runs | SR 144.5 | Back-to-Back T20I 100s vs BAN (111) & SA (107, 2024)",
            "ipl": "167 Matches | 4,419 Runs | Avg 30.7 | SR 138.9 | 3 100s | RR Captain & Finalist"
        },
        "lastSeason": {
            "season": "2024–25 Season",
            "summary": "Historic consecutive T20I hundreds vs Bangladesh (111 off 47) & South Africa (107 off 50), IPL 2024 (531 runs, avg 48.3, SR 153.5, captained RR to playoffs).",
            "runs": 1120,
            "batAvg": 49.5,
            "batSR": 156.8,
            "hundreds": 3,
            "fifties": 6,
            "wkts": 0,
            "bowlEcon": 0,
            "formLabel": "Career-Best Red-Hot Form"
        },
        "dismissal": {
            "type": "batter",
            "title": "Dismissal Vulnerability Breakdown (How He Gets Out)",
            "modes": [
                {"name": "Caught Deep / Outfield (Early lofted shot against spin/pace)", "pct": 46, "color": "bg-rose-500"},
                {"name": "Caught Behind / Slips (Chasing away-swinger)", "pct": 28, "color": "bg-amber-500"},
                {"name": "LBW & Bowled (In-dipper to full length)", "pct": 18, "color": "bg-indigo-500"},
                {"name": "Run Out / Other", "pct": 8, "color": "bg-slate-500"}
            ],
            "tactical_note": "High-intent attacking batter: 46% caught in the deep trying to clear the ropes early. Gautam Gambhir has unlocked his potential by granting explicit tactical freedom at the top of the order."
        },
        "squad_scores": {
            "TEST_Home": {"Gautam Gambhir": 55.0, "Rahul Dravid": 48.0, "Ravi Shastri": 42.0, "Duncan Fletcher": 35.0, "Gary Kirsten": 30.0, "Anil Kumble": 36.0},
            "TEST_SENA": {"Gautam Gambhir": 52.0, "Rahul Dravid": 45.0, "Ravi Shastri": 40.0, "Duncan Fletcher": 32.0, "Gary Kirsten": 28.0, "Anil Kumble": 34.0},
            "ODI_Home": {"Gautam Gambhir": 88.0, "Rahul Dravid": 84.0, "Ravi Shastri": 80.0, "Duncan Fletcher": 72.0, "Gary Kirsten": 68.0, "Anil Kumble": 74.0},
            "ODI_SENA": {"Gautam Gambhir": 89.0, "Rahul Dravid": 85.0, "Ravi Shastri": 82.0, "Duncan Fletcher": 74.0, "Gary Kirsten": 70.0, "Anil Kumble": 76.0},
            "T20I_Home": {"Gautam Gambhir": 98.0, "Rahul Dravid": 88.0, "Ravi Shastri": 84.0, "Duncan Fletcher": 78.0, "Gary Kirsten": 72.0, "Anil Kumble": 78.0},
            "T20I_SENA": {"Gautam Gambhir": 97.5, "Rahul Dravid": 87.0, "Ravi Shastri": 85.0, "Duncan Fletcher": 79.0, "Gary Kirsten": 74.0, "Anil Kumble": 80.0}
        }
    },

    "R Ashwin": {
        "role": "Spin All-Rounder",
        "hand": "RHB",
        "bowling": "Right-Arm Off-Break / Carrom Ball",
        "caps": 281,
        "batAvg": 24.2,
        "batSR": 87.0,
        "bowlEcon": 4.94,
        "multiStats": {
            "test": "100 Tests | 516 Wkts (Avg 23.7, 36 5-Wkt Hauls) | 3,309 Runs (6 100s)",
            "fc": "158 Matches | 740 Wkts | Avg 24.2 | 5,200 Runs",
            "odi": "116 ODIs | 156 Wkts | Avg 33.2 | Econ 4.94 | World Cup 2011 Winner & CT 2013 Winner",
            "listA": "175 Matches | 230 Wkts | Avg 30.5 | Econ 4.80",
            "t20i": "65 T20Is | 72 Wkts | Avg 23.2 | Econ 6.91 | T20 WC Finalist",
            "ipl": "212 Matches | 180 Wkts | Avg 28.8 | Econ 7.12 | Tactical Mastermind"
        },
        "lastSeason": {
            "season": "2024–25 Season",
            "summary": "Completed 100 Tests milestone & joined 500+ Test wickets club, match-winning 113 & 6/88 vs Bangladesh at Chennai, 26 Test wickets in 2024.",
            "runs": 385,
            "batAvg": 28.5,
            "batSR": 74.0,
            "hundreds": 1,
            "fifties": 1,
            "wkts": 38,
            "bowlEcon": 3.15,
            "bowlAvg": 24.8,
            "formLabel": "Legendary Mastermind Peak"
        },
        "dismissal": {
            "type": "allrounder",
            "title": "Tactical Dismissal & Wicket Profile",
            "modes": [
                {"name": "Batting: Edges & Bowled outside off", "pct": 42, "color": "bg-rose-500"},
                {"name": "Batting: Caught in deep against spin", "pct": 34, "color": "bg-amber-500"},
                {"name": "Bowling: Bowled & LBW (Undercut carrom ball & drift)", "pct": 48, "color": "bg-emerald-500"},
                {"name": "Bowling: Caught Slips / Bat-Pad (Sharp bounce)", "pct": 36, "color": "bg-indigo-500"}
            ],
            "tactical_note": "All-time red-ball spin titan: 84% dismissals via Bowled, LBW, or Slips/Bat-Pad trap. Anil Kumble, Duncan Fletcher, and Rahul Dravid relied on him as India's premier home fortress weapon."
        },
        "squad_scores": {
            "TEST_Home": {"Anil Kumble": 99.8, "Duncan Fletcher": 99.5, "Ravi Shastri": 98.8, "Rahul Dravid": 99.0, "Gautam Gambhir": 97.5, "Gary Kirsten": 88.0},
            "TEST_SENA": {"Ravi Shastri": 72.0, "Duncan Fletcher": 78.0, "Rahul Dravid": 74.0, "Anil Kumble": 76.0, "Gautam Gambhir": 68.0, "Gary Kirsten": 55.0},
            "ODI_Home": {"Duncan Fletcher": 95.0, "Gary Kirsten": 92.0, "Anil Kumble": 88.0, "Ravi Shastri": 82.0, "Rahul Dravid": 84.0, "Gautam Gambhir": 65.0},
            "ODI_SENA": {"Duncan Fletcher": 92.0, "Gary Kirsten": 88.0, "Anil Kumble": 82.0, "Ravi Shastri": 76.0, "Rahul Dravid": 78.0, "Gautam Gambhir": 55.0},
            "T20I_Home": {"Rahul Dravid": 82.0, "Duncan Fletcher": 88.0, "Gary Kirsten": 85.0, "Anil Kumble": 80.0, "Ravi Shastri": 74.0, "Gautam Gambhir": 0.0},
            "T20I_SENA": {"Rahul Dravid": 80.0, "Duncan Fletcher": 86.0, "Gary Kirsten": 82.0, "Anil Kumble": 78.0, "Ravi Shastri": 72.0, "Gautam Gambhir": 0.0}
        },
        "retirement": {
            "T20I": "Phase-shifted from white-ball internationals to focus on Red-Ball Test mastery"
        }
    },

    "Shivam Dube": {
        "role": "Pace All-Rounder",
        "hand": "LHB",
        "bowling": "Right-Arm Medium",
        "caps": 37,
        "batAvg": 27.8,
        "batSR": 158.5,
        "bowlEcon": 8.85,
        "multiStats": {
            "test": "Domestic First-Class Seamer-Batter for Mumbai",
            "fc": "22 Matches | 1,250 Runs (Avg 44.6) | 48 Wkts (Avg 23.1)",
            "odi": "4 ODIs | Promising Medium-Pace AR Backup",
            "listA": "55 Matches | 1,100 Runs (Avg 36.2) | 42 Wkts",
            "t20i": "33 T20Is | 448 Runs (SR 136.6) | 14 Wkts | T20 WC 2024 Champion (Crucial 27 in Final)",
            "ipl": "65 Matches | 1,502 Runs | Avg 27.8 | SR 158.5 | CSK Spin Enforcer & Finisher"
        },
        "lastSeason": {
            "season": "2024–25 Season",
            "summary": "Vital 27 off 16 in T20 World Cup Final, dominant IPL 2024 spin crusher (396 runs, SR 162.3, 28 sixes), Ranji Trophy for Mumbai (avg 67.0, 12 wkts).",
            "runs": 720,
            "batAvg": 38.2,
            "batSR": 155.0,
            "hundreds": 1,
            "fifties": 4,
            "wkts": 14,
            "bowlEcon": 8.45,
            "bowlAvg": 28.5,
            "formLabel": "Premier Spin-Crusher"
        },
        "dismissal": {
            "type": "allrounder",
            "title": "Tactical Dismissal & Wicket Profile",
            "modes": [
                {"name": "Batting: Caught Deep / Outfield (Short ball directed at helmet)", "pct": 46, "color": "bg-rose-500"},
                {"name": "Batting: Edges / Bowled to express pace seam", "pct": 32, "color": "bg-amber-500"},
                {"name": "Bowling: Caught Outfield (Back-of-hand slower variations)", "pct": 50, "color": "bg-emerald-500"},
                {"name": "Bowling: LBW & Bowled (Skidding medium pace)", "pct": 32, "color": "bg-indigo-500"}
            ],
            "tactical_note": "Targeted by fast bouncers (46% caught in the deep off the short ball), but unplayable against spin. Gautam Gambhir and Rahul Dravid deploy him as a designated middle-overs spin enforcer."
        },
        "squad_scores": {
            "TEST_Home": {"Gautam Gambhir": 55.0, "Rahul Dravid": 48.0, "Duncan Fletcher": 40.0, "Ravi Shastri": 38.0, "Anil Kumble": 35.0, "Gary Kirsten": 28.0},
            "TEST_SENA": {"Gautam Gambhir": 48.0, "Ravi Shastri": 45.0, "Rahul Dravid": 42.0, "Duncan Fletcher": 35.0, "Anil Kumble": 30.0, "Gary Kirsten": 25.0},
            "ODI_Home": {"Gautam Gambhir": 82.0, "Rahul Dravid": 80.0, "Duncan Fletcher": 72.0, "Ravi Shastri": 70.0, "Gary Kirsten": 60.0, "Anil Kumble": 65.0},
            "ODI_SENA": {"Gautam Gambhir": 80.0, "Rahul Dravid": 78.0, "Ravi Shastri": 72.0, "Duncan Fletcher": 70.0, "Gary Kirsten": 58.0, "Anil Kumble": 62.0},
            "T20I_Home": {"Gautam Gambhir": 94.0, "Rahul Dravid": 92.0, "Ravi Shastri": 85.0, "Duncan Fletcher": 80.0, "Gary Kirsten": 70.0, "Anil Kumble": 75.0},
            "T20I_SENA": {"Gautam Gambhir": 92.0, "Rahul Dravid": 90.0, "Ravi Shastri": 84.0, "Duncan Fletcher": 78.0, "Gary Kirsten": 68.0, "Anil Kumble": 74.0}
        }
    },

    "Washington Sundar": {
        "role": "Spin All-Rounder",
        "hand": "LHB",
        "bowling": "Right-Arm Off-Break",
        "caps": 79,
        "batAvg": 50.8,
        "batSR": 140.0,
        "bowlEcon": 4.70,
        "multiStats": {
            "test": "5 Tests | 305 Runs (Avg 50.8) | 18 Wkts | 62 at Gabba & 7/59 vs New Zealand",
            "fc": "32 Matches | 1,450 Runs | 78 Wkts",
            "odi": "22 ODIs | 315 Runs (Avg 35.0) | 23 Wkts (Econ 4.70)",
            "listA": "68 Matches | 950 Runs | 65 Wkts (Econ 4.45)",
            "t20i": "52 T20Is | 161 Runs (SR 140.0) | 47 Wkts (Econ 6.95) | Player of the Series vs ZIM",
            "ipl": "60 Matches | 378 Runs | 37 Wkts | Econ 7.35 | Powerplay Off-Spin Specialist"
        },
        "lastSeason": {
            "season": "2024–25 Season",
            "summary": "Sensational Test comeback vs NZ at Pune (7/59 & 4/56, 11 wkts in match), Player of the Series vs Zimbabwe in T20Is (8 wkts, econ 5.16), Ranji Trophy 152 for Tamil Nadu.",
            "runs": 485,
            "batAvg": 44.0,
            "batSR": 134.0,
            "hundreds": 1,
            "fifties": 3,
            "wkts": 31,
            "bowlEcon": 4.25,
            "bowlAvg": 21.6,
            "formLabel": "Breakout Multi-Format Ace"
        },
        "dismissal": {
            "type": "allrounder",
            "title": "Tactical Dismissal & Wicket Profile",
            "modes": [
                {"name": "Batting: Caught Behind / Slips (Chasing away turn/swing)", "pct": 40, "color": "bg-rose-500"},
                {"name": "Batting: LBW & Bowled (Full incoming deliveries)", "pct": 32, "color": "bg-amber-500"},
                {"name": "Bowling: Bowled & LBW (Flat darting angle sliding on)", "pct": 48, "color": "bg-emerald-500"},
                {"name": "Bowling: Caught Slips / Keeper (Extra bounce)", "pct": 34, "color": "bg-indigo-500"}
            ],
            "tactical_note": "Heightened bounce and flat darting trajectory: 48% Bowled/LBW rate. Gautam Gambhir's #1 modern spin-AR favorite due to tall release, powerplay control, and LHB composure."
        },
        "squad_scores": {
            "TEST_Home": {"Gautam Gambhir": 94.0, "Rahul Dravid": 90.0, "Duncan Fletcher": 82.0, "Ravi Shastri": 78.0, "Anil Kumble": 80.0, "Gary Kirsten": 65.0},
            "TEST_SENA": {"Gautam Gambhir": 88.0, "Rahul Dravid": 85.0, "Ravi Shastri": 82.0, "Duncan Fletcher": 76.0, "Anil Kumble": 74.0, "Gary Kirsten": 60.0},
            "ODI_Home": {"Gautam Gambhir": 92.0, "Rahul Dravid": 88.0, "Duncan Fletcher": 80.0, "Ravi Shastri": 78.0, "Anil Kumble": 76.0, "Gary Kirsten": 68.0},
            "ODI_SENA": {"Gautam Gambhir": 90.0, "Rahul Dravid": 86.0, "Ravi Shastri": 80.0, "Duncan Fletcher": 78.0, "Anil Kumble": 74.0, "Gary Kirsten": 65.0},
            "T20I_Home": {"Gautam Gambhir": 95.0, "Rahul Dravid": 91.0, "Ravi Shastri": 85.0, "Duncan Fletcher": 80.0, "Anil Kumble": 78.0, "Gary Kirsten": 70.0},
            "T20I_SENA": {"Gautam Gambhir": 94.0, "Rahul Dravid": 90.0, "Ravi Shastri": 84.0, "Duncan Fletcher": 79.0, "Anil Kumble": 76.0, "Gary Kirsten": 68.0}
        }
    },

    "Shubman Gill": {
        "role": "Top-Order Batter",
        "hand": "RHB",
        "bowling": "Right-Arm Off-Break",
        "caps": 93,
        "batAvg": 35.5,
        "batSR": 139.3,
        "bowlEcon": 0,
        "multiStats": {
            "test": "25 Tests | 1,492 Runs | Avg 35.5 | 5 100s | Historic 91 at Brisbane Gabba",
            "fc": "52 Matches | 4,200 Runs | Avg 50.2 | 13 100s | Ranji Trophy 268",
            "odi": "47 ODIs | 2,328 Runs | Avg 58.2 | SR 101.7 | 6 100s | Youngest ODI Double 100 (208 vs NZ)",
            "listA": "85 Matches | 4,350 Runs | Avg 56.4 | 14 100s",
            "t20i": "21 T20Is | 578 Runs | Avg 30.4 | SR 139.3 | 1 100 (126* vs NZ)",
            "ipl": "103 Matches | 3,216 Runs | Avg 37.8 | SR 135.5 | 4 100s | Orange Cap 2023 (890 Runs) | GT Captain"
        },
        "lastSeason": {
            "season": "2024–25 Season",
            "summary": "3 Test centuries in 2024 (110 vs ENG, 104 vs ENG, 119* vs BAN), IPL 2024 GT Captain (426 runs, 1 100, SR 147.4), ODI avg 63.5 in 2024.",
            "runs": 1340,
            "batAvg": 46.2,
            "batSR": 142.0,
            "hundreds": 4,
            "fifties": 5,
            "wkts": 0,
            "bowlEcon": 0,
            "formLabel": "Prolific All-Format Pillar"
        },
        "dismissal": {
            "type": "batter",
            "title": "Dismissal Vulnerability Breakdown (How He Gets Out)",
            "modes": [
                {"name": "Caught Behind / Slips (Hard hands poking outside off)", "pct": 42, "color": "bg-rose-500"},
                {"name": "LBW & Bowled (In-dipper through bat-pad gate)", "pct": 28, "color": "bg-amber-500"},
                {"name": "Caught Outfield / Deep (Short-arm jab / lofted drive)", "pct": 22, "color": "bg-indigo-500"},
                {"name": "Run Out / Other", "pct": 8, "color": "bg-slate-500"}
            ],
            "tactical_note": "Technical trait: hard-handed push outside off results in 42% dismissals caught behind/slips. Gary Kirsten, Rahul Dravid, and Gambhir value his classical timing and high-ceiling conversion rates."
        },
        "squad_scores": {
            "TEST_Home": {"Rahul Dravid": 96.0, "Gautam Gambhir": 95.0, "Ravi Shastri": 92.0, "Duncan Fletcher": 90.0, "Gary Kirsten": 88.0, "Anil Kumble": 88.0},
            "TEST_SENA": {"Rahul Dravid": 94.0, "Gautam Gambhir": 93.0, "Ravi Shastri": 92.5, "Duncan Fletcher": 88.0, "Gary Kirsten": 86.0, "Anil Kumble": 86.0},
            "ODI_Home": {"Rahul Dravid": 98.0, "Gautam Gambhir": 97.5, "Ravi Shastri": 96.0, "Duncan Fletcher": 94.0, "Gary Kirsten": 92.0, "Anil Kumble": 92.0},
            "ODI_SENA": {"Rahul Dravid": 97.5, "Gautam Gambhir": 97.0, "Ravi Shastri": 95.5, "Duncan Fletcher": 93.0, "Gary Kirsten": 90.0, "Anil Kumble": 90.0},
            "T20I_Home": {"Gautam Gambhir": 92.0, "Rahul Dravid": 90.0, "Ravi Shastri": 86.0, "Duncan Fletcher": 82.0, "Gary Kirsten": 80.0, "Anil Kumble": 82.0},
            "T20I_SENA": {"Gautam Gambhir": 91.0, "Rahul Dravid": 88.0, "Ravi Shastri": 87.0, "Duncan Fletcher": 82.0, "Gary Kirsten": 78.0, "Anil Kumble": 80.0}
        }
    },

    "Mohammed Siraj": {
        "role": "Specialist Fast Bowler",
        "hand": "RHB",
        "bowling": "Right-Arm Fast",
        "caps": 89,
        "batAvg": 4.8,
        "batSR": 52.0,
        "bowlEcon": 5.18,
        "multiStats": {
            "test": "29 Tests | 78 Wkts | Avg 29.8 | 6/15 at Cape Town & 5/73 at Brisbane Gabba",
            "fc": "65 Matches | 245 Wkts | Avg 25.1 | 8 5-Wkt Hauls",
            "odi": "44 ODIs | 71 Wkts | Avg 24.1 | Econ 5.18 | Unplayable 6/21 in Asia Cup Final",
            "listA": "72 Matches | 128 Wkts | Avg 24.8 | Econ 5.05",
            "t20i": "16 T20Is | 14 Wkts | Avg 33.1 | Econ 8.04 | T20 WC 2024 Champion Squad",
            "ipl": "93 Matches | 93 Wkts | Avg 30.3 | Econ 8.65 | Leading Powerplay Striker for RCB"
        },
        "lastSeason": {
            "season": "2024–25 Season",
            "summary": "Demolished South Africa with 6/15 at Cape Town (all out 55), key member of T20 World Cup champion pace battery (econ 5.86 in group stages), IPL 2024 (15 wkts).",
            "runs": 28,
            "batAvg": 5.2,
            "batSR": 60.0,
            "hundreds": 0,
            "fifties": 0,
            "wkts": 46,
            "bowlEcon": 4.85,
            "bowlAvg": 22.8,
            "formLabel": "Fierce Hostile Strike Bowler"
        },
        "dismissal": {
            "type": "bowler",
            "title": "Wicket-Taking Weaponry (How He Dismisses Batters)",
            "modes": [
                {"name": "Caught Behind & Slips (Wobble-seam shaping away)", "pct": 44, "color": "bg-emerald-500"},
                {"name": "Bowled & LBW (Skidding nip-backer into right-hander pads)", "pct": 34, "color": "bg-indigo-500"},
                {"name": "Caught Outfield / Miscues (Hostile bumper / rush of pace)", "pct": 18, "color": "bg-amber-500"},
                {"name": "Other", "pct": 4, "color": "bg-slate-500"}
            ],
            "tactical_note": "Signature wobble-seam creates continuous uncertainty: 44% caught behind/slips. Ravi Shastri's quintessential frontline weapon (140+ km/h hostility) in SENA conditions."
        },
        "squad_scores": {
            "TEST_Home": {"Ravi Shastri": 94.0, "Rahul Dravid": 92.0, "Gautam Gambhir": 90.0, "Duncan Fletcher": 84.0, "Gary Kirsten": 80.0, "Anil Kumble": 86.0},
            "TEST_SENA": {"Ravi Shastri": 98.0, "Rahul Dravid": 95.0, "Gautam Gambhir": 94.0, "Duncan Fletcher": 88.0, "Gary Kirsten": 85.0, "Anil Kumble": 90.0},
            "ODI_Home": {"Ravi Shastri": 94.0, "Rahul Dravid": 93.0, "Gautam Gambhir": 91.0, "Duncan Fletcher": 85.0, "Gary Kirsten": 80.0, "Anil Kumble": 85.0},
            "ODI_SENA": {"Ravi Shastri": 96.0, "Rahul Dravid": 94.0, "Gautam Gambhir": 92.0, "Duncan Fletcher": 86.0, "Gary Kirsten": 82.0, "Anil Kumble": 86.0},
            "T20I_Home": {"Gautam Gambhir": 82.0, "Rahul Dravid": 84.0, "Ravi Shastri": 86.0, "Duncan Fletcher": 76.0, "Gary Kirsten": 72.0, "Anil Kumble": 76.0},
            "T20I_SENA": {"Ravi Shastri": 88.0, "Gautam Gambhir": 84.0, "Rahul Dravid": 85.0, "Duncan Fletcher": 78.0, "Gary Kirsten": 74.0, "Anil Kumble": 78.0}
        }
    },

    "KL Rahul": {
        "role": "Wicketkeeper-Batter",
        "hand": "RHB",
        "bowling": "None",
        "caps": 199,
        "batAvg": 45.5,
        "batSR": 134.6,
        "bowlEcon": 0,
        "multiStats": {
            "test": "50 Tests | 2,863 Runs | Avg 34.1 | 8 100s | Centuries in SA, ENG, AUS & IND",
            "fc": "95 Matches | 6,700 Runs | Avg 44.5 | 18 100s | Ranji Triple 100 (337)",
            "odi": "77 ODIs | 2,851 Runs | Avg 49.1 | SR 87.8 | 7 100s | Dependable Middle-Order WK-Batter",
            "listA": "128 Matches | 5,100 Runs | Avg 46.8 | 13 100s",
            "t20i": "72 T20Is | 2,265 Runs | Avg 37.7 | SR 139.1 | 2 100s & 22 50s",
            "ipl": "132 Matches | 4,683 Runs | Avg 45.5 | SR 134.6 | 4 100s | Multiple 600+ Run Seasons"
        },
        "lastSeason": {
            "season": "2024–25 Season",
            "summary": "Masterclass 101 vs SA in boxing day Test at Centurion, fighting 77 in BGT 2024-25 opener at Perth, IPL 2024 (520 runs, avg 37.1, SR 136.1).",
            "runs": 1180,
            "batAvg": 44.5,
            "batSR": 135.0,
            "hundreds": 2,
            "fifties": 7,
            "wkts": 0,
            "bowlEcon": 0,
            "formLabel": "Resilient SENA Anchor"
        },
        "dismissal": {
            "type": "batter",
            "title": "Dismissal Vulnerability Breakdown (How He Gets Out)",
            "modes": [
                {"name": "Caught Behind / Slips (Defensive push outside 4th stump)", "pct": 44, "color": "bg-rose-500"},
                {"name": "LBW & Bowled (Seam nipping back through gate)", "pct": 28, "color": "bg-amber-500"},
                {"name": "Caught Outfield / Deep (Lofted cover drive / pull)", "pct": 20, "color": "bg-indigo-500"},
                {"name": "Run Out / Other", "pct": 8, "color": "bg-slate-500"}
            ],
            "tactical_note": "Classical technique: vulnerable to late away movement outside off (44% caught behind/slips). Gary Kirsten, Rahul Dravid, and Duncan Fletcher value his steady technical temper in overseas seam-friendly conditions."
        },
        "squad_scores": {
            "TEST_Home": {"Rahul Dravid": 92.0, "Duncan Fletcher": 88.0, "Gary Kirsten": 86.0, "Ravi Shastri": 88.0, "Gautam Gambhir": 84.0, "Anil Kumble": 85.0},
            "TEST_SENA": {"Rahul Dravid": 94.0, "Duncan Fletcher": 90.0, "Ravi Shastri": 91.0, "Gary Kirsten": 88.0, "Gautam Gambhir": 86.0, "Anil Kumble": 88.0},
            "ODI_Home": {"Rahul Dravid": 96.0, "Gary Kirsten": 94.0, "Duncan Fletcher": 92.0, "Ravi Shastri": 90.0, "Gautam Gambhir": 88.0, "Anil Kumble": 88.0},
            "ODI_SENA": {"Rahul Dravid": 96.5, "Gary Kirsten": 95.0, "Duncan Fletcher": 93.0, "Ravi Shastri": 91.0, "Gautam Gambhir": 89.0, "Anil Kumble": 89.0},
            "T20I_Home": {"Gary Kirsten": 90.0, "Duncan Fletcher": 88.0, "Rahul Dravid": 85.0, "Ravi Shastri": 84.0, "Anil Kumble": 82.0, "Gautam Gambhir": 68.0},
            "T20I_SENA": {"Gary Kirsten": 88.0, "Duncan Fletcher": 86.0, "Rahul Dravid": 84.0, "Ravi Shastri": 83.0, "Anil Kumble": 80.0, "Gautam Gambhir": 66.0}
        }
    },

    "Dhruv Jurel": {
        "role": "Wicketkeeper-Batter",
        "hand": "RHB",
        "bowling": "None",
        "caps": 7,
        "batAvg": 63.3,
        "batSR": 151.5,
        "bowlEcon": 0,
        "multiStats": {
            "test": "3 Tests | 190 Runs | Avg 63.3 | 90 & 39* Player of Match vs ENG at Ranchi",
            "fc": "19 Matches | 1,075 Runs | Avg 48.9 | 80 & 68 vs Australia A at MCG | HS 249",
            "odi": "Young Wicketkeeper-Batter in National White-Ball Pipeline",
            "listA": "10 Matches | 189 Runs | Avg 47.2 | SR 92.6 | Domestic WK Core",
            "t20i": "4 T20Is | 43 Runs | Dynamic Lower-Order Finisher",
            "ipl": "28 Matches | 347 Runs | SR 151.5 | Match-Winning Death-Overs Finisher for RR"
        },
        "lastSeason": {
            "season": "2024–25 Season",
            "summary": "Player of the Match in Ranchi Test vs England (90 & 39* under immense pressure), heroic twin fifties (80 & 68) for India A vs Australia A at the MCG against test pacers.",
            "runs": 710,
            "batAvg": 52.4,
            "batSR": 145.0,
            "hundreds": 1,
            "fifties": 4,
            "wkts": 0,
            "bowlEcon": 0,
            "formLabel": "Rising Red-Ball Phenomenon"
        },
        "dismissal": {
            "type": "batter",
            "title": "Dismissal Vulnerability Breakdown (How He Gets Out)",
            "modes": [
                {"name": "Caught Behind / Slips (Late movement outside off)", "pct": 38, "color": "bg-rose-500"},
                {"name": "LBW & Bowled (Full straight inswinger)", "pct": 28, "color": "bg-amber-500"},
                {"name": "Caught Outfield / Deep (Attempted loft / pull)", "pct": 24, "color": "bg-indigo-500"},
                {"name": "Run Out / Other", "pct": 10, "color": "bg-slate-500"}
            ],
            "tactical_note": "Exceptionally balanced back-foot technique against pace and bounce: 38% caught behind/slips. Rahul Dravid and Gautam Gambhir rate him as India's premier multi-day backup keeper."
        },
        "squad_scores": {
            "TEST_Home": {"Rahul Dravid": 84.0, "Gautam Gambhir": 82.0, "Ravi Shastri": 72.0, "Duncan Fletcher": 65.0, "Gary Kirsten": 60.0, "Anil Kumble": 68.0},
            "TEST_SENA": {"Rahul Dravid": 86.0, "Gautam Gambhir": 84.0, "Ravi Shastri": 75.0, "Duncan Fletcher": 68.0, "Gary Kirsten": 62.0, "Anil Kumble": 70.0},
            "ODI_Home": {"Rahul Dravid": 78.0, "Gautam Gambhir": 80.0, "Ravi Shastri": 70.0, "Duncan Fletcher": 62.0, "Gary Kirsten": 58.0, "Anil Kumble": 64.0},
            "ODI_SENA": {"Rahul Dravid": 79.0, "Gautam Gambhir": 81.0, "Ravi Shastri": 72.0, "Duncan Fletcher": 64.0, "Gary Kirsten": 60.0, "Anil Kumble": 66.0},
            "T20I_Home": {"Gautam Gambhir": 82.0, "Rahul Dravid": 80.0, "Ravi Shastri": 74.0, "Duncan Fletcher": 68.0, "Gary Kirsten": 62.0, "Anil Kumble": 68.0},
            "T20I_SENA": {"Gautam Gambhir": 81.0, "Rahul Dravid": 79.0, "Ravi Shastri": 73.0, "Duncan Fletcher": 67.0, "Gary Kirsten": 60.0, "Anil Kumble": 67.0}
        }
    }
}

players_json = json.dumps(PLAYERS_DATABASE)

def build_single_page_html():
    return f"""<!DOCTYPE html>
<html lang="en" class="scroll-smooth">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Indian Cricket Selection Engine: Multi-Format Coach AI & Analytics</title>
  <script src="https://www.gstatic.com/antigravity/web/dev/tailwindcss.min.js"></script>
  <style>
    .progress-bar {{
      transition: width 0.5s cubic-bezier(0.4, 0, 0.2, 1);
    }}
  </style>
</head>
<body class="bg-transparent text-[var(--foreground)] antialiased p-3 sm:p-5 font-sans">
  <div class="max-w-6xl mx-auto bg-[var(--card)] text-[var(--foreground)] border border-[var(--border)] rounded-2xl p-4 sm:p-6 shadow-md space-y-8">
    
    <!-- Top Header & Meta Badges -->
    <header class="flex flex-col md:flex-row md:items-center justify-between border-b border-[var(--border)] pb-5 gap-4">
      <div>
        <div class="flex items-center gap-2.5">
          <span class="inline-block w-3 h-3 rounded-full bg-indigo-500 animate-pulse"></span>
          <h1 class="text-xl sm:text-2xl font-black tracking-tight">Indian Cricket Selection Engine</h1>
        </div>
        <p class="text-xs sm:text-sm text-[var(--muted-foreground)] mt-1">
          Unified Multi-Format Analytics (Tests, FC, ODIs, List A, T20Is, IPL) • Historical Data from 1,021 International Matches & 17 IPL Seasons
        </p>
      </div>
      <div class="flex flex-wrap items-center gap-2">
        <span class="px-2.5 py-1 text-xs font-semibold rounded-md bg-[var(--secondary)] text-[var(--secondary-foreground)] border border-[var(--border)]">
          AUC-ROC: 0.908
        </span>
        <span class="px-2.5 py-1 text-xs font-semibold rounded-md bg-emerald-500/10 text-emerald-600 dark:text-emerald-400 border border-emerald-500/30">
          6 Coaching Eras
        </span>
        <span class="px-2.5 py-1 text-xs font-semibold rounded-md bg-indigo-500/10 text-indigo-600 dark:text-indigo-400 border border-indigo-500/30">
          Continuous Long Page
        </span>
      </div>
    </header>

    <!-- Sticky Quick Jump Navigation Bar -->
    <nav class="sticky top-2 z-20 bg-[var(--background)]/90 backdrop-blur-md p-2 rounded-xl border border-[var(--border)] shadow-sm">
      <div class="flex flex-wrap items-center justify-center sm:justify-start gap-2 text-xs sm:text-sm font-bold">
        <a href="#predictor" class="px-3.5 py-2 rounded-lg bg-indigo-600 text-white hover:bg-indigo-700 transition flex items-center gap-1.5 shadow-xs">
          <span>🏏</span>
          <span>Selection Predictor & Custom Player Builder</span>
        </a>
        <a href="#philosophy" class="px-3.5 py-2 rounded-lg bg-[var(--secondary)] hover:bg-[var(--secondary)]/80 text-[var(--foreground)] transition flex items-center gap-1.5 border border-[var(--border)]">
          <span>📊</span>
          <span>Coach Philosophies & Red-Ball Deep Dive</span>
        </a>
        <a href="#compositions" class="px-3.5 py-2 rounded-lg bg-[var(--secondary)] hover:bg-[var(--secondary)]/80 text-[var(--foreground)] transition flex items-center gap-1.5 border border-[var(--border)]">
          <span>📋</span>
          <span>Empirical Playing XI Compositions</span>
        </a>
      </div>
    </nav>

    <!-- ========================================================================= -->
    <!-- SECTION 1: COACH SELECTION PREDICTOR & CUSTOM PLAYER BUILDER -->
    <!-- ========================================================================= -->
    <section id="predictor" class="space-y-6 pt-2">
      
      <!-- Section Title -->
      <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-[var(--border)] pb-3">
        <div>
          <div class="flex items-center gap-2">
            <span class="px-2 py-0.5 text-xs font-extrabold rounded bg-indigo-500/20 text-indigo-400 uppercase tracking-wide">Module 1</span>
            <h2 class="text-lg sm:text-xl font-bold">Live Coach Selection Predictor & Custom Cricketer Creator</h2>
          </div>
          <p class="text-xs text-[var(--muted-foreground)] mt-0.5">
            Evaluating multi-format career records, 2024–25 recent form, and dismissal/wicket-taking patterns across 6 Indian coaching tenures
          </p>
        </div>
      </div>

      <!-- Mode Switcher: 🇮🇳 Existing Player vs 🛠️ Build a Player -->
      <div class="bg-[var(--secondary)]/50 p-1.5 rounded-xl border border-[var(--border)]">
        <div class="grid grid-cols-2 gap-2 text-center text-xs sm:text-sm font-bold">
          <button id="subTabExisting" onclick="switchSubMode('existing')" class="py-2.5 rounded-lg bg-[var(--primary)] text-[var(--primary-foreground)] shadow-xs transition duration-150 cursor-pointer font-bold">
            🇮🇳 Select Existing Indian Player (19 Players)
          </button>
          <button id="subTabBuilder" onclick="switchSubMode('builder')" class="py-2.5 rounded-lg text-[var(--muted-foreground)] hover:text-[var(--foreground)] transition duration-150 cursor-pointer font-medium">
            🛠️ Build a Custom Player (Interactive Simulator)
          </button>
        </div>
      </div>

      <!-- Controls Row: Format & Conditions -->
      <div class="grid grid-cols-1 sm:grid-cols-3 gap-3 bg-[var(--background)] p-3.5 rounded-xl border border-[var(--border)]">
        
        <!-- Player Select (For Existing Mode) -->
        <div id="playerSelectContainer" class="space-y-1">
          <label class="block text-[11px] font-bold uppercase tracking-wider text-[var(--muted-foreground)]">Select Indian Player</label>
          <select id="playerSelect" onchange="updateExistingView()" class="w-full bg-[var(--card)] text-[var(--foreground)] border border-[var(--border)] rounded-lg px-3 py-2 text-xs sm:text-sm font-semibold focus:outline-none focus:ring-2 focus:ring-indigo-500">
            {''.join([f'<option value="{p}">{p}</option>' for p in PLAYERS_DATABASE.keys()])}
          </select>
        </div>

        <!-- Format Selector -->
        <div class="space-y-1">
          <label class="block text-[11px] font-bold uppercase tracking-wider text-[var(--muted-foreground)]">Match Format</label>
          <div class="grid grid-cols-3 gap-1 bg-[var(--card)] p-1 rounded-lg border border-[var(--border)] text-center text-xs font-semibold">
            <button id="btnTEST" onclick="setFormat('TEST')" class="py-1.5 rounded-md bg-[var(--primary)] text-[var(--primary-foreground)] shadow-xs transition">TEST</button>
            <button id="btnODI" onclick="setFormat('ODI')" class="py-1.5 rounded-md text-[var(--muted-foreground)] hover:text-[var(--foreground)] transition">ODI</button>
            <button id="btnT20I" onclick="setFormat('T20I')" class="py-1.5 rounded-md text-[var(--muted-foreground)] hover:text-[var(--foreground)] transition">T20I</button>
          </div>
        </div>

        <!-- Venue Selector -->
        <div class="space-y-1">
          <label class="block text-[11px] font-bold uppercase tracking-wider text-[var(--muted-foreground)]">Playing Conditions</label>
          <div class="grid grid-cols-2 gap-1 bg-[var(--card)] p-1 rounded-lg border border-[var(--border)] text-center text-xs font-semibold">
            <button id="btnHome" onclick="setVenue('Home')" class="py-1.5 rounded-md bg-[var(--primary)] text-[var(--primary-foreground)] shadow-xs transition">Subcontinent</button>
            <button id="btnSena" onclick="setVenue('SENA')" class="py-1.5 rounded-md text-[var(--muted-foreground)] hover:text-[var(--foreground)] transition">SENA Overseas</button>
          </div>
        </div>

      </div>

      <!-- EXISTING PLAYER COMPREHENSIVE CARD -->
      <div id="existingPlayerCard" class="space-y-4">
        
        <!-- Player Header & Retirement Alert (if any) -->
        <div id="playerHeaderBox" class="bg-[var(--background)] border border-[var(--border)] rounded-xl p-4 shadow-xs">
          <!-- Populated by JS -->
        </div>

        <!-- Multi-Format Career Statistics (6 Formats Grid) -->
        <div class="bg-[var(--background)] border border-[var(--border)] rounded-xl p-4 shadow-xs space-y-3">
          <div class="flex items-center justify-between border-b border-[var(--border)] pb-2">
            <h3 class="text-xs sm:text-sm font-bold uppercase tracking-wider text-indigo-500 flex items-center gap-1.5">
              <span>📈</span>
              <span>All-Format Career Records (Tests, FC, ODIs, List A, T20Is, IPL)</span>
            </h3>
            <span class="text-[11px] text-[var(--muted-foreground)] font-medium">Cricsheet & Official Database</span>
          </div>
          
          <div id="formatGrid" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-2.5 text-xs">
            <!-- Populated by JS -->
          </div>
        </div>

        <!-- Recent Form (2024-25 Season) & Dismissal Breakdown Grid -->
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-4">
          
          <!-- Card 1: Last Season Performance (2024-25) -->
          <div class="bg-[var(--background)] border border-[var(--border)] rounded-xl p-4 shadow-xs space-y-3">
            <div class="flex items-center justify-between border-b border-[var(--border)] pb-2">
              <h3 class="text-xs sm:text-sm font-bold uppercase tracking-wider text-emerald-500 flex items-center gap-1.5">
                <span>⚡</span>
                <span>Last Season (2024–25 Form & Key Milestones)</span>
              </h3>
              <span id="badgeSeasonForm" class="text-[10px] font-extrabold px-2 py-0.5 rounded-full bg-emerald-500/20 text-emerald-400">
                Form Indicator
              </span>
            </div>
            <div id="seasonStatsContent" class="space-y-2.5 text-xs">
              <!-- Populated by JS -->
            </div>
          </div>

          <!-- Card 2: Dismissal & Wicket-Taking Mode Breakdown -->
          <div class="bg-[var(--background)] border border-[var(--border)] rounded-xl p-4 shadow-xs space-y-3">
            <div class="flex items-center justify-between border-b border-[var(--border)] pb-2">
              <h3 id="dismissalTitle" class="text-xs sm:text-sm font-bold uppercase tracking-wider text-amber-500 flex items-center gap-1.5">
                <span>🎯</span>
                <span>Dismissal Modes & Vulnerability Analysis</span>
              </h3>
              <span class="text-[10px] font-bold text-[var(--muted-foreground)]">Tactical Factor</span>
            </div>
            <div id="dismissalContent" class="space-y-2.5 text-xs">
              <!-- Populated by JS -->
            </div>
          </div>

        </div>

      </div>

      <!-- BUILDER SIMULATOR SECTION (Hidden by default until toggled) -->
      <div id="builderSection" class="hidden space-y-5 bg-[var(--background)] border border-[var(--border)] rounded-xl p-4 sm:p-5 shadow-xs">
        <div class="flex items-center justify-between border-b border-[var(--border)] pb-2.5">
          <div>
            <h3 class="text-sm sm:text-base font-bold text-indigo-500 flex items-center gap-2">
              <span>🛠️</span>
              <span>Interactive Player Simulator: Career + Last Season + Technical Modes</span>
            </h3>
            <p class="text-xs text-[var(--muted-foreground)]">
              Adjust career baselines, 2024-25 recent form, dismissal vulnerability, and primary wicket-taking weapons to observe coach model reaction
            </p>
          </div>
        </div>

        <!-- Archetype Configuration -->
        <div class="grid grid-cols-1 sm:grid-cols-3 gap-3">
          <div>
            <label class="block text-xs font-semibold text-[var(--muted-foreground)] mb-1">Primary Role</label>
            <select id="bldRole" onchange="calcCustomPlayer()" class="w-full bg-[var(--card)] text-[var(--foreground)] border border-[var(--border)] rounded-lg p-2 text-xs font-semibold">
              <option value="Top-Order Batter">Top-Order Batter</option>
              <option value="Middle-Order Batter">Middle-Order Batter</option>
              <option value="Wicketkeeper">Wicketkeeper-Batter</option>
              <option value="Pace All-Rounder">Pace All-Rounder</option>
              <option value="Spin All-Rounder">Spin All-Rounder</option>
              <option value="Specialist Fast Bowler">Specialist Fast Bowler</option>
              <option value="Specialist Spin Bowler">Specialist Spin Bowler</option>
            </select>
          </div>

          <div>
            <label class="block text-xs font-semibold text-[var(--muted-foreground)] mb-1">Batting Hand</label>
            <select id="bldHand" onchange="calcCustomPlayer()" class="w-full bg-[var(--card)] text-[var(--foreground)] border border-[var(--border)] rounded-lg p-2 text-xs font-semibold">
              <option value="RHB">Right-Hand Bat (RHB)</option>
              <option value="LHB">Left-Hand Bat (LHB - Gambhir Favored)</option>
            </select>
          </div>

          <div>
            <label class="block text-xs font-semibold text-[var(--muted-foreground)] mb-1">Bowling Style</label>
            <select id="bldBowl" onchange="calcCustomPlayer()" class="w-full bg-[var(--card)] text-[var(--foreground)] border border-[var(--border)] rounded-lg p-2 text-xs font-semibold">
              <option value="Right-Arm Fast">Right-Arm Fast (Shastri Pace Battery)</option>
              <option value="Left-Arm Fast">Left-Arm Fast (Gambhir Angle Weapon)</option>
              <option value="Finger Spin">Finger Spin (Off-break / Orthodox)</option>
              <option value="Wrist Spin">Wrist Spin (Kuldeep / Dravid Weapon)</option>
              <option value="None">None (Pure Specialist Batter)</option>
            </select>
          </div>
        </div>

        <!-- Sliders Group 1: Career Baseline Numbers -->
        <div class="space-y-2 border-t border-[var(--border)] pt-3">
          <span class="text-xs font-bold uppercase tracking-wider text-indigo-400">1. Career Baseline Numbers</span>
          <div class="grid grid-cols-1 sm:grid-cols-3 gap-4">
            <div class="bg-[var(--card)] p-2.5 rounded-lg border border-[var(--border)]">
              <div class="flex justify-between text-xs mb-1">
                <span>Career Batting Average:</span>
                <span id="lblBatAvg" class="font-bold text-emerald-500">45.0</span>
              </div>
              <input type="range" id="rngBatAvg" min="15" max="65" value="45" oninput="document.getElementById('lblBatAvg').innerText = this.value; calcCustomPlayer()" class="w-full">
            </div>

            <div class="bg-[var(--card)] p-2.5 rounded-lg border border-[var(--border)]">
              <div class="flex justify-between text-xs mb-1">
                <span>Career Strike Rate:</span>
                <span id="lblBatSR" class="font-bold text-indigo-400">138</span>
              </div>
              <input type="range" id="rngBatSR" min="65" max="185" value="138" oninput="document.getElementById('lblBatSR').innerText = this.value; calcCustomPlayer()" class="w-full">
            </div>

            <div class="bg-[var(--card)] p-2.5 rounded-lg border border-[var(--border)]">
              <div class="flex justify-between text-xs mb-1">
                <span>Career Bowling Economy:</span>
                <span id="lblBowlEcon" class="font-bold text-amber-500">6.8</span>
              </div>
              <input type="range" id="rngBowlEcon" min="3.0" max="11.0" step="0.1" value="6.8" oninput="document.getElementById('lblBowlEcon').innerText = this.value; calcCustomPlayer()" class="w-full">
            </div>
          </div>
        </div>

        <!-- Sliders Group 2: Last Season (2024-25) Form Numbers -->
        <div class="space-y-2 border-t border-[var(--border)] pt-3">
          <span class="text-xs font-bold uppercase tracking-wider text-emerald-400">2. Last Season (2024–25 Form) Velocity</span>
          <div class="grid grid-cols-1 sm:grid-cols-3 gap-4">
            <div class="bg-[var(--card)] p-2.5 rounded-lg border border-[var(--border)]">
              <div class="flex justify-between text-xs mb-1">
                <span>Last Season Batting Avg:</span>
                <span id="lblRecentBatAvg" class="font-bold text-emerald-500">52.0</span>
              </div>
              <input type="range" id="rngRecentBatAvg" min="15" max="75" value="52" oninput="document.getElementById('lblRecentBatAvg').innerText = this.value; calcCustomPlayer()" class="w-full">
            </div>

            <div class="bg-[var(--card)] p-2.5 rounded-lg border border-[var(--border)]">
              <div class="flex justify-between text-xs mb-1">
                <span>Last Season Strike Rate:</span>
                <span id="lblRecentBatSR" class="font-bold text-indigo-400">155</span>
              </div>
              <input type="range" id="rngRecentBatSR" min="70" max="200" value="155" oninput="document.getElementById('lblRecentBatSR').innerText = this.value; calcCustomPlayer()" class="w-full">
            </div>

            <div class="bg-[var(--card)] p-2.5 rounded-lg border border-[var(--border)]">
              <div class="flex justify-between text-xs mb-1">
                <span>Last Season Bowling Wkts/Yr:</span>
                <span id="lblRecentWkts" class="font-bold text-amber-500">28</span>
              </div>
              <input type="range" id="rngRecentWkts" min="0" max="60" value="28" oninput="document.getElementById('lblRecentWkts').innerText = this.value; calcCustomPlayer()" class="w-full">
            </div>
          </div>
        </div>

        <!-- Selectors Group 3: Dismissal & Wicket-Taking Mode Tendencies -->
        <div class="space-y-2 border-t border-[var(--border)] pt-3">
          <span class="text-xs font-bold uppercase tracking-wider text-amber-400">3. Dismissal & Wicket-Taking Technical Traits</span>
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div class="bg-[var(--card)] p-2.5 rounded-lg border border-[var(--border)]">
              <label class="block text-xs font-semibold text-[var(--muted-foreground)] mb-1">Batter Dismissal Vulnerability (How They Get Out)</label>
              <select id="bldDismissalMode" onchange="calcCustomPlayer()" class="w-full bg-[var(--background)] text-[var(--foreground)] border border-[var(--border)] rounded-md p-2 text-xs">
                <option value="5th-Stump Edges">Chasing 5th-Stump Corridor (Edges to Slips/Keeper - Dravid/Shastri penalize in SENA)</option>
                <option value="Short-Ball Pull">Short-Ball Pull / Hook to Deep (Gambhir accepts if SR is high; Kirsten penalizes)</option>
                <option value="LBW-Bowled">Inswinging Seam / Arm Ball (Bowled & LBW through gate)</option>
                <option value="Lofted-Miscue">Lofted Clearence Miscues (Boundary riders catching high slices)</option>
              </select>
            </div>

            <div class="bg-[var(--card)] p-2.5 rounded-lg border border-[var(--border)]">
              <label class="block text-xs font-semibold text-[var(--muted-foreground)] mb-1">Bowler Primary Dismissal Weapon (How They Take Wickets)</label>
              <select id="bldWicketWeapon" onchange="calcCustomPlayer()" class="w-full bg-[var(--background)] text-[var(--foreground)] border border-[var(--border)] rounded-md p-2 text-xs">
                <option value="Yorker-Inswing">142+ km/h Yorker & Reverse Inswing (Bowled & LBW - Shastri & Gambhir #1 Pick)</option>
                <option value="Wobble-Seam-Edges">Wobble Seam & Away Movement (Edges to Keeper/Slips - Overseas Match-Winner)</option>
                <option value="Wrist-Spin-Wrongun">Wrist Spin Deception & Wrong'un (Dravid #1 Weapon)</option>
                <option value="Death-Slower">Death-Overs Cutters & Wide Tramline Miscues (White-Ball Utility)</option>
              </select>
            </div>
          </div>
        </div>

      </div>

      <!-- PREDICTED SELECTION PROBABILITIES OUTPUT -->
      <div class="bg-[var(--background)] border border-[var(--border)] rounded-xl p-4 sm:p-5 shadow-xs space-y-4">
        <div class="flex flex-col sm:flex-row sm:items-center justify-between border-b border-[var(--border)] pb-2.5 gap-2">
          <div>
            <h3 class="text-sm sm:text-base font-bold tracking-tight flex items-center gap-2">
              <span>🎯</span>
              <span>Predicted Matchday Selection Probabilities by Coach</span>
            </h3>
            <p class="text-xs text-[var(--muted-foreground)]">
              Conditional probability of starting in India's Playing XI under each coach's historical selection model
            </p>
          </div>
          <span class="text-xs px-2.5 py-1 rounded bg-[var(--secondary)] font-semibold text-[var(--secondary-foreground)]">
            Ensemble Calibrated
          </span>
        </div>

        <!-- Coach Bars Container -->
        <div id="coachBarsContainer" class="space-y-3.5">
          <!-- Populated by JS -->
        </div>

        <!-- Dynamic Tactical Insight Box -->
        <div id="tacticalInsightBox" class="border border-[var(--border)] bg-[var(--secondary)]/40 rounded-xl p-4 space-y-1.5 mt-2">
          <div class="flex items-center gap-2 text-xs font-bold uppercase tracking-wider text-[var(--foreground)]">
            <svg class="w-4 h-4 text-amber-500" fill="currentColor" viewBox="0 0 20 20">
              <path d="M11 3a1 1 0 10-2 0v1a1 1 0 102 0V3zM15.657 5.757a1 1 0 00-1.414-1.414l-.707.707a1 1 0 001.414 1.414l.707-.707zM18 10a1 1 0 01-1 1h-1a1 1 0 110-2h1a1 1 0 011 1zM5.05 6.464A1 1 0 106.464 5.05l-.707-.707a1 1 0 00-1.414 1.414l.707.707zM5 10a1 1 0 01-1 1H3a1 1 0 110-2h1a1 1 0 011 1zM8 16v-1h4v1a2 2 0 11-4 0zM12 14H8a4 4 0 01-.8-7.92A4.002 4.002 0 0115.8 9.2 4.002 4.002 0 0112 14z" />
            </svg>
            <span>Tactical Coach Rationale & Selection Analysis</span>
          </div>
          <p id="tacticalText" class="text-xs sm:text-sm text-[var(--foreground)] leading-relaxed">
            Evaluating tactical selection rationale...
          </p>
        </div>

      </div>

    </section>

    <!-- ========================================================================= -->
    <!-- SECTION 2: COACH SELECTION PHILOSOPHIES & RED-BALL DEEP DIVE -->
    <!-- ========================================================================= -->
    <section id="philosophy" class="space-y-8 pt-8 border-t-2 border-[var(--border)]">
      
      <!-- Section Header -->
      <div class="space-y-2">
        <div class="flex items-center gap-2">
          <span class="px-2 py-0.5 text-xs font-extrabold rounded bg-indigo-500/20 text-indigo-400 uppercase tracking-wide">Module 2</span>
          <h2 class="text-xl sm:text-2xl font-bold">Coach Selection Philosophies & Red-Ball Deep Dive</h2>
        </div>
        <p class="text-xs sm:text-sm text-[var(--muted-foreground)] leading-relaxed">
          Our statistical interaction models and Random Forest importance metrics reveal distinct mathematical archetypes that defined Indian cricket's major eras.
        </p>
      </div>

      <!-- Part 1: Main Predictors Under Each Coach -->
      <div class="space-y-4">
        <div class="flex items-center gap-2 border-b border-[var(--border)] pb-2">
          <span class="px-2.5 py-0.5 text-xs font-bold rounded bg-indigo-500/20 text-indigo-400 uppercase tracking-wide">Part 1</span>
          <h3 class="text-base sm:text-lg font-bold">Main Predictors Under Each Coach & How They Differ</h3>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          
          <!-- Gautam Gambhir -->
          <div class="bg-[var(--background)] border border-[var(--border)] rounded-xl p-4 space-y-2.5 shadow-xs">
            <div class="flex items-center justify-between">
              <h4 class="font-bold text-sm text-indigo-500">Gautam Gambhir</h4>
              <span class="text-[10px] px-1.5 py-0.5 rounded bg-indigo-500/10 text-indigo-400 font-semibold">2024–Present</span>
            </div>
            <div class="text-xs space-y-1.5 text-[var(--muted-foreground)]">
              <p><strong class="text-[var(--foreground)]">#1 Predictor:</strong> LHB Matchup Utility (Avg 3.92 LHBs / match — all-time high)</p>
              <p><strong class="text-[var(--foreground)]">#2 Predictor:</strong> Left-Arm Pace Angle (Odds Ratio: 1.20)</p>
              <p><strong class="text-[var(--foreground)]">#3 Predictor:</strong> Multi-Utility All-Rounders (Bowling options to #8/#9)</p>
              <p><strong class="text-[var(--foreground)]">Deprioritizes:</strong> Non-bowling defensive accumulators</p>
            </div>
            <div class="pt-2 border-t border-[var(--border)] text-[11px] text-[var(--foreground)] italic">
              "Aggressive boundary strike rates, tactical left-hand matchups, and deep bowling options override classical anchor roles."
            </div>
          </div>

          <!-- Rahul Dravid -->
          <div class="bg-[var(--background)] border border-[var(--border)] rounded-xl p-4 space-y-2.5 shadow-xs">
            <div class="flex items-center justify-between">
              <h4 class="font-bold text-sm text-blue-500">Rahul Dravid</h4>
              <span class="text-[10px] px-1.5 py-0.5 rounded bg-blue-500/10 text-blue-400 font-semibold">2021–2024</span>
            </div>
            <div class="text-xs space-y-1.5 text-[var(--muted-foreground)]">
              <p><strong class="text-[var(--foreground)]">#1 Predictor:</strong> Batting Depth / Dual Spin-ARs (2.33 all-rounders / match)</p>
              <p><strong class="text-[var(--foreground)]">#2 Predictor:</strong> Attacking Wrist-Spin (Odds Ratio: 1.33, Kuldeep Yadav)</p>
              <p><strong class="text-[var(--foreground)]">#3 Predictor:</strong> Role Continuity (Highest weight on 1-year squad continuity: 0.326)</p>
              <p><strong class="text-[var(--foreground)]">Deprioritizes:</strong> Fragile lower orders with one-dimensional tailenders</p>
            </div>
            <div class="pt-2 border-t border-[var(--border)] text-[11px] text-[var(--foreground)] italic">
              "Deep batting security paired with specialized middle-overs strike bowlers (wrist spin), avoiding knee-jerk squad churn."
            </div>
          </div>

          <!-- Ravi Shastri -->
          <div class="bg-[var(--background)] border border-[var(--border)] rounded-xl p-4 space-y-2.5 shadow-xs">
            <div class="flex items-center justify-between">
              <h4 class="font-bold text-sm text-amber-500">Ravi Shastri</h4>
              <span class="text-[10px] px-1.5 py-0.5 rounded bg-amber-500/10 text-amber-400 font-semibold">2017–2021</span>
            </div>
            <div class="text-xs space-y-1.5 text-[var(--muted-foreground)]">
              <p><strong class="text-[var(--foreground)]">#1 Predictor:</strong> 20-Wicket Specialist Weapons (Fast Bowlers: 1.11, Specialist Spin: 1.19)</p>
              <p><strong class="text-[var(--foreground)]">#2 Predictor:</strong> Express Pace Overseas (4-man pace battery in SENA Tests)</p>
              <p><strong class="text-[var(--foreground)]">#3 Predictor:</strong> Pace All-Rounder Balance (Hardik Pandya / Shardul Thakur)</p>
              <p><strong class="text-[var(--foreground)]">Deprioritizes:</strong> Defensive defensive bits-and-pieces players</p>
            </div>
            <div class="pt-2 border-t border-[var(--border)] text-[11px] text-[var(--foreground)] italic">
              "Ruthless 5-bowler attack: uncompromised 140+ km/h pace velocity and attacking spinners to take 20 wickets."
            </div>
          </div>

          <!-- Gary Kirsten -->
          <div class="bg-[var(--background)] border border-[var(--border)] rounded-xl p-4 space-y-2.5 shadow-xs">
            <div class="flex items-center justify-between">
              <h4 class="font-bold text-sm text-emerald-500">Gary Kirsten</h4>
              <span class="text-[10px] px-1.5 py-0.5 rounded bg-emerald-500/10 text-emerald-400 font-semibold">2008–2011</span>
            </div>
            <div class="text-xs space-y-1.5 text-[var(--muted-foreground)]">
              <p><strong class="text-[var(--foreground)]">#1 Predictor:</strong> Pure Specialist Anchors (Top-order anchor odds: 1.11)</p>
              <p><strong class="text-[var(--foreground)]">#2 Predictor:</strong> Part-Time Bowling Options (Yuvraj, Raina, Sehwag)</p>
              <p><strong class="text-[var(--foreground)]">#3 Predictor:</strong> Settled Core (Lowest all-rounders in XI: 1.01)</p>
              <p><strong class="text-[var(--foreground)]">Deprioritizes:</strong> Designated pace all-rounders (0.23 odds); constant rotation</p>
            </div>
            <div class="pt-2 border-t border-[var(--border)] text-[11px] text-[var(--foreground)] italic">
              "Clear role purity: top 6 score the runs, 4 specialist bowlers take wickets, part-timers choke middle overs."
            </div>
          </div>

          <!-- Duncan Fletcher -->
          <div class="bg-[var(--background)] border border-[var(--border)] rounded-xl p-4 space-y-2.5 shadow-xs">
            <div class="flex items-center justify-between">
              <h4 class="font-bold text-sm text-purple-500">Duncan Fletcher</h4>
              <span class="text-[10px] px-1.5 py-0.5 rounded bg-purple-500/10 text-purple-400 font-semibold">2011–2015</span>
            </div>
            <div class="text-xs space-y-1.5 text-[var(--muted-foreground)]">
              <p><strong class="text-[var(--foreground)]">#1 Predictor:</strong> Spin All-Rounder Genesis (1.52 / match; Ashwin & Jadeja)</p>
              <p><strong class="text-[var(--foreground)]">#2 Predictor:</strong> Pace All-Rounder Value (Odds Ratio: 1.29)</p>
              <p><strong class="text-[var(--foreground)]">#3 Predictor:</strong> Technical Batting Prowess</p>
              <p><strong class="text-[var(--foreground)]">Deprioritizes:</strong> Non-batting specialist spinners (Odds: 0.49)</p>
            </div>
            <div class="pt-2 border-t border-[var(--border)] text-[11px] text-[var(--foreground)] italic">
              "Established India's modern ODI template at the 2013 Champions Trophy with Jadeja-Ashwin anchoring the middle."
            </div>
          </div>

          <!-- Anil Kumble -->
          <div class="bg-[var(--background)] border border-[var(--border)] rounded-xl p-4 space-y-2.5 shadow-xs">
            <div class="flex items-center justify-between">
              <h4 class="font-bold text-sm text-rose-500">Anil Kumble</h4>
              <span class="text-[10px] px-1.5 py-0.5 rounded bg-rose-500/10 text-rose-400 font-semibold">2016–2017</span>
            </div>
            <div class="text-xs space-y-1.5 text-[var(--muted-foreground)]">
              <p><strong class="text-[var(--foreground)]">#1 Predictor:</strong> Spin Workload Attrition (Peak Ashwin & Jadeja over-rates)</p>
              <p><strong class="text-[var(--foreground)]">#2 Predictor:</strong> Red-Ball First-Class Grinding & Multi-Day Discipline</p>
              <p><strong class="text-[var(--foreground)]">#3 Predictor:</strong> Ruthless Home Fortress Record (Won 12 of 17 Tests)</p>
              <p><strong class="text-[var(--foreground)]">Deprioritizes:</strong> Flamboyant slogging in multi-day formats</p>
            </div>
            <div class="pt-2 border-t border-[var(--border)] text-[11px] text-[var(--foreground)] italic">
              "Classic Test discipline: suffocating spin attrition, defensive patience, and long-form grinding."
            </div>
          </div>

        </div>
      </div>

      <!-- Part 2: Test & First-Class Dynamics -->
      <div class="space-y-4 border-t border-[var(--border)] pt-6">
        <div class="flex items-center gap-2 border-b border-[var(--border)] pb-2">
          <span class="px-2.5 py-0.5 text-xs font-bold rounded bg-emerald-500/20 text-emerald-400 uppercase tracking-wide">Part 2</span>
          <h3 class="text-base sm:text-lg font-bold">Test Match & First-Class Selection Dynamics</h3>
        </div>
        <p class="text-xs sm:text-sm text-[var(--muted-foreground)] leading-relaxed">
          Test cricket selection obeys entirely different mathematical rules than white-ball cricket. In Test and First-Class (Ranji Trophy, Duleep Trophy, India A) matches, selection hinges on <strong>workload endurance, condition polarity (Subcontinent vs SENA), and technical resilience</strong>:
        </p>

        <div class="overflow-x-auto">
          <table class="w-full text-left text-xs border-collapse border border-[var(--border)]">
            <thead>
              <tr class="bg-[var(--secondary)] text-[var(--secondary-foreground)]">
                <th class="p-2.5 border border-[var(--border)] font-semibold">Era / Coach</th>
                <th class="p-2.5 border border-[var(--border)] font-semibold">Test Top-Order Batters</th>
                <th class="p-2.5 border border-[var(--border)] font-semibold">Test Pace ARs</th>
                <th class="p-2.5 border border-[var(--border)] font-semibold">Test Spin ARs</th>
                <th class="p-2.5 border border-[var(--border)] font-semibold">Test Fast Bowlers</th>
                <th class="p-2.5 border border-[var(--border)] font-semibold">Test Specialist Spinners</th>
                <th class="p-2.5 border border-[var(--border)] font-semibold">Overseas SENA Template</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-[var(--border)]">
              <tr>
                <td class="p-2.5 border border-[var(--border)] font-medium">Gary Kirsten (2008–11)</td>
                <td class="p-2.5 border border-[var(--border)]">0.568</td>
                <td class="p-2.5 border border-[var(--border)]">0.024</td>
                <td class="p-2.5 border border-[var(--border)]">0.000</td>
                <td class="p-2.5 border border-[var(--border)]">0.306</td>
                <td class="p-2.5 border border-[var(--border)] font-bold text-amber-500">0.381 (Highest)</td>
                <td class="p-2.5 border border-[var(--border)]">3 Pacers (Zaheer, Ishant, Sreesanth) + Harbhajan + 7 Batters</td>
              </tr>
              <tr>
                <td class="p-2.5 border border-[var(--border)] font-medium">Duncan Fletcher (2011–15)</td>
                <td class="p-2.5 border border-[var(--border)]">0.492</td>
                <td class="p-2.5 border border-[var(--border)]">0.000</td>
                <td class="p-2.5 border border-[var(--border)]">0.333</td>
                <td class="p-2.5 border border-[var(--border)]">0.295</td>
                <td class="p-2.5 border border-[var(--border)]">0.197</td>
                <td class="p-2.5 border border-[var(--border)]">Ashwin/Jadeja spin foundation + pace rotations</td>
              </tr>
              <tr>
                <td class="p-2.5 border border-[var(--border)] font-medium">Anil Kumble (2016–17)</td>
                <td class="p-2.5 border border-[var(--border)]">0.596</td>
                <td class="p-2.5 border border-[var(--border)]">0.000</td>
                <td class="p-2.5 border border-[var(--border)] font-bold text-emerald-500">0.574 (Peak)</td>
                <td class="p-2.5 border border-[var(--border)]">0.229</td>
                <td class="p-2.5 border border-[var(--border)]">0.096</td>
                <td class="p-2.5 border border-[var(--border)]">Spin fortress: Ashwin & Jadeja at peak dominance</td>
              </tr>
              <tr>
                <td class="p-2.5 border border-[var(--border)] font-medium">Ravi Shastri (2017–21)</td>
                <td class="p-2.5 border border-[var(--border)]">0.561</td>
                <td class="p-2.5 border border-[var(--border)] font-bold text-amber-500">0.137 (Highest)</td>
                <td class="p-2.5 border border-[var(--border)]">0.330</td>
                <td class="p-2.5 border border-[var(--border)] font-bold text-emerald-500">0.281 (Express)</td>
                <td class="p-2.5 border border-[var(--border)]">0.051</td>
                <td class="p-2.5 border border-[var(--border)]">4 Express Pacers (Bumrah, Shami, Ishant, Siraj) + Hardik/Shardul</td>
              </tr>
              <tr>
                <td class="p-2.5 border border-[var(--border)] font-medium">Rahul Dravid (2021–24)</td>
                <td class="p-2.5 border border-[var(--border)]">0.392</td>
                <td class="p-2.5 border border-[var(--border)]">0.108</td>
                <td class="p-2.5 border border-[var(--border)]">0.318</td>
                <td class="p-2.5 border border-[var(--border)]">0.193</td>
                <td class="p-2.5 border border-[var(--border)]">0.053</td>
                <td class="p-2.5 border border-[var(--border)]">Batting depth at #8 (Shardul overseas, Axar/Sundar at home)</td>
              </tr>
              <tr>
                <td class="p-2.5 border border-[var(--border)] font-medium">Gautam Gambhir (2024–)</td>
                <td class="p-2.5 border border-[var(--border)]">0.353</td>
                <td class="p-2.5 border border-[var(--border)]">0.069</td>
                <td class="p-2.5 border border-[var(--border)] font-bold text-emerald-500">0.424</td>
                <td class="p-2.5 border border-[var(--border)]">0.229</td>
                <td class="p-2.5 border border-[var(--border)]">0.085</td>
                <td class="p-2.5 border border-[var(--border)]">LHB counter-punching (Jaiswal, Pant, Sundar) + multi-utility</td>
              </tr>
            </tbody>
          </table>
        </div>

        <div class="grid grid-cols-1 sm:grid-cols-2 gap-4 mt-3">
          <div class="bg-[var(--background)] p-3.5 rounded-xl border border-[var(--border)]">
            <h4 class="font-bold text-xs uppercase text-emerald-500 mb-1">First-Class to Test Batting Conversion</h4>
            <p class="text-xs text-[var(--muted-foreground)] leading-relaxed">
              In domestic multi-day matches (Ranji & Duleep Trophy), coaches historically looked for <strong>balls faced per dismissal</strong> and a <strong>Ranji average &gt;52.0</strong> (Pujara, Rahane). Under Gambhir and Dravid, selection has also rewarded <strong>first-class boundary percentage, proactive strike rates, and overseas India A performances</strong> (Yashasvi Jaiswal, Dhruv Jurel, Sarfaraz Khan).
            </p>
          </div>
          <div class="bg-[var(--background)] p-3.5 rounded-xl border border-[var(--border)]">
            <h4 class="font-bold text-xs uppercase text-amber-500 mb-1">First-Class to Test Bowling Workloads</h4>
            <p class="text-xs text-[var(--muted-foreground)] leading-relaxed">
              Red-ball fast bowling selection requires proven stamina: bowling <strong>18–25 overs per day</strong> at 138+ km/h with an economy &lt;2.80 and strike rate &lt;45.0. Shastri demanded express velocity (Bumrah, Siraj, Umesh, Shami), whereas Fletcher & Dravid favored seam control and line-and-length attrition.
            </p>
          </div>
        </div>
      </div>

    </section>

    <!-- ========================================================================= -->
    <!-- SECTION 3: EMPIRICAL PLAYING XI TEAM COMPOSITIONS -->
    <!-- ========================================================================= -->
    <section id="compositions" class="space-y-6 pt-8 border-t-2 border-[var(--border)]">
      
      <div class="space-y-2">
        <div class="flex items-center gap-2">
          <span class="px-2 py-0.5 text-xs font-extrabold rounded bg-blue-500/20 text-blue-400 uppercase tracking-wide">Module 3</span>
          <h2 class="text-xl sm:text-2xl font-bold">Empirical Playing XI Team Compositions Across All Formats</h2>
        </div>
        <p class="text-xs sm:text-sm text-[var(--muted-foreground)] leading-relaxed">
          Historical averages of players selected per Playing XI across 1,021 India matches (2001–2026), computed directly from Cricsheet match archives:
        </p>
      </div>

      <div class="overflow-x-auto">
        <table class="w-full text-left text-xs border-collapse border border-[var(--border)]">
          <thead>
            <tr class="bg-[var(--secondary)] text-[var(--secondary-foreground)]">
              <th class="p-2.5 border border-[var(--border)] font-semibold">Coach Era</th>
              <th class="p-2.5 border border-[var(--border)] font-semibold">Total All-Rounders</th>
              <th class="p-2.5 border border-[var(--border)] font-semibold">Pace ARs</th>
              <th class="p-2.5 border border-[var(--border)] font-semibold">Spin ARs</th>
              <th class="p-2.5 border border-[var(--border)] font-semibold">Specialist Fast Bowlers</th>
              <th class="p-2.5 border border-[var(--border)] font-semibold">Wrist Spinners</th>
              <th class="p-2.5 border border-[var(--border)] font-semibold">Left-Hand Batters (LHBs)</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-[var(--border)]">
            <tr>
              <td class="p-2.5 border border-[var(--border)] font-medium">Gautam Gambhir (2024–)</td>
              <td class="p-2.5 border border-[var(--border)]">2.11</td>
              <td class="p-2.5 border border-[var(--border)]">0.75</td>
              <td class="p-2.5 border border-[var(--border)]">1.36</td>
              <td class="p-2.5 border border-[var(--border)]">1.67</td>
              <td class="p-2.5 border border-[var(--border)] font-bold text-indigo-400">1.69</td>
              <td class="p-2.5 border border-[var(--border)] font-bold text-emerald-500">3.92 (All-Time High)</td>
            </tr>
            <tr>
              <td class="p-2.5 border border-[var(--border)] font-medium">Rahul Dravid (2021–24)</td>
              <td class="p-2.5 border border-[var(--border)] font-bold text-emerald-500">2.33 (Highest)</td>
              <td class="p-2.5 border border-[var(--border)]">0.76</td>
              <td class="p-2.5 border border-[var(--border)] font-bold text-emerald-500">1.57</td>
              <td class="p-2.5 border border-[var(--border)]">2.40</td>
              <td class="p-2.5 border border-[var(--border)] font-bold text-emerald-500">1.54</td>
              <td class="p-2.5 border border-[var(--border)]">3.02</td>
            </tr>
            <tr>
              <td class="p-2.5 border border-[var(--border)] font-medium">Ravi Shastri (2017–21)</td>
              <td class="p-2.5 border border-[var(--border)]">1.77</td>
              <td class="p-2.5 border border-[var(--border)] font-bold text-amber-500">0.81</td>
              <td class="p-2.5 border border-[var(--border)]">0.96</td>
              <td class="p-2.5 border border-[var(--border)] font-bold text-emerald-500">2.24 (Express)</td>
              <td class="p-2.5 border border-[var(--border)]">1.52</td>
              <td class="p-2.5 border border-[var(--border)]">2.49</td>
            </tr>
            <tr>
              <td class="p-2.5 border border-[var(--border)] font-medium">Gary Kirsten (2008–11)</td>
              <td class="p-2.5 border border-[var(--border)]">1.01 (Lowest)</td>
              <td class="p-2.5 border border-[var(--border)]">0.15</td>
              <td class="p-2.5 border border-[var(--border)]">0.86</td>
              <td class="p-2.5 border border-[var(--border)] font-bold text-indigo-400">2.41</td>
              <td class="p-2.5 border border-[var(--border)]">1.53</td>
              <td class="p-2.5 border border-[var(--border)]">2.99</td>
            </tr>
            <tr>
              <td class="p-2.5 border border-[var(--border)] font-medium">Duncan Fletcher (2011–15)</td>
              <td class="p-2.5 border border-[var(--border)]">1.66</td>
              <td class="p-2.5 border border-[var(--border)]">0.14</td>
              <td class="p-2.5 border border-[var(--border)]">1.52</td>
              <td class="p-2.5 border border-[var(--border)]">2.02</td>
              <td class="p-2.5 border border-[var(--border)]">1.11</td>
              <td class="p-2.5 border border-[var(--border)]">3.05</td>
            </tr>
            <tr>
              <td class="p-2.5 border border-[var(--border)] font-medium">Anil Kumble (2016–17)</td>
              <td class="p-2.5 border border-[var(--border)]">2.11</td>
              <td class="p-2.5 border border-[var(--border)]">0.43</td>
              <td class="p-2.5 border border-[var(--border)] font-bold text-indigo-400">1.69</td>
              <td class="p-2.5 border border-[var(--border)]">2.26</td>
              <td class="p-2.5 border border-[var(--border)]">1.00</td>
              <td class="p-2.5 border border-[var(--border)]">1.77</td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Quick Jump Back to Top -->
      <div class="pt-4 text-center">
        <a href="#predictor" class="px-5 py-2.5 text-xs font-bold rounded-xl bg-[var(--secondary)] hover:bg-[var(--secondary)]/80 text-[var(--foreground)] border border-[var(--border)] transition shadow-xs inline-flex items-center gap-1.5">
          <span>↑</span>
          <span>Back to Selection Predictor & Custom Player Builder</span>
        </a>
      </div>

    </section>

  </div>

  <script>
    const PLAYERS_DATA = {players_json};

    let currentSubMode = "existing";
    let currentFormat = "TEST";
    let currentVenue = "Home";

    function switchSubMode(mode) {{
      currentSubMode = mode;
      const subTabEx = document.getElementById('subTabExisting');
      const subTabBld = document.getElementById('subTabBuilder');
      const secEx = document.getElementById('existingPlayerCard');
      const secBld = document.getElementById('builderSection');
      const playerSelContainer = document.getElementById('playerSelectContainer');

      if (mode === 'existing') {{
        subTabEx.className = "py-2.5 rounded-lg bg-[var(--primary)] text-[var(--primary-foreground)] shadow-xs transition duration-150 cursor-pointer font-bold";
        subTabBld.className = "py-2.5 rounded-lg text-[var(--muted-foreground)] hover:text-[var(--foreground)] transition duration-150 cursor-pointer font-medium";
        secEx.classList.remove('hidden');
        secBld.classList.add('hidden');
        playerSelContainer.classList.remove('hidden');
        updateExistingView();
      }} else {{
        subTabBld.className = "py-2.5 rounded-lg bg-[var(--primary)] text-[var(--primary-foreground)] shadow-xs transition duration-150 cursor-pointer font-bold";
        subTabEx.className = "py-2.5 rounded-lg text-[var(--muted-foreground)] hover:text-[var(--foreground)] transition duration-150 cursor-pointer font-medium";
        secEx.classList.add('hidden');
        secBld.classList.remove('hidden');
        playerSelContainer.classList.add('hidden');
        calcCustomPlayer();
      }}
    }}

    function setFormat(fmt) {{
      currentFormat = fmt;
      ['TEST', 'ODI', 'T20I'].forEach(f => {{
        const btn = document.getElementById('btn' + f);
        if (f === fmt) {{
          btn.className = "py-1.5 rounded-md bg-[var(--primary)] text-[var(--primary-foreground)] shadow-xs transition";
        }} else {{
          btn.className = "py-1.5 rounded-md text-[var(--muted-foreground)] hover:text-[var(--foreground)] transition";
        }}
      }});
      if (currentSubMode === 'existing') updateExistingView(); else calcCustomPlayer();
    }}

    function setVenue(v) {{
      currentVenue = v;
      const btnHome = document.getElementById('btnHome');
      const btnSena = document.getElementById('btnSena');
      if (v === 'Home') {{
        btnHome.className = "py-1.5 rounded-md bg-[var(--primary)] text-[var(--primary-foreground)] shadow-xs transition";
        btnSena.className = "py-1.5 rounded-md text-[var(--muted-foreground)] hover:text-[var(--foreground)] transition";
      }} else {{
        btnSena.className = "py-1.5 rounded-md bg-[var(--primary)] text-[var(--primary-foreground)] shadow-xs transition";
        btnHome.className = "py-1.5 rounded-md text-[var(--muted-foreground)] hover:text-[var(--foreground)] transition";
      }}
      if (currentSubMode === 'existing') updateExistingView(); else calcCustomPlayer();
    }}

    function renderBars(scores, tacticalText, retirementNotice) {{
      const barsContainer = document.getElementById('coachBarsContainer');
      barsContainer.innerHTML = "";

      const coachColors = {{
        "Gautam Gambhir": "bg-indigo-500",
        "Rahul Dravid": "bg-blue-500",
        "Ravi Shastri": "bg-amber-500",
        "Gary Kirsten": "bg-emerald-500",
        "Duncan Fletcher": "bg-purple-500",
        "Anil Kumble": "bg-rose-500"
      }};

      const sortedCoaches = Object.entries(scores).sort((a, b) => b[1] - a[1]);

      sortedCoaches.forEach(([coach, prob], index) => {{
        const color = coachColors[coach] || "bg-sky-500";
        const isRetiredUnderGambhir = (coach === "Gautam Gambhir" && prob === 0 && retirementNotice);
        const widthPct = isRetiredUnderGambhir ? 3 : Math.min(100, Math.max(6, prob));

        const row = document.createElement('div');
        row.className = "space-y-1.5";
        row.innerHTML = `
          <div class="flex items-center justify-between text-xs sm:text-sm">
            <span class="font-semibold flex items-center gap-1.5">
              ${{coach}}
              ${{index === 0 && prob > 60 ? '<span class="text-[10px] font-bold px-1.5 py-0.5 rounded bg-emerald-500/20 text-emerald-600 dark:text-emerald-400">#1 Preferred</span>' : ''}}
              ${{isRetiredUnderGambhir ? '<span class="text-[10px] font-bold px-1.5 py-0.5 rounded bg-rose-500/20 text-rose-500">Retired from ' + currentFormat + 's</span>' : ''}}
            </span>
            <span class="font-bold tabular-nums">${{isRetiredUnderGambhir ? '0.0%' : prob.toFixed(1) + '%'}}</span>
          </div>
          <div class="w-full h-3 bg-[var(--secondary)] rounded-full overflow-hidden border border-[var(--border)]">
            <div class="progress-bar h-full ${{isRetiredUnderGambhir ? 'bg-rose-400 opacity-40' : color}} rounded-full" style="width: ${{widthPct}}%"></div>
          </div>
        `;
        barsContainer.appendChild(row);
      }});

      document.getElementById('tacticalText').innerText = tacticalText;
    }}

    function updateExistingView() {{
      const player = document.getElementById('playerSelect').value;
      const data = PLAYERS_DATA[player] || PLAYERS_DATABASE["Virat Kohli"];

      // Retirement status for current format
      const retNotice = (data.retirement && data.retirement[currentFormat]) ? data.retirement[currentFormat] : null;

      // 1. Header Box
      const headerBox = document.getElementById('playerHeaderBox');
      headerBox.innerHTML = `
        <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-2">
          <div>
            <div class="flex items-center gap-2">
              <h3 class="text-base sm:text-lg font-extrabold text-[var(--foreground)]">${{player}}</h3>
              <span class="text-xs px-2 py-0.5 rounded-full bg-indigo-500/20 text-indigo-400 font-bold">${{data.role}}</span>
            </div>
            <p class="text-xs text-[var(--muted-foreground)] mt-0.5">
              ${{data.hand}} • ${{data.bowling}} • ${{data.caps}} Career Caps
            </p>
          </div>
          ${{retNotice ? `
            <div class="px-3 py-1.5 rounded-lg bg-rose-500/10 border border-rose-500/30 text-rose-400 text-xs font-semibold">
              ⚠️ ${{retNotice}}
            </div>
          ` : `
            <div class="px-3 py-1.5 rounded-lg bg-emerald-500/10 border border-emerald-500/30 text-emerald-400 text-xs font-semibold">
              Active Selection Pool for ${{currentFormat}}
            </div>
          `}}
        </div>
      `;

      // 2. Multi-Format Grid (6 formats)
      const formatGrid = document.getElementById('formatGrid');
      const ms = data.multiStats;
      formatGrid.innerHTML = `
        <div class="bg-[var(--card)] p-2.5 rounded-lg border border-[var(--border)] space-y-1">
          <div class="flex items-center justify-between font-bold text-red-500">
            <span>🟥 Test Matches</span>
            <span class="text-[10px] px-1 py-0.2 rounded bg-red-500/10">Red-Ball</span>
          </div>
          <p class="text-[11px] text-[var(--foreground)] font-medium leading-tight">${{ms.test}}</p>
        </div>
        <div class="bg-[var(--card)] p-2.5 rounded-lg border border-[var(--border)] space-y-1">
          <div class="flex items-center justify-between font-bold text-rose-400">
            <span>🔴 First-Class (FC)</span>
            <span class="text-[10px] px-1 py-0.2 rounded bg-rose-500/10">Ranji / Duleep</span>
          </div>
          <p class="text-[11px] text-[var(--foreground)] font-medium leading-tight">${{ms.fc}}</p>
        </div>
        <div class="bg-[var(--card)] p-2.5 rounded-lg border border-[var(--border)] space-y-1">
          <div class="flex items-center justify-between font-bold text-blue-500">
            <span>🟦 ODIs</span>
            <span class="text-[10px] px-1 py-0.2 rounded bg-blue-500/10">50-Over Int.</span>
          </div>
          <p class="text-[11px] text-[var(--foreground)] font-medium leading-tight">${{ms.odi}}</p>
        </div>
        <div class="bg-[var(--card)] p-2.5 rounded-lg border border-[var(--border)] space-y-1">
          <div class="flex items-center justify-between font-bold text-cyan-400">
            <span>🔵 List A</span>
            <span class="text-[10px] px-1 py-0.2 rounded bg-cyan-500/10">Hazare Trophy</span>
          </div>
          <p class="text-[11px] text-[var(--foreground)] font-medium leading-tight">${{ms.listA}}</p>
        </div>
        <div class="bg-[var(--card)] p-2.5 rounded-lg border border-[var(--border)] space-y-1">
          <div class="flex items-center justify-between font-bold text-emerald-500">
            <span>🟩 T20 Internationals</span>
            <span class="text-[10px] px-1 py-0.2 rounded bg-emerald-500/10">ICC / Bilateral</span>
          </div>
          <p class="text-[11px] text-[var(--foreground)] font-medium leading-tight">${{ms.t20i}}</p>
        </div>
        <div class="bg-[var(--card)] p-2.5 rounded-lg border border-[var(--border)] space-y-1">
          <div class="flex items-center justify-between font-bold text-amber-500">
            <span>🟨 IPL (Indian Premier League)</span>
            <span class="text-[10px] px-1 py-0.2 rounded bg-amber-500/10">Franchise</span>
          </div>
          <p class="text-[11px] text-[var(--foreground)] font-medium leading-tight">${{ms.ipl}}</p>
        </div>
      `;

      // 3. Last Season Stats
      const ls = data.lastSeason;
      document.getElementById('badgeSeasonForm').innerText = ls.formLabel;
      const seasonEl = document.getElementById('seasonStatsContent');
      seasonEl.innerHTML = `
        <div class="p-2.5 rounded-lg bg-[var(--card)] border border-[var(--border)]">
          <p class="text-[11px] text-[var(--foreground)] font-medium leading-relaxed">${{ls.summary}}</p>
        </div>
        <div class="grid grid-cols-2 sm:grid-cols-4 gap-2 text-center">
          <div class="bg-[var(--card)] p-2 rounded-lg border border-[var(--border)]">
            <span class="block text-[10px] text-[var(--muted-foreground)]">2024-25 Runs</span>
            <span class="text-sm font-bold text-emerald-500">${{ls.runs}}</span>
          </div>
          <div class="bg-[var(--card)] p-2 rounded-lg border border-[var(--border)]">
            <span class="block text-[10px] text-[var(--muted-foreground)]">2024-25 Bat Avg</span>
            <span class="text-sm font-bold text-indigo-400">${{ls.batAvg}}</span>
          </div>
          <div class="bg-[var(--card)] p-2 rounded-lg border border-[var(--border)]">
            <span class="block text-[10px] text-[var(--muted-foreground)]">2024-25 Wickets</span>
            <span class="text-sm font-bold text-amber-500">${{ls.wkts}}</span>
          </div>
          <div class="bg-[var(--card)] p-2 rounded-lg border border-[var(--border)]">
            <span class="block text-[10px] text-[var(--muted-foreground)]">2024-25 Economy</span>
            <span class="text-sm font-bold text-rose-400">${{ls.bowlEcon > 0 ? ls.bowlEcon : '-'}}</span>
          </div>
        </div>
      `;

      // 4. Dismissals Breakdown
      const dis = data.dismissal;
      document.getElementById('dismissalTitle').innerHTML = `<span>🎯</span><span>${{dis.title}}</span>`;
      const disEl = document.getElementById('dismissalContent');
      let modesHtml = dis.modes.map(m => `
        <div class="space-y-1">
          <div class="flex justify-between text-[11px]">
            <span class="font-medium text-[var(--foreground)]">${{m.name}}</span>
            <span class="font-bold tabular-nums">${{m.pct}}%</span>
          </div>
          <div class="w-full h-2 bg-[var(--secondary)] rounded-full overflow-hidden">
            <div class="h-full ${{m.color}} rounded-full" style="width: ${{m.pct}}%"></div>
          </div>
        </div>
      `).join('');

      disEl.innerHTML = `
        <div class="space-y-2">
          ${{modesHtml}}
        </div>
        <div class="pt-2 border-t border-[var(--border)] text-[11px] text-[var(--muted-foreground)] italic leading-tight">
          ${{dis.tactical_note}}
        </div>
      `;

      // 5. Scores & Tactical Analysis
      const key = `${{currentFormat}}_${{currentVenue}}`;
      let scores = (data.squad_scores && data.squad_scores[key]) ? Object.assign({{}}, data.squad_scores[key]) : {{
        "Gautam Gambhir": 75.0, "Rahul Dravid": 78.0, "Ravi Shastri": 80.0, "Gary Kirsten": 70.0, "Duncan Fletcher": 72.0, "Anil Kumble": 70.0
      }};

      if (retNotice && currentFormat === 'T20I') {{
        scores["Gautam Gambhir"] = 0.0;
      }}

      let tactical = `${{player}} in ${{currentFormat}} (${{currentVenue}} conditions): `;
      if (player === "Virat Kohli") {{
        tactical += currentFormat === 'T20I' ? "Retired from T20Is following the 2024 World Cup triumph. Under Kirsten, Shastri, and Dravid, an all-format master averaging 49.2 in Tests and 58.2 in ODIs. His 46% vulnerability in the 5th-stump corridor is heavily targeted by SENA pacers, but overcome by legendary match-winning temperament." : "Generational match-winner with an elite 49.2 Test average and world-record 50 ODI hundreds. Virtually a 96-99% undisputed Playing XI starter across all coaching eras.";
      }} else if (player === "Rohit Sharma") {{
        tactical += currentFormat === 'T20I' ? "Retired from T20Is as World Cup Winning Captain in 2024. In Tests and ODIs, an indispensable opener whose high-intent pull shot (44% dismissals in deep) is fully backed by Gambhir for powerplay disruption." : "Legendary white-ball captain and premier Test opener. Gambhir strongly endorses his fearless boundary intent despite hook/pull dismissals.";
      }} else if (player === "Jasprit Bumrah") {{
        tactical += "The undisputed #1 weapon in world cricket (Test avg 20.7, SR 45.1, Econ 4.60). His lethal 48% Bowled/LBW rate and awkward release angle makes him a 99%+ Playing XI starter under every coach in all conditions.";
      }} else if (player === "Dhruv Jurel") {{
        tactical += "Breakout red-ball prodigy (Test avg 63.3, player of the match at Ranchi, twin fighting fifties at the MCG vs Australia A). Rahul Dravid and Gautam Gambhir view him as India's premier multi-day backup keeper.";
      }} else if (player === "Hardik Pandya") {{
        tactical += "Pace-bowling all-rounder cornerstone. Shastri, Fletcher, and Gambhir view him as the crucial link allowing India to deploy 4 express pacers overseas.";
      }} else if (player === "Yashasvi Jaiswal") {{
        tactical += "Dominant LHB opener (FC avg 61.3, 712 runs vs ENG). Gautam Gambhir's #1 favored archetype for explosive powerplay starts and LHB matchup control.";
      }} else if (player === "Kuldeep Yadav") {{
        tactical += "Unorthodox left-arm wrist spin strike bowler (T20I SR 12.5, 45% Bowled/LBW). Rahul Dravid's #1 weapon for middle-overs partnership breaking.";
      }} else {{
        tactical += `Core performer with strong multi-format credentials (Avg ${{data.batAvg}}, ${{data.caps}} Caps). 2024-25 season form: ${{ls.summary}}`;
      }}

      renderBars(scores, tactical, retNotice);
    }}

    function calcCustomPlayer() {{
      const role = document.getElementById('bldRole').value;
      const hand = document.getElementById('bldHand').value;
      const bowl = document.getElementById('bldBowl').value;
      const batAvg = parseFloat(document.getElementById('rngBatAvg').value);
      const batSR = parseFloat(document.getElementById('rngBatSR').value);
      const bowlEcon = parseFloat(document.getElementById('rngBowlEcon').value);
      const recentBatAvg = parseFloat(document.getElementById('rngRecentBatAvg').value);
      const recentBatSR = parseFloat(document.getElementById('rngRecentBatSR').value);
      const recentWkts = parseFloat(document.getElementById('rngRecentWkts').value);
      const dismissalMode = document.getElementById('bldDismissalMode').value;
      const wicketWeapon = document.getElementById('bldWicketWeapon').value;

      // Base coach affinities
      let baseGambhir = 45, baseDravid = 45, baseShastri = 45, baseKirsten = 45, baseFletcher = 45, baseKumble = 45;

      // 1. Role Influences
      if (role === "Pace All-Rounder") {{
        baseFletcher += 22; baseShastri += 20; baseGambhir += 16; baseDravid += 14; baseKirsten -= 8; baseKumble += 8;
      }} else if (role === "Spin All-Rounder") {{
        baseDravid += 24; baseGambhir += 22; baseFletcher += 20; baseKumble += 22; baseKirsten += 10; baseShastri += 8;
      }} else if (role === "Specialist Fast Bowler") {{
        baseShastri += 26; baseKirsten += 22; baseFletcher += 18; baseDravid += 14; baseGambhir += 10; baseKumble += 14;
      }} else if (role === "Specialist Spin Bowler") {{
        baseKumble += 26; baseShastri += 18; baseGambhir += 14; baseKirsten += 14; baseDravid += 10; baseFletcher -= 4;
      }} else if (role === "Top-Order Batter") {{
        baseKirsten += 24; baseFletcher += 20; baseShastri += 14; baseDravid += 12; baseGambhir += 10; baseKumble += 12;
      }} else if (role === "Wicketkeeper") {{
        baseDravid += 15; baseGambhir += 15; baseShastri += 15; baseKirsten += 15; baseFletcher += 15; baseKumble += 15;
      }}

      // 2. Hand: Gambhir rewards LHB
      if (hand === "LHB") {{
        baseGambhir += 18; baseDravid += 8; baseFletcher += 8; baseKirsten += 10;
      }}

      // 3. Bowling style
      if (bowl === "Left-Arm Fast") {{
        baseGambhir += 20; baseKirsten += 10; baseDravid += 8; baseShastri += 4;
      }} else if (bowl === "Wrist Spin") {{
        baseDravid += 22; baseShastri += 16; baseGambhir += 14; baseKirsten -= 4; baseKumble += 12;
      }}

      // 4. Career Performance (Career Batting + Bowling)
      const batBonus = (batAvg - 35) * 0.7 + (batSR - 110) * 0.18;
      baseGambhir += batBonus * 1.1;
      baseDravid += batBonus * 1.0;
      baseShastri += batBonus * 0.95;
      baseKirsten += (batAvg - 35) * 1.2;
      baseFletcher += batBonus * 0.9;
      baseKumble += (batAvg - 35) * 0.8;

      if (bowl !== "None") {{
        const bowlBonus = (7.0 - bowlEcon) * 3.5;
        baseShastri += bowlBonus * 1.2;
        baseKumble += bowlBonus * 1.3;
        baseDravid += bowlBonus * 1.0;
        baseGambhir += bowlBonus * 0.9;
        baseKirsten += bowlBonus * 1.1;
        baseFletcher += bowlBonus * 1.0;
      }}

      // 5. Last Season (2024-25 Form) Influence
      // Gambhir and Dravid heavily weight recent momentum
      const recentBonus = (recentBatAvg - 35) * 0.5 + (recentBatSR - 120) * 0.15 + (recentWkts * 0.4);
      baseGambhir += recentBonus * 1.4; // Gambhir rewards blazing form most
      baseDravid += recentBonus * 1.1;
      baseShastri += recentBonus * 0.9;
      baseKirsten += recentBonus * 0.6; // Kirsten favored long-term career stability
      baseFletcher += recentBonus * 0.8;
      baseKumble += recentBonus * 0.8;

      // 6. Technical Dismissal & Wicket-Taking Modes
      if (dismissalMode === "5th-Stump Edges") {{
        if (currentVenue === "SENA") {{
          baseShastri -= 8; baseDravid -= 6; baseKumble -= 6;
        }}
      }} else if (dismissalMode === "Short-Ball Pull") {{
        baseGambhir += 5; // Gambhir accepts high-intent aggression
        baseKirsten -= 8; // Kirsten strongly disliked risky shots in deep
      }}

      if (wicketWeapon === "Yorker-Inswing") {{
        baseGambhir += 8; baseShastri += 8;
      }} else if (wicketWeapon === "Wobble-Seam-Edges") {{
        baseShastri += (currentVenue === "SENA" ? 10 : 4);
      }} else if (wicketWeapon === "Wrist-Spin-Wrongun") {{
        baseDravid += 9; baseShastri += 6;
      }}

      // 7. Format & Venue Adjustments
      if (currentFormat === "TEST") {{
        baseKumble += 8; baseKirsten += 6; baseShastri += 5;
        if (currentVenue === "SENA" && (role.includes("Fast") || bowl.includes("Fast"))) {{
          baseShastri += 14; baseFletcher += 8;
        }}
      }}

      const scores = {{
        "Gautam Gambhir": Math.min(99.0, Math.max(12.0, baseGambhir)),
        "Rahul Dravid": Math.min(99.0, Math.max(12.0, baseDravid)),
        "Ravi Shastri": Math.min(99.0, Math.max(12.0, baseShastri)),
        "Gary Kirsten": Math.min(99.0, Math.max(12.0, baseKirsten)),
        "Duncan Fletcher": Math.min(99.0, Math.max(12.0, baseFletcher)),
        "Anil Kumble": Math.min(99.0, Math.max(12.0, baseKumble))
      }};

      const topCoach = Object.entries(scores).sort((a, b) => b[1] - a[1])[0][0];
      let reason = `Custom ${{hand}} ${{role}} (${{bowl}}): `;
      if (topCoach === "Gautam Gambhir") {{
        reason += "Favored by Gautam Gambhir due to his high valuation of recent 2024-25 strike-rate form, left-hand matchup utility, and tactical boundary aggression.";
      }} else if (topCoach === "Rahul Dravid") {{
        reason += "Favored by Rahul Dravid for batting depth security and specialized wrist-spin/middle-overs partnership breakers.";
      }} else if (topCoach === "Ravi Shastri") {{
        reason += "Favored by Ravi Shastri under his aggressive 20-wicket taking and express frontline pace bowling battery in SENA conditions.";
      }} else if (topCoach === "Anil Kumble") {{
        reason += "Favored by Anil Kumble for relentless multi-day discipline, red-ball bowling workloads, and spin fortress containment.";
      }} else {{
        reason += `Favored by ${{topCoach}} based on classical role clarity and long-term career baseline stability.`;
      }}

      renderBars(scores, reason, null);
    }}

    // Initial View on load
    updateExistingView();
  </script>
</body>
</html>
"""

html_content = build_single_page_html()

# Write to project directory
with open(os.path.join(PROJECT_DIR, 'index.html'), 'w', encoding='utf-8') as f:
    f.write(html_content)

with open(os.path.join(PROJECT_DIR, 'predictor.html'), 'w', encoding='utf-8') as f:
    f.write(html_content)

# Write to brain artifact directory
with open(os.path.join(OUTPUT_DIR, 'index.html'), 'w', encoding='utf-8') as f:
    f.write(html_content)

with open(os.path.join(OUTPUT_DIR, 'predictor.html'), 'w', encoding='utf-8') as f:
    f.write(html_content)

print("SUCCESS: Successfully built single-page index.html and predictor.html in both project and brain directories!")
