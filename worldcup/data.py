"""
Team database for 2026 FIFA World Cup.

Factor ratings are on a 0-100 scale.
Elo ratings are actual World Football Elo values (eloratings.net, June 2026).

Rating dimensions:
  elo          - World Football Elo rating (raw, ~1670-2155 range)
  def_rating   - Defensive solidity + GK quality (0-100)
  resilience   - Clutch/knockout performance, penalty record (0-100)
  sp_att       - Set piece attack threat (0-100)
  sp_def       - Set piece defensive organisation (0-100)
  squad_score  - Age profile in 25-29 peak band + positional depth (0-100)
"""

# 2026 World Cup groups (draw: 5 Dec 2025, Kennedy Center, Washington D.C.)
GROUPS = {
    "A": ["Mexico", "South Africa", "South Korea", "Czechia"],
    "B": ["Canada", "Bosnia and Herzegovina", "Qatar", "Switzerland"],
    "C": ["Brazil", "Morocco", "Haiti", "Scotland"],
    "D": ["USA", "Paraguay", "Australia", "Turkey"],
    "E": ["Germany", "Curaçao", "Côte d'Ivoire", "Ecuador"],
    "F": ["Netherlands", "Japan", "Sweden", "Tunisia"],
    "G": ["Belgium", "Egypt", "Iran", "New Zealand"],
    "H": ["Spain", "Cabo Verde", "Saudi Arabia", "Uruguay"],
    "I": ["France", "Senegal", "Iraq", "Norway"],
    "J": ["Argentina", "Algeria", "Austria", "Jordan"],
    "K": ["Portugal", "DR Congo", "Uzbekistan", "Colombia"],
    "L": ["England", "Croatia", "Ghana", "Panama"],
}

# fmt: off
TEAMS = {
    # ── TIER 1 ── Contenders
    "Spain": {
        "elo": 2155, "def_rating": 88, "resilience": 85,
        "sp_att": 82, "sp_def": 85, "squad_score": 92,
    },
    "Argentina": {
        "elo": 2113, "def_rating": 80, "resilience": 97,  # 2022 champion, penalty kings
        "sp_att": 80, "sp_def": 78, "squad_score": 85,
    },
    "France": {
        "elo": 2062, "def_rating": 82, "resilience": 88,
        "sp_att": 85, "sp_def": 83, "squad_score": 95,
    },
    "England": {
        "elo": 2020, "def_rating": 80, "resilience": 70,  # penalty shootout history
        "sp_att": 88, "sp_def": 82, "squad_score": 90,
    },
    "Brazil": {
        "elo": 1988, "def_rating": 78, "resilience": 75,
        "sp_att": 78, "sp_def": 80, "squad_score": 88,
    },
    "Portugal": {
        "elo": 1984, "def_rating": 78, "resilience": 78,
        "sp_att": 82, "sp_def": 80, "squad_score": 82,
    },
    "Germany": {
        "elo": 1975, "def_rating": 80, "resilience": 82,
        "sp_att": 80, "sp_def": 82, "squad_score": 85,
    },

    # ── TIER 2 ── Dark horses
    "Netherlands": {
        "elo": 1945, "def_rating": 76, "resilience": 72,
        "sp_att": 80, "sp_def": 78, "squad_score": 83,
    },
    "Belgium": {
        "elo": 1930, "def_rating": 74, "resilience": 70,
        "sp_att": 76, "sp_def": 75, "squad_score": 78,
    },
    "Croatia": {
        "elo": 1920, "def_rating": 78, "resilience": 88,  # 2018 finalist, 2022 3rd
        "sp_att": 72, "sp_def": 78, "squad_score": 72,
    },
    "Morocco": {
        "elo": 1900, "def_rating": 85, "resilience": 82,  # 2022 semi-finalists, elite defence
        "sp_att": 68, "sp_def": 85, "squad_score": 80,
    },
    "Colombia": {
        "elo": 1895, "def_rating": 72, "resilience": 70,
        "sp_att": 70, "sp_def": 70, "squad_score": 78,
    },
    "Uruguay": {
        "elo": 1890, "def_rating": 76, "resilience": 78,
        "sp_att": 68, "sp_def": 75, "squad_score": 72,
    },

    # ── TIER 3 ── Solid mid-tier
    "USA": {
        "elo": 1875, "def_rating": 70, "resilience": 68,
        "sp_att": 68, "sp_def": 70, "squad_score": 75,
    },
    "Japan": {
        "elo": 1870, "def_rating": 74, "resilience": 72,
        "sp_att": 62, "sp_def": 74, "squad_score": 78,
    },
    "Mexico": {
        "elo": 1860, "def_rating": 68, "resilience": 66,
        "sp_att": 65, "sp_def": 68, "squad_score": 70,
    },
    "Switzerland": {
        "elo": 1855, "def_rating": 74, "resilience": 75,
        "sp_att": 65, "sp_def": 74, "squad_score": 72,
    },
    "Sweden": {
        "elo": 1850, "def_rating": 72, "resilience": 68,
        "sp_att": 70, "sp_def": 72, "squad_score": 70,
    },
    "South Korea": {
        "elo": 1845, "def_rating": 68, "resilience": 70,
        "sp_att": 62, "sp_def": 68, "squad_score": 72,
    },
    "Senegal": {
        "elo": 1840, "def_rating": 72, "resilience": 70,
        "sp_att": 65, "sp_def": 70, "squad_score": 75,
    },
    "Ecuador": {
        "elo": 1835, "def_rating": 76, "resilience": 66,  # 13 clean sheets in CONMEBOL qualifying
        "sp_att": 62, "sp_def": 74, "squad_score": 68,
    },
    "Austria": {
        "elo": 1830, "def_rating": 70, "resilience": 65,
        "sp_att": 65, "sp_def": 70, "squad_score": 72,
    },
    "Norway": {
        "elo": 1825, "def_rating": 68, "resilience": 65,
        "sp_att": 72, "sp_def": 68, "squad_score": 75,  # Haaland aerial threat
    },
    "Iran": {
        "elo": 1815, "def_rating": 72, "resilience": 68,
        "sp_att": 60, "sp_def": 72, "squad_score": 65,
    },
    "Egypt": {
        "elo": 1810, "def_rating": 70, "resilience": 68,
        "sp_att": 65, "sp_def": 70, "squad_score": 68,
    },
    "Australia": {
        "elo": 1805, "def_rating": 66, "resilience": 70,
        "sp_att": 60, "sp_def": 66, "squad_score": 68,
    },
    "Côte d'Ivoire": {
        "elo": 1800, "def_rating": 65, "resilience": 65,
        "sp_att": 62, "sp_def": 65, "squad_score": 70,
    },
    "Algeria": {
        "elo": 1800, "def_rating": 66, "resilience": 65,
        "sp_att": 60, "sp_def": 66, "squad_score": 68,
    },
    "Turkey": {
        "elo": 1795, "def_rating": 64, "resilience": 65,
        "sp_att": 63, "sp_def": 64, "squad_score": 68,
    },
    "DR Congo": {
        "elo": 1785, "def_rating": 64, "resilience": 62,
        "sp_att": 60, "sp_def": 62, "squad_score": 65,
    },
    "Paraguay": {
        "elo": 1780, "def_rating": 65, "resilience": 64,
        "sp_att": 58, "sp_def": 65, "squad_score": 64,
    },
    "Saudi Arabia": {
        "elo": 1775, "def_rating": 62, "resilience": 65,  # 2022 upset vs Argentina
        "sp_att": 58, "sp_def": 62, "squad_score": 63,
    },
    "Tunisia": {
        "elo": 1770, "def_rating": 66, "resilience": 62,
        "sp_att": 58, "sp_def": 65, "squad_score": 64,
    },
    "South Africa": {
        "elo": 1765, "def_rating": 63, "resilience": 60,
        "sp_att": 58, "sp_def": 63, "squad_score": 62,
    },
    "Ghana": {
        "elo": 1760, "def_rating": 60, "resilience": 62,
        "sp_att": 60, "sp_def": 60, "squad_score": 65,
    },
    "Uzbekistan": {
        "elo": 1755, "def_rating": 62, "resilience": 60,
        "sp_att": 55, "sp_def": 62, "squad_score": 62,
    },
    "Czechia": {
        "elo": 1750, "def_rating": 64, "resilience": 62,
        "sp_att": 62, "sp_def": 63, "squad_score": 65,
    },
    "Scotland": {
        "elo": 1745, "def_rating": 63, "resilience": 60,
        "sp_att": 65, "sp_def": 63, "squad_score": 65,
    },
    "Cabo Verde": {
        "elo": 1740, "def_rating": 62, "resilience": 60,
        "sp_att": 55, "sp_def": 60, "squad_score": 60,
    },
    "Canada": {
        "elo": 1735, "def_rating": 64, "resilience": 62,
        "sp_att": 60, "sp_def": 63, "squad_score": 68,
    },
    "New Zealand": {
        "elo": 1730, "def_rating": 58, "resilience": 58,
        "sp_att": 52, "sp_def": 58, "squad_score": 58,
    },
    "Jordan": {
        "elo": 1725, "def_rating": 60, "resilience": 58,
        "sp_att": 52, "sp_def": 60, "squad_score": 58,
    },
    "Iraq": {
        "elo": 1720, "def_rating": 58, "resilience": 58,
        "sp_att": 52, "sp_def": 58, "squad_score": 58,
    },
    "Bosnia and Herzegovina": {
        "elo": 1700, "def_rating": 58, "resilience": 56,
        "sp_att": 60, "sp_def": 58, "squad_score": 60,
    },
    "Haiti": {
        "elo": 1710, "def_rating": 55, "resilience": 55,
        "sp_att": 50, "sp_def": 55, "squad_score": 55,
    },
    "Qatar": {
        "elo": 1695, "def_rating": 55, "resilience": 54,
        "sp_att": 50, "sp_def": 55, "squad_score": 56,
    },
    "Panama": {
        "elo": 1690, "def_rating": 58, "resilience": 56,
        "sp_att": 50, "sp_def": 58, "squad_score": 58,
    },
    "Curaçao": {
        "elo": 1670, "def_rating": 50, "resilience": 50,
        "sp_att": 45, "sp_def": 50, "squad_score": 52,
    },
}
# fmt: on

# Factor weights (user-specified)
WEIGHTS = {
    "elo":        0.30,
    "defense":    0.25,
    "resilience": 0.20,
    "set_piece":  0.15,
    "squad":      0.10,
}

# Tournament constants
BASE_GOALS_PER_TEAM = 1.30   # avg WC goals per team per 90-min match
ELO_SCALE = 400              # Elo scale factor (logistic)
SHOOTOUT_BASE_WIN = 0.50     # equal-resilience teams split 50/50
