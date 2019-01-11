from prefa import dfa, ere

class Lexer(object):
    """Simple example of a toy lexer.

    Using a bunch of recognizers (which are minimal DFAs) to perform very
    simple lexing analysis.
    """

    def __init__(self, rules):
        self.recognizers = dict([(r, dfa.DFiniteAutomata(ere.Regex(rules[r])) \
                                     .minimalDFA()) for r in rules])

    def tokenize(self, input_str):
        """Tokenize the input string.

        Tokenize the input string according to the lexing rules. First split
        the input according to whitespaces, then check every element using
        the recognizers.

        Args:
            input_str - str, the string to perform lexing

        Returns:
            output_str - str, the result of tokenizing
        """
        elements, output_str = input_str.strip().split(), ''
        for s in elements:
            match_flag = False
            for r in self.recognizers:
                if self.recognizers[r].simulate(s):
                    output_str += '%10s:  %s\n' % (r, s)
                    match_flag = True
                    break
            if not match_flag:  # Will raise ValueError if no matching.
                raise ValueError('No matching rule for %r' % s)
        print(output_str)

if __name__ == '__main__':
    rules = {
        'L-FORMAL': '<',
        'R-FORMAL': '>',
        'L-BODY':   '{',
        'R-BODY':   '}',
        'BOOL-AND': '&&',
        'COMMA':    ',',
        'ASSIGN':   '<=',
        'DEF':      'def',
        'SELF':     'self',
        'RET':      'return',
        'INT':      '[0-9]+',
        'ID':       '[A-Z]+'
    }
    program = '''
            def AND < self , X , Y > {
                X <= 1
                Y <= 99
                return X && Y
            }
        '''
    Lexer(rules).tokenize(program)
