from prefa import fa, ere, nfa
from copy import deepcopy
# import fa, ere, nfa

class DFiniteAutomata(fa.FiniteAutomata):
    """Determinstic Finite Automata child class.

    Can be initilaized from a formatted source file or a Regular Expression,
    or from an NFiniteAutomata. Representation structure is just like
    FiniteAutomata parent class.

    Attributes:
        initial    - str , the initial state
        acceptings - set , set of accepting states
        table      - dict, the transition table
        alphabet   - list, alphabet in sorted order
        states     - list, list of all states in sorted order
    """ 

    def __init__(self, input):
        if type(input) == str:                  # 1. Input from source file
            self._initFromFile(input)
        elif type(input) == nfa.NFiniteAutomata:    # 2. Input from NFA convertion
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
                Bool, True iff nullable, else False
            """
            if node.value == '~' or node.value == '*':
                return True
            elif node.left is None and node.right is None:
                return False
            elif node.value == '-':
                return nullable(node.left) and nullable(node.right)
            elif node.value == '|':
                return nullable(node.left) or  nullable(node.right)

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
            elif node.value == '|':
                return firstpos(node.left) | firstpos(node.right)

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
            elif node.value == '|':
                return lastpos(node.left) | lastpos(node.right)

        # Do a DFS traverse from root node, calculate followpos table for
        # every position number. FOLLOWPOS will be stored as a dict.
        followpos = {}
        stack = [input_regex.tree]
        stack[-1].visited = False
        while len(stack) > 0:
            node = stack[-1]
            if node.visited:
                stack.pop()
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
            else:
                if node.right is not None:
                    stack.append(node.right)
                    node.right.visited = False
                if node.left is not None:
                    stack.append(node.left)
                    node.left.visited  = False
                node.visited = True

        # Set and initialize the fields to prepare for construction.
        S0 = firstpos(input_regex.tree)
        DStates, marker, namer = [('S0', S0)], 0, 0
        self.alphabet = input_regex.alphabet
        if '~' in self.alphabet:
            self.alphabet.remove('~')
        self.table = {}
        self.states = []
        self.initial, self.acceptings = 'S0', set()

        # Iteratively construct the transition table from FOLLOWPOS infos.
        # Here, DFA state "U" is the set of several position numbers, and
        # "name_U" is the actual name to be stored in transtion table for
        # this DFA state U.
        while (marker < len(DStates)):
            name_U, U = DStates[marker]
            self.table[name_U] = dict([(a, set()) for a in self.alphabet])
            self.states.append(name_U)
            if '#' in [input_regex.index[i] for i in U]:    # True iff U is
                self.acceptings.add(name_U)                 # accepting
            for a in self.alphabet:
                V = set()
                for pos in U:
                    if pos not in followpos:
                        followpos[pos] = set()
                    if input_regex.index[pos] == a:
                        V |= followpos[pos]
                if len(V) > 0:
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
            self.table[name_U] = dict([(a, set()) for a in self.alphabet])
            self.states.append(name_U)
            if len(U & input_nfa.acceptings) > 0:   # True iff U is accepting
                self.acceptings.add(name_U)
            for a in self.alphabet:
                V = input_nfa.epsClosure(input_nfa.move(U, a))
                if len(V) > 0:
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

    def minimalDFA(self):
        """DFA minimization.

        Produces a minimized DFA which is equivalent to the original one, by
        the method of group partitioning. Will return a minimized copy
        instead of modifying itself.

        Returns:
            DFiniteAutomata, which is the minimized one.
        """

        # Make a deep copy of self.
        min_dfa = deepcopy(self)

        # Conduct minimization by repeatedly partitioning the state groups.
        # Initially there are two groups, one containing all accepting
        # states and another containing all other states. Then, iterate over
        # all the groups and split that group into smaller ones according to
        # their transtions.
        partition = [self.acceptings, set(self.states)-self.acceptings]
        while True:
            change_flag = False
            new_partition = []
            for group in partition:
                dest = dict([(s, dict([(a, self.move(s, a))
                       for a in self.alphabet])) for s in group])
                same = dict([(s, dict([(s, True)
                       for s in group])) for s in group])
                marked = dict([(s, False) for s in group])
                for s1 in group:        # Pass 1, judge whether in same group
                    for s2 in group:    # for every pair of states in group.
                        for a in self.alphabet:
                            for check_group in partition:
                                if len(dest[s1][a] & check_group) != \
                                   len(dest[s2][a] & check_group):
                                    same[s1][s2] = False
                                    change_flag = True
                                    break
                for s1 in group:        # Pass 2, extract sub-groups and then
                    if not marked[s1]:  # add into the new partition.
                        new_group = set()
                        for s2 in group:
                            if not marked[s2] and same[s1][s2]:
                                marked[s2] = True
                                new_group.add(s2)
                        new_partition.append(new_group)
            partition = new_partition
            if not change_flag:
                break

        # Generate updated transtion table and states information for the
        # minimized DFA, then return this minimized copy.
        state_dict, count = {}, 0
        for S in partition:
            state_dict['S'+str(count)] = S
            count += 1
        min_dfa.acceptings, min_dfa.states = set(), []
        for s in state_dict:
            min_dfa.table[s] = dict([(a, set()) for a in self.alphabet])
            if self.initial in state_dict[s]:
                min_dfa.initial = s
            if len(self.acceptings & state_dict[s]) > 0:
                min_dfa.acceptings.add(s)
            for a in self.alphabet:
                for s_end in state_dict:
                    if len(self.table[list(state_dict[s])[0]][a] & \
                       state_dict[s_end]) > 0:
                        min_dfa.table[s][a] = {s_end}
                        break
        min_dfa.states = sorted(list(state_dict.keys()))
        return min_dfa

if __name__ == '__main__':
    print(DFiniteAutomata('../input/DFA'))
    print(DFiniteAutomata(nfa.NFiniteAutomata('../input/NFA')))

    rexpr = ere.Regex('(a|~)*b*a|ba')
    print(rexpr)
    print(DFiniteAutomata(rexpr))

    min_dfa = DFiniteAutomata(rexpr).minimalDFA()
    print(min_dfa)
    print(min_dfa.simulate('aabbbaba', verbose=True))
    print(min_dfa.simulate('aaaabba'))
