#!/usr/bin/python

#Inspiré du lecteur de S-expressions de lis.py de P. Norvig
def read_from_tokens(s):
	tokens=s.replace('(',' ( ').replace(')',' ) ').split()
    "Read an expression from a sequence of tokens."
    if len(tokens) == 0:
        raise SyntaxError('unexpected EOF while reading')
    token = tokens.pop(0)
    if '(' == token:
        L = []
        while tokens[0] != ')':
            L.append(read_from_tokens(tokens))
        tokens.pop(0) # pop off ')'
        return L
    elif ')' == token:
        raise SyntaxError('unexpected )')
    else:
        return token
