#!/usr/bin/env python3

"""check the probability that a group with a given structure of players has enough players to play at a random meeting.

Usage: ./spielfaehig.py prob players min_players
    - prob: the probability of each player to take part in the game.
    - players: the total number of players who might take part.
    - min_players: the number of players you need to play. 
"""

__copyright__ = """© 2010 Arne Babenhauserheide

You can use this under the GNU GPLv3 or later, if you provide the correct license texts and such — see http://gnu.org/licenses/gpl.html"""

from math import factorial
fac = factorial # ja, ich bin faul :)
def nük(n, k): 
   if k > n: return 0
   return fac(n) / (fac(k)*fac(n-k))

def binom(p, n, k): 
   return nük(n, k) * p** k * (1-p)**(n-k)

def spielfähig(p, n, min_spieler): 
   return sum([binom(p, n, k) for k in range(min_spieler, n+1)])

if __name__ == "__main__":
    from sys import argv
    # help output if the number of arguments doesn’t fit.
    if not argv[3:]:
        print(__doc__)
        exit()
    print(spielfähig(float(argv[1]), int(argv[2]), int(argv[3])))
