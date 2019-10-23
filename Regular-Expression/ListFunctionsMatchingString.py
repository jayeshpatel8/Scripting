import re
import regex as re

SearchFor='ASSERT|LOG_EVENT|printf'

regex = r'''(?= (\b\w{7,}\b)\ *\([^<\/\\:;>!{}=&|\"]+?\)\s*{[^}]+(''' + SearchFor + r'''))\1'''

test_str = ("void Firmware1 (void * i){\n"
	"    printf();\n"
	"}\n"
	"void Firmware2 (void * i){\n"
	"    LOG_EVENT();\n"
	"}"
	"void Firmware3 (void * i){\n"
	"    ASSERT();\n"
	"}"  )

matches = re.finditer(regex, test_str, re.MULTILINE | re.VERBOSE | re.IGNORECASE)

for matchNum, match in enumerate(matches, start=1):
    print("Found the Match in Function {}:".format(match.group(1)))
    for groupNum in range(1, len(match.groups())):
        groupNum = groupNum + 1  
        print("\t\t\t\t\t {match}() has {group} ".format(group = match.group(groupNum),match = match.group()))
    print("\n")
