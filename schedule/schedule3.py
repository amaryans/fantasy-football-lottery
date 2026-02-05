import random
import csv
from collections import Counter, defaultdict

def pair_key(a, b):
    return tuple(sorted((a, b)))

def round_robin_weeks(teams):
    """Circle method: returns n-1 weeks of perfect matchings."""
    n = len(teams)
    assert n % 2 == 0, "Even number of teams required."
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

def build_pod_priority(divisions):
    """
    Returns a dict of set of preferred partners for each team:
    same 'rank' across different divisions (A1-B1-C1, etc.).
    """
    div_names = list(divisions.keys())
    rank_pods = []
    for r in range(4):
        rank_pods.append([divisions[d][r] for d in div_names])
    pod_pref = defaultdict(set)
    for pod in rank_pods:
        for i in range(len(pod)):
            for j in range(len(pod)):
                if i != j:
                    pod_pref[pod[i]].add(pod[j])
    return pod_pref

def perfect_matching_with_priority(teams, allowed_pairs, prefer_pairs):
    """
    Backtracking perfect matching:
    - teams: list of teams (even)
    - allowed_pairs: set of undirected pairs (sorted tuples) allowed this week
    - prefer_pairs: set of pairs to try first (subset of allowed_pairs)
    Returns: list of (a,b) covering all teams exactly once, or None.
    """
    allowed = set(tuple(sorted(p)) for p in allowed_pairs)
    prefer = [p for p in prefer_pairs if p in allowed]
    others = [p for p in allowed if p not in prefer]

    # Build adjacency keyed by team, with priority ordering
    adj = defaultdict(list)
    for a, b in prefer + others:
        adj[a].append(b)
        adj[b].append(a)

    used = set()

    def backtrack(unmatched, chosen):
        if not unmatched:
            return chosen
        # pick the node with fewest options (heuristic)
        t = min(unmatched, key=lambda x: sum(1 for y in adj[x] if y in unmatched))
        # Try preferred neighbors first by ordering adj list:
        neighs = [y for y in adj[t] if y in unmatched]
        # Sort: preferred edges first (by membership in prefer set)
        neighs.sort(key=lambda y: (pair_key(t, y) not in prefer))
        for y in neighs:
            k = pair_key(t, y)
            if k in used or k not in allowed:
                continue
            used.add(k)
            res = backtrack(unmatched - {t, y}, chosen + [(t, y)])
            if res is not None:
                return res
            used.remove(k)
        return None

    return backtrack(set(teams), [])

def build_schedule(divisions, rivals, seed=None):
    """
    12 teams (3x4). Output 14 weeks with validations:
      - W1-11: round robin
      - W12: rivalry rematches
      - W13-14: perfect matchings from remaining capacity,
                preferring same-rank cross-division ("pod") pairs.
      - No team plays twice in a week. Total 14 per team.
      - Rival pairs appear exactly twice total.
      - Any pair appears at most twice.
    """
    if seed is not None:
        random.seed(seed)

    # Teams list
    teams = [t for div in divisions.values() for t in div]
    if len(teams) != 12:
        raise ValueError("Expected exactly 12 teams (3 divisions × 4).")

    # Weeks 1-11: single round-robin
    base_weeks = round_robin_weeks(teams)

    # Week 12: rivalry week (validate 6 2-way pairs)
    uniq_rival_pairs = set(pair_key(t, r) for t, r in rivals.items() if t < r)
    if len(uniq_rival_pairs) != 6:
        raise ValueError("Rivals mapping must contain 6 distinct two-way pairs.")
    rivalry_week = list(uniq_rival_pairs)

    # Count pair usages and team game counts after first 12 weeks
    pair_counts = Counter()
    team_counts = Counter()
    for wk in base_weeks + [rivalry_week]:
        for a, b in wk:
            k = pair_key(a, b)
            pair_counts[k] += 1
            team_counts[a] += 1
            team_counts[b] += 1

    # Build pod preference map (prefer same-rank, cross-division)
    pod_pref = build_pod_priority(divisions)
    # Prefer set for week construction turns into specific pairs per team
    def preferred_pairs_set():
        pref = set()
        for a in teams:
            for b in pod_pref[a]:
                pref.add(pair_key(a, b))
        return pref

    # Allowed pairs for extra weeks: capacity < 2 and not a rival pair (rivals already at 2)
    all_pairs = set(pair_key(a, b) for i, a in enumerate(teams) for b in teams[i+1:])
    non_rival_pairs = all_pairs - uniq_rival_pairs

    def allowed_pairs_now():
        return {p for p in non_rival_pairs if pair_counts[p] < 2}

    # Week 13: perfect matching (prioritize pods)
    w13_allowed = allowed_pairs_now()
    if len(w13_allowed) < 6:
        raise RuntimeError("Not enough allowed pairs to build Week 13.")
    w13_pref = preferred_pairs_set() & w13_allowed
    week13 = perfect_matching_with_priority(teams, w13_allowed, w13_pref)
    if week13 is None:
        raise RuntimeError("Failed to find a valid perfect matching for Week 13.")
    for a, b in week13:
        k = pair_key(a, b)
        pair_counts[k] += 1
        team_counts[a] += 1
        team_counts[b] += 1

    # Week 14: recompute allowed (capacity left), again prefer pods
    w14_allowed = allowed_pairs_now()
    if len(w14_allowed) < 6:
        raise RuntimeError("Not enough allowed pairs to build Week 14.")
    w14_pref = preferred_pairs_set() & w14_allowed
    week14 = perfect_matching_with_priority(teams, w14_allowed, w14_pref)
    if week14 is None:
        raise RuntimeError("Failed to find a valid perfect matching for Week 14.")
    for a, b in week14:
        k = pair_key(a, b)
        pair_counts[k] += 1
        team_counts[a] += 1
        team_counts[b] += 1

    # Combine weeks
    weeks = base_weeks + [rivalry_week, week13, week14]

    # ---------- Validations ----------
    # (1) No team twice in any week, and full coverage
    for i, games in enumerate(weeks, start=1):
        seen = set()
        for a, b in games:
            if a in seen or b in seen:
                raise AssertionError(f"Team double-booked in Week {i}.")
            seen.add(a); seen.add(b)
        if len(seen) != len(teams):
            raise AssertionError(f"Incomplete Week {i}.")

    # (2) Exactly 14 games per team
    for t in teams:
        if team_counts[t] != 14:
            raise AssertionError(f"{t} has {team_counts[t]} games (expected 14).")

    # (3) Rival pairs exactly twice; any pair ≤ 2
    for p in uniq_rival_pairs:
        if pair_counts[p] != 2:
            raise AssertionError(f"Rival pair {p} does not occur exactly twice.")
    for p, c in pair_counts.items():
        if c > 2:
            raise AssertionError(f"Pair {p} occurs {c} times (>2).")

    return weeks
def export_schedule_csv(weeks, teams, filename="schedule.csv"):
    """Export schedule as CSV with teams as columns, weeks as rows."""
    with open(filename, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Week"] + teams)
        for i, games in enumerate(weeks, start=1):
            row = ["Week " + str(i)]
            matchups = {team: "" for team in teams}
            for a, b in games:
                matchups[a] = b
                matchups[b] = a
            row.extend(matchups[t] for t in teams)
            writer.writerow(row)

# ---------- Example ----------
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

    weeks = build_schedule(divisions, rivals, seed=42)
    teams = [t for div in divisions.values() for t in div]
    export_schedule_csv(weeks, teams, "schedule.csv")
    for i, games in enumerate(weeks, start=1):
        print(f"Week {i}:")
        for a, b in games:
            print(f"  {a} vs {b}")
        print()
