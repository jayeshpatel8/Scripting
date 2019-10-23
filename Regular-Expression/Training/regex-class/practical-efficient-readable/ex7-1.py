# ex7-1.py

import regex

dates = [
'02-02-2019',
'02-22-2019',
'12-02-2019',
'12-22-2019'
]

re1 = regex.compile('''

    # REGEX GOES HERE

    ''', regex.X)

for date in dates:
    m = re1.search(date)
    if (m):
        print('MATCH!')
        print(m)

