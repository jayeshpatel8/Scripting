### $python ../PatchYourFunction.py -h 
### usage: PatchYourFunction.py [-h] [-d]

### optional arguments:
  ### -h, --help  show this help message and exit
  ### -d, --dir   Patch Function in current directory
  
  Automation to patch your 100/1000s of files:
  
  1) Patch & Repair Functions
  2) Verify the changes
  3) Add newly created strings's to Database
  4) Generate Report
  5) Find Duplicates
  
  - Patch & Repair Functions
    Patch:
          Replaces the matched string specified by (search_str) with (replace_str) if its inside any function
          As ctags limitations with multiple #defines to find the function names, it internally parses the Function name by itself

          Patch any of this string:
              search_str=['trace_printf','trace_printf2','trace_printf3','trace_print']
          Replace with one of this string:
              replace_str=["","TRACE_INFO","TRACE_ERROR","TRACE_WARNING","TRACE_DEBUG"]

          Find currently its inside which function and Number of time serach_str found in fn
          Prepare message_id = functionname _ No of time search_str found till now inside current function , 
          Add this prepared message_id as a first parameter to matched search_str    
          Example:
          trace_print("this is a test 5"); => TRACE_INFO(MY_TEST_FUNCTION_1,"this is a test 5");
    Repair:
         If any of replace_str string found, it will check it message name & correct (Number part) if needed

  - Verify the changes:
        Verification of Chages done by using git diff and diff utility and result will be printed.
        
        Diff Util    File Name      Total TP verified    Total TP Failed    Cnt1    Cnt2
        -----------  -----------  -------------------  -----------------  ------  ------
        Diff         test3.cpp                     18                  0       0       0
        Git-diff     test3.cpp                     18                  0       0       0
        #######   ***********  File: test3.cpp -Success - Verification ************** ############  

  - Add newly created strings's to Database:
        It will add newly defined messages to Database and create a report of it.
        db_created_msg_name.txt ==> All newly created message will be added to this log file
        db_err_msg_name.txt ==> All failed to create message will be added to this log file
        db_duplicate_msg_name.txt ==> All Duplicate message will be added to this log file while creattion.
        
  - **Generate Report**
  
       Report will be printed for all files with full details as below.
       
       | File Name   |   MaxMsgLen |   Total | Not Repl   | Skipped   | AddMsgDB   | DupMsgDB   | DiffTP   | Fail   | Cnt1   |
       | ----------- | ----------- | ------- | ---------- | --------- | ---------- | ---------- | -------- | ------ | ------ |
       | test.c      |          18 |       9 |            |           |            |            |          |        |        |
       | test1.c     |          18 |      12 |            |           |            |            |          |        |        |
       | test2.c     |          18 |      15 |            |           |            |            |          |        |        |
       | test3.cpp   |          19 |      18 |            |           |            |            |          |        |        |
       | Total       |          19 |      54 |   0        |   0       |   0        |   0        |   0      |   0    |   0    |

       
  ## Find Duplicates
      This will be useful to find any duplicate message without creation.
      >> Press Enter to "Check Duplicate Msg Name"...NO
  

 ## output file : file_name.temp cotains replaced text                                                     
  ## Input to Script:                                                                                       
       void My_test_function(void\* p, int q,char arr)                                                   
      {                                                                                                  
          trace_print("this is a test 5");                                                                  
          trace_print("this is a test 6");                                                                
          trace_print( "Replace this fn  %d %d %c ",*p,q, *arr);                                            
      }                                                                                                  
  ## Output of Script:                                                                                      
     void My_test_function(void* p, int q,char arr)                                                      
     {                                                                                                   
        TRACE_INFO(MY_TEST_FUNCTION_1,"this is a test 5");                                                 
        TRACE_INFO(MY_TEST_FUNCTION_2,"this is a test 6");                                               
        TRACE_INFO(MY_TEST_FUNCTION_3, "Replace this fn  %d %d %c ",*p,q, *arr);                           
     }
