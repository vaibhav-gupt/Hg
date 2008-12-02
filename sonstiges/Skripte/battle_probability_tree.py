#!/usr/bin/env python
# encoding: utf-8

# floating point division
from __future__ import division

# nicer output
from pprint import pprint

"""Calculate probability trees for different 1d6 battles.

Plan: 
- sample dicts
- dice difference calculator (chances for a difference)
- get chances for the different results
- build single result dict with probs
- build battle tree with final probs

"""


### Constants ###

average_char = {'ability':12, # average
'weapon':4, # sword
'armor':3, # leather armor
'wound':4 # wound value
}

very_good_char = {'ability':15, # average
'weapon':4, # sword
'armor':3, # leather armor
'wound':4 # wound value
}

exceptional_char = {'ability':18, # average
'weapon':4, # sword
'armor':3, # leather armor
'wound':4 # wound value
}

sturdy_char = {'ability':12, # average
'weapon':4, # sword
'armor':3, # leather armor
'wound':6 # wound value
}

average_char_in_strong_armor = {'ability':12, # average
'weapon':4, # sword
'armor':10, # full plate
'wound':4 # wound value
}

average_char_with_strong_weapon = {'ability':12, # average
'weapon':10, # heavy double axe
'armor':3, # leather armor
'wound':4 # wound value
}

die = [-5, -3, -1, 2, 4, 6]


### Functions ###

def dice_diff_prob(diff=4): 
	"""Calculate the chance to get at least a given difference in a simple opposed roll.

Ideas: 
	- Also calculate the chances with rerolls of 6 and 5. 

	>>> dice_diff_prob()
	0.27777777777777779

"""
	hits=0
	rolls=0
	for i in die: 
		for j in die: 
			rolls += 1
			if i - j >= diff:
				hits += 1
	return hits / rolls


def generate_result(chars=[average_char, average_char], depth=0, max_depth=4):
	"""Generate the probability tree iteratively.

	>>> # pprint(generate_result())

TODO: Reduce the probabilities for win by win_wound and win_critical, and for 
win_wound by win_critical and the same for lose. 

"""
	# Stop the recursion when we get too deep or one of the chars can't fight anymore. 
	if chars[0]['ability'] <= 0 or chars[1]['ability'] <= 0 or depth>=max_depth: 
		return None
	result = {}
	result['chars'] = chars

	# Prepare the char damag values when the attacker (chars[0]) wins
	char_0 = chars[0]['ability'] + chars[0]['weapon']
	char_1 = chars[1]['ability'] + chars[1]['armor']

	
	## win and inflict a critical wound
	# the chance to inflict a critical wound is the smaller of the chance to 
	# hit at all and the chance to archieve 12 points of difference. 
	res = []
	res.append(min(dice_diff_prob(diff = char_1 - char_0 + 12), 
		dice_diff_prob(diff = chars[0]['ability'] - chars[1]['ability'])))
	res.append(None)
	result['win_critical'] = res 

	## win and inflict a wound
	res = []
	res.append(min(dice_diff_prob(diff = char_1 - char_0 + 4), 
		dice_diff_prob(diff = chars[1]['ability'] - chars[0]['ability'])) - result['win_critical'][0])
	char_changed = chars[1].copy()
	char_changed['ability'] -= 3
	res.append(generate_result(chars=[chars[0], char_changed], depth=depth+1))
	result['win_wound'] = res

	## just win
	res = []
	res.append(dice_diff_prob(diff = chars[1]['ability'] - chars[0]['ability']) - result['win_critical'][0] - result['win_wound'][0])
	res.append(generate_result(chars=chars, depth=depth+1))
	result['win'] = res


	# prepare the char damage values when the attacker loses (chars[0])
	char_0 = chars[0]['ability'] + chars[0]['armor']
	char_1 = chars[1]['ability'] + chars[1]['weapon']

	## lose and receive a critical wound
	res = []
	res.append(min(1 - dice_diff_prob(diff = char_1 - char_0 - 11), 
		1 - dice_diff_prob(diff = chars[1]['ability'] - chars[0]['ability'])))
	res.append(None)
	result['lose_critical'] = res

	## lose and receive a wound
	res = []
	res.append(min(1 - dice_diff_prob(diff = char_1 - char_0 - 3), 
		1 - dice_diff_prob(diff = chars[1]['ability'] - chars[0]['ability'])) - result['lose_critical'][0])
	char_changed = chars[0].copy()
	char_changed['ability'] -= 3
	res.append(generate_result(chars=[char_changed, chars[1]], depth=depth+1))
	result['lose_wound'] = res

	## just lose
	res = []
	res.append((1 - dice_diff_prob(diff = chars[1]['ability'] - chars[0]['ability'])) - result['lose_critical'][0] - result['lose_wound'][0])
	res.append(generate_result(chars=chars, depth=depth+1))
	result['lose'] = res
	
	return result

def clean_tree(tree): 
	"""Clean the probability tree for display."""
	# Stop the recursion when we get a leaf
	if tree is None: 
		return None
	del tree['chars']
	for i in tree.values(): 
		i[1] = clean_tree(i[1])
	return tree

def aggregate_tree(tree, prob=1.0): 
	"""Aggregate the probabilities in each subtree into a combined probability."""
	# Stop the recursion when we get a leaf
	if tree is None: 
		return None
	# aggregate the tree
	for i in tree.values(): 
		# aggregate the earlier probabilities
		i[0] *= prob
		# and aggregate the subtree
		i[1] = aggregate_tree(i[1], i[0])
	
	return tree

def clean_leaves(tree): 
	"""Clean out the now unneeded None values in the leaves."""
	# Clean out unnecessary None values
	for i in tree.keys(): 
		# if we hit a leaf, turn the list into its probability value only. 
		if tree[i][1] is None:
			tree[i] = tree[i][0]
		# else turn the list into the subtree and move into the subtree
		else: 
			tree[i] = tree[i][1]
			clean_leaves(tree[i])
	
	return tree

def remove_low_prob(tree, threshold=0.005): 
	"""Remove all branches with only leaves which have a probability below the threshold."""
	for i in tree.keys(): 
		# remove low probability items
		if tree[i] < threshold: 
			del tree[i]
		elif not isinstance(tree[i], float): 
			remove_low_prob(tree[i], threshold=threshold)
	for i in tree.keys(): 
		# also remove (now) empty dicts
		if not tree[i]: 
			del tree[i]
	return tree

def generate_tree(chars=[average_char, average_char]):
	"""Generate a clean probability tree.

	#>>> pprint(generate_tree())
"""
	tree = generate_result(chars=chars)
	tree = clean_tree(tree)
	tree = aggregate_tree(tree)
	tree = clean_leaves(tree)
	return remove_low_prob(tree)

### Self Test ###

def _test(): 
	from doctest import testmod
	testmod()

if __name__ == "__main__": 
	_test()
	print "Exceptional char (18) vs. average char (12)"
	pprint(generate_tree(chars=[exceptional_char, average_char]))
