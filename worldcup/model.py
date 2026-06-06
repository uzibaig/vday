"""
Match prediction engine.

Combines the five weighted factors into per-team expected-goals (λ),
then draws from Poisson to simulate scorelines.

Factor weights (per user spec):
  Elo            30%
  Defensive      25%
  Resilience     20%
  Set Pieces     15%
  Squad          10%
"""

import math
import random
from typing import Tuple

from data import TEAMS, WEIGHTS, BASE_GOALS_PER_TEAM, ELO_SCALE, SHOOTOUT_BASE_WIN

# ── Elo range for normalisation (min/max across all 48 teams)
_ELO_MIN = min(t["elo"] for t in TEAMS.values())
_ELO_MAX = max(t["elo"] for t in TEAMS.values())


def _norm_elo(elo: float) -> float:
    """Normalise raw Elo to [0, 100]."""
    return (elo - _ELO_MIN) / (_ELO_MAX - _ELO_MIN) * 100


def composite_attack(team: str) -> float:
    """
    Weighted composite attack strength (0-100).

    Elo (30%) + weighted average of attack-side factor ratings.
    Set pieces and resilience contribute to goal-scoring ability;
    squad depth sustains quality across 7 matches.
    """
    t = TEAMS[team]
    elo_score = _norm_elo(t["elo"])
    # For attack: use sp_att and resilience (clutch scoring), squad
    # def_rating not directly relevant on attack side — omit
    score = (
        WEIGHTS["elo"]        * elo_score
        + WEIGHTS["defense"]  * elo_score        # Elo still proxies attack quality
        + WEIGHTS["resilience"] * t["resilience"]
        + WEIGHTS["set_piece"] * t["sp_att"]
        + WEIGHTS["squad"]    * t["squad_score"]
    )
    return score


def composite_defense(team: str) -> float:
    """
    Weighted composite defensive strength (0-100).

    Elo (30%) + defensive solidity + resilience (holding leads) +
    set piece defence + squad depth.
    """
    t = TEAMS[team]
    elo_score = _norm_elo(t["elo"])
    score = (
        WEIGHTS["elo"]          * elo_score
        + WEIGHTS["defense"]    * t["def_rating"]
        + WEIGHTS["resilience"] * t["resilience"]
        + WEIGHTS["set_piece"]  * t["sp_def"]
        + WEIGHTS["squad"]      * t["squad_score"]
    )
    return score


# Pre-compute composites once for speed
_ATK = {team: composite_attack(team) for team in TEAMS}
_DEF = {team: composite_defense(team) for team in TEAMS}


def expected_goals(team_a: str, team_b: str) -> Tuple[float, float]:
    """
    Poisson λ for (team_a, team_b) in a neutral-site match.

    Formula:
        λ_a = BASE * (ATK_a / 50) * (50 / DEF_b) * elo_boost_a
        λ_b = BASE * (ATK_b / 50) * (50 / DEF_a) * elo_boost_b

    The Elo boost applies a logistic correction so strong Elo gaps
    shift λ beyond what pure factor ratings alone capture.
    """
    elo_diff_a = TEAMS[team_a]["elo"] - TEAMS[team_b]["elo"]

    # Elo win-probability logistic
    p_a = 1 / (1 + 10 ** (-elo_diff_a / ELO_SCALE))

    # Map win-prob to goal multiplier: p=0.5 → ×1.0, p=0.75 → ×1.3
    elo_mult_a = (p_a / 0.5) ** 0.5
    elo_mult_b = ((1 - p_a) / 0.5) ** 0.5

    lam_a = BASE_GOALS_PER_TEAM * (_ATK[team_a] / 50) * (50 / _DEF[team_b]) * elo_mult_a
    lam_b = BASE_GOALS_PER_TEAM * (_ATK[team_b] / 50) * (50 / _DEF[team_a]) * elo_mult_b

    # Clamp to sensible range
    lam_a = max(0.2, min(lam_a, 5.0))
    lam_b = max(0.2, min(lam_b, 5.0))

    return lam_a, lam_b


def _poisson_draw(lam: float) -> int:
    """Generate a Poisson-distributed integer (Knuth algorithm)."""
    L = math.exp(-lam)
    k, p = 0, 1.0
    while p > L:
        k += 1
        p *= random.random()
    return k - 1


def simulate_match(
    team_a: str,
    team_b: str,
    allow_draw: bool = True,
) -> Tuple[str, int, int]:
    """
    Simulate one match. Returns (winner_or_draw, goals_a, goals_b).

    If allow_draw=False (knockout), goes to extra-time / penalties
    when scores are level after 90 min.
    """
    lam_a, lam_b = expected_goals(team_a, team_b)
    goals_a = _poisson_draw(lam_a)
    goals_b = _poisson_draw(lam_b)

    if goals_a > goals_b:
        return team_a, goals_a, goals_b
    elif goals_b > goals_a:
        return team_b, goals_a, goals_b
    else:
        if allow_draw:
            return "draw", goals_a, goals_b
        else:
            return _extra_time_and_penalties(team_a, team_b, goals_a, goals_b)


def _extra_time_and_penalties(
    team_a: str, team_b: str, goals_a: int, goals_b: int
) -> Tuple[str, int, int]:
    """
    Extra time: small chance of a goal from either side.
    Penalties: resilience-weighted shootout probability.
    """
    # Extra time — reduced goal rate (~30% of 90-min rate over 30 min)
    lam_a, lam_b = expected_goals(team_a, team_b)
    et_a = _poisson_draw(lam_a * 0.3)
    et_b = _poisson_draw(lam_b * 0.3)

    if et_a > et_b:
        return team_a, goals_a + et_a, goals_b + et_b
    elif et_b > et_a:
        return team_b, goals_a + et_a, goals_b + et_b
    else:
        # Penalty shootout — resilience determines P(win)
        res_a = TEAMS[team_a]["resilience"]
        res_b = TEAMS[team_b]["resilience"]
        p_a_wins = res_a / (res_a + res_b)
        winner = team_a if random.random() < p_a_wins else team_b
        return winner, goals_a + et_a, goals_b + et_b
