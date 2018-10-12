from prefa.fa import FiniteAutomata     # FA prototype
from prefa.nfa import NFiniteAutomata   # NFA class
from prefa.re import Regex              # Regular Expression class

class DFiniteAutomata(FiniteAutomata):
    """Determinstic Finite Automata child class.

    Can be initilaized from a formatted source file or a Regular Expression,
    or from an NFiniteAutomata. Representation structure is just like
    FiniteAutomata parent class.

    Attributes:
        initial    - str , the initial state
        acceptings - set , set of acccepting states
        table      - dict, the transition table
        alphabet   - list, alphabet in sorted order
        states     - list, list of all states in sorted order
    """ 

    def __init__(self, input):
        # TODO(jose): Error checking
        if type(input) == str:                  # 1. Input from source file
            self._initFromFile(input)
        elif type(input) == NFiniteAutomata:    # 2. Input from NFA convertion
            self._initFromNFA(input)
        else:                                   # 3. Input from a regex
            self._initFromRE(input)

    def _initFromRE(self, input_regex):
        """Initializer for a Regular Expression.

        Takes a Regular Expression, builds an DFA by utilizing position
        numbers for non-epsilon leaves.

        Args:
            input_regex - str, input Regular Expression
        """

        def nullable(node):
            """Is sub-regex rooted at NODE nullable?

            Args:
                node - Node, current root node

            Returns:
                bool, True iff nullable, else False
            """
            if node.value == '~' or node.value == '*':
                return True
            elif node.left is None and node.right is None:
                return False
            elif node.value == '-':
                return nullable(node.left) and nullable(node.right)
            elif node.value == '+':
                return nullable(node.left) or  nullable(node.right)
            else:
                # TODO(jose): Error checking
                pass

        def firstpos(node):
            """Which positions can be first in sub-regex rooted at NODE?

            Args:
                node - Node, current root node

            Returns:
                set, set of firstpos on NODE
            """
            if node.value == '~':
                return set()
            elif node.left is None and node.right is None:
                return {node.pos}
            elif node.value == '*':
                return firstpos(node.left)
            elif node.value == '-':
                if nullable(node.left):
                    return firstpos(node.left) | firstpos(node.right)
                return firstpos(node.left)
            elif node.value == '+':
                return firstpos(node.left) | firstpos(node.right)
            else:
                # TODO(jose): Error checking
                pass

        def lastpos(node):
            """Which positions can be last in sub-regex rooted at NODE?

            Args:
                node - Node, current root node

            Returns:
                set, set of lastpos on NODE
            """
            if node.value == '~':
                return set()
            elif node.left is None and node.right is None:
                return {node.pos}
            elif node.value == '*':
                return lastpos(node.left)
            elif node.value == '-':
                if nullable(node.right):
                    return lastpos(node.left) | lastpos(node.right)
                return lastpos(node.right)
            elif node.value == '+':
                return lastpos(node.left) | lastpos(node.right)
            else:
                # TODO(jose): Error checking
                pass

        # Do a DFS traverse from root node, calculate followpos table for
        # every position number. FOLLOWPOS will be stored as a dict.
        followpos = {}
        stack = [input_regex.tree]
        while len(stack) > 0:
            node = stack.pop()
            if node.value == '-':
                for i in lastpos(node.left):
                    if i in followpos:
                        followpos[i] |= firstpos(node.right)
                    else:
                        followpos[i]  = firstpos(node.right)
            elif node.value == '*':
                for i in lastpos(node.left):
                    if i in followpos:
                        followpos[i] |= firstpos(node.left)
                    else:
                        followpos[i]  = firstpos(node.left)
            if node.right is not None:
                stack.append(node.right)
            if node.left is not None:
                stack.append(node.left)

        # Set and initialize the fields to prepare for construction.
        S0 = firstpos(input_regex.tree)
        DStates, marker, namer = [('S0', S0)], 0, 0
        self.alphabet = input_regex.alphabet
        self.table = {}
        self.states = []
        self.initial, self.acceptings = 'S0', set()

        # Iteratively construct the transition table from FOLLOWPOS infos.
        # Here, DFA state "U" is the set of several position numbers, and
        # "name_U" is the actual name to be stored in transtion table for
        # this DFA state U.
        while (marker < len(DStates)):
            name_U, U = DStates[marker]
            self.table[name_U] = {}
            self.states.append(name_U)
            if '#' in [input_regex.index[i] for i in U]:    # True iff U is
                self.acceptings.add(name_U)                 # accepting
            for a in self.alphabet:
                V = set()
                for pos in U:
                    if input_regex.index[pos] == a:
                        V |= followpos[pos]
                if len(V) == 0:
                    self.table[name_U][a] = {'-'}
                else:
                    name_V = None
                    for tup in DStates:     # Falls in iff V is in DStates
                        if len(tup[1] ^ V) == 0:
                            name_V = tup[0]
                            break
                    if name_V is None:      # True iff V is not in DStates
                        namer += 1
                        name_V = 'S' + str(namer)
                        DStates.append((name_V, V))
                    self.table[name_U][a] = {name_V}
            marker += 1

    def _initFromNFA(self, input_nfa):
        """Initializer for an NFiniteAutomata.

        Takes a Regular Expression, builds an DFA by utilizing position
        numbers for non-epsilon leaves.

        Args:
            input_regex - str, input Regular Expression
        """
            
        # Set and initialize the fields to prepare for construction.
        S0 = input_nfa.epsClosure({input_nfa.initial})
        DStates, marker, namer = [('S0', S0)], 0, 0
        self.table = {}
        self.states = []
        self.alphabet = input_nfa.alphabet
        self.alphabet.remove('~')
        self.initial, self.acceptings = 'S0', set()

        # Iteratively construct the transition table from INPUT_NFA infos.
        # Here, DFA state "U" is the set of several INPUT_NFA states, and
        # "name_U" is the actual name to be stored in transtion table for
        # this DFA state U.
        while (marker < len(DStates)):
            name_U, U = DStates[marker]
            self.table[name_U] = {}
            self.states.append(name_U)
            if len(U & input_nfa.acceptings) > 0:   # True iff U is accepting
                self.acceptings.add(name_U)
            for a in self.alphabet:
                V = input_nfa.epsClosure(input_nfa.move(U, a))
                if len(V) == 0:
                    self.table[name_U][a] = {'-'}
                else:
                    name_V = None
                    for tup in DStates:     # Falls in iff V is in DStates
                        if len(tup[1] ^ V) == 0:
                            name_V = tup[0]
                            break
                    if name_V is None:      # True iff V is not in DStates
                        namer += 1
                        name_V = 'S' + str(namer)
                        DStates.append((name_V, V))
                    self.table[name_U][a] = {name_V}
            marker += 1

if __name__ == '__main__':
    print(DFiniteAutomata('../input/DFA'))
    print(DFiniteAutomata(NFiniteAutomata('../input/NFA')))

    re = Regex('(a+~)bc*')
    print(re)
    print(DFiniteAutomata(re))
