# -*- coding: utf-8 -*-
"""
Created on Mon Apr  8 00:21:37 2019

@author: Efsun Sezer
"""

from collections import OrderedDict
import random

class CFG(OrderedDict):
    def __init__(self, *args):
        super().__init__(map(lambda s: s.replace(' ', '').split('->'), args))
        
    def __repr__(self):
        return '\n'.join('{} -> {}'.format(k, v) for k, v in self.items())

    def take_grammar_rules(self, symbol):
        return self[symbol].split('|')


def sentence_generation(context_free_grammar, start_symbol='S'):
    string = []
    def depth_first_search(root):
        local_str = ''
        random_rule = random.choice(context_free_grammar.take_grammar_rules(root))
        for char in random_rule:
            if char in context_free_grammar:
                result = depth_first_search(char)
                if result:
                    string.append(result)
            else:
                local_str += char
        return local_str

    depth_first_search(start_symbol)
    return ' '.join(string[:-1])+' '+ string[-1]

if __name__ == "__main__":
#    store the grammar rule from grammar file
#    S  = sentence
#    NP = noun phrase
#    VP = verb phrase
#    PP = prepositional phrase
#    Det = determiner
#    Prep = preposition
#    Adj = adjective

    grammar_rule = [
        'S -> NP VP',
        'VP -> Verb NP',
        'NP -> Det Noun |NP PP',
        'PP -> Prep NP',
        'Noun -> Adj Noun',
        'Verb -> "ate" | "wanted" | "kissed" | "washed" | "pickled"',
        'Det -> "the" | "a" | "every"',
        'Noun -> "president" | "sandwich" | "pickle" | "mouse" | "floor"',
        'Adj -> "fine" | "delicious" | "beautiful" | "old"',
        'Prep -> "with" | "on" | "under" | "in"'
    ]

    # Renaming for simplicity
    grammar_dict = OrderedDict([
        ('VP',      'A'),
        ('NP',      'B'),
        ('PP',      'C'),
        ('Noun',    'D'),
        ('Verb',    'E'),
        ('Det',     'F'),
        ('Adj',     'G'),
        ('Prep',    'H'),
    
    ])

    for i in range(len(grammar_rule)):
        grammar_rule[i] = grammar_rule[i].replace('\"', '')
        for key in grammar_dict:
            grammar_rule[i] = grammar_rule[i].replace(key, grammar_dict[key])

    context_free_grammar = CFG(*grammar_rule)
    
    
    text_file= open("random-sentence.txt","w+")
    
    # Run your program multiple times
    print("----Generate sentences and write it to the file----")
    for i in range(20):
        print("----%d . sentence----" % (i+1))
        sentence=sentence_generation(context_free_grammar)
        print(sentence) 
        text_file.write("%s\n" %sentence)
           
    text_file.close()       
     
        
        
        
        
        
        
        
        