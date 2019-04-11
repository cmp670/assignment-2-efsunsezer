# -*- coding: utf-8 -*-
"""
Created on Mon Apr  8 00:29:49 2019
@author: Efsun Sezer
"""

import sys
import numpy as np

class structure():
	""" Build the pars trees structure """
	def __init__(self, symbol, child1 = None, child2 = None, terminal = None):
		""" constructor """
		self.symbol = symbol
		self.child1 = child1
		self.child2 = child2
		self.terminal = terminal

	def take_symbol(self):
		return self.symbol

	def first_child(self):
		""" return the first child """
		return self.child1

	def second_child(self):
		""" return the second child """
		return self.child2

	def terminal(self):
		""" return the terminal """
		return self.terminal
    
	def symbol_setting(self, symbol):
		"""set the symbol """
		self.symbol = symbol
        
def cyk_parser(string, grammar_rules, non_terms, terms):
    
	N = length(string)
	result = False

	#Initialize table
	table = [[[] for i in range(N)] for j in range(N)]

	
	if ' ' in string:
		splits = string.split(' ')
		for s in range(1, N+1):
			Rule_Update(splits[s-1], s-1, grammar_rules, table)
	else:
		for s in range(1, N+1):
			Rule_Update(string[s-1], s-1, grammar_rules, table)

	
	for l in range(2,N+1): 
		for s in range(1,N-l+2): 
			for p in range(1,l): 
				Rule_Update_2(grammar_rules, non_terms, terms, table, l-1, s-1, p-1)

	finalLength = len(table[N-1][0])
	finalVector = []

	for i in range(finalLength):
		finalVector.append(table[N-1][0][i].take_symbol())

	if non_terms[0] in finalVector:
		result = True
		print('Sentence \'' + string + '\' belongs to the given grammar.' )
		print(' ')
		print('Parsing tree of the sentence :')


		for X in table[N-1][0]:
			if X.take_symbol() == non_terms[0]:
				tree = tree_build(X,0)
				print(tree)
				print('\n\n\n')
	else:
		print('Sentence \'' + string + '\' does not belong to the given grammar.' )

		
	return result

def length(string):
	""" Find the number of terminals that are used in the tested string """
	if ' ' in string:
		splits = string.split(' ')
		return len(splits)
	else:
		return len(string)
    
def tree_build(startSymbol, depth = 0):
	""" Print a Pars Tree """
	tree = ""

	if startSymbol.second_child() != None:
		tree += tree_build(startSymbol.second_child(), depth + 1)

	if startSymbol.terminal() != None:
		tree += '\n' + "    "*depth + startSymbol.take_symbol() + '->' + startSymbol.terminal()
	else:
		tree += "\n" + "    "*depth + startSymbol.take_symbol()


	if startSymbol.first_child()!= None:
		tree += tree_build(startSymbol.first_child(), depth + 1)

	return tree

def Rule_Update(symbol, symbolPos, rules, table):
	for rule in rules:
		if symbol == rule[1]: 
			table[0][symbolPos].append(structure(symbol = rule[0], terminal = rule[1]))


def Rule_Update_2(rules, non_terminals, terminals, table, l, s, p):
	
	for rule in rules:
		left = rule[0] 
		right = rule[1]

		if right not in terminals:
			child1 = None
			child2 = None
			right1 = right.split(' ')[0]
			right2 = right.split(' ')[1]
			
			parent1Length = len(table[p][s])
			
			for i in range(parent1Length):
				if right1 == table[p][s][i].take_symbol():
					child1 = table[p][s][i]


			parent2Length = len(table[l-p-1][s+p+1])
			
			for i in range(parent2Length):
				if right2 == table[l-p-1][s+p+1][i].take_symbol():
					child2 = table[l-p-1][s+p+1][i]
			if child1 != None and child2 != None:
				table[l][s].append(structure(symbol = left, child1 = child1, child2 = child2))


if __name__ == '__main__':
#    store the grammar rule from grammar file
#    S  = sentence
#    NP = noun phrase
#    VP = verb phrase
#    PP = prepositional phrase
#    Det = determiner
#    Prep = preposition
#    Adj = adjective
   non_terminals = ["S","NP","VP","Verb","Noun","PP","Det","Prep","Adj"]
   terminals = [
    "ate","wanted","kissed","washed","pickled",
    "the","a","very",
    "president", "sandwich", "pickle","mouse","floor",
    "fine", "delicious", "beautiful", "old",
    "with", "on", "under", "in", 
    ]
	         
   grammar_rules = [
                     ("S", "NP VP"), 
                     ("VP", "Verb NP"),
                     ("NP", "Det Noun"),("NP", "NP PP"),
                     ("PP", "Prep NP"),
                     ("Noun", "Adj Noun"),
                     ("Verb", "ate"),("Verb", "wanted"),("Verb", "kissed"),("Verb", "washed"),("Verb", "pickled"),
                     ("Det", "the"),("Det", "a"),("Det", "very"),
                     ("Noun", "president"),("Noun", "sandwich"),("Noun", "pickle"),("Noun", "mouse"),("Noun", "floor"),
                     ("Adj","fine"),("Adj","delicious"),("Adj","beautiful"),("Adj", "old"),
                     ("Prep", "with" ), ("Prep", "on"),("Prep","under"),("Prep", "in")
                    ]
  
    
   with open('sentence.txt') as f:
     all_sentences = [line.rstrip() for line in f]
   print('----sentence checking: whether a given sentence is grammatically correct or not----' )
   
   for i in range(len(all_sentences)):
        print("----Sentence is: %s ----\n" % (all_sentences[i]))
        recognition_result= cyk_parser(all_sentences[i],grammar_rules,non_terminals,terminals)
        

   

	
	
