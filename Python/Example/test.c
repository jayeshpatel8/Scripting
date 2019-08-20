void my_test_fn1  (void * p, void (*fp)(int))
{

  trace_print("this is a test");
#if defined(TRACE_ON_1) && !defined(TRACE_ON_2) && !defined(TRACE_ON_3)
  trace_print("this is a test 2");
#endif
}

  trace_print("this is a test 3");
  trace_print("this is a test 4");
#if defined(TRACE_ON_1) && !defined(TRACE_ON_2) && !defined(TRACE_ON_3)
// This is a second Test function
void my_test_fn2(void * p, void *fp) {
  for (i = 0; i < XNS_MEM_OCH_MAX_BLOCKS; i++)
  {
      if (!p)
      {
        if (!fp)
        {
          for (i = 0; i < XNS_MEM_OCH_MAX_BLOCKS; i++)
          {
              if (!p)
              {
                if (!fp)
                {
                  trace_print("this is a test fn 2 %d %d \n",*fp,*p);
                }
              }
          }
        }
      }
  }
  for (i = 0; i < XNS_MEM_OCH_MAX_BLOCKS; i++)
  {
      if (!p)
      {
        if (!fp)
        {
          for (i = 0; i < XNS_MEM_OCH_MAX_BLOCKS; i++)
          {
              if (!p)
              {
                if (!fp)
                {
                  trace_print("this is a test fn 2 %d %d \n",*fp,*p);
                }
              }
          }
        }
      }
  }
        if (!fp)
        {
          trace_print("this is a test fn 2 %d %d \n",*fp,*p);
        }
  for (i = 0; i < XNS_MEM_OCH_MAX_BLOCKS; i++)
  {
      if (!p)
      {
        if (!fp)
        {
          for (i = 0; i < XNS_MEM_OCH_MAX_BLOCKS; i++)
          {
              if (!p)
              {
                if (!fp)
                {
                  trace_print("this is a test fn 2 %d %d \n",*fp,*p);
                }
              }
          }
        }
      }
  }
}
#endif
trace_print(" This shall not be changed ");
void My_test_function(void* p, int q,char arr)
{
    trace_print("Patch this test 5");
    TRACE_INFO(My_TEST_FUNCTION_1, "Repair this  test 6");
    trace_print( "Patch this 7  %d %d %c ",*p,q, *arr);
}




