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
- Contemplate a way to output any bit string, not just the encodings of normalized lambda expressions

## Sources
- http://semarch.linguistics.fas.nyu.edu/barker/Iota/
- http://jwodder.freeshell.org/lambda.html
- http://en.wikipedia.org/wiki/Combinatory_logic
- http://en.wikipedia.org/wiki/De_Bruijn_index
- http://homepages.cwi.nl/~tromp/cl/cl.html
