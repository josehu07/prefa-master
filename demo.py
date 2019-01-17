##############################################################################
# Author: Jose, Robert & King                                                #
#  Date:  2019.01.15                                                         #
##############################################################################

from prefa import ere, nfa, dfa, pgui

input('\n#1. Parse a given RE \'a+(a|~)?[0-2]?\':\n')
my_re = ere.Regex('a+(a|~)?[0-2]?')
print(my_re)
input('(Press \"Enter\")')

input('\n#2. Build an NFA from the previous RE:\n')
my_nfa1 = nfa.NFiniteAutomata(my_re)
print(my_nfa1)
input('(Press \"Enter\")')

input('\n#3. Build a DFA from the previous RE directly:\n')
my_dfa1 = dfa.DFiniteAutomata(my_re)
print(my_dfa1)
input('(Press \"Enter\")')

input('\n#4. Build a DFA from the previous NFA \"my_nfa1\":\n')
my_dfa2 = dfa.DFiniteAutomata(my_nfa1)
print(my_dfa2)
input('(Press \"Enter\")')

input('\n#5. Minimize this DFA:\n')
min_dfa = my_dfa2.minimalDFA()
print(min_dfa)
input('(Press \"Enter\")')

input('\n#6. Build an NFA from a source file \'input/NFA\':\n')
my_nfa2 = nfa.NFiniteAutomata('input/NFA')
print(my_nfa2)
input('(Press \"Enter\")')

input('\n#7. Build a DFA from a source file \'input/DFA\':\n')
my_dfa2 = dfa.DFiniteAutomata('input/DFA')
print(my_dfa2)
input('(Press \"Enter\")')

input('\n#8. Show detailed steps of simulation on \'aa2a\':\n')
result = min_dfa.simulate('aa2a', verbose=True)
print(result)
input('(Press \"Enter\")')

input('\n#9: GUI display of DFA / NFA structure.\n')
pgui.FADrawer(my_nfa1).staticShow()
pgui.FADrawer(min_dfa).staticShow()
input('(Press \"Enter\")')
