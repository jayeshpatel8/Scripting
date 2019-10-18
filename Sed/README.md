# FindReplaceTraceFunction_Sed  
#### For FindReplaceTraceFunction_Sed_V2 Go down further

Replaces the matched string specified by (search_str) with (replace_str) if its inside any function
 search_str & replace_str are also a function name
 Find search_str currently inside which function and Line Number
 Prepare msg_id = $("functionname" "_" "line Nuber", ") 
 Add this prepared msg_id as a first parameter to matched search_str
 output file : file_name.temp cotains replaced text


*************************************************************************
## Example: ./FindReplaceTraceFunction_Sed test.c trace_print TRACE_INFO
*************************************************************************

*************************************************************************
## Input file: test.c
*************************************************************************
void my_test_fn  (void * p, void (*fp)(int))
{

  trace_print("this is a test");
  trace_print("this is a test 2");
}

  trace_print("this is a test 3");
  trace_print("this is a test 4");

// This is a second Test function
void my_test_fn2(void * p, void *fp) {
  if (!p)
  {
    if (!fp)
    {
      trace_print("this is a test fn 2 %d %d \n",*fp,*p);
    }
  }
}

trace_print(" This shall not be changed ");
void My_test_funciton(void* p, int q,char arr)
{
  trace_print("this is a test 5");
    trace_print("this is a test 6");
  trace_print( "Replace this fn  %d %d %c ",*p,q, *arr);
}



*************************************************************************
## Output file: test.c.temp

*************************************************************************

void my_test_fn  (void * p, void (*fp)(int))
{

  TRACE_INFO(MY_TEST_FN_4,"this is a test");
  TRACE_INFO(MY_TEST_FN_5,"this is a test 2");
}

  trace_print("this is a test 3");
  trace_print("this is a test 4");

// This is a second Test function
void my_test_fn2(void * p, void *fp) {
  if (!p)
  {
    if (!fp)
    {
      TRACE_INFO(MY_TEST_FN2_17,"this is a test fn 2 %d %d \n",*fp,*p);
    }
  }
}

trace_print(" This shall not be changed ");
void My_test_funciton(void* p, int q,char arr)
{
  TRACE_INFO(MY_TEST_FUNCITON_25,"this is a test 5");
    TRACE_INFO(MY_TEST_FUNCITON_26,"this is a test 6");
  TRACE_INFO(MY_TEST_FUNCITON_27, "Replace this fn  %d %d %c ",*p,q, *arr);
}


*************************************************************************
## diff of input and output file

*************************************************************************

diff --git a/test.c b/test.c.temp
index 6b8d4636bb85..20e7a0870ed7 100644
--- a/test.c
+++ b/test.c.temp
@@ -1,8 +1,8 @@
 void my_test_fn  (void * p, void (*fp)(int))
 {
   
-  trace_print("this is a test");
-  trace_print("this is a test 2");
+  TRACE_INFO(MY_TEST_FN_4,"this is a test");
+  TRACE_INFO(MY_TEST_FN_5,"this is a test 2");
 }
 
   trace_print("this is a test 3");
@@ -14,7 +14,7 @@ void my_test_fn2(void * p, void *fp) {
   {
     if (!fp)
     {
-      trace_print("this is a test fn 2 %d %d \n",*fp,*p);
+      TRACE_INFO(MY_TEST_FN2_17,"this is a test fn 2 %d %d \n",*fp,*p);
     }
   }
 }
@@ -22,9 +22,9 @@ void my_test_fn2(void * p, void *fp) {
 trace_print(" This shall not be changed ");
 void My_test_funciton(void* p, int q,char arr)
 {
-  trace_print("this is a test 5");
-    trace_print("this is a test 6");
-  trace_print( "Replace this fn  %d %d %c ",*p,q, *arr);
+  TRACE_INFO(MY_TEST_FUNCITON_25,"this is a test 5");
+    TRACE_INFO(MY_TEST_FUNCITON_26,"this is a test 6");
+  TRACE_INFO(MY_TEST_FUNCITON_27, "Replace this fn  %d %d %c ",*p,q, *arr);
 }
=================================================================================

## FindReplaceTraceFunction_Sed_V2     
                
=================================================================================

*************************************************************************
Example: ./FindReplaceTraceFunction_Sed_V2 test.c trace_print TRACE_INFO
*************************************************************************
Usage ./FindReplaceTraceFunction_Sed_V2 fileName SearchString ReplaceString : Output file filename.temp
Defaults: SearchString=trace_print ReplaceString=TRACE_INFO
           Replaces the matched string specified by (search_str) with (replace_str) if its inside any function          
           Find currently its inside which function and Number of time serach_str found in fn                           
           Prepare message_id = functionname _ No of time search_str found till now inside current function ,  
           Add this prepared message_id as a first parameter to matched search_str                                       
           output file : file_name.temp cotains replaced text                                                            
           Input to Script:                                                                                          
                void My_test_funciton(void\* p, int q,char arr)                                                           
               {                                                                                                         
                trace_print(this is a test 5);                                                                         
                  trace_print(this is a test 6);                                                                       
                trace_print( Replace this fn %d %d %c ,*p,q, *arr);                                                   
               }                                                                                                         
           Output of Script:                                                                                         
              void My_test_funciton(void* p, int q,char arr)                                                             
              {                                                                                                          
               TRACE_INFO(MY_TEST_FUNCITON_1,this is a test 5);                                                        
                 TRACE_INFO(MY_TEST_FUNCITON_2,this is a test 6);                                                      
               TRACE_INFO(MY_TEST_FUNCITON_3, Replace this fn %d %d %c ,*p,q, *arr);                                  
              }
