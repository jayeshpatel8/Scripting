
## Lists the functions that matches search string

#### For PCRE: (?= (\b\w{7,}\b)\ *\([^<\/:;>!{}=&|\"]+?\)\s*{[^}]+(ASSERT|LOG_EVENT|printf))\1
#### For Python: (?= (\b\w{7,}\b)\ *\([^<\/\\:;>!{}=&|\"]+?\)\s*{[^}]+(ASSERT|LOG_EVENT|printf))\1
#### For example:   
 
SearchFor='ASSERT|LOG_EVENT|printf'

 test_str = ("void Firmware1 (void * i){\n"
	"    printf();\n"
	"}\n"
	"void Firmware2 (void * i){\n"
	"    LOG_EVENT();\n"
	"}"
	"void Firmware3 (void * i){\n"
	"    ASSERT();\n"
	"}"  )
--------
Output:
-------
#### Found the Match in Function Firmware1:
                     Firmware1() has printf

#### Found the Match in Function Firmware2:
                     Firmware2() has LOG_EVENT

#### Found the Match in Function Firmware3:
                     Firmware3() has ASSERT
