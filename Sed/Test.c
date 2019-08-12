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
