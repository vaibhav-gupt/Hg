#!/usr/bin/env python
# encoding: utf-8

# floating point division
from __future__ import division

# nicer output
from pprint import pprint

"""Calculate probability trees for different 1d6 battles.

Simplifications: 
- A char fights as long as his ability is above a certain threshold (MIN_ABILITY). 
- A critical wound always ends the battle. 

"""

### Config ###

#: The maximum depth of the battle tree
MAX_DEPTH = 4

#: Minimum ability to be able to keep fighting
MIN_ABILITY = 6


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
'wound':10 # wound value
}

average_char_in_strong_armor = {'ability':12, # average
'weapon':4, # sword
'armor':10, # full plate
'wound':4 # wound value
}

average_char_with_strong_weapon = {'ability':12, # average
'weapon':14, # very heavy battle axe
'armor':3, # leather armor
'wound':4 # wound value
}

average_char_with_strong_weapon_and_armor = {'ability':12, # average
'weapon':14, # very heavy battle axe
'armor':10, # full plate
'wound':4 # wound value
}

legendary_char = {'ability':24, # legendary
'weapon':24, # sonic blade
'armor':10, # light combat armor
'wound':4 # wound value
}

space_marine = {'ability':15, # very good
'weapon':36, # laser sword
'armor':36, # light battle suit
'wound':5 # wound value
}


die = [-5, -3, -1, 2, 4, 6]

# die with rerolling
double_die = 6*die
double_die[0] = -10
double_die[-1] = 12

triple_die = 6*double_die
triple_die[0] = -15
triple_die[-1] = 18

quadruple_die = 6*triple_die
quadruple_die[0] = -20
quadruple_die[-1] = 24

quintuple_die = 6*quadruple_die
quintuple_die[0] = -25
quintuple_die[-1] = 30


### Functions ###

def dice_diff_prob(diff=4, die=triple_die): 
	"""Calculate the chance to get at least a given difference in a simple opposed roll.

Ideas: 
	- Also calculate the chances with rerolls of 6 and 5. 

	>>> dice_diff_prob(die=die)
	0.27777777777777779
	>>> dice_diff_prob(die=double_die)
	0.29475308641975306
	>>> dice_diff_prob(die=triple_die)
	0.29496742112482854
	
	# dice_diff_prob(die=quadruple_die)
	# 0.29497337486663616

"""
	hits=0
	rolls=0
	for i in die: 
		for j in die: 
			rolls += 1
			if i - j >= diff:
				hits += 1
				
	return hits / rolls


def generate_result(chars=[average_char, average_char], depth=0, max_depth=MAX_DEPTH, die=die):
	"""Generate the probability tree iteratively.

	>>> # pprint(generate_result())

TODO: Reduce the probabilities for win by win_wound and win_critical, and for 
win_wound by win_critical and the same for lose. 

"""
	# Stop the recursion when we get too deep or one of the chars can't fight anymore. 
	if chars[0]['ability'] <= MIN_ABILITY or chars[1]['ability'] <= MIN_ABILITY: 
		return None
	if depth>=max_depth: 
		return 'max depth'
	result = {}
	result['chars'] = chars

	# Prepare the char damag values when the attacker (chars[0]) wins
	char_0 = chars[0]['ability'] + chars[0]['weapon']
	char_1 = chars[1]['ability'] + chars[1]['armor']

	
	## win and inflict a critical wound
	# the chance to inflict a critical wound is the smaller of the chance to 
	# hit at all and the chance to archieve a critical wound. 
	res = []
	res.append(min(dice_diff_prob(diff = char_1 - char_0 + 3*chars[1]['wound'], die=die), 
		dice_diff_prob(diff = chars[0]['ability'] - chars[1]['ability'], die=die)))
	res.append(None)
	result['win_critical'] = res 

	## win and inflict a wound
	res = []
	res.append(min(dice_diff_prob(diff = char_1 - char_0 + chars[1]['wound'], die=die), 
		dice_diff_prob(diff = chars[1]['ability'] - chars[0]['ability'], die=die )) - result['win_critical'][0])
	char_changed = chars[1].copy()
	char_changed['ability'] -= 3
	res.append(generate_result(chars=[chars[0], char_changed], depth=depth+1, max_depth=max_depth))
	result['win_wound'] = res

	## just win
	res = []
	res.append(dice_diff_prob(diff = chars[1]['ability'] - chars[0]['ability'], die=die) - result['win_critical'][0] - result['win_wound'][0])
	res.append(generate_result(chars=chars, depth=depth+1, max_depth=max_depth))
	result['win'] = res


	# prepare the char damage values when the attacker loses (chars[0])
	char_0 = chars[0]['ability'] + chars[0]['armor']
	char_1 = chars[1]['ability'] + chars[1]['weapon']

	## lose and receive a critical wound
	res = []
	res.append(min(1 - dice_diff_prob(diff = char_1 - char_0 - 3*chars[0]['wound'] + 1, die=die), 
		1 - dice_diff_prob(diff = chars[1]['ability'] - chars[0]['ability'], die=die)))
	res.append(None)
	result['lose_critical'] = res

	## lose and receive a wound
	res = []
	res.append(min(1 - dice_diff_prob(diff = char_1 - char_0 - chars[0]['wound'] + 1, die=die), 
		1 - dice_diff_prob(diff = chars[1]['ability'] - chars[0]['ability'], die=die)) - result['lose_critical'][0])
	char_changed = chars[0].copy()
	char_changed['ability'] -= 3
	res.append(generate_result(chars=[char_changed, chars[1]], depth=depth+1, max_depth=max_depth))
	result['lose_wound'] = res

	## just lose
	res = []
	res.append((1 - dice_diff_prob(diff = chars[1]['ability'] - chars[0]['ability'], die=die)) - result['lose_critical'][0] - result['lose_wound'][0])
	res.append(generate_result(chars=chars, depth=depth+1, max_depth=max_depth))
	result['lose'] = res
	
	return result

def clean_tree(tree): 
	"""Clean the probability tree for display."""
	# Stop the recursion when we get a leaf
	if tree is None: 
		return None
	if tree == 'max depth': 
		return 'max depth'
	del tree['chars']
	for i in tree.values(): 
		i[1] = clean_tree(i[1])
	return tree

def aggregate_tree(tree, prob=1.0): 
	"""Aggregate the probabilities in each subtree into a combined probability."""
	# Stop the recursion when we get a leaf
	if tree is None: 
		return None
	if tree == 'max depth': 
		return 'max depth'
	# aggregate the tree
	for i in tree.values(): 
		# aggregate the earlier probabilities
		i[0] *= prob
		# and aggregate the subtree
		i[1] = aggregate_tree(i[1], i[0])
	
	return tree

def prob_to_win_or_lose(tree, win=0, lose=0): 
	"""Find the probability to win or lose the fight."""
	# only needed for 0 turn battles
	if tree == 'max depth': 
		return win, lose
	for i in tree.keys(): 
		if tree[i][1] is None: 
			if i in ['win', 'win_wound', 'win_critical']: 
				win += tree[i][0]
			else: 
				lose += tree[i][0]
		elif tree[i][1] == 'max depth': 
			return win, lose
		else: 
			win, lose = prob_to_win_or_lose(tree[i][1], win=win, lose=lose)
	return win, lose

def clean_leaves(tree): 
	"""Clean out the now unneeded None and 'max depth' values in the leaves."""
	if tree == 'max depth': 
		return 'max depth'
	# Clean out unnecessary None and 'max depth' values
	for i in tree.keys(): 
		# if we hit a leaf, turn the list into its probability value only. 
		if tree[i][1] is None or tree[i][1] == 'max depth':
			tree[i] = tree[i][0]
		# else turn the list into the subtree and move into the subtree
		else: 
			tree[i] = tree[i][1]
			clean_leaves(tree[i])
	return tree

def remove_low_prob(tree, threshold=0.01): 
	"""Remove all branches with only leaves which have a probability below the threshold."""
	if tree == 'max depth': 
		return 'max depth'
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

def generate_tree(chars=[average_char, average_char], min_prob=0.005, die=triple_die, number_of_turns=MAX_DEPTH):
	"""Generate a clean probability tree.

	#>>> pprint(generate_tree())
"""
	tree = generate_result(chars=chars, die=die, max_depth=number_of_turns+1)
	tree = clean_tree(tree)
	tree = aggregate_tree(tree)
	win, lose = prob_to_win_or_lose(tree)
	tree = clean_leaves(tree)
	tree = remove_low_prob(tree, threshold=min_prob)
	return win, lose


### Self Test ###

def _test(): 
	from doctest import testmod
	testmod()

def test_battle_length(): 
	"""Test the results for different battle length'"""
	print "Test battle length"
	print "Average char (12) vs. average char (12)"
	for i in range(5): 
		win, lose = generate_tree(chars=[average_char, average_char], number_of_turns=i)
		print "  Probs after", i, "turns:", "Win:", win, "Lose:", lose, "Draw:", 1 - (win+lose)
	print "\nVery good char (15) vs. average char (12)"
	for i in range(5): 
		win, lose = generate_tree(chars=[very_good_char, average_char], number_of_turns=i)
		print "  Probs after", i, "turns:", "Win:", win, "Lose:", lose, "Draw:", 1 - (win+lose)
	print "\nExceptional char (18) vs. average char (12)"
	for i in range(5): 
		win, lose = generate_tree(chars=[exceptional_char, average_char], number_of_turns=i)
		print "  Probs after", i, "turns:", "Win:", win, "Lose:", lose, "Draw:", 1 - (win+lose)
	print "\nLegend (24, weapon " + str(legendary_char['weapon']) + ", armor " + str(legendary_char['armor']) + ")", 
	print "vs.", 
	print "Space Marine (15, weapon " + str(space_marine['weapon']) + ", armor " + str(space_marine['armor']) + ", wound threshold " + str(space_marine['wound']) + ")"
	for i in range(9): 
		win, lose = generate_tree(chars=[legendary_char, space_marine], number_of_turns=i)
		print "  Probs after", i, "turns:", "Win:", win, "Lose:", lose, "Draw:", 1 - (win+lose)


def test_example_battles(): 
	"""Run several example battles for the number of turns given in MAX_DEPTH."""
	print "\n\nProbs after", MAX_DEPTH, "turns:"

	print "\nVery good char (15) vs. average char (12) without critical hits"
	win, lose = generate_tree(chars=[very_good_char, average_char], die=die)
	print "Win:", win, "Lose:", lose, "Draw:", 1 - (win+lose)

	print "Very good char (15) vs. average char (12)"
	win, lose = generate_tree(chars=[very_good_char, average_char])
	print "Win:", win, "Lose:", lose, "Draw:", 1 - (win+lose)

	print "\nExceptional char (18) vs. average char (12)"
	win, lose = generate_tree(chars=[exceptional_char, average_char])
	print "Win:", win, "Lose:", lose, "Draw:", 1 - (win+lose)

	print "\nVery good char (15) vs. average char in strong armor (12, armor " + str(average_char_in_strong_armor['armor']) + ")"
	win, lose = generate_tree(chars=[very_good_char, average_char_in_strong_armor])
	print "Win:", win, "Lose:", lose, "Draw:", 1 - (win+lose)

	print "\nVery good char (15) vs. average char with powerful weapon (12, weapon " + str(average_char_with_strong_weapon['weapon']) + ")"
	win, lose = generate_tree(chars=[very_good_char, average_char_with_strong_weapon])
	print "Win:", win, "Lose:", lose, "Draw:", 1 - (win+lose)

	print "\nVery good char (15) vs. sturdy char (12, wound threshold " + str(sturdy_char['wound']) + ")"
	win, lose = generate_tree(chars=[very_good_char, sturdy_char])
	print "Win:", win, "Lose:", lose, "Draw:", 1 - (win+lose)

	print "\nExceptional char (18) vs. average char with powerful weapon (12, weapon " + str(average_char_with_strong_weapon_and_armor['weapon']) + ") and strong armor (armor " + str(average_char_with_strong_weapon_and_armor['armor']) + ")"
	win, lose = generate_tree(chars=[exceptional_char, average_char_with_strong_weapon_and_armor])
	print "Win:", win, "Lose:", lose, "Draw:", 1 - (win+lose)


def read_chars_from_files(char1, char2): 
	"""Read the chars from simple files which get evaled (insecure!)."""
	f = open(char1, "r")
	data = f.read()
	f.close()
	char1 = eval(data)

	f = open(char2, "r")
	data = f.read()
	f.close()
	char2 = eval(data)

	return char1, char2


def help(): 
	"""Print help."""
	from sys import argv
	print "Usage:", argv[0], "[options] [chars]"
	print ""
	print "Examples: "
	print ' -', argv[0]
	print "   Do the default tests"
	print ""
	print ' -', argv[0], " char1 char2"
	print "   Let the two given chars fight against each other."
	print "   You can find example chars in the folder 'battle_prob_chars'"
	print ""
	print ' - ', argv[0], " --turns=X"
	print "   Let the Chars fight for the given number of turns."
	print "   You can find example chars in the folder 'battle_prob_chars'"

if __name__ == "__main__": 
	_test()

	from sys import argv
	if "--help" in argv: 
		help()
		exit()
	
	#: The default number of turns
	turns = MAX_DEPTH
	
	if len(argv) == 1: 	
		# do the default tests
		test_battle_length()
		test_example_battles()
		exit()

	# parse all opts
	for i in argv[:]: 
		if i.startswith("--turns"): 
			turns = int(i[6:])
			argv.remove(i)
	
	if len(argv) >= 3: 
		char1, char2 = read_chars_from_files(argv[-2], argv[-1])
		print "\n" + char1['name'] + "(" + str(char1['ability']) + ", weapon " + str(char1['weapon']) + ", armor " + str(char1['armor']) + ", wound threshold " + str(char1['wound']) + ")", 
 		print "vs.", 
		print char2['name'] + "(" + str(char2['ability']) + ", weapon " + str(char2['weapon']) + ", armor " + str(char2['armor']) + ", wound threshold " + str(char2['wound']) + ")" 
		for turns in range(8): 
			win, lose = generate_tree(chars=[char1, char2], number_of_turns=turns)
			print "  Probs after", turns, "turns:", "Win:", win, "Lose:", lose, "Draw:", 1 - (win+lose)


