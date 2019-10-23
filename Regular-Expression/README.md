
## Lists the functions that matches search string
#### Explaination: 
     (?=               ### Start of Look forward for -
         (\b\w{7,}\b)  ### Group 1(function name): Check for word of more than 7 char (function name)
         \ *           ### Optional space character
         \(            ###  Check for opening brace of Function
         [ ^           ###  if one or more non matching character
             <
             \
             /
             :
             ;
             >
             !
             {
             }
             =
             &
             |
             \"
             ]+?
         \)           ###  Check for Closing brace of Function
         \s*          ### Optional space character
         {            ### Check for opening/first curly brace of Function
         [^}]+        ### Check for Closing/last curly brace of Function
         (ASSERT|LOG_EVENT|printf)  ### Search string inside function
     )                ### End of Look forward
     \1               ### if there is a match then print Group 1(function name)

#### Python /gimx
 	(?= (\b\w{7,}\b)\ *\([^<\/\\:;>!{}=&|\"]+?\)\s*{[^}]+(ASSERT|LOG_EVENT|printf))\1

####  PCRE  /gimx
	(?= (\b\w{7,}\b)\ *\([^<\/:;>!{}=&|\"]+?\)\s*{[^}]+(ASSERT|LOG_EVENT|printf))\1

### For example:   
 
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
