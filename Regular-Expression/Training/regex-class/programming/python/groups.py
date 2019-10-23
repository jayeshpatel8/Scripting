# groups.py

import re

s = 'john@example.com'

re1 = re.compile(r'''
    ^
    (\w+)     # user
    @
    (\w+)     # left part of domain
    \.
    (\w+)     # right part of domain
    $
    ''', re.X)

# like //g
m = re1.search(s)

if m:
    print('MATCH!')
    print('match object:', m)
    print('all groups:', m.groups())
    print('group 0:', m.group(0))
    print('group 1:', m.group(1))
    print('group 2:', m.group(2))
    print('loop through the groups:')
    for group in m.groups():
        print('    ', group)
