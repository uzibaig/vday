"""
Monte Carlo simulator — runs N full tournaments and aggregates probabilities.
"""

from __future__ import annotations
import random
from collections import defaultdict
from typing import Dict

from data import TEAMS
from tournament import simulate_tournament


def run_simulation(n: int = 10_000, seed: int = 42) -> Dict:
    """
    Run N tournament simulations.

    Returns probability distributions for each team at each stage.
    """
    random.seed(seed)

    counts: Dict[str, Dict[str, int]] = {
        team: {
            "champion": 0,
            "runner_up": 0,
            "third": 0,
            "fourth": 0,
            "semi_finalist": 0,
            "quarter_finalist": 0,
            "r16": 0,
            "r32": 0,
            "group_exit": 0,
        }
        for team in TEAMS
    }

    for _ in range(n):
        result = simulate_tournament()

        champion      = result["champion"]
        runner_up     = result["runner_up"]
        third         = result["third"]
        fourth        = result["fourth"]
        semis         = result["semi_finalists"]
        quarters      = result["quarter_finalists"]
        r16_teams     = result["r16"]
        r32_teams     = result["r32"]

        # All 48 teams start; track who reached what
        for team in TEAMS:
            if team == champion:
                counts[team]["champion"] += 1
            elif team == runner_up:
                counts[team]["runner_up"] += 1
            elif team == third:
                counts[team]["third"] += 1
            elif team == fourth:
                counts[team]["fourth"] += 1
            elif team in semis:
                counts[team]["semi_finalist"] += 1
            elif team in quarters:
                counts[team]["quarter_finalist"] += 1
            elif team in r16_teams:
                counts[team]["r16"] += 1
            elif team in r32_teams:
                counts[team]["r32"] += 1
            else:
                counts[team]["group_exit"] += 1

    # Convert to probabilities
    probs = {
        team: {stage: cnt / n for stage, cnt in stages.items()}
        for team, stages in counts.items()
    }

    return probs
