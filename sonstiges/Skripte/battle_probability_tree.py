#!/usr/bin/env python
# encoding: utf-8

# floating point division
from __future__ import division

"""Calculate probability trees for different 1d6 battles.

Plan: 
- sample dicts
- dice difference calculator (chances for a difference)
- get chances for the different results
- build single result dict with probs
- build battle tree with final probs

"""

sample_char = {'ability':12, # average
'weapon':4, # sword
'armor':3 # leather armor
}

sample_result = {'chars': [],
'win_critical': [0.1, None], # it ends here
'win_wound': [0.2, {}],
'win': [0.2, {}],
'lose': [0.2, {}],
'lose_wound': [0.2, {}],
'lose_critical': [0.2, {}]
}

die = [-5, -3, -1, 2, 4, 6]

def dice_diff_chance(diff): 
	"""Calculate the chance to get a given difference in a simple opposed roll.

	>>> dice_diff_chance(4)
	0.27777777777777779

"""
	wins=0
	losses=0
	for i in die: 
		for j in die: 
			if i - j >= diff: 
				wins += 1
			else: 
				losses += 1
	return wins / (wins + losses)


### Self Test ###

def _test(): 
	from doctest import testmod
	testmod()

if __name__ == "__main__": 
	_test()

