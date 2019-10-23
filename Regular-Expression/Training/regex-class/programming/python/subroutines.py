# subroutines.py

# sudo pip3 install regex
import regex

s = '''
Name: John Doe
Phone: +1 312 555 1212
Email: john@doe.org
'''

re1 = regex.compile('''
    (?(DEFINE)
      (?<NAME>  \w+ \s \w+               )
      (?<PHONE> \+ (?: \d \s? ){6,14} \d )
      (?<EMAIL> [\w.+-]+ @ [a-z0-9.-]+   )
    )

    ^ Name:  \s (?&NAME)  $ \s
    ^ Phone: \s (?&PHONE) $ \s
    ^ Email: \s (?&EMAIL) $ \s
    ''', regex.X | regex.M | regex.I)

m = re1.search(s)
if (m):
    print('MATCH!')
    print(m)

