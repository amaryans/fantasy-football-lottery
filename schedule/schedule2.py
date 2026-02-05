from collections import Counter
import random

def pair_key(a, b):
    return tuple(sorted((a, b)))

def round_robin_weeks(teams):
    """Circle method for a single round robin (n-1 weeks)."""
    n = len(teams)
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

def build_schedule(divisions, rivals, seed=None):
    if seed is not None:
        random.seed(seed)

    teams = [t for div in divisions.values() for t in div]
    if len(teams) != 12:
        raise ValueError("Must have exactly 12 teams (3 divisions × 4).")

    # Step 1: Weeks 1-11 = full round robin
    base_weeks = round_robin_weeks(teams)

    # Step 2: Week 12 = Rivalry Week
    uniq_rival_pairs = set(pair_key(t, r) for t, r in rivals.items() if t < r)
    rivalry_week = list(uniq_rival_pairs)

    # Track how many times each pair has been scheduled
    pair_counts = Counter()
    for wk in base_weeks + [rivalry_week]:
        for a, b in wk:
            pair_counts[pair_key(a, b)] += 1

    # Step 3: Weeks 13 & 14 = fill extra games
    # Rule: Each team must reach 14 games total
    team_counts = Counter()
    for wk in base_weeks + [rivalry_week]:
        for a, b in wk:
            team_counts[a] += 1
            team_counts[b] += 1

    week13, week14 = [], []
    used = set()

    # Build pods by rank
    div_names = list(divisions.keys())
    pods = [[divisions[d][rank] for d in div_names] for rank in range(4)]

    for pod in pods:
        a, b, c = pod
        candidates = [(a, b), (b, c), (a, c)]
        random.shuffle(candidates)
        # assign one to week 13, one to week 14, skip the third
        for game, week in zip(candidates[:2], [week13, week14]):
            t1, t2 = game
            if team_counts[t1] < 14 and team_counts[t2] < 14:
                week.append(game)
                team_counts[t1] += 1
                team_counts[t2] += 1
                pair_counts[pair_key(*game)] += 1

    # If some teams still need a game, fill with "one-offs"
    all_pairs = [pair_key(a, b) for i, a in enumerate(teams) for b in teams[i+1:]]
    for week in [week13, week14]:
        while len(week) < 6:  # need 6 games per week
            # pick two teams with <14 games
            candidates = [t for t in teams if team_counts[t] < 14]
            if len(candidates) < 2:
                break
            t1, t2 = random.sample(candidates, 2)
            pk = pair_key(t1, t2)
            if pair_counts[pk] < 2:  # allow at most 2 meetings
                week.append((t1, t2))
                team_counts[t1] += 1
                team_counts[t2] += 1
                pair_counts[pk] += 1

    weeks = base_weeks + [rivalry_week, week13, week14]

    # ---------- Validation ----------
    for i, games in enumerate(weeks, start=1):
        seen = set()
        for a, b in games:
            if a in seen or b in seen:
                raise AssertionError(f"Team double-booked in Week {i}")
            seen.update([a, b])
        if len(seen) != 12:
            raise AssertionError(f"Incomplete Week {i}")

    for t in teams:
        if team_counts[t] != 14:
            raise AssertionError(f"{t} has {team_counts[t]} games (expected 14)")

    return weeks


# ---------- Example usage ----------
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

    # Print
    for i, games in enumerate(weeks, start=1):
        print(f"Week {i}:")
        for a, b in games:
            print(f"  {a} vs {b}")
        print()