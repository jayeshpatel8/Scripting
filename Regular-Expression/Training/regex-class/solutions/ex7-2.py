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
    (?(DEFINE)
      (?<MUSTHAVE> (?=[MDCLXVI]) ) # one of these roman numerals must exist
      (?<MS>       M*            ) # zero or more Ms
      (?<CDSECTION> (?: 
                      C [MD] |     # C then either M or D
                      D? C{0,3}    # optional D and up to 3 C
                    ) )
      (?<XLSECTION> (?: 
                      X [CL] |     # X then either C or L
                      L? X{0,3} )  # optional L and up to 3 X
                    )
      (?<IVSECTION> (?: 
                      I [XV] |     # I then either X or V
                      V? I{0,3} )  # optional V and up to 3 I
                    )
    )

    ^ 
      (?&MUSTHAVE)
      (?&MS)
      (?&CDSECTION)
      (?&XLSECTION)
      (?&IVSECTION)
    $
    ''', regex.X | regex.I)

for numeral in numerals:
    m = re1.search(numeral)
    if (m):
        print(numeral + ' MATCH!')

