# *pREFA* Project
Presentation tool for Regular Expressions and Finite Automatas.

## Description
***pREFA*** (*Presentation tools for Regular Expressions & Finite Automatas*) is a presentation tool (*pre*) for Regular Expressions (*RE*) and Finite Automatas (*FA*), aiming at RE / NFA / DFA construction, analysis & displaying.

### Functions Established
1. Read and Analyze Regular Expressions
    - Construct and show the syntax tree structure of the RE.
    - Do position number marking.
    - Extended RE symbols and notations.
2. Build Finite Automatas
    - Build NFA / DFA from an RE or a formatted source file.
    - Conversion from NFA to DFA using *Subset Construction*.
    - DFA minimization
3. Finite Automatas Display.
    - Show an FA in the form of pretty formatted transition table.
    - Simulate the checking process on a given string, and get the result.

### Current Version
[ ver 1.1.0 ]

### Authors
- Authors: Jose, Robert & King
- Contact: huguanzhou123@sina.com

## Installation

### Python Library Package Distribution
Install with `pip3`. The package name is `prefa` (all lower cases).
```bash
pip3 install prefa
```
Then you can `import` and use this package in *Python3*.

## Tutorial

### Prerequisites

#### RE Specifications
Normal Regular Expressions follow these specifications:

Notation | Meaning
:-: | :-:
`~` | Put an empty String here (epsilon)
`a` | Put a character `a` here
`r1`&#124;`r2` | Either what `r1` or `r2` generates can appear here
`r1r2` | What `r1`'s generates concatenates with `r2`'s
`r*` | *Kleen Closure* of what `r` generates

The following Extended Regular Expression notation shorthands are also supported:

Notation | Meaning
:-: | :-:
`[a-zA-Z]` | Anyone in range [a, z] or [A, Z]
`r+` | *Positive Closure* of what r generates
`r?` | What r generates appear once or not

> **All keyword characters (i.e. `~|()[]-+?*`) CANNOT be used as a character in the alphabet. Any other single character will be considered as a valid character.**

The precedence of RE symbols are: `?` = `*` = `+` > *Concatenation* > `|`. All binary-connection symbols are *Left-associative*.

#### FA Source Format
A Finite Automata source file follows the following transition table format:
    
  - First title row is also the alphabet, `~` colomn is optional.
  - First title column is also the states set.
  - Every inner line gives the `move` set (i.e. GOTO set) from a state, when input is a char symbol:
      - `-` means empty transition.
      - Single-transition do not need `{}`s.
      - Multi-transitions are recommended to have `{}`s.
  - State attributes can appear at the end of every line:
      - Empty means no special attributes.
      - `i` means *Initial*.
      - `a` means *Accepting* (There can be multiple accepting states).
      - `ia` can appear simultaneously, meaning *Initial & Accepting*.

```
           a        b        c        ~ 
q0         -        -        -  {q1,q2}   i
q1        q1  {q2,q3}        -        -   
q2   {q1,q3}       q2        -        -   
q3         -        -       q3        -   a
```

### Use as Python Library
This *pREFA* package can be imported as name `prefa`, and it contains the following modules (so use `from prefa import [MOD]` to import the modules you need):

1. `re`: Basic Regular Expressions
2. `fa`: Finite Automata prototype
3. `dfa`: Deterministic Finite Automata construction
4. `nfa`: Non-deterministic Finite Automata construction

#### Regular Expressions
To construct a Regular Expression from a string, and display its structure, do:
```
>>> from prefa import re
>>> rexpr = re.Regex('(~|a)bc*e')
>>> print(rexpr)
Original:  (~|a)bc*e
Augmented: ((~|a)-b-c*-e)-#
                        ____-_
                       /      \
                ______-_      5,#
               /        \
          ____-____     4,e
         /         \
    ____-_         _*
   /      \       /
  |_      2,b   3,c
 /  \
~   1,a

>>> rexpr = re.Regex('a+(a|~)?[0-2]?')  # Extended RE notations are also supported.
>>> print(rexpr)
Original:  a+(a|~)?[0-2]?
Augmented: (a-(a)*-((a|~)|~)-((0|1|2)|~))-#
                            ____________________-_
                           /                      \
              ____________-________________       7,#
             /                             \
      ______-________                   ____|
     /               \                 /     \
   _-____           __|           ____|_      ~
  /      \         /   \         /      \
1,a      _*      _|     ~      _|_      6,2
        /       /  \          /   \
      2,a     3,a   ~       4,0   5,1
```

#### NFAs
To generate a Non-deterministic Finite Automata and show its transition table, you can do so from a source file, or a `Regex` instance:
```
>>> from prefa import nfa
>>> my_nfa = nfa.NFiniteAutomata('input/NFA')
>>> print(my_nfa)
           a        b        c        ~ 
q0         -        -        -  {q1,q2}   i
q1        q1  {q2,q3}        -        -   
q2   {q1,q3}       q2        -        -   
q3         -        -       q3        -   a

>>> my_nfa = nfa.NFiniteAutomata(Regex('(~|a)bc*e'))
>>> print(my_nfa)
           a        b        c        e        ~
s0        s1        -        -        -       s1   i
s1         -       s2        -        -        -
s2         -        -        -        -  {s3,s5}
s3         -        -       s4        -        - 
s4         -        -        -        -  {s3,s5}   
s5         -        -        -       sf        -   
sf         -        -        -        -        -   a

```

#### DFAs
To generate a Deterministic Finite Automata and show its transition table, you can do so from a source file, a `Regex` instance, or an `NFiniteAutomata` instance (here happens NFA to DFA conversion):
```
>>> from prefa import dfa
>>> my_dfa = dfa.DFiniteAutomata('input/DFA')
>>> print(my_dfa)
      a   b   c 
S0   S1  S2   -   i
S1   S3  S2  S4   a
S2   S1  S5  S4   a
S3   S3  S2   -   
S4    -   -  S4   a
S5   S1  S5   -   

>>> my_dfa = dfa.DFiniteAutomata(Regex('(~|a)bc*e'))
>>> print(my_dfa)
      a   b   c   e 
S0   S1  S2   -   -   i
S1    -  S2   -   -   
S2    -   -  S2  S3   
S3    -   -   -   -   a

>>> my_dfa = dfa.DFiniteAutomata(my_nfa)    # `my_nfa` is the NFA from previous example
>>> print(my_dfa)
      a   b   c   e 
S0   S1  S2   -   -   i
S1    -  S2   -   -   
S2    -   -  S3  S4   
S3    -   -  S3  S4   
S4    -   -   -   -   a

```

#### DFA Minimization
To minimize a DFA, do:
```
>>> my_dfa = DFiniteAutomata(Regex('(a|~)*b*a|ba'))
>>> min_dfa = my_dfa.minimalDFA()
>>> print(min_dfa)
      a   b 
S0    -   -   a
S1   S1  S2   a
S2   S0  S2   
S3   S1  S2   i

```

#### Check Simulation
To simulate the checking process of a Finite Automata on a given input string, do (can simulate on both DFAs or NFAs):
```
>>> print(min_DFA.simulate('aaaabba'))
True
>>> result = min_DFA.simulate('aabbbaba', verbose=True)   # Set `verbose` to show details step by step
  0:       S3
  1: --a-> S0
  2: --a-> S0
  3: --b-> S2
  4: --b-> S2
  5: --b-> S2
  6: --a-> S1
  7: --b-> ERROR

>>> print(result)
False
```

## Documentation
All the source codes are well-documented in the standard *Google Python Standard*. Therefore, for further informations on module contents and their usage, simply use the `help()` function in Python3, or any other *docstring* extraction tools.
