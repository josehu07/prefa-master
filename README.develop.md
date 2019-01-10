# Coding Standard
Mainly follows Google's Python3 coding style sheet (https://zh-google-styleguide.readthedocs.io/en/latest/google-python-styleguide/python_style_rules/), except for the following scenes:

- Format of an entry in Attributes, Args and Returns in docstrings are a bit different. Here is an example to follow:
```python
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
        ...
```
- Necessary vertical aligns are needed for prettier looking. Sorry for my rigidness, but hope you can withstand.
```python
if i in followpos:
    followpos[i] |= firstpos(node.left)
else:
    followpos[i]  = firstpos(node.left)
```
- Better naming standard. Details are as follows:
    - Variables:   `new_var_name`
    - Class names: `Regex(object)`
    - Functions:   `doThisOperation()`

# TODOs
Mark your TODO tasks with a comment like `# TODO(name): balabala` in the corresponding position in the code.

1. GUI presentation
2. Testing correctness of exiting functions
3. Error checking routines

# How to upload to *Pypi*
Install `setuptools` and `twine` libraries through `pip3`:
```bash
pip3 install setuptools
pip3 install twine
```

Install `twine` from `apt`:
```bash
sudo apt install twine
```

Move into the project directory, i.e. `prefa-master/`. Update version and develop status infos in `setup.py`, since any upload must issue a version update, or a name-race will happen.

Build the distribution package into `.whl` wheel by:
```bash
python3 setup.py bdist_wheel
```

Upload through `twine`, into account `Jose`:
```bash
twine upload dist/prefa-[Version]-py3-none-any.whl
Enter your username: Jose
Enter your password: # PASSWORD :)
```
