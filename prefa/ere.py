# from prefa import bintree
import bintree

class Regex(object):
    """Class of a Regular Expression.

    Only supports single-char symbols in alphabet! Concatenations are
    represented with '-'. End symbol '#' will be added in EXPR, but will not
    be in ALPHABET. Binary syntax tree will be generated and position numbers
    will be marked.

    Notice that '~' is regarded as epsilon here, and will not get a position
    number during the marking process. That also means we cannot use `~` as a
    normal char symbol like 'a' / '0' in the input alphabet.

    Attributes:
        expr     - str , RE expression with concatenations as '-'
        tree     - Node, binary syntax tree of RE
        alphabet - list, alphabet in sorted order
        index    - dict, table recording posnumber-symbol pairs
    """

    def __init__(self, input_re_string):
        # TODO(jose): Check correctness of input RE.

        def doOperation(operator_stack, operand_stack):
            """Conducts an operation.

            Pops the stack top operator, then pops corresponding number of
            operands, do the operation, and push the result operand back into
            stack. Notice that '*' node's child is assigned to its left one.

            Args:
                operator_stack - list, stack of operators
                operand_stack  - list, stack of operands
            """
            op = operator_stack.pop()
            if op == '*':
                node = bintree.Node(op)
                node.left = operand_stack.pop()
                operand_stack.append(node)
            elif op == '-' or op == '|':
                node = bintree.Node(op)
                node.right = operand_stack.pop()
                node.left  = operand_stack.pop()
                operand_stack.append(node)

        def fetchPrevBlock(input_str):
            """Cut the last block off a RE string.

            A block can be either a single char, or a block of RE strings
            enclosed with '(' and ')', or a block of extended notation
            enclosed with '[' and ']'. This function cuts the last whole
            block off the input string.

            Args:
                input_str - str, string to extract the last block

            Returns:
                (remain_str, last_block) - tuple
            """
            assert(len(input_str) > 0)
            assert(input_str[-1] != '|' and input_str[-1] != '(')
            if input_str[-1] in '*+?':
                tail_symbol = input_str[-1]
                return fetchPrevBlock(input_str[:-1])[0], \
                       fetchPrevBlock(input_str[:-1])[1] + tail_symbol
            elif input_str[-1] == ')':
                last_block = input_str[-1]
                input_str = input_str[:-1]
                synch_count = 1
                while synch_count > 0:
                    c = input_str[-1]
                    input_str = input_str[:-1]
                    last_block = c + last_block
                    if c == ')':
                        synch_count += 1
                    elif c == '(':
                        synch_count -= 1
                return input_str, last_block
            elif input_str[-1] == ']':
                last_block = ''
                met_left = False
                while not met_left:
                    c = input_str[-1]
                    input_str = input_str[:-1]
                    last_block = c + last_block
                    if c == '[':
                        met_left = True
                return input_str, last_block
            else:
                return input_str[:-1], input_str[-1]

        def dealRange(input_str):
            """Deals with ranges notations.

            Expand the ranges notation at the end of input string to
            the tedious sequence of ors.

            Args:
                input_str - str, string to deal with

            Returns:
                output_str - str, string after expansion
            """
            extend_str = ''
            while input_str[-1] != '[':
                start, end = input_str[-3], input_str[-1]
                for asc in range(ord(start), ord(end)+1):
                    extend_str += chr(asc) + '|'
                input_str = input_str[:-3]
            extend_str = extend_str[:-1]
            return input_str[:-1] + '(' + extend_str + ')'

        # Expand Extended RE symbols first. This is the simplest way to
        # support these extended RE notations.
        self.ori_expr, re_string = input_re_string, ''
        for c in input_re_string:
            if c == '?':
                re_string, last_block = fetchPrevBlock(re_string)
                re_string += '(' + last_block + '|~)'
            elif c == '+':
                re_string, last_block = fetchPrevBlock(re_string)
                re_string += last_block + '(' + last_block + ')*'
            elif c == ']':
                re_string = dealRange(re_string)
            else:
                re_string += c

        # Insert '-' as concatenation indicator, and collects alphabet along
        # the process. Concatenation happens only when current char is a
        # symbol and previous char is not '|' / '('. End symbol '#' will also
        # be added.
        self.expr, self.alphabet = '', []
        for c in re_string:
            if c not in '()|*' and c not in self.alphabet:
                self.alphabet.append(c)
            if c not in ')|*' and len(self.expr) > 0 and \
               self.expr[-1] not in '(|':
                    self.expr += '-'
            self.expr += c
        if len(self.expr) > 0:
            self.expr = '(' + self.expr + ')-'
        self.expr += '#'
        self.alphabet.sort()

        # Construct binary syntax tree for RE. Overall process is just like
        # calculating in-fix expressions, but the difference is that every
        # operation will be a tree construction step.
        priority = {'(': 0, '|': 1, '-': 2, '*': 3}
        operator_stack, operand_stack = [], []
        for c in self.expr:
            if c not in '()|*-':    # True iff c is a symbol
                operand_stack.append(bintree.Node(c))
            elif c == '(':
                operator_stack.append(c)
            elif c != ')':          # True iff c is '|' / '-' / '*'
                while (len(operator_stack) > 0 and
                       priority[c] <= priority[operator_stack[-1]]):
                    doOperation(operator_stack, operand_stack)
                operator_stack.append(c)
            elif c == ')':
                while operator_stack[-1] != '(':
                    doOperation(operator_stack, operand_stack)
                operator_stack.pop()
        while len(operator_stack) > 0:
            doOperation(operator_stack, operand_stack)
        self.tree = operand_stack.pop()
        self.index = self.tree._markLeafPos()

    def __str__(self):
        return 'Original:  ' + self.ori_expr + '\nAugmented: ' + \
               self.expr + str(self.tree)

    def __repr__(self):
        return 'Regex({})'.format(self.expr)

if __name__ == '__main__':
    print(Regex('(~|a)bc*e'))
    print(Regex('(a|e)bc*'))
    print([Regex('a|c'), Regex('(0|1)*')])
    print(Regex('a+(a|~)?[0-2]?'))
