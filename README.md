# Jot interpreter

This is an interpreter for Jot, an extremely minimalistic programming language which is based on lambda calculus.

## How does it work?

Both the program and input are considered the input to the interpreter (binary string):

`1`

The Jot input is converted into the corresponding combinatory logic expression:

`I S K`

The combinatory logic expression is then converted into a lambda expression using de Bruijn indices (shown using backticks instead of parentheses):

    ``^1^^^``31`21^^2

The lambda expression is then reduced to normal form (this is where computation happens):

    ^^1

The normalized lambda expression is then encoded in binary:

`01000000100000110`

## TODO
- Consider implementing combinatory logic using trit strings, then attempt to find a one-point combinator which does not apply any arguments to an abstraction.
    - ```Sxyz -> ``xz`yz
    - ``Kxy -> x
    - Or use only the application operator ` and a one-point combinator X
    - Output is the normal form of the input CL expression
    - Every irreducible input is a quine

## Sources
- http://semarch.linguistics.fas.nyu.edu/barker/Iota/
- http://jwodder.freeshell.org/lambda.html
- http://en.wikipedia.org/wiki/Combinatory_logic
- http://en.wikipedia.org/wiki/De_Bruijn_index
- http://homepages.cwi.nl/~tromp/cl/cl.html
