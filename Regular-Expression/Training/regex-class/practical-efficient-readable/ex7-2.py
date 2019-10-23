# ex7-2.py

import regex

numerals = [
'MCM',
'LXXX',
'XVII',
'MMXIX',
'III',
'xlvii'
]

re1 = regex.compile('''
    ^ [MDCLXVI]+ $
    ''', regex.X | regex.I)

for numeral in numerals:
    m = re1.search(numeral)
    if (m):
        print(numeral + ' MATCH!')

