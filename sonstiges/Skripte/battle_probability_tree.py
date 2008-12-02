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

sample_char = {'ability':12, # average
'weapon':4, # sword
'armor':3, # leather armor
'wound':4 # wound value
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


def generate_result(chars=[sample_char, sample_char], depth=0, max_depth=4):
	"""Generate the probability tree iteratively.

	>>> # pprint(generate_result())

"""
	# Stop the recursion when we get too deep or one of the chars can't fight anymore. 
	if chars[0]['ability'] <= 0 or chars[1]['ability'] <= 0 or depth>=max_depth: 
		return None
	result = {}
	result['chars'] = chars
	char_0 = chars[0]['ability'] + chars[0]['weapon']
	char_1 = chars[1]['ability'] + chars[1]['armor']

	# the chance to inflict a critical wound is the smaller of the chance to 
	# hit at all and the chance to archieve 12 points of difference. 
	res = []
	res.append(min(dice_diff_prob(diff = char_1 - char_0 + 12), 
		dice_diff_prob(diff = chars[0]['ability'] - chars[1]['ability'])))
	res.append(None)
	result['win_critical'] = res 

	res = []
	res.append(min(dice_diff_prob(diff = char_1 - char_0 + 4), 
		dice_diff_prob(diff = chars[1]['ability'] - chars[0]['ability'])))
	char_changed = chars[1].copy()
	char_changed['ability'] -= 3
	res.append(generate_result(chars=[chars[0], char_changed], depth=depth+1))
	result['win_wound'] = res

	res = []
	res.append(dice_diff_prob(diff = chars[1]['ability'] - chars[0]['ability']))
	res.append(generate_result(chars=chars, depth=depth+1))
	result['win'] = res


	char_0 = chars[0]['ability'] + chars[0]['armor']
	char_1 = chars[1]['ability'] + chars[1]['weapon']

	res = []
	res.append(1 - dice_diff_prob(diff = chars[1]['ability'] - chars[0]['ability']))
	res.append(generate_result(chars=chars, depth=depth+1))
	result['lose'] = res

	res = []
	res.append(min(1 - dice_diff_prob(diff = char_1 - char_0 - 3), 
		1 - dice_diff_prob(diff = chars[1]['ability'] - chars[0]['ability'])))
	char_changed = chars[0].copy()
	char_changed['ability'] -= 3
	res.append(generate_result(chars=[char_changed, chars[1]], depth=depth+1))
	result['lose_wound'] = res

	res = []
	res.append(min(1 - dice_diff_prob(diff = char_1 - char_0 - 11), 
		1 - dice_diff_prob(diff = chars[1]['ability'] - chars[0]['ability'])))
	res.append(None)
	result['lose_critical'] = res
	
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
	for i in tree: 
		# if we hit a leaf, turn the list into its probability value only. 
		if tree[i][1] is None:
			tree[i] = tree[i][0]
		# else turn the list into the subtree and move into the subtree
		else: 
			tree[i] = tree[i][1]
			clean_leaves(tree[i])
	return tree
	

def generate_tree(chars=[sample_char, sample_char]):
	"""Generate a clean probability tree.

	>>> pprint(generate_tree())
"""
	tree = generate_result(chars=chars)
	tree = clean_tree(tree)
	tree = aggregate_tree(tree)
	return clean_leaves(tree)

### Self Test ###

def _test(): 
	from doctest import testmod
	testmod()

if __name__ == "__main__": 
	_test()

