# *pREFA* Project
Presentation tool for Regular Expressions and Finite Automatas.

## Description
***pREFA*** (*Presentation tools for Regular Expressions & Finite Automatas*) is a presentation tool (*pre*) for Regular Expressions (*RE*) and Finite Automatas (*FA*), aiming at RE / NFA / DFA construction, analysis & displaying.

#### Functions Established
1. Read and Analyze Regular Expressions
    - Construct and show the syntax tree structure of the RE
    - Do position number marking
2. Build Finite Automatas
    - Build NFA / DFA from an RE or a formatted source file
    - Conversion from NFA to DFA
3. Finite Automatas Display
    - Show an FA in the form of pretty formatted transition table

#### Current Version
[ ver 0.0.2 ]

#### Authors
- Authors: Jose, Robert & King
- Contact: huguanzhou123@sina.com

## Installation

#### Python Library Package Distribution
Install with `pip3`. The package name is `prefa` (all lower cases).
```bash
sudo pip3 install prefa
```
Then you can `import` and use this package in *Python3*.

#### Command Line Tool Distribution
NOT AVAILABLE NOW

## Tutorial

#### Prerequisites
- In Regular Expression strings, `~` represents epsilon and SHOULD NOT be used as a normal char symbol.
- A *minus* symbol `-` is used to represent a *Concatenation*, and a `#` is used as an end symbol.
- A Finite Automata source file follows the following format (like a transition table):
    - First row title line is also the alphabet, `~` colomn is optional.
    - First title column is also the states set.
    - Every inner line gives the `move` set from a state, when input is a char symbol:
        - `-` means empty transition.
        - Single transition do not need `{}`s.
        - Multi transitions are recommended to have `{}`s.
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
- DFA Minimizing, FA GUI displaying and simulation, & Extended RE operators are not yet supported :(

#### Use as Python Library
This *pREFA* package can be imported as name `prefa`, and it contains the following modules:

1. `re`: Basic Regular Expressions
2. `fa`: Finite Automata prototype
3. `dfa`: Deterministic Finite Automata construction
4. `nfa`: Non-deterministic Finite Automata construction

To construct a Regular Expression from a string, and display its structure, do:
```python
>>> from prefa import re
>>> regex = re.Regex('(~+a)bc*e')
>>> print(regex)
(~+a)-b-c*-e-#
                        ____-_
                       /      \
                ______-_      5,#
               /        \
          ____-____     4,e
         /         \
    ____-_         _*
   /      \       /
  +_      2,b   3,c
 /  \
~   1,a

```

To generate a Finite Automata from a source file, and show its transition table, do:
```python
>>> from prefa import fa
>>> my_fa = fa.FiniteAutomata('input/NFA')  # `input/NFA` is the source file path
>>> print(my_fa)
           a        b        c        ~ 
q0         -        -        -  {q1,q2}   i
q1        q1  {q2,q3}        -        -   
q2   {q1,q3}       q2        -        -   
q3         -        -       q3        -   a

```

To generate a Non-deterministic Finite Automata, you can do so from a source file, or a Regular Expression:
```python
>>> from prefa import nfa
>>> my_nfa = nfa.NFiniteAutomata('input/NFA')
>>> print(my_nfa)
           a        b        c        ~ 
q0         -        -        -  {q1,q2}   i
q1        q1  {q2,q3}        -        -   
q2   {q1,q3}       q2        -        -   
q3         -        -       q3        -   a

>>> my_nfa = nfa.NFiniteAutomata(regex)     # `regex` is the RE from previous example
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

To generate a Deterministic Finite Automata, you can do so from a source file, or a Regular Expression, or an `NFiniteAutomata` instance (here happens NFA $\rightarrow$ DFA conversion):
```python
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

>>> my_dfa = dfa.DFiniteAutomata(regex)     # `regex` is the RE from previous example
>>> print(my_dfa)
      a   b   c   e 
S0   S1  S2   -   -   i
S1    -  S2   -   -   
S2    -   -  S2  S3   
S3    -   -   -   -   a

>>> my_dfa = dfa.DFiniteAutomata(my_nfa)    # `my_nfa` is the NFA from previous example
>>> print(my_dfa)   # You can see that Minimization is not done yet :(
      a   b   c   e 
S0   S1  S2   -   -   i
S1    -  S2   -   -   
S2    -   -  S3  S4   
S3    -   -  S3  S4   
S4    -   -   -   -   a

```
