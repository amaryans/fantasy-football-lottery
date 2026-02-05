import random
from collections import defaultdict, Counter

# ---------- Helpers ----------

def pair_key(a, b):
    return tuple(sorted((a, b)))

def round_robin_weeks(teams):
    """
    Circle method for single round robin.
    For even n, returns n-1 weeks. Each week is a list of (team1, team2) pairs.
    """
    n = len(teams)
    assert n % 2 == 0, "Number of teams must be even."
    arr = teams[:]
    fixed = arr[0]
    rot = arr[1:]
    weeks = []
    for _ in range(n - 1):
        pairings = []
        left = [fixed] + rot[: (n // 2 - 1)]
        right = rot[(n // 2 - 1):][::-1]
        for a, b in zip(left, right):
            pairings.append((a, b))
        weeks.append(pairings)
        rot = [rot[-1]] + rot[:-1]
    return weeks

def find_perfect_matching(teams, allowed_pairs, banned_pairs=None):
    """
    Backtracking perfect matching finder.
    - teams: list of team names (even count)
    - allowed_pairs: iterable of 2-tuples or frozensets {a,b} allowed this week
    - banned_pairs: iterable of pairs to exclude (optional)
    Returns list of (a,b) pairs covering all teams exactly once, or None.
    """
    # Normalize to sorted tuple keys
    allowed = set(tuple(sorted(p)) for p in allowed_pairs)
    banned = set(tuple(sorted(p)) for p in (banned_pairs or set()))
    allowed -= banned

    adj = defaultdict(list)
    T = set(teams)
    for a in teams:
        for b in teams:
            if a == b:
                continue
            k = pair_key(a, b)
            if k in allowed:
                adj[a].append(b)

    used_pairs = set()

    # Heuristic: pick the team with fewest options next
    def backtrack(remaining, chosen):
        if not remaining:
            return chosen
        t = min(remaining, key=lambda x: sum(1 for y in adj[x] if y in remaining))
        for opp in list(adj[t]):
            if opp not in remaining:
                continue
            k = pair_key(t, opp)
            if k not in allowed or k in used_pairs:
                continue
            used_pairs.add(k)
            nxt = remaining - {t, opp}
            res = backtrack(nxt, chosen + [(t, opp)])
            if res is not None:
                return res
            used_pairs.remove(k)
        return None

    return backtrack(set(teams), [])

# ---------- Main builder ----------

def build_schedule(divisions, rivals, seed=None):
    """
    Build a 14-week schedule for 12 teams (3 divisions x 4).
    Rules implemented:
      - Weeks 1-11: every team plays every other team once (single round robin).
      - Week 12: rivalry rematches (each rival pair plays twice total).
      - Weeks 13-14: two additional perfect matchings from NON-rival pairs
                     so each team gets exactly two more distinct opponents.
    Guarantees:
      - Each team plays exactly once per week.
      - Each team has exactly 14 games total.
      - Rival pairs occur exactly twice; no pair occurs more than twice.
    """
    if seed is not None:
        random.seed(seed)

    # Teams list
    teams = [t for div in divisions.values() for t in div]
    if len(teams) != 12:
        raise ValueError("This script assumes exactly 12 teams (3 divisions x 4).")

    # 1) Base single round robin (11 weeks)
    base_weeks = round_robin_weeks(teams)

    # 2) Rivalry week (Week 12)
    # Normalize and ensure exactly 6 distinct pairs
    uniq_rival_pairs = set(tuple(sorted((t, r))) for t, r in rivals.items() if t < r)
    if len(uniq_rival_pairs) != 6:
        raise ValueError("Rivals mapping must contain 6 distinct two-way pairs (each pair listed both directions).")
    rivalry_week = list(uniq_rival_pairs)  # 6 games

    # 3) Two more weeks from non-rival pairs via perfect matchings
    all_pairs = set(pair_key(a, b) for i, a in enumerate(teams) for b in teams[i + 1:])
    non_rival_pairs = all_pairs - uniq_rival_pairs

    # Pick two disjoint perfect matchings so each team gets two different extra opponents
    extra_week_1 = find_perfect_matching(teams, non_rival_pairs)
    if extra_week_1 is None:
        raise RuntimeError("Failed to find first extra perfect matching.")

    used_pairs = set(pair_key(a, b) for a, b in extra_week_1)
    extra_week_2 = find_perfect_matching(teams, non_rival_pairs - used_pairs)
    if extra_week_2 is None:
        raise RuntimeError("Failed to find second extra perfect matching.")

    # 4) Combine all 14 weeks
    weeks = []
    weeks.extend(base_weeks)             # Weeks 1..11
    weeks.append(rivalry_week)           # Week 12
    weeks.append(extra_week_1)           # Week 13
    weeks.append(extra_week_2)           # Week 14

    # ---------- Validation ----------
    # a) Weekly uniqueness
    for i, games in enumerate(weeks, start=1):
        seen = set()
        for a, b in games:
            if a in seen or b in seen:
                raise AssertionError(f"Team scheduled twice in Week {i}: {a} or {b}")
            seen.add(a); seen.add(b)
        if len(seen) != len(teams):
            raise AssertionError(f"Incomplete Week {i}: not all teams scheduled.")

    # b) Pair counts
    from collections import Counter
    pair_counts = Counter()
    for games in weeks:
        for a, b in games:
            pair_counts[pair_key(a, b)] += 1

    for p in uniq_rival_pairs:
        if pair_counts[p] != 2:
            raise AssertionError(f"Rival pair {p} does not meet exactly twice.")

    for p, c in pair_counts.items():
        if p not in uniq_rival_pairs and c not in (1, 2):
            raise AssertionError(f"Non-rival pair {p} occurs {c} times (allowed: 1 or 2).")

    # c) Team totals
    team_counts = Counter()
    for games in weeks:
        for a, b in games:
            team_counts[a] += 1
            team_counts[b] += 1
    for t in teams:
        if team_counts[t] != 14:
            raise AssertionError(f"{t} has {team_counts[t]} games (expected 14).")

    return weeks

if __name__ == "__main__":
    divisions = {
        "Division A": ["Austin", "Sam", "Logan", "Dom"],
        "Division B": ["Owen", "Jakeb", "Gus", "TCoop"],
        "Division C": ["Batches", "Addi", "Beans", "Carson"],
    }

    # Define rivals explicitly
    rivals = {
        "Austin": "Logan",
        "Sam": "Dom",
        "Logan": "Austin",
        "Dom": "Sam",
        "Owen": "Gus",
        "Gus": "Owen",
        "Jakeb": "TCoop",
        "TCoop": "Jakeb",
        "Beans": "Batches",
        "Batches": "Beans",
        "Addi": "Carson",
        "Carson": "Addi",
    }

    weeks = build_schedule(divisions, rivals)
    print(weeks)
    # Print week-by-week schedule
    for i, games in enumerate(weeks, start=1):
        print(f"Week {i}:")
        for g in games:
            print(f"  {g[0]} vs {g[1]}")
        print()
