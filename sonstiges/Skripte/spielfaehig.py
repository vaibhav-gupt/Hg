#!/usr/bin/env python3

"""check the probability that a group with a given structure of players has enough players to play at a random meeting.

Usage: ./spielfaehig.py prob players min_players
    - prob: the probability of each player to take part in the game.
    - players: the total number of players who might take part.
    - min_players: the number of players you need to play. 
"""

__copyright__ = """© 2010 Arne Babenhauserheide

You can use this under the GNU GPLv3 or later, if you provide the correct license texts and such → http://gnu.org/licenses/gpl.html"""

# simple binomials
from math import factorial
fac = factorial # ja, ich bin faul :)
def nük(n, k): 
   if k > n: return 0
   return fac(n) / (fac(k)*fac(n-k))

def binom(p, n, k): 
   return nük(n, k) * p** k * (1-p)**(n-k)

# fast binomials, thanks to bertm
from math import log, exp
from itertools import accumulate
def precalc_binom(p, n):
    # log(0!), log(1!), log(2!), ..., log(n!)
    log_facs = [1] + list(accumulate([log(i) for i in range(1, n + 1)]))
    log_p = log(p)
    log_1mp = log(1 - p)
    def log_combs(k):
        # Ensure symmetry
        k = min(k, n - k)
        return log_facs[n] - log_facs[n - k] - log_facs[k]
    def binom(k):
        return exp(log_combs(k) + log_p * k + log_1mp * (n - k))
    return binom


def spielfähig(p, n, min_spieler): 
    binom = precalc_binom(p, n)
    try:
        return sum([binom(k) for k in range(min_spieler, n+1)])
    except ValueError: return 1.0

if __name__ == "__main__":
    from sys import argv
    # help output if the number of arguments doesn’t fit.
    if not argv[3:]:
        print(__doc__)
        exit()
    print(spielfähig(float(argv[1]), int(argv[2]), int(argv[3])))
