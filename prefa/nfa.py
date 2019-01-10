from prefa import fa, re
# import fa, re

class NFiniteAutomata(fa.FiniteAutomata):
    """Non-determinsitic Finite Automata child class.
    
    Can be initialized from a formatted source file or a Regular Expression.
    Representation structure is just like FiniteAutomata parent class, except
    that '~' is considered an epsilon here rather than a normal symbol. Will
    support epsilon closure calculation.

    Attributes:
        initial    - str , the initial state
        acceptings - set , set of acccepting states
        table      - dict, the transition table
        alphabet   - list, alphabet in sorted order
        states     - list, list of all states in sorted order
    """

    def __init__(self, input):
        if type(input) == str:      # 1. Input from source file
            self._initFromFile(input)
        else:                       # 2. Input from a regex
            self._initFromRE(input)

    def _initFromRE(self, input_regex):
        """Initializer for a Regular Expression.

        Takes a Regular Expression, builds an NFA from bottom-up, using
        Thompson's construction method.

        Args:
            input_regex - str, input Regular Expression
        """

        def calcTable(node):
            """Generates the state table of sub-regex rooted at node.

            Recursively constructs the transition table by a traversal of the
            Regular Expression's binary syntax tree. Follows the Thompson's
            construction method when building. The returned table is not full,
            which means that empty transitions are not inserted as '-' yet.

            Args:
                node - Node, current root of a regex

            Returns:
                (table, count) - tuple, state table and name count
            """

            # Reached a leaf node, then directly return with the most simple
            # transition table. 
            if node.value in input_regex.alphabet:
                return {'s0': {node.value: {'sf'}}, 'sf': {}}, 1

            # Meet '*' node, then add a new initial state and a new accepting
            # state, change original initial and accepting state into two
            # newly named states, adds epsilon transitions for them. Do not
            # forget to update names refering to old 's0' / 'sf' to their new
            # names.
            elif node.value == '*':
                table, count = calcTable(node.left)
                name_i, name_f = 's' + str(count), 's' + str(count+1)
                for s in table:     # Update old names to new ones
                    for a in table[s]:
                        if 's0' in table[s][a]:
                            table[s][a].remove('s0')
                            table[s][a].add(name_i)
                        if 'sf' in table[s][a]:
                            table[s][a].remove('sf')
                            table[s][a].add(name_f)
                table[name_i] = table['s0']     # Transplant to newly named
                table[name_f] = table['sf']     # inner states
                if '~' in table[name_f]:
                    table[name_f]['~'] |= {name_i, 'sf'}
                else:
                    table[name_f]['~']  = {name_i, 'sf'}
                table['s0'] = {'~': {name_i, 'sf'}}     # Make new 's0' / 'sf'
                table['sf'] = {}
                return table, count + 2
            
            # Meet '-' node, then concatenate its left child with its right
            # child, by transplanting every state in right child into a newly
            # named state into the left child.
            elif node.value == '-':
                if node.right.value == '#':   # Neglect '#' symbol in tree
                    return calcTable(node.left)
                table_l, count_l = calcTable(node.left)
                table_r, count_r = calcTable(node.right)
                for s in table_r:   # Update old names in right child
                    for a in table_r[s]:
                        tmp_set = table_r[s][a]
                        for dst in tmp_set - {'sf'}:
                            table_r[s][a].remove(dst)
                            table_r[s][a].add('s' + str(int(dst[1:]) + count_l))
                for s in table_l:   # Update old 'sf' names in left child
                    for a in table_l[s]:
                        if 'sf' in table_l[s][a]:
                            table_l[s][a].remove('sf')
                            table_l[s][a].add('s' + str(count_l))
                count = count_l     # Insert right child entries into left
                for i in range(count_r):
                    table_l['s'+str(count)] = table_r['s'+str(i)]
                    count += 1
                for a in table_l['sf']:
                    if a in table_l['s'+str(count_l)]:
                        table_l['s'+str(count_l)][a].update(table_l['sf'][a])
                    else:
                        table_l['s'+str(count_l)][a] = table_l['sf'][a]
                table_l['sf'] = table_r['sf']
                return table_l, count

            # Meet '|' node, then merge the two initial nodes and two
            # accepting nodes from left and right child. States in right child
            # are also renamed and inserted into elft child.
            elif node.value == '|':
                table_l, count_l = calcTable(node.left)
                table_r, count_r = calcTable(node.right)
                for s in table_r:   # Update old names in right child
                    for a in table_r[s]:
                        tmp_set = table_r[s][a]
                        for dst in tmp_set - {'s0', 'sf'}:
                            table_r[s][a].remove(dst)
                            table_r[s][a].add('s' + str(int(dst[1:]) +
                                              count_l - 1))
                for i in range(1, count_r):     # Insert right into left
                    table_l['s'+str(count_l)] = table_r['s'+str(i)]
                    count_l += 1
                for a in table_r['s0']:     # Merge two s0
                    if a in table_l['s0']:
                        table_l['s0'][a].update(table_r['s0'][a])
                    else:
                        table_l['s0'][a] = table_r['s0'][a]
                for a in table_r['sf']:     # Merge two s0
                    if a in table_l['sf']:
                        table_l['sf'][a].update(table_r['sf'][a])
                    else:
                        table_l['sf'][a] = table_r['sf'][a]
                return table_l, count_l

        # Generate and complete table at root recursively, then collects all
        # other fields.
        self.alphabet = input_regex.alphabet
        if '~' not in self.alphabet:
            self.alphabet.append('~')
        self.table = calcTable(input_regex.tree)[0]
        for s in self.table:
            for a in self.alphabet:
                if a not in self.table[s]:
                    self.table[s][a] = set()
        self.states = sorted(self.table.keys())
        self.initial, self.acceptings = 's0', {'sf'}

if __name__ == '__main__':
    print(NFiniteAutomata('../input/NFA'))
    
    rexpr = re.Regex('(a|~)bc*')
    print(rexpr)
    print(NFiniteAutomata(rexpr))

    my_nfa = NFiniteAutomata(re.Regex('[a-c]+b*|a'))
    print(my_nfa)
    print(my_nfa.simulate('acbabbb', verbose=True))
    print(my_nfa.simulate('ad'))
