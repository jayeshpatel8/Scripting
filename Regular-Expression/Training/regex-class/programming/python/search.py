# search.py

import re

s = 'Python uses the re module'

if (re.search('re module', s)):
    print('MATCH 1!')

# re.match() only matches at the
# beginning of the string
# use re.search() instead
if (re.match('re module', s)):
    print('MATCH 2 - NOT!')

# can create a regex object and
# use it to search
re1 = re.compile(r'''
    ^
    .*
    (\s\w+)*
    $
    ''', re.X)

if (re1.search(s)):
    print('MATCH 3!')

