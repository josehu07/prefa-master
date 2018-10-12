from prefa.bintree import Node  # Binary tree data structure

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
        index    - dict, table recording pos number-symbol pairs
    """

    def __init__(self, input_re_string):

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
                node = Node(op)
                node.left = operand_stack.pop()
                operand_stack.append(node)
            elif op == '-' or op == '+':
                node = Node(op)
                node.right = operand_stack.pop()
                node.left  = operand_stack.pop()
                operand_stack.append(node)

        # Insert '-' as concatenation indicator, and collects alphabet along
        # the process. Concatenation happens only when current char is a
        # symbol and previous char is not '+' / '('. End symbol '#' will also
        # be added.
        self.ori_expr, self.expr = input_re_string, ''
        self.alphabet = []
        for c in input_re_string:
            if c not in '()+*':     # True iff c is a symbol
                if c not in self.alphabet:
                    self.alphabet.append(c)
                if len(self.expr) > 0 and self.expr[-1] not in '(+':
                    self.expr += '-'
            self.expr += c
        self.expr += '-#'
        # TODO(jose): Modify sort, let 'q2' < 'q10'
        self.alphabet.sort()

        # Construct binary syntax tree for RE. Overall process is just like
        # calculating in-fix expressions, but the difference is that every
        # operation will be a tree construction step.
        priority = {'(': 0, '+': 1, '-': 2, '*': 3}
        operator_stack, operand_stack = [], []
        for c in self.expr:
            if c not in '()+*-':    # True iff c is a symbol
                operand_stack.append(Node(c))
            elif c == '(':
                operator_stack.append(c)
            elif c != ')':          # True iff c is '+' / '-' / '*'
                while (len(operator_stack) > 0 and
                       priority[c] <= priority[operator_stack[-1]]):
                    doOperation(operator_stack, operand_stack)
                operator_stack.append(c)
            elif c == ')':
                while operator_stack[-1] != '(':
                    doOperation(operator_stack, operand_stack)
                operator_stack.pop()
            else:
                # TODO(jose): Error checking
                pass
        while len(operator_stack) > 0:
            doOperation(operator_stack, operand_stack)
        # TODO(jose): Error checking
        self.tree = operand_stack.pop()
        self.index = self.tree._markLeafPos()

    def __str__(self):
        # TODO(jose): Prettier format
        return self.expr + str(self.tree)

    def __repr__(self):
        return 'Regex({})'.format(self.expr)

if __name__ == '__main__':
    print(Regex('(a+e)bc*'))
    print([Regex('a+c'), Regex('(0+1)*')])
