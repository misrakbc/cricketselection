"""
player_metadata.py
Enriches Indian players with authoritative cricket metadata:
- Batting hand: LHB (Left-hand bat) or RHB (Right-hand bat)
- Bowling arm: Right, Left, or None
- Bowling style: Pace, Finger Spin, Wrist Spin, or None
- Primary role: Top-Order Batter, Middle-Order Batter, Wicketkeeper, Pace All-Rounder,
  Spin All-Rounder, Specialist Fast Bowler, Specialist Spin Bowler
"""

# Explicit definitions for key players; remaining will use empirical heuristic fallback
PLAYER_ARCHETYPES = {
    # Wicketkeepers
    "MS Dhoni": {"hand": "RHB", "arm": "Right", "bowling": "Pace", "role": "Wicketkeeper"},
    "RR Pant": {"hand": "LHB", "arm": "None", "bowling": "None", "role": "Wicketkeeper"},
    "KL Rahul": {"hand": "RHB", "arm": "None", "bowling": "None", "role": "Wicketkeeper"},
    "KD Karthik": {"hand": "RHB", "arm": "None", "bowling": "None", "role": "Wicketkeeper"},
    "SV Samson": {"hand": "RHB", "arm": "None", "bowling": "None", "role": "Wicketkeeper"},
    "Ishan Kishan": {"hand": "LHB", "arm": "None", "bowling": "None", "role": "Wicketkeeper"},
    "WP Saha": {"hand": "RHB", "arm": "None", "bowling": "None", "role": "Wicketkeeper"},
    "PA Patel": {"hand": "LHB", "arm": "None", "bowling": "None", "role": "Wicketkeeper"},
    "D Dasgupta": {"hand": "RHB", "arm": "None", "bowling": "None", "role": "Wicketkeeper"},
    "J Sharma": {"hand": "RHB", "arm": "None", "bowling": "None", "role": "Wicketkeeper"},
    "Dhruv Jurel": {"hand": "RHB", "arm": "None", "bowling": "None", "role": "Wicketkeeper"},
    "DC Jurel": {"hand": "RHB", "arm": "None", "bowling": "None", "role": "Wicketkeeper"},
    "DH Mongia": {"hand": "LHB", "arm": "Left", "bowling": "Finger Spin", "role": "Middle-Order Batter"},
    
    # Top Order Batters
    "RG Sharma": {"hand": "RHB", "arm": "Right", "bowling": "Finger Spin", "role": "Top-Order Batter"},
    "V Kohli": {"hand": "RHB", "arm": "Right", "bowling": "Pace", "role": "Top-Order Batter"},
    "S Dhawan": {"hand": "LHB", "arm": "Right", "bowling": "Finger Spin", "role": "Top-Order Batter"},
    "V Sehwag": {"hand": "RHB", "arm": "Right", "bowling": "Finger Spin", "role": "Top-Order Batter"},
    "SR Tendulkar": {"hand": "RHB", "arm": "Right", "bowling": "Wrist Spin", "role": "Top-Order Batter"},
    "G Gambhir": {"hand": "LHB", "arm": "Right", "bowling": "Wrist Spin", "role": "Top-Order Batter"},
    "Shubman Gill": {"hand": "RHB", "arm": "Right", "bowling": "Finger Spin", "role": "Top-Order Batter"},
    "YBK Jaiswal": {"hand": "LHB", "arm": "Right", "bowling": "Wrist Spin", "role": "Top-Order Batter"},
    "R Dravid": {"hand": "RHB", "arm": "Right", "bowling": "Finger Spin", "role": "Top-Order Batter"},
    "CA Pujara": {"hand": "RHB", "arm": "Right", "bowling": "Wrist Spin", "role": "Top-Order Batter"},
    "AM Rahane": {"hand": "RHB", "arm": "Right", "bowling": "Pace", "role": "Top-Order Batter"},
    "MA Agarwal": {"hand": "RHB", "arm": "None", "bowling": "None", "role": "Top-Order Batter"},
    "PP Shaw": {"hand": "RHB", "arm": "None", "bowling": "None", "role": "Top-Order Batter"},
    "RD Gaikwad": {"hand": "RHB", "arm": "Right", "bowling": "Finger Spin", "role": "Top-Order Batter"},
    "Abhishek Sharma": {"hand": "LHB", "arm": "Left", "bowling": "Finger Spin", "role": "Top-Order Batter"},
    "B Sai Sudharsan": {"hand": "LHB", "arm": "Right", "bowling": "Wrist Spin", "role": "Top-Order Batter"},
    "W Jaffer": {"hand": "RHB", "arm": "Right", "bowling": "Finger Spin", "role": "Top-Order Batter"},
    "A Chopra": {"hand": "RHB", "arm": "Right", "bowling": "Pace", "role": "Top-Order Batter"},
    "A Mukund": {"hand": "LHB", "arm": "Right", "bowling": "Wrist Spin", "role": "Top-Order Batter"},
    "D Padikkal": {"hand": "LHB", "arm": "Right", "bowling": "Finger Spin", "role": "Top-Order Batter"},
    
    # Middle Order Batters
    "Yuvraj Singh": {"hand": "LHB", "arm": "Left", "bowling": "Finger Spin", "role": "Middle-Order Batter"},
    "SK Raina": {"hand": "LHB", "arm": "Right", "bowling": "Finger Spin", "role": "Middle-Order Batter"},
    "VVS Laxman": {"hand": "RHB", "arm": "Right", "bowling": "Finger Spin", "role": "Middle-Order Batter"},
    "SA Yadav": {"hand": "RHB", "arm": "Right", "bowling": "Finger Spin", "role": "Middle-Order Batter"},
    "SS Iyer": {"hand": "RHB", "arm": "Right", "bowling": "Wrist Spin", "role": "Middle-Order Batter"},
    "AT Rayudu": {"hand": "RHB", "arm": "Right", "bowling": "Finger Spin", "role": "Middle-Order Batter"},
    "MK Pandey": {"hand": "RHB", "arm": "Right", "bowling": "Pace", "role": "Middle-Order Batter"},
    "Tilak Varma": {"hand": "LHB", "arm": "Right", "bowling": "Finger Spin", "role": "Middle-Order Batter"},
    "Rinku Singh": {"hand": "LHB", "arm": "Right", "bowling": "Finger Spin", "role": "Middle-Order Batter"},
    "KM Jadhav": {"hand": "RHB", "arm": "Right", "bowling": "Finger Spin", "role": "Middle-Order Batter"},
    "M Kaif": {"hand": "RHB", "arm": "Right", "bowling": "Finger Spin", "role": "Middle-Order Batter"},
    "SN Thakur": {"hand": "RHB", "arm": "Right", "bowling": "Pace", "role": "Pace All-Rounder"},
    "Sarfaraz Khan": {"hand": "RHB", "arm": "Right", "bowling": "Wrist Spin", "role": "Middle-Order Batter"},

    # Pace All-Rounders
    "HH Pandya": {"hand": "RHB", "arm": "Right", "bowling": "Pace", "role": "Pace All-Rounder"},
    "IK Pathan": {"hand": "LHB", "arm": "Left", "bowling": "Left-Arm Fast", "role": "Pace All-Rounder"},
    "Shardul Thakur": {"hand": "RHB", "arm": "Right", "bowling": "Pace", "role": "Pace All-Rounder"},
    "Shivam Dube": {"hand": "LHB", "arm": "Right", "bowling": "Pace", "role": "Pace All-Rounder"},
    "Nitish Kumar Reddy": {"hand": "RHB", "arm": "Right", "bowling": "Pace", "role": "Pace All-Rounder"},
    "V Shankar": {"hand": "RHB", "arm": "Right", "bowling": "Pace", "role": "Pace All-Rounder"},
    "Harshit Rana": {"hand": "RHB", "arm": "Right", "bowling": "Pace", "role": "Pace All-Rounder"},
    "VR Iyer": {"hand": "LHB", "arm": "Right", "bowling": "Pace", "role": "Pace All-Rounder"},
    "AB Agarkar": {"hand": "RHB", "arm": "Right", "bowling": "Pace", "role": "Pace All-Rounder"},

    # Spin All-Rounders
    "RA Jadeja": {"hand": "LHB", "arm": "Left", "bowling": "Left-Arm Orthodox", "role": "Spin All-Rounder"},
    "R Ashwin": {"hand": "RHB", "arm": "Right", "bowling": "Finger Spin", "role": "Spin All-Rounder"},
    "AR Patel": {"hand": "LHB", "arm": "Left", "bowling": "Left-Arm Orthodox", "role": "Spin All-Rounder"},
    "Washington Sundar": {"hand": "LHB", "arm": "Right", "bowling": "Finger Spin", "role": "Spin All-Rounder"},
    "KH Pandya": {"hand": "LHB", "arm": "Left", "bowling": "Left-Arm Orthodox", "role": "Spin All-Rounder"},
    "DJ Hooda": {"hand": "RHB", "arm": "Right", "bowling": "Finger Spin", "role": "Spin All-Rounder"},
    "YK Pathan": {"hand": "RHB", "arm": "Right", "bowling": "Finger Spin", "role": "Spin All-Rounder"},
    "Shahbaz Ahmed": {"hand": "LHB", "arm": "Left", "bowling": "Left-Arm Orthodox", "role": "Spin All-Rounder"},
    "J Yadav": {"hand": "RHB", "arm": "Right", "bowling": "Finger Spin", "role": "Spin All-Rounder"},

    # Specialist Fast Bowlers (Right Arm)
    "JJ Bumrah": {"hand": "RHB", "arm": "Right", "bowling": "Pace", "role": "Specialist Fast Bowler"},
    "Mohammed Shami": {"hand": "RHB", "arm": "Right", "bowling": "Pace", "role": "Specialist Fast Bowler"},
    "Mohammed Siraj": {"hand": "RHB", "arm": "Right", "bowling": "Pace", "role": "Specialist Fast Bowler"},
    "B Kumar": {"hand": "RHB", "arm": "Right", "bowling": "Pace", "role": "Specialist Fast Bowler"},
    "I Sharma": {"hand": "RHB", "arm": "Right", "bowling": "Pace", "role": "Specialist Fast Bowler"},
    "UT Yadav": {"hand": "RHB", "arm": "Right", "bowling": "Pace", "role": "Specialist Fast Bowler"},
    "DL Chahar": {"hand": "RHB", "arm": "Right", "bowling": "Pace", "role": "Specialist Fast Bowler"},
    "Avesh Khan": {"hand": "RHB", "arm": "Right", "bowling": "Pace", "role": "Specialist Fast Bowler"},
    "Mukesh Kumar": {"hand": "RHB", "arm": "Right", "bowling": "Pace", "role": "Specialist Fast Bowler"},
    "Akash Deep": {"hand": "RHB", "arm": "Right", "bowling": "Pace", "role": "Specialist Fast Bowler"},
    "M Prasidh Krishna": {"hand": "RHB", "arm": "Right", "bowling": "Pace", "role": "Specialist Fast Bowler"},
    "Umran Malik": {"hand": "RHB", "arm": "Right", "bowling": "Pace", "role": "Specialist Fast Bowler"},
    "MM Patel": {"hand": "RHB", "arm": "Right", "bowling": "Pace", "role": "Specialist Fast Bowler"},
    "S Sreesanth": {"hand": "RHB", "arm": "Right", "bowling": "Pace", "role": "Specialist Fast Bowler"},
    "VR Aaron": {"hand": "RHB", "arm": "Right", "bowling": "Pace", "role": "Specialist Fast Bowler"},
    "P Kumar": {"hand": "RHB", "arm": "Right", "bowling": "Pace", "role": "Specialist Fast Bowler"},
    "DS Kulkarni": {"hand": "RHB", "arm": "Right", "bowling": "Pace", "role": "Specialist Fast Bowler"},
    "Shivam Mavi": {"hand": "RHB", "arm": "Right", "bowling": "Pace", "role": "Specialist Fast Bowler"},
    "Navdeep Saini": {"hand": "RHB", "arm": "Right", "bowling": "Pace", "role": "Specialist Fast Bowler"},
    "A Kamboj": {"hand": "RHB", "arm": "Right", "bowling": "Pace", "role": "Specialist Fast Bowler"},
    "Mayank Yadav": {"hand": "RHB", "arm": "Right", "bowling": "Pace", "role": "Specialist Fast Bowler"},

    # Specialist Fast Bowlers (Left Arm)
    "Z Khan": {"hand": "RHB", "arm": "Left", "bowling": "Left-Arm Fast", "role": "Specialist Fast Bowler"},
    "Arshdeep Singh": {"hand": "LHB", "arm": "Left", "bowling": "Left-Arm Fast", "role": "Specialist Fast Bowler"},
    "A Nehra": {"hand": "RHB", "arm": "Left", "bowling": "Left-Arm Fast", "role": "Specialist Fast Bowler"},
    "KK Ahmed": {"hand": "RHB", "arm": "Left", "bowling": "Left-Arm Fast", "role": "Specialist Fast Bowler"},
    "T Natarajan": {"hand": "LHB", "arm": "Left", "bowling": "Left-Arm Fast", "role": "Specialist Fast Bowler"},
    "BB Sran": {"hand": "LHB", "arm": "Left", "bowling": "Left-Arm Fast", "role": "Specialist Fast Bowler"},
    "C Sakariya": {"hand": "LHB", "arm": "Left", "bowling": "Left-Arm Fast", "role": "Specialist Fast Bowler"},
    "RP Singh": {"hand": "RHB", "arm": "Left", "bowling": "Left-Arm Fast", "role": "Specialist Fast Bowler"},
    "JD Unadkat": {"hand": "RHB", "arm": "Left", "bowling": "Left-Arm Fast", "role": "Specialist Fast Bowler"},

    # Specialist Spin Bowlers (Wrist / Mystery)
    "YS Chahal": {"hand": "RHB", "arm": "Right", "bowling": "Wrist Spin", "role": "Specialist Spin Bowler"},
    "Kuldeep Yadav": {"hand": "LHB", "arm": "Left", "bowling": "Wrist Spin", "role": "Specialist Spin Bowler"},
    "Ravi Bishnoi": {"hand": "RHB", "arm": "Right", "bowling": "Wrist Spin", "role": "Specialist Spin Bowler"},
    "CV Varun": {"hand": "RHB", "arm": "Right", "bowling": "Wrist Spin", "role": "Specialist Spin Bowler"},
    "A Kumble": {"hand": "RHB", "arm": "Right", "bowling": "Wrist Spin", "role": "Specialist Spin Bowler"},
    "A Mishra": {"hand": "RHB", "arm": "Right", "bowling": "Wrist Spin", "role": "Specialist Spin Bowler"},
    "PP Chawla": {"hand": "LHB", "arm": "Right", "bowling": "Wrist Spin", "role": "Specialist Spin Bowler"},
    "M Kartik": {"hand": "LHB", "arm": "Left", "bowling": "Left-Arm Orthodox", "role": "Specialist Spin Bowler"},
    "RD Chahar": {"hand": "RHB", "arm": "Right", "bowling": "Wrist Spin", "role": "Specialist Spin Bowler"},

    # Specialist Spin Bowlers (Finger)
    "Harbhajan Singh": {"hand": "RHB", "arm": "Right", "bowling": "Finger Spin", "role": "Specialist Spin Bowler"},
    "PP Ojha": {"hand": "LHB", "arm": "Left", "bowling": "Left-Arm Orthodox", "role": "Specialist Spin Bowler"},
}

def get_player_profile(player_name, career_runs=0, career_balls_faced=0, career_wickets=0, career_overs_bowled=0):
    """
    Returns profile dict for a player. Uses explicit dictionary if available,
    otherwise infers from empirical performance.
    """
    if player_name in PLAYER_ARCHETYPES:
        return PLAYER_ARCHETYPES[player_name]

    # Heuristic fallback based on career stats
    is_bowler = career_overs_bowled > 15
    is_batter = career_balls_faced > 50

    if is_bowler and is_batter and career_wickets >= 5 and career_runs >= 50:
        role = "Spin All-Rounder" if career_overs_bowled > 50 and (career_runs/max(1, career_wickets) > 15) else "Pace All-Rounder"
        bowling = "Finger Spin" if "Spin" in role else "Pace"
    elif is_bowler:
        role = "Specialist Fast Bowler"
        bowling = "Pace"
    else:
        role = "Middle-Order Batter"
        bowling = "None"

    return {
        "hand": "RHB",
        "arm": "Right",
        "bowling": bowling,
        "role": role
    }
