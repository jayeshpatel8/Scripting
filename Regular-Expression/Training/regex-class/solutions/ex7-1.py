# ex7-1.py

import regex

dates = [
'02-02-2019',
'02-22-2019',
'12-02-2019',
'12-22-2019'
]

re1 = regex.compile('''
    (?(DEFINE)
      (?<TWODIGITS>  \d\d        )
      (?<MONTH>     (?&TWODIGITS) )
      (?<DAY>       (?&TWODIGITS) )
      (?<YEAR>      \d\d\d\d     )
    )

    ^ ((?&MONTH)) - ((?&DAY)) - ((?&YEAR)) $
    ''', regex.X)

for date in dates:
    m = re1.search(date)
    if (m):
        print('MATCH!')
        print(m)

