"""
build_unified_app.py
Builds index.html and predictor.html with 2 large, prominent, easy-to-see tabs.
Tab 1: 📊 Coach Predictors & Red-Ball Deep Dive
Tab 2: 🏏 Live Predictor & Player Builder (with 19 players + custom builder)
"""

import json

with open('data/processed/all_players_web.json', 'r') as f:
    players_data = json.load(f)

STATS_MAP = {
    "Virat Kohli": ("115 Tests | 8,947 Runs | Avg 49.2 | 29 100s", "First-Class: 144 Matches | 11,200 Runs | Avg 51.5 | 36 100s"),
    "Rohit Sharma": ("59 Tests | 4,137 Runs | Avg 45.0 | 12 100s", "First-Class: 125 Matches | 8,900 Runs | Avg 52.8 | 29 100s"),
    "Jasprit Bumrah": ("36 Tests | 159 Wickets | Avg 20.7 | SR 45.1", "First-Class: 74 Matches | 340 Wickets | Avg 22.1 | 16 5-Wkt Hauls"),
    "Hardik Pandya": ("11 Tests | 532 Runs (Avg 31.3) | 17 Wkts (Avg 31.1)", "First-Class: 29 Matches | 1,351 Runs | 48 Wickets"),
    "Yashasvi Jaiswal": ("14 Tests | 1,407 Runs | Avg 56.3 | 2 Double 100s", "First-Class: 32 Matches | 3,250 Runs | Avg 61.3 | 12 100s"),
    "Kuldeep Yadav": ("12 Tests | 53 Wickets | Avg 21.1 | 4 5-Wkt Hauls", "First-Class: 42 Matches | 165 Wickets | Avg 28.4"),
    "Axar Patel": ("14 Tests | 55 Wickets (Avg 19.3) | 646 Runs (Avg 35.9)", "First-Class: 58 Matches | 215 Wickets | 2,400 Runs"),
    "Arshdeep Singh": ("White-Ball Specialist | 102 Int Caps | 95 T20I Wkts", "First-Class: 19 Matches | 55 Wickets | Avg 29.8"),
    "Rishabh Pant": ("33 Tests | 2,271 Runs | Avg 43.7 | 6 100s", "First-Class: 58 Matches | 4,100 Runs | Avg 49.5 | 11 100s"),
    "Ravindra Jadeja": ("72 Tests | 3,030 Runs (Avg 36.5) | 294 Wkts (Avg 24.1)", "First-Class: 130 Matches | 7,200 Runs | 510 Wickets"),
    "Suryakumar Yadav": ("1 Test | 42 T20I Avg (SR 168.5) | T20 Captain", "First-Class: 84 Matches | 5,650 Runs | Avg 43.8 | 14 100s"),
    "Sanju Samson": ("30 ODIs (Avg 56.7) | Back-to-Back T20I 100s (2024)", "First-Class: 64 Matches | 3,800 Runs | Avg 38.5 | 11 100s"),
    "R Ashwin": ("100 Tests | 516 Wickets (Avg 23.7) | 3,309 Runs", "First-Class: 158 Matches | 740 Wickets | Avg 24.2"),
    "Shivam Dube": ("LHB Powerplay & Spin Destroyer | 48 Int Caps", "First-Class: 22 Matches | 1,250 Runs (Avg 44.6) | 48 Wkts"),
    "Washington Sundar": ("5 Tests | 305 Runs (Avg 50.8) | 18 Wickets", "First-Class: 32 Matches | 1,450 Runs | 78 Wickets"),
    "Shubman Gill": ("25 Tests | 1,492 Runs | Avg 35.5 | 5 100s", "First-Class: 52 Matches | 4,200 Runs | Avg 50.2 | 13 100s"),
    "Mohammed Siraj": ("29 Tests | 78 Wickets | Avg 29.8 | 6-15 at Cape Town", "First-Class: 65 Matches | 245 Wickets | Avg 25.1"),
    "KL Rahul": ("50 Tests | 2,863 Runs | Avg 34.1 | 8 100s", "First-Class: 95 Matches | 6,700 Runs | Avg 44.5 | 18 100s"),
    "Dhruv Jurel": ("3 Tests | 190 Runs | Avg 63.3 | Player of Match Ranchi", "First-Class: 19 Matches | 1,075 Runs | Avg 48.9 | 80 & 68 at MCG")
}

for p, stats in STATS_MAP.items():
    if p in players_data:
        players_data[p]['testStats'] = stats[0]
        players_data[p]['fcStats'] = stats[1]

players_json_str = json.dumps(players_data)

def generate_html(default_tab="deepdive"):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Indian Cricket Coach Selection Predictor & Red-Ball Deep Dive</title>
  <script src="https://www.gstatic.com/antigravity/web/dev/tailwindcss.min.js"></script>
  <style>
    .progress-bar {{
      transition: width 0.6s cubic-bezier(0.4, 0, 0.2, 1);
    }}
  </style>
</head>
<body class="bg-transparent text-[var(--foreground)] antialiased p-3 sm:p-5 font-sans">
  <div class="max-w-5xl mx-auto bg-[var(--card)] text-[var(--foreground)] border border-[var(--border)] rounded-2xl p-4 sm:p-6 shadow-md space-y-6">
    
    <!-- Top Header -->
    <div class="flex flex-col sm:flex-row sm:items-center justify-between border-b border-[var(--border)] pb-4 gap-3">
      <div>
        <div class="flex items-center gap-2">
          <span class="inline-block w-3 h-3 rounded-full bg-indigo-500 animate-pulse"></span>
          <h1 class="text-xl sm:text-2xl font-bold tracking-tight">Indian Cricket Selection Engine</h1>
        </div>
        <p class="text-xs sm:text-sm text-[var(--muted-foreground)] mt-0.5">
          Trained on 1,021 Cricsheet India matches (2001–2026) across Tests, ODIs & T20Is
        </p>
      </div>
      <div class="flex items-center gap-2">
        <span class="px-2.5 py-1 text-xs font-semibold rounded-md bg-[var(--secondary)] text-[var(--secondary-foreground)] border border-[var(--border)]">
          AUC-ROC: 0.908
        </span>
      </div>
    </div>

    <!-- 2 BIG, PROMINENT TABS -->
    <div class="bg-[var(--background)] p-1.5 rounded-2xl border-2 border-[var(--border)] shadow-xs">
      <div class="grid grid-cols-1 sm:grid-cols-2 gap-2">
        
        <!-- Tab 1 Button -->
        <button id="mainTabDeepDive" onclick="switchMainTab('deepdive')" class="flex items-center justify-center gap-2.5 py-3.5 px-4 rounded-xl text-sm sm:text-base font-bold transition duration-150 cursor-pointer text-center">
          <span class="text-lg">📊</span>
          <span>Coach Predictors & Red-Ball</span>
        </button>

        <!-- Tab 2 Button -->
        <button id="mainTabPredictor" onclick="switchMainTab('predictor')" class="flex items-center justify-center gap-2.5 py-3.5 px-4 rounded-xl text-sm sm:text-base font-bold transition duration-150 cursor-pointer text-center">
          <span class="text-lg">🏏</span>
          <span>Live Predictor & Player Builder</span>
        </button>

      </div>
    </div>

    <!-- TAB 1 CONTENT: COACH PREDICTORS & RED-BALL DEEP DIVE -->
    <div id="contentDeepDive" class="space-y-8">
      
      <!-- Part 1: Main Predictors Under Each Coach -->
      <div class="space-y-4">
        <div class="flex items-center gap-2">
          <span class="px-2.5 py-1 text-xs font-bold rounded bg-indigo-500/20 text-indigo-400 uppercase tracking-wide">Part 1</span>
          <h2 class="text-lg sm:text-xl font-bold">Main Predictors Under Each Coach & How They Differ</h2>
        </div>
        <p class="text-xs sm:text-sm text-[var(--muted-foreground)] leading-relaxed">
          Our statistical models (Interaction Logistic Regression with odds multipliers and Random Forest feature importances) reveal distinct philosophies that guided selection across Indian cricket's major coaching eras:
        </p>

        <!-- Coach Cards Grid -->
        <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
          
          <!-- Gautam Gambhir -->
          <div class="bg-[var(--background)] border border-[var(--border)] rounded-xl p-4 space-y-2.5 shadow-xs">
            <div class="flex items-center justify-between">
              <h3 class="font-bold text-sm text-indigo-500">Gautam Gambhir</h3>
              <span class="text-[10px] px-1.5 py-0.5 rounded bg-indigo-500/10 text-indigo-400 font-semibold">2024–Present</span>
            </div>
            <div class="text-xs space-y-1.5 text-[var(--muted-foreground)]">
              <p><strong class="text-[var(--foreground)]">#1 Predictor:</strong> LHB Matchup Utility (Avg 3.92 LHBs / match — highest in history)</p>
              <p><strong class="text-[var(--foreground)]">#2 Predictor:</strong> Left-Arm Pace Angle (Odds Ratio: 1.20)</p>
              <p><strong class="text-[var(--foreground)]">#3 Predictor:</strong> Multi-Utility All-Rounders (Bowling depth to #8/#9)</p>
              <p><strong class="text-[var(--foreground)]">Deprioritizes:</strong> Pure non-bowling specialist anchors (Top-order odds: 0.71, Specialist pace: 0.75)</p>
            </div>
            <div class="pt-2 border-t border-[var(--border)] text-[11px] text-[var(--foreground)]">
              <em>"Matchups, bowling options in the top 7, and high boundary strike rates take precedence over traditional accumulators."</em>
            </div>
          </div>

          <!-- Rahul Dravid -->
          <div class="bg-[var(--background)] border border-[var(--border)] rounded-xl p-4 space-y-2.5 shadow-xs">
            <div class="flex items-center justify-between">
              <h3 class="font-bold text-sm text-blue-500">Rahul Dravid</h3>
              <span class="text-[10px] px-1.5 py-0.5 rounded bg-blue-500/10 text-blue-400 font-semibold">2021–2024</span>
            </div>
            <div class="text-xs space-y-1.5 text-[var(--muted-foreground)]">
              <p><strong class="text-[var(--foreground)]">#1 Predictor:</strong> Batting Depth / Dual Spin-ARs (2.33 all-rounders / match)</p>
              <p><strong class="text-[var(--foreground)]">#2 Predictor:</strong> Attacking Wrist-Spin (Odds Ratio: 1.33, Kuldeep Yadav)</p>
              <p><strong class="text-[var(--foreground)]">#3 Predictor:</strong> Role Continuity (Highest weight on 1-year format continuity: 0.326)</p>
              <p><strong class="text-[var(--foreground)]">Deprioritizes:</strong> One-dimensional tailenders who cannot bat</p>
            </div>
            <div class="pt-2 border-t border-[var(--border)] text-[11px] text-[var(--foreground)]">
              <em>"Deep batting security paired with specialized middle-overs strike bowlers (wrist spin), avoiding knee-jerk squad churn."</em>
            </div>
          </div>

          <!-- Ravi Shastri -->
          <div class="bg-[var(--background)] border border-[var(--border)] rounded-xl p-4 space-y-2.5 shadow-xs">
            <div class="flex items-center justify-between">
              <h3 class="font-bold text-sm text-amber-500">Ravi Shastri</h3>
              <span class="text-[10px] px-1.5 py-0.5 rounded bg-amber-500/10 text-amber-400 font-semibold">2017–2021</span>
            </div>
            <div class="text-xs space-y-1.5 text-[var(--muted-foreground)]">
              <p><strong class="text-[var(--foreground)]">#1 Predictor:</strong> 20-Wicket Specialist Weapons (Specialist Spin: 1.19, Fast Bowlers: 1.11)</p>
              <p><strong class="text-[var(--foreground)]">#2 Predictor:</strong> Express Pace Overseas (4-man pace battery in SENA Tests)</p>
              <p><strong class="text-[var(--foreground)]">#3 Predictor:</strong> Pace All-Rounder Balance (Hardik Pandya / Shardul Thakur)</p>
              <p><strong class="text-[var(--foreground)]">Deprioritizes:</strong> Bits-and-pieces players who neither take wickets nor dominate</p>
            </div>
            <div class="pt-2 border-t border-[var(--border)] text-[11px] text-[var(--foreground)]">
              <em>"Aggressive 5-bowler template: backing frontline pace and attacking spinners ('Kul-Cha') to bowl opponents out twice."</em>
            </div>
          </div>

          <!-- Gary Kirsten -->
          <div class="bg-[var(--background)] border border-[var(--border)] rounded-xl p-4 space-y-2.5 shadow-xs">
            <div class="flex items-center justify-between">
              <h3 class="font-bold text-sm text-emerald-500">Gary Kirsten</h3>
              <span class="text-[10px] px-1.5 py-0.5 rounded bg-emerald-500/10 text-emerald-400 font-semibold">2008–2011</span>
            </div>
            <div class="text-xs space-y-1.5 text-[var(--muted-foreground)]">
              <p><strong class="text-[var(--foreground)]">#1 Predictor:</strong> Pure Specialist Anchors (Top-order anchor odds: 1.11)</p>
              <p><strong class="text-[var(--foreground)]">#2 Predictor:</strong> Part-Time Bowling Utility (Yuvraj, Raina, Sehwag over designated ARs)</p>
              <p><strong class="text-[var(--foreground)]">#3 Predictor:</strong> Settled Core & Low Churn (Lowest all-rounders in XI: 1.01)</p>
              <p><strong class="text-[var(--foreground)]">Deprioritizes:</strong> Frequent rotations; designated pace all-rounders (0.23 odds)</p>
            </div>
            <div class="pt-2 border-t border-[var(--border)] text-[11px] text-[var(--foreground)]">
              <em>"Clear role definitions: top 6 score the runs, 4 specialist bowlers take wickets, part-timers squeeze middle overs."</em>
            </div>
          </div>

          <!-- Duncan Fletcher -->
          <div class="bg-[var(--background)] border border-[var(--border)] rounded-xl p-4 space-y-2.5 shadow-xs">
            <div class="flex items-center justify-between">
              <h3 class="font-bold text-sm text-purple-500">Duncan Fletcher</h3>
              <span class="text-[10px] px-1.5 py-0.5 rounded bg-purple-500/10 text-purple-400 font-semibold">2011–2015</span>
            </div>
            <div class="text-xs space-y-1.5 text-[var(--muted-foreground)]">
              <p><strong class="text-[var(--foreground)]">#1 Predictor:</strong> Spin All-Rounder Genesis (1.52 / match; Ashwin & Jadeja)</p>
              <p><strong class="text-[var(--foreground)]">#2 Predictor:</strong> Pace All-Rounder Value (Odds Ratio: 1.29)</p>
              <p><strong class="text-[var(--foreground)]">#3 Predictor:</strong> Technical Batting Prowess (Rebuilding transition era)</p>
              <p><strong class="text-[var(--foreground)]">Deprioritizes:</strong> Non-batting specialist spinners (Odds Ratio: 0.49)</p>
            </div>
            <div class="pt-2 border-t border-[var(--border)] text-[11px] text-[var(--foreground)]">
              <em>"Instituted India's modern limited-overs template at the 2013 Champions Trophy with Jadeja-Ashwin anchoring the middle."</em>
            </div>
          </div>

          <!-- Anil Kumble -->
          <div class="bg-[var(--background)] border border-[var(--border)] rounded-xl p-4 space-y-2.5 shadow-xs">
            <div class="flex items-center justify-between">
              <h3 class="font-bold text-sm text-rose-500">Anil Kumble</h3>
              <span class="text-[10px] px-1.5 py-0.5 rounded bg-rose-500/10 text-rose-400 font-semibold">2016–2017</span>
            </div>
            <div class="text-xs space-y-1.5 text-[var(--muted-foreground)]">
              <p><strong class="text-[var(--foreground)]">#1 Predictor:</strong> Spin Dominance & Tireless Workloads (Ashwin & Jadeja peak)</p>
              <p><strong class="text-[var(--foreground)]">#2 Predictor:</strong> Red-Ball Grinding & First-Class Pedigree</p>
              <p><strong class="text-[var(--foreground)]">#3 Predictor:</strong> Ruthless Home Fortress Record (Won 12 of 17 Tests)</p>
              <p><strong class="text-[var(--foreground)]">Deprioritizes:</strong> Flamboyant white-ball slogging in multi-day formats</p>
            </div>
            <div class="pt-2 border-t border-[var(--border)] text-[11px] text-[var(--foreground)]">
              <em>"Classic Test discipline: relentless spin suffocation, defensive patience, and grinding batting."</em>
            </div>
          </div>

        </div>
      </div>

      <!-- Part 2: Test & First-Class Dynamics -->
      <div class="space-y-4 border-t border-[var(--border)] pt-6">
        <div class="flex items-center gap-2">
          <span class="px-2.5 py-1 text-xs font-bold rounded bg-emerald-500/20 text-emerald-400 uppercase tracking-wide">Part 2</span>
          <h2 class="text-lg sm:text-xl font-bold">Test Match & First-Class Selection Dynamics</h2>
        </div>
        <p class="text-xs sm:text-sm text-[var(--muted-foreground)] leading-relaxed">
          Test cricket selection obeys entirely different mathematical rules than white-ball formats. In Test and First-Class (Ranji Trophy, Duleep Trophy, India A) cricket, match selection hinges on <strong>workload endurance, condition polarity (Home vs SENA), and long-innings defense</strong>:
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
              In domestic multi-day matches (Ranji & Duleep Trophy), coaches historically looked for <strong>balls faced per dismissal</strong> and a <strong>Ranji average &gt;52.0</strong> (e.g. Cheteshwar Pujara, Ajinkya Rahane, Mayank Agarwal). Under Gambhir and Dravid, selection has also rewarded <strong>first-class boundary percentage, proactive strike rates, and overseas India A performances</strong> (Yashasvi Jaiswal, Dhruv Jurel, Sarfaraz Khan).
            </p>
          </div>
          <div class="bg-[var(--background)] p-3.5 rounded-xl border border-[var(--border)]">
            <h4 class="font-bold text-xs uppercase text-amber-500 mb-1">First-Class to Test Bowling Workloads</h4>
            <p class="text-xs text-[var(--muted-foreground)] leading-relaxed">
              Red-ball fast bowling selection requires proven stamina: bowling <strong>18–25 overs per day</strong> at 138+ km/h with an economy &lt;2.80 and strike rate &lt;45.0. Shastri demanded express velocity (Bumrah, Siraj, Umesh, Shami), whereas Fletcher & Dravid favored seam control and line-and-length attrition (Bhuvneshwar, Shami, Mukesh Kumar).
            </p>
          </div>
        </div>
      </div>

      <!-- Part 3: Empirical Playing XI Composition Scorecard -->
      <div class="space-y-4 border-t border-[var(--border)] pt-6">
        <div class="flex items-center gap-2">
          <span class="px-2.5 py-1 text-xs font-bold rounded bg-blue-500/20 text-blue-400 uppercase tracking-wide">Part 3</span>
          <h2 class="text-lg sm:text-xl font-bold">Empirical Playing XI Team Compositions Across All Formats</h2>
        </div>
        <div class="overflow-x-auto">
          <table class="w-full text-left text-xs border-collapse border border-[var(--border)]">
            <thead>
              <tr class="bg-[var(--secondary)] text-[var(--secondary-foreground)]">
                <th class="p-2.5 border border-[var(--border)] font-semibold">Coach</th>
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
                <td class="p-2.5 border border-[var(--border)] font-medium">Gautam Gambhir</td>
                <td class="p-2.5 border border-[var(--border)]">2.11</td>
                <td class="p-2.5 border border-[var(--border)]">0.75</td>
                <td class="p-2.5 border border-[var(--border)]">1.36</td>
                <td class="p-2.5 border border-[var(--border)]">1.67</td>
                <td class="p-2.5 border border-[var(--border)]">1.69</td>
                <td class="p-2.5 border border-[var(--border)] font-bold text-emerald-500">3.92 (All-Time High)</td>
              </tr>
              <tr>
                <td class="p-2.5 border border-[var(--border)] font-medium">Rahul Dravid</td>
                <td class="p-2.5 border border-[var(--border)] font-bold text-emerald-500">2.33 (Highest)</td>
                <td class="p-2.5 border border-[var(--border)]">0.76</td>
                <td class="p-2.5 border border-[var(--border)] font-bold text-emerald-500">1.57</td>
                <td class="p-2.5 border border-[var(--border)]">2.40</td>
                <td class="p-2.5 border border-[var(--border)] font-bold text-emerald-500">1.54</td>
                <td class="p-2.5 border border-[var(--border)]">3.02</td>
              </tr>
              <tr>
                <td class="p-2.5 border border-[var(--border)] font-medium">Ravi Shastri</td>
                <td class="p-2.5 border border-[var(--border)]">1.77</td>
                <td class="p-2.5 border border-[var(--border)] font-bold text-amber-500">0.81</td>
                <td class="p-2.5 border border-[var(--border)]">0.96</td>
                <td class="p-2.5 border border-[var(--border)] font-bold text-emerald-500">2.24 (Express)</td>
                <td class="p-2.5 border border-[var(--border)]">1.52</td>
                <td class="p-2.5 border border-[var(--border)]">2.49</td>
              </tr>
              <tr>
                <td class="p-2.5 border border-[var(--border)] font-medium">Gary Kirsten</td>
                <td class="p-2.5 border border-[var(--border)]">1.01 (Lowest)</td>
                <td class="p-2.5 border border-[var(--border)]">0.15</td>
                <td class="p-2.5 border border-[var(--border)]">0.86</td>
                <td class="p-2.5 border border-[var(--border)]">2.41</td>
                <td class="p-2.5 border border-[var(--border)]">1.53</td>
                <td class="p-2.5 border border-[var(--border)]">2.99</td>
              </tr>
              <tr>
                <td class="p-2.5 border border-[var(--border)] font-medium">Duncan Fletcher</td>
                <td class="p-2.5 border border-[var(--border)]">1.66</td>
                <td class="p-2.5 border border-[var(--border)]">0.14</td>
                <td class="p-2.5 border border-[var(--border)]">1.52</td>
                <td class="p-2.5 border border-[var(--border)]">2.02</td>
                <td class="p-2.5 border border-[var(--border)]">1.11</td>
                <td class="p-2.5 border border-[var(--border)]">3.05</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- Button jump to Tab 2 -->
      <div class="border-t border-[var(--border)] pt-6 text-center">
        <button onclick="switchMainTab('predictor')" class="px-6 py-3 text-sm font-bold rounded-xl bg-indigo-600 text-white hover:bg-indigo-700 transition shadow-sm cursor-pointer inline-flex items-center gap-2">
          <span>Go to Live Predictor & Player Builder</span>
          <span>→</span>
        </button>
      </div>

    </div>

    <!-- TAB 2 CONTENT: LIVE PREDICTOR & PLAYER BUILDER -->
    <div id="contentPredictor" class="hidden space-y-6">
      
      <!-- Sub-Mode Switcher: Existing Player vs Build a Player -->
      <div class="bg-[var(--secondary)]/50 p-1.5 rounded-xl border border-[var(--border)]">
        <div class="grid grid-cols-2 gap-2 text-center text-xs sm:text-sm font-bold">
          <button id="subTabExisting" onclick="switchSubMode('existing')" class="py-2.5 rounded-lg transition duration-150 cursor-pointer">
            🇮🇳 Select Existing Indian Player
          </button>
          <button id="subTabBuilder" onclick="switchSubMode('builder')" class="py-2.5 rounded-lg transition duration-150 cursor-pointer">
            🛠️ Build a Custom Player
          </button>
        </div>
      </div>

      <!-- Section A: Existing Player Selection -->
      <div id="existingPlayerSection" class="space-y-4">
        <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
          
          <div class="space-y-1.5">
            <label class="block text-xs font-bold uppercase tracking-wider text-[var(--muted-foreground)]">Select Indian Player</label>
            <select id="playerSelect" onchange="updateView()" class="w-full bg-[var(--background)] text-[var(--foreground)] border border-[var(--border)] rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-[var(--primary)] font-medium">
              {''.join([f'<option value="{p}">{p}</option>' for p in players_data.keys()])}
            </select>
          </div>

          <div class="space-y-1.5">
            <label class="block text-xs font-bold uppercase tracking-wider text-[var(--muted-foreground)]">Match Format</label>
            <div class="grid grid-cols-3 gap-1 bg-[var(--background)] p-1 rounded-lg border border-[var(--border)] text-center text-xs font-semibold">
              <button id="btnTEST" onclick="setFormat('TEST')" class="py-1.5 rounded-md bg-[var(--primary)] text-[var(--primary-foreground)] shadow-xs transition">TEST</button>
              <button id="btnODI" onclick="setFormat('ODI')" class="py-1.5 rounded-md text-[var(--muted-foreground)] hover:text-[var(--foreground)] transition">ODI</button>
              <button id="btnT20I" onclick="setFormat('T20I')" class="py-1.5 rounded-md text-[var(--muted-foreground)] hover:text-[var(--foreground)] transition">T20I</button>
            </div>
          </div>

          <div class="space-y-1.5">
            <label class="block text-xs font-bold uppercase tracking-wider text-[var(--muted-foreground)]">Venue Conditions</label>
            <div class="grid grid-cols-2 gap-1 bg-[var(--background)] p-1 rounded-lg border border-[var(--border)] text-center text-xs font-semibold">
              <button id="btnHome" onclick="setVenue('Home')" class="py-1.5 rounded-md bg-[var(--primary)] text-[var(--primary-foreground)] shadow-xs transition">Subcontinent</button>
              <button id="btnSena" onclick="setVenue('SENA')" class="py-1.5 rounded-md text-[var(--muted-foreground)] hover:text-[var(--foreground)] transition">SENA Overseas</button>
            </div>
          </div>

        </div>

        <!-- Player Profile Card -->
        <div id="playerBio" class="bg-[var(--background)] border border-[var(--border)] rounded-xl p-4 text-sm grid grid-cols-2 sm:grid-cols-4 gap-3 shadow-xs">
          <!-- Populated via JS -->
        </div>
      </div>

      <!-- Section B: Build a Player Simulator -->
      <div id="builderSection" class="hidden space-y-4 bg-[var(--background)] border border-[var(--border)] rounded-xl p-4 shadow-xs">
        <div class="flex items-center justify-between border-b border-[var(--border)] pb-2">
          <h3 class="text-sm font-bold uppercase tracking-wider text-indigo-500">🛠️ Custom Cricketer Creator</h3>
          <span class="text-xs text-[var(--muted-foreground)]">Live Probability Engine</span>
        </div>

        <!-- Archetype Configuration -->
        <div class="grid grid-cols-1 sm:grid-cols-3 gap-3">
          <div>
            <label class="block text-xs font-semibold text-[var(--muted-foreground)] mb-1">Primary Role</label>
            <select id="bldRole" onchange="calcCustomPlayer()" class="w-full bg-[var(--card)] text-[var(--foreground)] border border-[var(--border)] rounded-lg p-2 text-xs">
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
            <select id="bldHand" onchange="calcCustomPlayer()" class="w-full bg-[var(--card)] text-[var(--foreground)] border border-[var(--border)] rounded-lg p-2 text-xs">
              <option value="RHB">Right-Hand Bat (RHB)</option>
              <option value="LHB">Left-Hand Bat (LHB)</option>
            </select>
          </div>

          <div>
            <label class="block text-xs font-semibold text-[var(--muted-foreground)] mb-1">Bowling Style</label>
            <select id="bldBowl" onchange="calcCustomPlayer()" class="w-full bg-[var(--card)] text-[var(--foreground)] border border-[var(--border)] rounded-lg p-2 text-xs">
              <option value="Right-Arm Fast">Right-Arm Fast / Seam</option>
              <option value="Left-Arm Fast">Left-Arm Fast (Arshdeep/Zaheer angle)</option>
              <option value="Finger Spin">Finger Spin (Off-break / Orthodox)</option>
              <option value="Wrist Spin">Wrist Spin (Kuldeep / Leg-break)</option>
              <option value="None">None (Pure Batter / Keeper)</option>
            </select>
          </div>
        </div>

        <!-- Sliders Grid -->
        <div class="grid grid-cols-1 sm:grid-cols-3 gap-4 pt-2">
          <div>
            <div class="flex justify-between text-xs mb-1">
              <span>Batting Average:</span>
              <span id="lblBatAvg" class="font-bold text-emerald-500">45.0</span>
            </div>
            <input type="range" id="rngBatAvg" min="15" max="65" value="45" oninput="document.getElementById('lblBatAvg').innerText = this.value; calcCustomPlayer()" class="w-full">
          </div>

          <div>
            <div class="flex justify-between text-xs mb-1">
              <span>Batting Strike Rate:</span>
              <span id="lblBatSR" class="font-bold text-indigo-400">140</span>
            </div>
            <input type="range" id="rngBatSR" min="70" max="185" value="140" oninput="document.getElementById('lblBatSR').innerText = this.value; calcCustomPlayer()" class="w-full">
          </div>

          <div>
            <div class="flex justify-between text-xs mb-1">
              <span>Bowling Economy:</span>
              <span id="lblBowlEcon" class="font-bold text-amber-500">6.8</span>
            </div>
            <input type="range" id="rngBowlEcon" min="3.0" max="11.0" step="0.1" value="6.8" oninput="document.getElementById('lblBowlEcon').innerText = this.value; calcCustomPlayer()" class="w-full">
          </div>
        </div>
      </div>

      <!-- Live Coach Selection Probabilities Bars -->
      <div class="space-y-4">
        <div class="flex items-center justify-between">
          <h2 class="text-sm font-bold uppercase tracking-wider text-[var(--foreground)]">Predicted Selection Probability by Coach</h2>
          <span class="text-xs text-[var(--muted-foreground)]">Playing XI Matchday Likelihood</span>
        </div>

        <div id="coachBarsContainer" class="space-y-3">
          <!-- Populated via JS -->
        </div>
      </div>

      <!-- Tactical Insight Box -->
      <div id="tacticalInsight" class="border border-[var(--border)] bg-[var(--secondary)]/40 rounded-xl p-4">
        <h3 class="text-xs font-bold uppercase tracking-wider text-[var(--foreground)] mb-1 flex items-center gap-1.5">
          <svg class="w-4 h-4 text-amber-500" fill="currentColor" viewBox="0 0 20 20">
            <path d="M11 3a1 1 0 10-2 0v1a1 1 0 102 0V3zM15.657 5.757a1 1 0 00-1.414-1.414l-.707.707a1 1 0 001.414 1.414l.707-.707zM18 10a1 1 0 01-1 1h-1a1 1 0 110-2h1a1 1 0 011 1zM5.05 6.464A1 1 0 106.464 5.05l-.707-.707a1 1 0 00-1.414 1.414l.707.707zM5 10a1 1 0 01-1 1H3a1 1 0 110-2h1a1 1 0 011 1zM8 16v-1h4v1a2 2 0 11-4 0zM12 14H8a4 4 0 01-.8-7.92A4.002 4.002 0 0115.8 9.2 4.002 4.002 0 0112 14z" />
          </svg>
          Tactical Coach Rationale
        </h3>
        <p id="tacticalText" class="text-xs sm:text-sm text-[var(--foreground)] leading-relaxed">
          Loading tactical insight...
        </p>
      </div>

    </div>

  </div>

  <script>
    const PLAYERS_DATA = {players_json_str};

    let currentMainTab = "{default_tab}";
    let currentSubMode = "existing";
    let currentFormat = "TEST";
    let currentVenue = "Home";

    function switchMainTab(tab) {{
      currentMainTab = tab;
      const btnDeepDive = document.getElementById('mainTabDeepDive');
      const btnPredictor = document.getElementById('mainTabPredictor');
      const contentDeepDive = document.getElementById('contentDeepDive');
      const contentPredictor = document.getElementById('contentPredictor');

      if (tab === 'deepdive') {{
        btnDeepDive.className = "flex items-center justify-center gap-2.5 py-3.5 px-4 rounded-xl text-sm sm:text-base font-bold transition duration-150 cursor-pointer text-center bg-indigo-600 text-white shadow-md";
        btnPredictor.className = "flex items-center justify-center gap-2.5 py-3.5 px-4 rounded-xl text-sm sm:text-base font-bold transition duration-150 cursor-pointer text-center text-[var(--muted-foreground)] hover:text-[var(--foreground)] hover:bg-[var(--secondary)]/40";
        contentDeepDive.classList.remove('hidden');
        contentPredictor.classList.add('hidden');
      }} else {{
        btnPredictor.className = "flex items-center justify-center gap-2.5 py-3.5 px-4 rounded-xl text-sm sm:text-base font-bold transition duration-150 cursor-pointer text-center bg-indigo-600 text-white shadow-md";
        btnDeepDive.className = "flex items-center justify-center gap-2.5 py-3.5 px-4 rounded-xl text-sm sm:text-base font-bold transition duration-150 cursor-pointer text-center text-[var(--muted-foreground)] hover:text-[var(--foreground)] hover:bg-[var(--secondary)]/40";
        contentDeepDive.classList.add('hidden');
        contentPredictor.classList.remove('hidden');
        if (currentSubMode === 'existing') updateView(); else calcCustomPlayer();
      }}
    }}

    function switchSubMode(mode) {{
      currentSubMode = mode;
      const subTabEx = document.getElementById('subTabExisting');
      const subTabBld = document.getElementById('subTabBuilder');
      const secEx = document.getElementById('existingPlayerSection');
      const secBld = document.getElementById('builderSection');

      if (mode === 'existing') {{
        subTabEx.className = "py-2.5 rounded-lg bg-[var(--primary)] text-[var(--primary-foreground)] shadow-xs transition duration-150 cursor-pointer font-bold";
        subTabBld.className = "py-2.5 rounded-lg text-[var(--muted-foreground)] hover:text-[var(--foreground)] transition duration-150 cursor-pointer font-medium";
        secEx.classList.remove('hidden');
        secBld.classList.add('hidden');
        updateView();
      }} else {{
        subTabBld.className = "py-2.5 rounded-lg bg-[var(--primary)] text-[var(--primary-foreground)] shadow-xs transition duration-150 cursor-pointer font-bold";
        subTabEx.className = "py-2.5 rounded-lg text-[var(--muted-foreground)] hover:text-[var(--foreground)] transition duration-150 cursor-pointer font-medium";
        secEx.classList.add('hidden');
        secBld.classList.remove('hidden');
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
      if (currentSubMode === 'existing') updateView(); else calcCustomPlayer();
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
      if (currentSubMode === 'existing') updateView(); else calcCustomPlayer();
    }}

    function renderBars(scores, tacticalText) {{
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
        const widthPct = Math.min(100, Math.max(6, prob));

        const row = document.createElement('div');
        row.className = "space-y-1";
        row.innerHTML = `
          <div class="flex items-center justify-between text-xs sm:text-sm">
            <span class="font-medium flex items-center gap-1.5">
              ${{coach}}
              ${{index === 0 && prob > 40 ? '<span class="text-[10px] font-bold px-1.5 py-0.5 rounded bg-emerald-500/20 text-emerald-600 dark:text-emerald-400">#1 Preferred</span>' : ''}}
            </span>
            <span class="font-bold tabular-nums">${{prob.toFixed(1)}}%</span>
          </div>
          <div class="w-full h-3 bg-[var(--secondary)] rounded-full overflow-hidden border border-[var(--border)]">
            <div class="progress-bar h-full ${{color}} rounded-full" style="width: ${{widthPct}}%"></div>
          </div>
        `;
        barsContainer.appendChild(row);
      }});

      document.getElementById('tacticalText').innerText = tacticalText;
    }}

    function updateView() {{
      const player = document.getElementById('playerSelect').value;
      const data = PLAYERS_DATA[player] || PLAYERS_DATA["Virat Kohli"];

      // Update Bio
      const bioEl = document.getElementById('playerBio');
      bioEl.innerHTML = `
        <div>
          <span class="text-xs text-[var(--muted-foreground)] block">Role</span>
          <span class="font-semibold text-xs sm:text-sm">${{data.role}}</span>
        </div>
        <div>
          <span class="text-xs text-[var(--muted-foreground)] block">Bat / Bowl Style</span>
          <span class="font-semibold text-xs sm:text-sm">${{data.hand}} / ${{data.bowling}}</span>
        </div>
        <div>
          <span class="text-xs text-[var(--muted-foreground)] block">Test Match Record</span>
          <span class="font-semibold text-xs sm:text-sm text-emerald-500">${{data.testStats || "Modern Core"}}</span>
        </div>
        <div>
          <span class="text-xs text-[var(--muted-foreground)] block">First-Class Multi-Day Record</span>
          <span class="font-semibold text-xs sm:text-sm text-indigo-400">${{data.fcStats || "Domestic Multi-Day Core"}}</span>
        </div>
      `;

      const key = `${{currentFormat}}_${{currentVenue}}`;
      const scores = (data.squad_scores && data.squad_scores[key]) ? data.squad_scores[key] : {{
        "Gautam Gambhir": 75.0, "Rahul Dravid": 78.0, "Ravi Shastri": 80.0, "Gary Kirsten": 70.0, "Duncan Fletcher": 72.0
      }};

      let tactical = `${{player}} in ${{currentFormat}} (${{currentVenue}} conditions): `;
      if (player === "Virat Kohli") {{
        tactical += "Generational match-winner with an elite 49.2 Test average. Virtually an undisputed starter across all red-ball and ODI squads.";
      }} else if (player === "Dhruv Jurel") {{
        tactical += "Breakout red-ball star under Dravid and Gambhir (Test avg 63.3, twin fifties at the MCG for India A). High priority backup keeper-batter.";
      }} else if (player === "Hardik Pandya") {{
        tactical += "Pace all-rounder cornerstone. Shastri and Fletcher heavily rely on him to balance 4 pacers overseas.";
      }} else if (player === "Yashasvi Jaiswal") {{
        tactical += "Dominant LHB opener (First-Class avg 61.3). Gambhir's #1 favored archetype for explosive powerplay starts.";
      }} else if (player === "Jasprit Bumrah") {{
        tactical += "All-format strike bowler (Test avg 20.7, SR 45.1). An undisputed 99%+ selection lock under every coach.";
      }} else {{
        tactical += `Core player with proven performance credentials (Avg ${{data.batAvg}}, ${{data.caps}} Career Caps).`;
      }}

      renderBars(scores, tactical);
    }}

    function calcCustomPlayer() {{
      const role = document.getElementById('bldRole').value;
      const hand = document.getElementById('bldHand').value;
      const bowl = document.getElementById('bldBowl').value;
      const batAvg = parseFloat(document.getElementById('rngBatAvg').value);
      const batSR = parseFloat(document.getElementById('rngBatSR').value);
      const bowlEcon = parseFloat(document.getElementById('rngBowlEcon').value);

      // Base probabilities by role & format
      let baseGambhir = 50, baseDravid = 50, baseShastri = 50, baseKirsten = 50, baseFletcher = 50;

      // Role adjustments
      if (role === "Pace All-Rounder") {{
        baseFletcher += 20; baseShastri += 18; baseGambhir += 14; baseDravid += 12; baseKirsten -= 10;
      }} else if (role === "Spin All-Rounder") {{
        baseDravid += 22; baseGambhir += 20; baseFletcher += 18; baseKirsten += 12; baseShastri += 6;
      }} else if (role === "Specialist Fast Bowler") {{
        baseShastri += 24; baseKirsten += 20; baseFletcher += 15; baseDravid += 12; baseGambhir += 8;
      }} else if (role === "Specialist Spin Bowler") {{
        baseShastri += 18; baseGambhir += 12; baseKirsten += 14; baseDravid += 8; baseFletcher -= 5;
      }} else if (role === "Top-Order Batter") {{
        baseKirsten += 22; baseFletcher += 18; baseShastri += 12; baseDravid += 10; baseGambhir += 8;
      }}

      // Hand adjustments: Gambhir rewards LHB
      if (hand === "LHB") {{
        baseGambhir += 16; baseDravid += 8; baseFletcher += 8; baseKirsten += 12;
      }}

      // Left-Arm Pacer bonus: Gambhir highest
      if (bowl === "Left-Arm Fast") {{
        baseGambhir += 18; baseKirsten += 10; baseDravid += 8; baseShastri += 2;
      }} else if (bowl === "Wrist Spin") {{
        baseDravid += 20; baseShastri += 14; baseGambhir += 12; baseKirsten -= 4;
      }}

      // Batting stats influence
      const batBonus = (batAvg - 35) * 0.7 + (batSR - 110) * 0.2;
      baseGambhir += batBonus * 1.2;
      baseDravid += batBonus * 1.0;
      baseShastri += batBonus * 0.9;
      baseKirsten += (batAvg - 35) * 1.1;
      baseFletcher += batBonus * 0.9;

      // Format & Venue adjustments
      if (currentFormat === "TEST") {{
        baseKirsten += 5; baseShastri += 5;
        if (currentVenue === "SENA" && (role.includes("Fast") || bowl.includes("Fast"))) {{
          baseShastri += 14; baseFletcher += 8;
        }}
      }}

      const scores = {{
        "Gautam Gambhir": Math.min(99.0, Math.max(10.0, baseGambhir)),
        "Rahul Dravid": Math.min(99.0, Math.max(10.0, baseDravid)),
        "Ravi Shastri": Math.min(99.0, Math.max(10.0, baseShastri)),
        "Gary Kirsten": Math.min(99.0, Math.max(10.0, baseKirsten)),
        "Duncan Fletcher": Math.min(99.0, Math.max(10.0, baseFletcher))
      }};

      const topCoach = Object.entries(scores).sort((a, b) => b[1] - a[1])[0][0];
      let reason = `Custom ${{hand}} ${{role}} (${{bowl}}): `;
      if (topCoach === "Gautam Gambhir") {{
        reason += "Favored by Gautam Gambhir due to his high valuation of Left-Hand batting balance, multi-utility options, and left-arm angles.";
      }} else if (topCoach === "Rahul Dravid") {{
        reason += "Favored by Rahul Dravid for batting depth and specialized spin bowling weapons.";
      }} else if (topCoach === "Ravi Shastri") {{
        reason += "Favored by Ravi Shastri under his aggressive 20-wicket taking and express frontline pace template.";
      }} else {{
        reason += `Favored by ${{topCoach}} based on classical role-clarity and traditional specialist balance.`;
      }}

      renderBars(scores, reason);
    }}

    // Check URL hash if any (#predictor or #deepdive)
    if (window.location.hash === '#predictor') {{
      switchMainTab('predictor');
    }} else if (window.location.hash === '#deepdive') {{
      switchMainTab('deepdive');
    }} else {{
      switchMainTab('{default_tab}');
    }}

    // Initialize sub-mode
    switchSubMode('existing');
  </script>
</body>
</html>
"""

# Generate index.html (defaults to deepdive tab)
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(generate_html(default_tab="deepdive"))

# Generate predictor.html (defaults to predictor tab)
with open('predictor.html', 'w', encoding='utf-8') as f:
    f.write(generate_html(default_tab="predictor"))

print("Built unified index.html and predictor.html with 2 prominent tabs successfully!")
