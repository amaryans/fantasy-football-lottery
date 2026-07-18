from itertools import combinations
from random import sample


def fcomb0(n, k):
    """
    Compute the number of ways to choose $k$ elements out of a pile of $n.$

    Use an iterative approach with the multiplicative formula:
    $$\frac{n!}{k!(n - k)!} =
    \frac{n(n - 1)\dots(n - k + 1)}{k(k-1)\dots(1)} =
    \prod_{i = 1}^{k}\frac{n + 1 - i}{i}$$

    Also rely on the symmetry: $C_n^k = C_n^{n - k},$ so the product can
    be calculated up to $\min(k, n - k).$

    :param n: the size of the pile of elements
    :param k: the number of elements to take from the pile
    :return: the number of ways to choose k elements out of a pile of n
    """

    # When k out of sensible range, should probably throw an exception.
    # For compatibility with scipy.special.{comb, binom} returns 0 instead.
    if k < 0 or k > n:
        return 0

    if k == 0 or k == n:
        return 1

    total_ways = 1
    for i in range(min(k, n - k)):
        total_ways = total_ways * (n - i) // (i + 1)

    return total_ways


class Simulator():
    def __init__(self, n_picks, n_balls, chances):
        self.n_picks = n_picks
        self.n_balls = n_balls
        self.chances = chances

        self.len_ch = len(self.chances)
        self.seeds = [x for x in range(self.len_ch)]

        self.combs = [cmb for cmb in combinations(self.seeds, self.n_balls)]

        self.winning_seeds = list()
        for seed in self.seeds:
            self.winning_seeds += self.chances[seed] * [seed]
        self.winning_seeds += [self.len_ch] * (int(fcomb0(self.len_ch, self.n_balls)) - sum(self.chances))
        self.win_seeds = sample(self.winning_seeds, len(self.winning_seeds))

        self.hashtable = dict(zip(self.combs, self.win_seeds))

    def lottery(self):
        return tuple(sorted(sample(self.seeds, self.n_balls)))

    def play_lottery(self):
        order = [x for x in range(self.len_ch)]
        skips = [self.len_ch]

        n_draws = self.n_picks
        while n_draws:
            draw = self.lottery()

            if self.hashtable[draw] in skips:
                continue
            skips.append(self.hashtable[draw])

            old_index = order.index(self.hashtable[draw])
            order.insert(self.n_picks - n_draws, order.pop(old_index))

            n_draws -= 1

        return order
