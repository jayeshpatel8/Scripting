import pprint as pp
import pdb
import os
import sys
import itertools
import argparse
from tabulate import tabulate
import subprocess

DEBUG = True
VERIFY_DEBUG = False
#DEBUG = True

parser = argparse.ArgumentParser()
parser.add_argument("-d","--dir",action="store_true",help = "Patch Function in current directory")
args = parser.parse_args()
report=[""]
Gen_Report=False

if args.dir:
    print(" Patching Your Functions in current directory ")

# Database files
db_script_file_path = "/scripts/"
db_script_file_name = "tool.pl"

if not "WORKSPACE" in os.environ:
  print("ERROR: $WORKSPACE variable not set. Run your script to fix this")
  raise SystemExit


WorkspaceDir = os.environ["WORKSPACE"]
print("Current workspace: " + WorkspaceDir)

# Patch any of this string
search_str1=['trace_printf','trace_printf2','trace_printf3','trace_print']
# Replace with one of this string
replace_str1=["","TRACE_INFO","TRACE_ERROR","TRACE_WARNING","TRACE_DEBUG"]

#Log Files
File_log=open("log.txt", "w")
#data base log file
File_db_duplicate_msg_name=open("db_duplicate_msg_name.txt", "w")
File_db_err_msg_name=open("db_err_msg_name.txt", "w")
File_db_created_msg_name=open("db_created_msg_name.txt", "a")

MAX_MSG_NAME_LEN=63-9
#MAX_MSG_NAME_LEN=63-8
MAX_MSG_NAME_POSTFIX_LEN=4 #_123
max_msg_len=0

NOT_FOUND=0
SEARCH_STR=1
REPLACE_STR=2

TotalDuplicateMsgNameInDB=0
TotalMsgNameAddedToDB=0

LineToFuncName={}
ListOfFiles=[]
ExceptionFiles=['trace.c']

# Print to log files & consol
def printToBoth(s):
    File_log.write(s)
    print(s)

def getIntValue(s):
    if s!=' ':
        return int(s)
    else:
        return 0
def WaitForUserInput(s):
    if VERIFY_DEBUG:
        if raw_input("!!!!  (" +s+ ") Enter to Continue...")!="":
            raise SystemExit
# Create a list for files to patch ,removes exception files
def CreateFileList():
    FileName='fileList.txt'
    result_code = os.system('ls *.c *.cpp > '+FileName)
    if os.path.exists(FileName):
        fp = open(FileName, "r")
        for Line in fp:
            Line=Line.replace("\n","")
            if Line not in ExceptionFiles:
                ListOfFiles.append(Line)
        fp.close()
        os.remove(FileName)
        File_log.write("\n****** SUCCESS: File List created ******")
    else:
        print("!!!!! ERROR: File List not created !!!!!!!!!")
        raise SystemExit
    return True

def printFuncMsg(msg_str,fn_name,LineNum,Line,print_to_file_only):
    if print_to_file_only==True:
        File_log.write("\n"+"-############################################################################")
        File_log.write("\n"+"-###################     "+msg_str+" ###################")
        File_log.write("\n"+"Function: --   " + fn_name+"()  --  "+ str(LineNum)+"  --  " +Line)
        File_log.write("\n"+"-############################################################################")
    else:
        printToBoth("\n"+"-############################################################################")
        printToBoth("\n"+"-###################     "+msg_str+" ###################")
        printToBoth("\n"+"Function: --   " + fn_name+"()  --  "+ str(LineNum)+"  --  " +Line)
        printToBoth("\n"+"-############################################################################")

def GenerateReport(report):
    rl=len(report)
    #printToBoth(str(len(report)))
    printToBoth("\n********************* REPORT **********************************\n")
    table=[]
    tt=[0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    for i in range(1,rl,14):
        for j in range(0,13,1):
            if report[i+j]=='0':
                report[i+j]=' '
            elif j!=0:
                if j!=4:
                    tt[j]+=getIntValue(report[i+j])
                else:
                    if tt[j]<getIntValue(report[i+j]):
                        tt[j]=getIntValue(report[i+j])
        if report[i+1]==report[i+2]: #'Total'!='Not Repl'
            report[i+2]=' '
        if report[i+1]==report[i+7]:
            report[i+7]=' '
        if report[i+9]==report[i+10]:
            report[i+9]=report[i+10]=' '
        if report[i+11]==report[i+13]:
            report[i+11]=report[i+13]=' '
        if report[i+1]==report[i+7]  and report[i+8]==' ' and (report[i+9]==report[i+10]):
            report[i+7]=report[i+8]=report[i+9]=report[i+10]=' '

        if report[i+1]==report[i+11] and report[i+12]==' ' and (report[i+11]==report[i+13]):
            report[i+11]=        report[i+12]=        report[i+13]=' '
        table.append((report[i],report[i+4],report[i+1],report[i+2],report[i+3],report[i+5],report[i+6],report[i+7],report[i+8],report[i+9],report[i+10],report[i+11],report[i+12],report[i+13],report[i+11]))
    if tt[9]==tt[10]:
        tt[9]=tt[10]=0
    table.append(("Total",tt[4],tt[1],tt[1]-tt[2],tt[3],tt[5],tt[6],tt[1]-tt[7],tt[8],tt[9],tt[10],tt[1]-tt[11],tt[12],tt[13],tt[1]-tt[11]))
    printToBoth(tabulate(table,headers=     ['File Name', 'MaxMsgLen','Total','Not Repl','Skipped','AddMsgDB','DupMsgDB','DiffTP','Fail',  'Cnt1','Cnt2',   'GDiffTP', 'Fail',   'Cnt1',      'Cnt2']))

# FindDuplicateMsg from database file
def FindDuplicateMsg():
    MsgNameFile=WorkspaceDir+"message_name.txt"
    SearchPath=WorkspaceDir
    print("Search Path : " + SearchPath)
    file = open(MsgNameFile, "r")
    if file:
        for Line in file:
            Line=(Line.split())[1]
            batcmd = 'grep -rsw '+Line+" "+SearchPath+"*.c *.h "+"|wc -l"
            output = subprocess.check_output(batcmd, shell=True)
            if int(output) > 1 :
                    print("-------------------------------------------------------------------------------------")
                    print(Line +" : " +output)
                    batcmd = 'grep -rswn '+Line+", "+SearchPath+"*.c *.h "
                    result_code = os.system(batcmd)
        file.close()

#  Build a dictionary of Function name and its line number in file using  ctag
def CreateFuncNameTagWithLineNum(File1):
    batcmd = 'ctags -x --c-kinds=f --sort=no '+File1
    result_code = os.system(batcmd + ' > tag.txt')
    LineToFuncName.clear()
    if os.path.exists('tag.txt'):
        fp = open('tag.txt', "r")
        for Line in fp:
            fn_line = Line.split()
            LineToFuncName[int(fn_line[2])]=fn_line[0]
        fp.close()
    else:
        print("!!!!! ERROR: C-Tags dict not created !!!!!!!!!")
        raise SystemExit
    #print(LineToFuncName[fn_line[2]]+"="+fn_line[2])
    return True

prev_LineNum_str=""
prev_LineNum_conv_str=""

#FindFuncNameFromLineNum from LineToFuncName dictionary
def FindFuncNameFromLineNum(LineNum):
    prev_fn="Invalid"
    global prev_LineNum_str
    global prev_LineNum_conv_str
    for key in sorted(LineToFuncName.keys()):
        #print(LineNum)
        if LineNum.find(",")!= -1:
            LineNum = LineNum[:LineNum.find(",")]
        try:
            if (key)>=int(LineNum):
                #print(str(key)+" "+LineNum)
                return prev_fn
        except ValueError:
            if (prev_LineNum_str == LineNum):
                LineNum=prev_LineNum_conv_str
            else:
                print(LineNum)
                prev_LineNum_str=LineNum
                LineNum = input('PLease input a valid integer')
                prev_LineNum_conv_str=LineNum
        prev_fn=LineToFuncName[key]
    #print(str(key)+" " + LineToFuncName[key]+" ")
    #print(int(LineNum))
    return prev_fn

#Verify using git diff utility for each line of change in file
def GitDiff_Verify(File_out):
    gtotal_change=0
    gtotal_tp_failed=0
    gtp_cnt1=0
    gtp_cnt2=0
    if os.path.exists(File_out):
        fp = open(File_out, "r")
        for Line in fp:
            if Line.find("@@ -")!=-1:
                gtotal_change+=1
                fn_name="Invalid"
                if Line.find("(")!=-1:
                    pre_element=""
                    fn_line = iter(Line.split())
                    for element in fn_line:
                        if (element.find("(")!=-1):
                            if element=="(" or element.split("(")[0]=="":
                                if pre_element=="":
                                    print("!!!!!!!!!!! ERROR LineNum: "+str(LineNum)+" >> "+Line)
                                    WaitForUserInput(" " + SelectedFile + " , function: "+str(sys._getframe().f_code.co_name)+",Line: "+str(sys._getframe().f_lineno))
                                    return [False,gtotal_change,gtotal_tp_failed,gtp_cnt1,gtp_cnt2]
                                fn_name=pre_element
                            else:
                                fn_name = (element.split("(")[0]).replace(" ", "")
                        pre_element =element.replace(" ", "")
                else:
                    fn_name = (Line.split()[len(Line.split())-1]).replace(" ", "")
                if fn_name!="Invalid":
                    change_line=(((Line.split())[1]).replace("-",""))
                    fn_name=fn_name.replace("~", "D")
                    if fn_name.find("("):
                        fn_name=fn_name.split("(")[0]
            elif Line[:1]=='+' and Line[:2]!="++":
                gtp_cnt2+=1
                if Line.find(fn_name.upper())==-1 and Line.find((FindFuncNameFromLineNum(change_line)).upper())==-1:
                    print((FindFuncNameFromLineNum(change_line)))
                    gtotal_tp_failed+=1
                    print("-------------------------------------------")
                    print("Line    >> "+Line)
                    print("fn_name >> "+fn_name+"\n")
            elif Line[:1]=='-' and Line[:2]!="--":
                gtp_cnt1+=1

        fp.close()
    else:
        return [False,gtotal_change,gtotal_tp_failed,gtp_cnt1,gtp_cnt2]
    total=[True,gtotal_change,gtotal_tp_failed,gtp_cnt1,gtp_cnt2]
    return total

#Verify using diff utility for each line of change in file
def Diff_Verify(File_out):
    total_tp=0
    total_change=0
    total_tp_failed=0
    tp_cnt1=0
    tp_cnt2=0
    total=[False, 0,0,0,0]
    if os.path.exists(File_out):
        fp = open(File_out, "r")
        state="SEARCH_FN"

        LineNum=0
        Line_prev=["","",""]
        Line_cnt=0
        for Line in fp:
            if state=="SEARCH_FN":
                if Line.find("***************")!=-1:
                    #print(Line)
                    total_change+=1
                    fn_name="Invalid"
                    if Line.find("(")!=-1:
                        pre_element=""
                        fn_line = iter(Line.split())
                        for element in fn_line:
                            if (element.find("(")!=-1):
                                if element=="(" or element.split("(")[0]=="":
                                    if pre_element=="":
                                        print("!!!!!!!!!!! ERROR LineNum: "+str(LineNum)+" >> "+Line)
                                        #return False
                                        raise SystemExit
                                    fn_name=pre_element
                                else:
                                    fn_name = (element.split("(")[0]).replace(" ", "")
                            pre_element =element.replace(" ", "")
                    else:
                        fn_name = (Line.split()[len(Line.split())-1]).replace(" ", "")
                    if fn_name!="Invalid":
                        fn_name=fn_name.replace("~", "D")
                        state="SEARCH_TRACE1"
                        tp_cnt1=0
                        tp_cnt2=0
                        #print(fn_name)
            elif state=="SEARCH_TRACE1":
                if Line.find("***")!=-1 and len(Line)<=19:
                    change_line=Line
                    change_line=(((Line.split())[1]).split(","))
                    change_line=str(int(change_line[1]) + (int(change_line[1])-int(change_line[0]))/2)
                    fn_line1=Line.replace("***", "-")
                    fn_line1=Line.replace("*", "-")
                    #print(Line)
                elif Line.find("! ")!=-1:
                    for tp_str in replace_str1:
                        if tp_str!="" and Line.find(tp_str)!=-1:
                            File_log.write(Line)
                            if Line.find(fn_name.upper())!=-1 or Line.find((FindFuncNameFromLineNum(change_line)).upper())!=-1:
                                tp_cnt1+=1
                            else :
                                print((FindFuncNameFromLineNum(change_line)))
                                tp_cnt1+=1
                                print("===========================================")
                                print("!!!!! fn_name Not Found : fn_name:" + fn_name )
                                print(" Line: "+fn_line1)
                                print(Line)
                                File_log.write("\n"+  (FindFuncNameFromLineNum(change_line)))
                                File_log.write("\n"+  "===========================================")
                                File_log.write("\n"+  "!!!!! fn_name Not Found : fn_name:" + fn_name )
                                File_log.write("\n"+  " Line: "+fn_line1)
                                File_log.write("\n"+  Line)

                                prev_line=Line_cnt
                                for i in range(3):
                                    if prev_line>=3:
                                        prev_line=0
                                    print(">>>>>>>>   "+Line_prev[prev_line])
                                    File_log.write("\n"+  ">>>>>>>>   "+Line_prev[prev_line])
                                    prev_line+=1
                                total_tp_failed+=1
                                WaitForUserInput(" " + SelectedFile + " , function: "+str(sys._getframe().f_code.co_name)+",Line: "+str(sys._getframe().f_lineno))
                                #return False
                    #print(Line)
                elif Line.find("---")!=-1:
                    if fn_line1==Line:
                        state="SEARCH_TRACE2"
                    else:
                        print("!!!!! Line Mismatch: " + fn_line1 +" != "+ Line)
                        WaitForUserInput(" " + SelectedFile + " , function: "+str(sys._getframe().f_code.co_name)+",Line: "+str(sys._getframe().f_lineno))
                        return total
            elif state=="SEARCH_TRACE2":
                if Line.find("! ")!=-1:
                    found=0
                    for tp_str in search_str1:
                        if tp_str!="" and Line.find(tp_str+"(")!=-1:
                            tp_cnt2+=1
                            found=1
                            break
                    if found ==0 :
                        for tp_str in replace_str1:
                            if tp_str!="" and Line.find(tp_str)!=-1:
                                tp_cnt2+=1
                                break
                    if (tp_cnt2 == tp_cnt1):
                        state="SEARCH_FN"
                        fn_name="Invalid"
                        total_tp+=tp_cnt2
                elif Line.find("*************** ")!=-1:
                    total_change+=1
                    print("!!!!! TP Count Mismatch: tp_cnt1=" + str(tp_cnt1) + " tp_cnt2="+ str(tp_cnt2))
                    print(" Line: "+fn_line1)
                    print(Line)
                    WaitForUserInput(" " + SelectedFile + " , function: "+str(sys._getframe().f_code.co_name)+",Line: "+str(sys._getframe().f_lineno))
                    return total
            LineNum+=1
            if (Line_cnt>=3):
                Line_cnt=0
            Line_prev[Line_cnt]=Line
            Line_cnt+=1

        fp.close()
        #os.remove('output.txt')
        #print(output)

    else:
        return total
    total=[True, total_tp,total_tp_failed,tp_cnt1,tp_cnt2]
    return total

#Verify the changes using diff utility for each line of change in file
def Verify(File1, File2):
    #GIT DIFF Verify
    batcmd = 'git diff -U0 --no-index '+File1+" "+File2
    #batcmd = 'git diff -p --no-index '+File1+" "+File2
    File_out='output_gitdiff.txt'
    result_code = os.system(batcmd + ' >  '+File_out)
    [gdiff_rc,gtotal_change,gtotal_tp_failed,gtp_cnt1,gtp_cnt2] = GitDiff_Verify(File_out)

    batcmd = 'diff -p '+File2+" "+File1
    File_out='output_diff.txt'
    result_code = os.system(batcmd + ' > '+File_out)
    [diff_rc,total_tp,total_tp_failed,tp_cnt1,tp_cnt2] = Diff_Verify(File_out)

    # To preprae a Table list for Report Generation
    table=[]
    tt=[]
    print("")
    if diff_rc==True:
        if tp_cnt1!=tp_cnt2:
            table.append( ["Diff",SelectedFile,(total_tp),(total_tp_failed),(tp_cnt1),(tp_cnt2)])
        else:
            table.append( ["Diff",SelectedFile,(total_tp),(total_tp_failed),(0),(0)])
    if gdiff_rc==True:
        if gtp_cnt1!=gtp_cnt2:
            table.append( ["Git-diff",SelectedFile,(gtp_cnt2),(gtotal_tp_failed),(gtp_cnt1),(gtp_cnt2)])
        else:
            table.append( ["Git-diff",SelectedFile,(gtp_cnt2),(gtotal_tp_failed),(0),(0)])
    printToBoth(tabulate(table,headers=     ['Diff Util','File Name', 'Total TP verified','Total TP Failed','Cnt1','Cnt2']))

    if VERIFY_DEBUG:
        if total_tp_failed!=0 or (tp_cnt1!=tp_cnt2) or gtotal_tp_failed!=0 or (gtp_cnt1!=gtp_cnt2):
            WaitForUserInput(" " + SelectedFile + " , function: "+str(sys._getframe().f_code.co_name)+",Line: "+str(sys._getframe().f_lineno))

    report.extend([str(total_tp),str(total_tp_failed),str(tp_cnt1),str(tp_cnt2),str(gtp_cnt2),str(gtotal_tp_failed),str(gtp_cnt1)])

    if gdiff_rc==True and diff_rc==True:
        return True
    else:
        return False


def AddMsgNameToDataBase(Msg_Name):
    SelectedMsg="y"
    status=1
    if SelectedMsg=="y" or SelectedMsg=="Y" :
        res = os.system("perl " + WorkspaceDir+db_script_file_path+db_script_file_name + " --name=" + Msg_Name )
        File_log.write("\n \n \n"+"----------------------------------------------------------")
        if res != 0:
            File_log.write("\n"+"---        ERROR in Adding  " + Msg_Name+"  Error code("+ str(res)+")        ---")

            status=0
            if res==31488:
                global TotalDuplicateMsgNameInDB
                TotalDuplicateMsgNameInDB+=1
                if File_db_duplicate_msg_name:
                    File_db_duplicate_msg_name.write(Msg_Name+"\n")
            else:
                if File_db_err_msg_name:
                    File_db_err_msg_name.write(Msg_Name+"\n")
        else:
            File_log.write("\n"+"---------- Successfully in Added  " + Msg_Name+"    ----------")
            if File_db_created_msg_name:
                File_db_created_msg_name.write(Msg_Name+"\n")
        File_log.write("\n"+"----------------------------------------------------------\n \n ")

    elif SelectedMsg=="e":
        status=-1
    else:
      File_log.write("\n"+" Skipped " + Msg_Name)
      status=0
    return status

def GetCurrentFuncName(fn_name_list,LineNum):
    multiple_fn_found=0
    fn_name_sel_index=0
    for id,fn in enumerate(fn_name_list):
        if len(fn)>10:
            File_log.write("\n"+"("+str(id)+") "+fn)
            #print("\n"+"("+str(id)+") "+fn)
            fn_name_sel_index=id
            multiple_fn_found+=1
        else:
            fn_name_list[id]="NO_FN" + "("+str(id)+") "+fn+"  <<< Replaced by NO_FN"
            #File_log.write("\n"+"("+str(id)+") "+fn+"  <<< Replaced by NO_FN")
            #print("\n"+"("+str(id)+") "+fn+"  <<< Replaced by NO_FN")
    if multiple_fn_found>1:
        if (FindFuncNameFromLineNum(str(LineNum)) in fn_name_list):
            fn_name=FindFuncNameFromLineNum(str(LineNum))
        else:
            fn_name_list.append(FindFuncNameFromLineNum(str(LineNum)))
            for id,fn in enumerate(fn_name_list):
                print("("+str(id)+") "+fn)
                File_log.write("\n"+"("+str(id)+") "+fn)
            print("\n"+"Line:("+str(LineNum)+"), ")
            fn_name_sel_index = input("File:"+SelectedFile +" [** Multiple_fn_found **]  Enter Index :")
            fn_name=fn_name_list[fn_name_sel_index]
        del fn_name_list[:]
        fn_name_list.append(fn_name)
    else:
        #print(fn_name_list)
        fn_name=fn_name_list[fn_name_sel_index]
        if DEBUG:
            File_log.write("\n"+"Line:("+str(LineNum)+"), fn = "+fn_name)
    fn_name=fn_name.replace("*","")
    return fn_name

def ParseLineToFindFunc(Line,LineNum,Prev_line,fn_start,fn_name,fn_name_list,NoOfTracePrintInFun,selected_fn_name):
    extra_brace=0
    if (Line.find("(")!=-1) and (fn_start==0):
        #File_log.write("\n"+str(LineNum)+" "+Line)
        #File_log.write("\n"+SelectedFile.split())
        pre_element=""
        fn_name_found=0
        if Line[0:1]=='(':
            fn_name=str((Prev_line.split())[len(Prev_line.split())-1])
            NoOfTracePrintInFun=0;
            fn_name_found=1
            #File_log.write("\n"+str(LineNum)+" "+Line)
        else:
            fn_line = iter(Line.split())
            for element in fn_line:
                if (element.find("(")!=-1):
                    if DEBUG:
                        File_log.write("\n"+element+" "+pre_element)
                    if element=="(":
                        fn_name=pre_element
                        fn_name_found=10
                    if element.split("(")[0]=="":
                        #File_log.write("\n"+pre_element)
                        if len(element.split("(")[1])>1 and (element.split("(")[1])[0]!='*' and (element.split("(")[1])[1]!='*':
                            fn_name = pre_element
                            fn_name_found=2
                        elif len(element.split("(")[1])>0 and (element.split("(")[1])[0]!='*':
                            fn_name = pre_element
                            fn_name_found=3
                    else:
                        #File_log.write("\n"+element.replace(" ", ""))
                        fn_name = element.split("(")[0].replace(" ", "")
                        fn_name_found=4
                    NoOfTracePrintInFun=0;
                    #File_log.write("\n"+str(LineNum)+" "+Line)
                pre_element=element.replace(" ", "")
        if (fn_name_found!=0):
            selected_fn_name="Invalid"
            if fn_name.find("::")!=-1:
                fn_name=(fn_name.split("::"))[1]
            fn_name=fn_name.replace("~", "D")
            fn_name_list.append(fn_name)
            if DEBUG:
                File_log.write("\n"+str(LineNum)+":-"+str(fn_name_found)+"-"+fn_name)
        #if DEBUG:
            #File_log.write("\n"+str(len(Line.split())))
    if (Line.find("{")!=-1):
        if (Line.find("extern \"C\" {")!=-1) :
            if DEBUG:
                File_log.write("\n"+"Invalid: "+str(LineNum)+" "+fn_name)
            extra_brace+=1;
        else:
            fn_start+=1;
        if DEBUG:
            #if fn_start==1 and fn_name!="Invalid":
            File_log.write("\n"+"{ "+str(fn_start)+" ->"+str(LineNum)+" "+Line)
    if (Line.find("}")!=-1):
        if DEBUG:
            File_log.write("\n"+"} "+str(fn_start)+" ->"+str(LineNum)+" "+Line)
        if fn_start==0:
            fn_name="Invalid"
            if DEBUG:
                File_log.write("\n"+" E:} ->"+str(LineNum)+" "+Line)
            if extra_brace!=0:
                extra_brace-=1
            else:
                printFuncMsg("ERROR - Invalid END '}'","",LineNum,Line,False)
                WaitForUserInput(" " + SelectedFile + " , function: "+str(sys._getframe().f_code.co_name)+",Line: "+str(sys._getframe().f_lineno))
        else:
            fn_start-=1;
            if (fn_start==0):
                del fn_name_list[:]
                fn_name="Invalid"
                if DEBUG:
                    File_log.write("\n"+" } --fn_name_list is Clear--")

    #print(fn_name_list)
    return [fn_start, fn_name,NoOfTracePrintInFun,selected_fn_name]

def ReplaceMatchedStrWithMsgName(Line, LineNum, search_str, fn_name, found, NoOfTracePrintInFun, TotalReplaced, TotalSkipped):
    choise=1

    while(choise!=0):
        #c = input(" Enter (0)Skip, (1) - INFO , (2) - ERR, (3) - WAR, (4) - DEBUG ")
        choise=1#c
        if choise!=0:
            if choise<0 and choise>4:
                File_log.write("\n"+" Incorrect choise -> Try again")
            else:
                NoOfTracePrintInFun+=1
                if (NoOfTracePrintInFun%10)==0 and fn_name!=FindFuncNameFromLineNum(str(LineNum)):
                    print("LineNum: "+str(LineNum)+" FunName: "+FindFuncNameFromLineNum(str(LineNum)))
                    if raw_input("[ *** Total Trace MessageName is > %10 *** ] =>   "+fn_name+"() = "+str(NoOfTracePrintInFun)+"  Enter to Continue")!='':
                        raise SystemExit

                Msg_Name=fn_name.upper()+"_"+str(NoOfTracePrintInFun)
                msg_len_temp=len(Msg_Name)
                global max_msg_len
                if (msg_len_temp>max_msg_len):
                    max_msg_len=msg_len_temp

                # ADD MSG NAME to DATA base
                if msg_len_temp<=(MAX_MSG_NAME_LEN):
                    #ret_code=AddMsgNameToDataBase(Msg_Name)
                    ret_code=0
                    if ret_code==-1:
                        return  False,True
                    else:
                        global TotalMsgNameAddedToDB
                        TotalMsgNameAddedToDB+=ret_code
                temp_line=""
                if (found==SEARCH_STR):
                    temp_line =Line.replace(search_str,replace_str1[choise],1)
                    temp_line=temp_line.replace("(","("+fn_name.upper()+"_"+str(NoOfTracePrintInFun)+", ",1)
                elif found==REPLACE_STR:
                    existing_msg_name = (Line.split(",")[0]).split("(")[1]
                    if Msg_Name != existing_msg_name:
                        temp_line =Line.replace(existing_msg_name,Msg_Name,1)
                if temp_line!="":
                    File_log.write("\n"+"----------------------------------------------------------------------------------------------")
                    File_log.write("\n"+"\n  -----     Replaced: --"+str(LineNum)+" with "+replace_str1[choise]+"   ------  \n")
                    File_log.write("\n"+"----------------------------------------------------------------------------------------------")
                    File_log.write("\n"+ " "+Line+" "+"\n"+ " "+temp_line+"")
                    #File_log.write("\n"+"----------------------------------------------------------------------------------------------")
                    #print (">> "+ Line+ " << " + temp_line)
                    Line=temp_line
                    TotalReplaced+=1
        else:
            File_log.write("\n"+"----------------------------------------------------------------------------------------------")
            File_log.write("\n"+"  ->           Skipped  :"+str(LineNum)+"               \n\n")
            #File_log.write("\n"+"----------------------------------------------------------------------------------------------")
            TotalSkipped+=1
        choise=0
    return [Line, NoOfTracePrintInFun, TotalReplaced, TotalSkipped]

def ParseFunNameAndAddMsgName(file, fileContent,filename ):
    if file:
      File_log.write("\n"+"Scanning for Message NAME in file " + file.name + "...")
    else:
        return False,True
    TotalReplaced=0
    TotalSkipped=0
    LineNum=0
    fn_start=0
    fn_name="Invalid"
    selected_fn_name="Invalid"
    NoOfTracePrintInFun=0;

    msg_name={} #Len shall be less than 53 = 63-9

    Prev_line=""
    fn_name_list=[]
    for Line in file:
        LineNum+=1
        [fn_start, fn_name,NoOfTracePrintInFun,selected_fn_name] = ParseLineToFindFunc(Line,LineNum,Prev_line,fn_start,fn_name,fn_name_list,NoOfTracePrintInFun,selected_fn_name)

        if fn_start>=1 and fn_name!="Invalid":
            found=NOT_FOUND
            for search_str in search_str1: #Search for  PRINTF MSG
                if (Line.find(search_str+"(")!=-1):
                    found=SEARCH_STR
                    break
            if (found==NOT_FOUND):
                for search_str in replace_str1: #Search for existing TRACE_INFO etc.
                    if search_str!="" and (Line.find(search_str+"(")!=-1):
                        found=REPLACE_STR
                        break
            if (found!=NOT_FOUND):
                if selected_fn_name=="Invalid":
                    fn_name=GetCurrentFuncName(fn_name_list,LineNum)
                    selected_fn_name=""
                    if len(fn_name)<=10:
                        printFuncMsg("ERROR: Msg Name is Inavlid",fn_name,LineNum,Line,False)
                        WaitForUserInput(" " + SelectedFile + " , function: "+str(sys._getframe().f_code.co_name)+",Line: "+str(sys._getframe().f_lineno))
                        return False,True
                    printFuncMsg("",fn_name,LineNum,Line,True)
                    File_log.write("\n"+"Function- -- " + fn_name+"()  --  "+ str(LineNum)+"  --  ")
                    if len(fn_name)>(MAX_MSG_NAME_LEN-MAX_MSG_NAME_POSTFIX_LEN):
                        if fn_name in msg_name:
                            printFuncMsg("ERROR: Duplicate Msg Name",fn_name,LineNum,Line,True)
                            fn_name_sel = raw_input("[MessageName Duplicate] Enter to Continue :  "+fn_name[0:(MAX_MSG_NAME_LEN-MAX_MSG_NAME_POSTFIX_LEN-1)]+"\n               Else Enter S to STOP it  ")
                            if fn_name_sel!="":
                                return  False,True
                            fn_name=msg_name[fn_name]
                        else:
                            #t_fn_name = raw_input("[MessageName Len > (MAX_MSG_NAME_LEN-MAX_MSG_NAME_POSTFIX_LEN)] Enter to Use:  "+fn_name[0:(MAX_MSG_NAME_LEN-MAX_MSG_NAME_POSTFIX_LEN-1)]+"\n                        Else Enter name of less then 52 char  ")
                            t_fn_name=""
                            if t_fn_name=="":
                                t_fn_name = fn_name[0:(MAX_MSG_NAME_LEN-MAX_MSG_NAME_POSTFIX_LEN-1)]
                            if (len(t_fn_name)<=(MAX_MSG_NAME_LEN-MAX_MSG_NAME_POSTFIX_LEN)):
                                msg_name[fn_name]=t_fn_name
                                fn_name=t_fn_name
                            else:
                                printFuncMsg("ERROR: Duplicate Msg Name Entered",fn_name,LineNum,Line,False)
                                WaitForUserInput(" " + SelectedFile + " , function: "+str(sys._getframe().f_code.co_name)+",Line: "+str(sys._getframe().f_lineno))
                                return  False,True

                [Line, NoOfTracePrintInFun, TotalReplaced, TotalSkipped] = ReplaceMatchedStrWithMsgName(Line, LineNum, search_str, fn_name, found, NoOfTracePrintInFun, TotalReplaced, TotalSkipped)

        fileContent.write(Line)
        Prev_line=Line
    # For report Generation
    table=[]
    global TotalMsgNameAddedToDB
    global max_msg_len

    table.append( [filename,(max_msg_len),(TotalReplaced+TotalSkipped),(TotalReplaced),(TotalSkipped),(TotalMsgNameAddedToDB),(TotalDuplicateMsgNameInDB)])
    printToBoth(tabulate(table,headers=     ['File Name', 'MaxMsgLen','Total','Repl','Skipped','AddMsgDB','DupMsgDB']))
    if (TotalReplaced+TotalSkipped)!=0:
        if max_msg_len>=54:
            printToBoth("\n"+"----------------------------------      WARNING          -------------------------------------------")
            printToBoth("\n"+"-------------        Max Msg Name Length  >= "+str(max_msg_len)+"      ------------------------------------")
            printToBoth("\n"+"----------------------------------      WARNING          -------------------------------------------")
            WaitForUserInput(" " + SelectedFile + " , function: "+str(sys._getframe().f_code.co_name)+",Line: "+str(sys._getframe().f_lineno))
            return False,True
    else:
        return True, True
    report.extend([filename, str(TotalReplaced+TotalSkipped), str(TotalReplaced), str(TotalSkipped), str(max_msg_len), str(TotalMsgNameAddedToDB), str(TotalDuplicateMsgNameInDB)])
    return True, False

# Main Patch Functon
def Patch(SelectedFile):
    if SelectedFile == "":
        File_log.write("\n"+"Exiting... Enterted Filename: ("+ SelectedFile +")")
        raise SystemExit
    rc=True
    while True:
        fp = open(SelectedFile, "r")
        if fp:
            File_log.write("\n"+"File  " + SelectedFile + " is opened:" )
            TempFile = SelectedFile + ".temp"
            TempFileFp = open(TempFile, "w")
            if rc==True:
                rc = CreateFuncNameTagWithLineNum(SelectedFile)
            if rc==True:
                rc, skipVerify = ParseFunNameAndAddMsgName(fp,TempFileFp,SelectedFile)
            TempFileFp.close()
            #os.remove(SelectedFile)
            #os.rename(TempFile, SelectedFile)
            File_log.write("\n"+"Done")
            if rc==True and str(skipVerify)=="False":
                rc=Verify(SelectedFile,TempFile)
                if rc==True:
                    print("#######   ***********  " +"File: " + SelectedFile +" -Success - Verification ************** ############")
                else:
                    print("#######   ***********  !!!! " +"File: " + SelectedFile +" -Failed - Verification  !!!! ************** ############")

            if skipVerify==True:
                os.remove(TempFile)
        else:
            File_log.write("\n"+"Failed to open a File:" + SelectedFile)
            File_log.write("\n"+"Invalid input. Specify a Enter Key to exit")
            continue
        if fp:
            fp.close()
            File_log.write("\n"+"File " + SelectedFile + " is Closed:" )
        break
    return rc

if args.dir:
    CreateFileList()
    File_log.write("\n"+str(ListOfFiles))
    for SelectedFile in ListOfFiles:
        Gen_Report=Patch(SelectedFile)
        if Gen_Report==False and VERIFY_DEBUG:
            break
        Gen_Report=True
else:
    SelectedFile = raw_input("Specify the file to define  Message Name: ")
    Gen_Report=Patch(SelectedFile)

if True == Gen_Report:
    GenerateReport(report)
    if raw_input(">> Press Enter to \"Check Duplicate Msg Name\"...")=="":
        FindDuplicateMsg()
else:
    printToBoth("File: "+SelectedFile+" Report Generation Failed")

if File_db_created_msg_name:
    File_db_created_msg_name.close()
if File_db_err_msg_name:
    File_db_err_msg_name.close()
if File_db_duplicate_msg_name:
    File_db_duplicate_msg_name.close()

if File_log:
    File_log.close()

raise SystemExit
