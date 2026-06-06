"""
2026 FIFA World Cup Prediction Model
=====================================
Factors & weights:
  Elo rating           30%
  Defensive solidity   25%
  Tournament resilience 20%
  Set piece efficiency  15%
  Squad composition     10%

Usage:
  python main.py [--sims N] [--seed S] [--single]

  --sims   number of Monte Carlo simulations (default 10000)
  --seed   random seed (default 42)
  --single run and print one detailed tournament walkthrough
"""

import argparse
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from data import GROUPS, TEAMS, WEIGHTS
from simulate import run_simulation
from tournament import simulate_tournament
from model import composite_attack, composite_defense, expected_goals


# ── Pretty-print helpers ──────────────────────────────────────────────────────

_FLAG = {
    "Spain": "🇪🇸", "Argentina": "🇦🇷", "France": "🇫🇷", "England": "🏴󠁧󠁢󠁥󠁮󠁧󠁿",
    "Brazil": "🇧🇷", "Portugal": "🇵🇹", "Germany": "🇩🇪", "Netherlands": "🇳🇱",
    "Belgium": "🇧🇪", "Croatia": "🇭🇷", "Morocco": "🇲🇦", "Colombia": "🇨🇴",
    "Uruguay": "🇺🇾", "USA": "🇺🇸", "Japan": "🇯🇵", "Mexico": "🇲🇽",
    "Switzerland": "🇨🇭", "Sweden": "🇸🇪", "South Korea": "🇰🇷", "Senegal": "🇸🇳",
    "Ecuador": "🇪🇨", "Austria": "🇦🇹", "Norway": "🇳🇴", "Iran": "🇮🇷",
    "Egypt": "🇪🇬", "Australia": "🇦🇺", "Côte d'Ivoire": "🇨🇮", "Algeria": "🇩🇿",
    "Turkey": "🇹🇷", "DR Congo": "🇨🇩", "Paraguay": "🇵🇾", "Saudi Arabia": "🇸🇦",
    "Tunisia": "🇹🇳", "South Africa": "🇿🇦", "Ghana": "🇬🇭", "Uzbekistan": "🇺🇿",
    "Czechia": "🇨🇿", "Scotland": "🏴󠁧󠁢󠁳󠁣󠁴󠁿", "Cabo Verde": "🇨🇻", "Canada": "🇨🇦",
    "New Zealand": "🇳🇿", "Jordan": "🇯🇴", "Iraq": "🇮🇶",
    "Bosnia and Herzegovina": "🇧🇦", "Haiti": "🇭🇹", "Qatar": "🇶🇦",
    "Panama": "🇵🇦", "Curaçao": "🇨🇼",
}


def flag(team: str) -> str:
    return _FLAG.get(team, "🏳️")


def bar(p: float, width: int = 20) -> str:
    filled = round(p * width)
    return "█" * filled + "░" * (width - filled)


def pct(p: float) -> str:
    return f"{p*100:5.1f}%"


def print_title_block():
    print()
    print("╔══════════════════════════════════════════════════════════════╗")
    print("║       2026 FIFA WORLD CUP — PREDICTIVE MODEL RESULTS        ║")
    print("╠══════════════════════════════════════════════════════════════╣")
    print("║  Factor weights                                              ║")
    print(f"║    Elo rating           {WEIGHTS['elo']*100:.0f}%                                  ║")
    print(f"║    Defensive solidity   {WEIGHTS['defense']*100:.0f}%                                  ║")
    print(f"║    Tournament resilience {WEIGHTS['resilience']*100:.0f}%                                 ║")
    print(f"║    Set piece efficiency  {WEIGHTS['set_piece']*100:.0f}%                                 ║")
    print(f"║    Squad composition    {WEIGHTS['squad']*100:.0f}%                                  ║")
    print("╚══════════════════════════════════════════════════════════════╝")
    print()


def print_team_ratings():
    print("━" * 72)
    print("COMPOSITE TEAM RATINGS  (attack / defense, 0-100 scale)")
    print("━" * 72)
    print(f"{'Team':<28} {'ATK':>5} {'DEF':>5} {'Elo':>5}")
    print("─" * 72)
    ranked = sorted(TEAMS.keys(), key=lambda t: -(composite_attack(t) + composite_defense(t)) / 2)
    for team in ranked:
        atk = composite_attack(team)
        dfn = composite_defense(team)
        elo = TEAMS[team]["elo"]
        name = f"{flag(team)} {team}"
        print(f"{name:<28} {atk:5.1f} {dfn:5.1f} {elo:5d}")
    print()


def print_group_strength():
    print("━" * 72)
    print("GROUP STRENGTH OVERVIEW")
    print("━" * 72)
    print(f"{'Group':<6} {'Teams':<52} {'Avg Elo':>7}")
    print("─" * 72)
    for g, teams in GROUPS.items():
        avg_elo = sum(TEAMS[t]["elo"] for t in teams) / len(teams)
        team_str = ", ".join(f"{flag(t)}{t}" for t in teams)
        print(f"  {g}    {team_str:<52} {avg_elo:>7.0f}")
    print()


def print_monte_carlo_results(probs: dict, top_n: int = 20):
    print("━" * 72)
    print("MONTE CARLO RESULTS  (10,000 simulations)")
    print("━" * 72)

    # ── Championship probabilities ──
    print("\n  CHAMPION PROBABILITIES — Top 20")
    print(f"  {'Team':<26} {'Win%':>6}  {'Bar'}")
    print("  " + "─" * 60)
    ranked = sorted(probs.keys(), key=lambda t: -probs[t]["champion"])
    for team in ranked[:top_n]:
        p = probs[team]["champion"]
        if p < 0.0005:
            continue
        name = f"{flag(team)} {team}"
        print(f"  {name:<26} {pct(p)}  {bar(p, 25)}")

    # ── Final probabilities ──
    print("\n  FINALIST PROBABILITIES — Top 16")
    print(f"  {'Team':<26} {'Final%':>7}  {'Semi%':>7}  {'QF%':>7}")
    print("  " + "─" * 60)
    ranked_final = sorted(
        probs.keys(),
        key=lambda t: -(probs[t]["champion"] + probs[t]["runner_up"]),
    )
    for team in ranked_final[:16]:
        p_final = probs[team]["champion"] + probs[team]["runner_up"]
        p_semi  = p_final + probs[team]["semi_finalist"]
        p_qf    = p_semi + probs[team]["quarter_finalist"]
        name = f"{flag(team)} {team}"
        print(f"  {name:<26} {pct(p_final)}  {pct(p_semi)}  {pct(p_qf)}")

    # ── Group stage qualification odds per group ──
    print("\n  GROUP STAGE QUALIFICATION ODDS (P reaching R32)")
    print(f"  {'Team':<26} {'Qual%':>6}  {'Bar'}")
    print("  " + "─" * 60)
    for g, teams in GROUPS.items():
        print(f"\n  ── Group {g} ──")
        for team in sorted(teams, key=lambda t: -probs[t]["group_exit"]):
            p_qual = 1 - probs[team]["group_exit"]
            name = f"{flag(team)} {team}"
            print(f"  {name:<26} {pct(p_qual)}  {bar(p_qual, 20)}")

    print()


def print_single_run():
    print("━" * 72)
    print("SINGLE TOURNAMENT SIMULATION  (deterministic seed=1)")
    print("━" * 72)
    import random
    random.seed(1)
    simulate_tournament(verbose=True)
    print()


def print_expected_goals_preview():
    """Show expected goals for a few marquee matchups."""
    print("━" * 72)
    print("EXPECTED GOALS — MARQUEE GROUP MATCHUPS")
    print("━" * 72)
    matchups = [
        ("Spain", "Uruguay"),
        ("France", "Senegal"),
        ("Argentina", "Austria"),
        ("England", "Croatia"),
        ("Brazil", "Morocco"),
        ("Germany", "Ecuador"),
        ("Portugal", "Colombia"),
        ("Netherlands", "Japan"),
    ]
    print(f"  {'Match':<40} {'xG A':>5}  {'xG B':>5}")
    print("  " + "─" * 55)
    for a, b in matchups:
        la, lb = expected_goals(a, b)
        print(f"  {flag(a)} {a:<18} vs {flag(b)} {b:<15} {la:5.2f}  {lb:5.2f}")
    print()


def main():
    parser = argparse.ArgumentParser(description="2026 World Cup Prediction Model")
    parser.add_argument("--sims", type=int, default=10_000)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--single", action="store_true", help="Run one verbose simulation")
    args = parser.parse_args()

    print_title_block()
    print_team_ratings()
    print_group_strength()
    print_expected_goals_preview()

    if args.single:
        print_single_run()
        return

    print(f"Running {args.sims:,} Monte Carlo simulations (seed={args.seed})...")
    probs = run_simulation(n=args.sims, seed=args.seed)
    print_monte_carlo_results(probs)


if __name__ == "__main__":
    main()
