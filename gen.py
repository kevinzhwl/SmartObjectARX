#file_operation.py

import fileinput,sys
import os
import glob
import re

def getAlltree(dir_path):
    for name in os.listdir(dir_path):
        full_path = os.path.join(dir_path, name)
        if os.path.isfile(full_path):
            filesize=isLarge(full_path)           
            if filesize > 0:
               print("path 最高%s filesize%d" % (full_path,filesize))             
        #if os.path.isdir(full_path):
         #   getAlltree(full_path)
            
filename = r'c:/autodesk/objectarx/demo/inc-t/acpointcloud.h'
filepath = r'c:/autodesk/objectarx/demo/inc-t/'
fn = r'acpointcloud.h'

def isClassLine(str):
    if str.startswith('class') :
        return True
    else :
        return False

def removeLastComma(str):
    strlen = len(str)
    if str[strlen-1] == ':' :
        cls = str[0:strlen-1]
    else : cls = ''
    return cls

def removeLastChars(str,cnt = 1):
    strlen = len(str)
    cls = str[0:strlen-cnt]
    return cls

def getSmartClsname(str,strtail):
    strlen = len(str)
    taillen = len(strtail)
    if str[strlen-taillen] ==  strtail :
        cls = str[0:strlen-taillen]
    else : cls = ''
    return cls

def isSuffix(str,suffix):
    strlen = len(str)
    suflen = len(suffix)
    if str[strlen-suflen:suflen] ==  suffix :
        cls = str[0:strlen-suflen]
    else : cls = ''
    return cls


def process(strline,nextline,fpath,fname):
    #pre process
    strArray = strline.split(' ')
    arrayCount = 0
    for k,v in enumerate(strArray):
        #print k,v
        arrayCount += 1
        
    if strArray[0] != 'class' : return  
#    print ('split:', strArray ,arrayCount)
# process by different line-mode
    clsname = ''
    
    if arrayCount == 5 :
#('split:', ['class', 'Ac3dDwfNavTreeNode', ':', 'public', 'AcRxObject\n'], 5)
        if strArray[2] == ':':
            clsname = strArray[1]
#('split:', ['class', 'ATL_NO_VTABLE', 'AcadToolImpl', ':', '\n'], 5)
        elif strArray[1] == 'ATL_NO_VTABLE' and strArray[4] == ':':
            clsname = strArray[2]
#('split:', ['class', 'CAMERADLLIMPEXP', 'AcDbCamera:', 'public', 'AcDbEntity\n'], 5)
        elif strArray[1] == 'CAMERADLLIMPEXP' and strArray[3] == 'public':
            clsname = removeLastComma(strArray[2])
#('split:', ['class', 'ADESK_NO_VTABLE', 'AcDbCurve:', 'public', 'AcDbEntity\n'], 5)
        elif strArray[1] == 'ADESK_NO_VTABLE' and strArray[3] == 'public':
            clsname = removeLastComma(strArray[2])
#('split:', ['class', 'ACDB_PORT', 'AcConstrainedBoundedLine:', 'public', 'AcConstrainedLine\n'], 5)
        elif strArray[1] == 'ACDB_PORT' and strArray[3] == 'public':
            clsname = removeLastComma(strArray[2])
#('split:', ['class', 'AcEdServices:', 'public', 'AcRxService', '\n'], 5)
        elif strArray[2] == 'public' and strArray[4] == '\n' :
            clsname = removeLastComma(strArray[1])
#('split:', ['class', 'AcDbBody:', 'public', '', 'AcDbEntity\n'], 5)
        elif strArray[2] == 'public' and strArray[3] == '' :
            clsname = removeLastComma(strArray[1])
#('split:', ['class', 'AcDbHyperlinkCollection', '', '', '\n'], 5)
        elif strArray[2] == '' and strArray[3] == '' and strArray[4] == '' :
            clsname = strArray[1]
#('split:', ['class', 'ACTCUI_PORT', 'CAcTcUiManager', '', '\n'], 5)
        elif strArray[1] == 'ACTCUI_PORT' and strArray[3] == '' and strArray[4] == '\n' :
            clsname = strArray[2]
#('split:', ['class', 'ADUI_PORT', 'CAdUiRegistryWriteAccess:', 'public', 'CAdUiRegistryAccess\n'], 5)
        elif strArray[1] == 'ADUI_PORT' and strArray[3] == 'public' :
            clsname = removeLastComma(strArray[2])

# 连在一起写不起作用，不知道为什么
# 屏蔽一些无效的字节
#('split:', ['class', 'C', ':', 'public', 'B\n'], 5)
        if strArray[1] == 'C' :#and strArray[2] == ':' and strArray[3] == 'public' and strArray[4] == 'B\n'
            clsname =''
            #print ('split:', strArray ,arrayCount)
#('split:', ['class', '', '', '', 'CAdUiSearchBoxEditor;\n'], 5)
#('split:', ['class', '', '', '', 'CAdUiSearchBoxClearButton;\n'], 5)
        elif strArray[4] == 'CAdUiSearchBoxEditor;\n' :
            clsname =''
        elif strArray[4] == 'CAdUiSearchBoxClearButton;\n' :
            clsname =''
        else :
            clsname = ''

        clsname = '' # for debug 

    if arrayCount == 4 :
        clsname = ''
#        if arrayCount == 4 and strArray[0] == 'class' and strArray[1] == 'ACDB_PORT' and strArray[3] == '{\n':
#            clsname = strArray[2]
#        elif arrayCount == 3 and strArray[0] == 'class' and strArray[2] == '{\n' :
#            clsname = strArray[1]
#        else :
#            clsname = ''
    if arrayCount == 31 :
        clsname = ''
#('split:', ['class', 'AcDbAppSystemVariables', '{\n'], 3)
        if strArray[2] == '{\n' :
            clsname = strArray[1]
#('split:', ['class', 'ACDB_PORT', 'AcAutoConstrainEvaluationCallback\n'], 3)
        elif strArray[1] == 'ACDB_PORT' :
            clsname = removeLastChars(strArray[2])
#('split:', ['class', 'ADESK_NO_VTABLE', 'AcDbClassIterator\n'], 3)
        elif  strArray[1] == 'ADESK_NO_VTABLE' :
            clsname = removeLastChars(strArray[2])
#('split:', ['class', 'ACAD_PORT', 'AcEdInputPoint\n'], 3)
        elif  strArray[1] == 'ACAD_PORT' :
            clsname = removeLastChars(strArray[2])
#('split:', ['class', 'ACTC_PORT', 'AcTcImage\n'], 3)
        elif  strArray[1] == 'ACTC_PORT' :
            clsname = removeLastChars(strArray[2])
#('split:', ['class', 'AcDMMNode', '\n'], 3)
        elif  strArray[2] == '\n' :
            clsname = strArray[1]
#('split:', ['class', 'ACUI_PORT', 'CAcUiMRUComboBox;\n'], 3)
        elif  strArray[1] == 'ACUI_PORT' :
            if re.search(r';\n$',strArray[2]) : clsname = ''
            if re.search(r'[a-zA-Z0-9_]\n$',strArray[2]) : clsname = removeLastChars(strArray[2])
#            elif isSuffix(strArray[2],';\n') : clsname = ''
#            if isSuffix(strArray[2],';\n') : clsname = ''
    if arrayCount == 3 :
        clsname = ''
#('split:', ['class', '__declspec(novtable)', 'AdHostImageAppServices\n'], 3)
        if r'__declspec(novtable)' == strArray[1] :
           clsname = removeLastChars(strArray[2],1)
#('split:', ['class', 'AcDbAppSystemVariables', '{\n'], 3)
        elif re.search(r'^{?\n$',strArray[2]) :
            clsname = strArray[1]
        elif re.search(r'(ACUI_PORT|ACAD_PORT)|((ACTC_PORT|ADESK_NO_VTABLE)|ACDB_PORT)',strArray[1]) :
            if re.search(r'[a-zA-Z0-9_]\n$',strArray[2]) : clsname = removeLastChars(strArray[2])
            elif re.search(r'[a-zA-Z0-9_]{+\n$',strArray[2]) : clsname = removeLastChars(strArray[2],2)
        elif re.search(r'ADAF_PORT|ADUI_PORT',strArray[1]) :
            if re.search(r'[a-zA-Z0-9_]\n$',strArray[2]) : clsname = removeLastChars(strArray[2])
        elif r':\n' == strArray[2] :
            clsname = strArray[1]

        if strArray[1] == 'A' or r'DLLScope' == strArray[1] :#and strArray[2] == ':' and strArray[3] == 'public' and strArray[4] == 'B\n'
            clsname =''
        if r'CNavListCtrl;\n' == strArray[2] or r';\n' == strArray[2] or r'CAsiUcStr;' == strArray[2] :
            clsname = ''

        clsname = '' #for debug 
            
    if arrayCount == 2 :
        clsname = ''
        #print( strArray)
        strtext = strArray[1]
        #if re.search(r';\n$',strtext) : clsname = ''
        if re.search(r'[a-zA-Z0-9_]\n$',strtext) : clsname = removeLastChars(strtext)
        if re.search(r'[a-zA-Z0-9_]{\n$',strtext) : clsname = removeLastChars(strtext,2)
        #if clsname != '' : print (clsname)

        clsname = '' #for debug 


    if arrayCount == 21 :
        clsname = ''
        #print( strArray)
        strtext = strArray[1]
        strlen = len(strtext)
        if strlen >=2 :
            strlast = strtext[-2:]
            if strlast == ';\n' :
                clsname = ''
            elif strlast[-1] == '\n' :
                clsname = strtext[0:-1]

            print ( clsname)
        elif strlen == 1 and strtext == '\n':
            clsname = ''
        else :
            clsname = ''


    if arrayCount == 6 :
        clsname = ''
#('split:', ['class', 'AcApLayoutManager', ':', 'public', 'AcDbLayoutManager', '{\n'], 6)
#('split:', ['class', 'AcDbLayoutManager:', 'public', 'AcRxObject', '', '{\n'], 6)
        if re.search(r'ACDB_PORT|ADESK_NO_VTABLE|ACFDUI_PORT|ADESK_DEPRECATED|ACTC_PORT|ACTCUI_PORT|ACUI_PORT|ADUI_PORT|AXAUTOEXP|SCENEDLLIMPEXP|LIGHTDLLIMPEXP|DLLIMPEXP|ISMDLLACCESS',strArray[1]) :
            if r':' == strArray[3] : clsname = strArray[2]
            else : clsname = removeLastComma(strArray[2])
        elif r':' == strArray[2]  :
            clsname = strArray[1]
        elif r':' == strArray[3]  and r''==strArray[2] :
            clsname = strArray[1]
        elif r'public' == strArray[2] :
            clsname = removeLastComma(strArray[1])
        elif re.search(r'^{?\n$',strArray[5]) :
            if r':' == strArray[2] : clsname = strArray[1]
            elif r':' == strArray[3]: clsname = strArray[2]
            elif r'' != removeLastComma(strArray[1]) : clsname = removeLastComma(strArray[1])
            elif r'' != removeLastComma(strArray[2]) : clsname = removeLastComma(strArray[2])

        if r'__declspec(novtable)' == strArray[1] and r':' == strArray[3]:
           clsname = strArray[2]



#    if clsname == 'C' :
#        print ('debug info c',strArray)

    if len(clsname) != 0 :
        content = '#include "' + fname + '"'
        fopath = fpath + '/'+ clsname;
        fo = open(fopath,'w')
        fo.writelines(content)
        fo.close()
    return


def printclass(str):
    if str.startswith('class') :
        strArray = str.split(' ')
        arrayCount = 0
        for k,v in enumerate(strArray):
            #print k,v
            arrayCount += 1
            
        print ('split:', strArray ,arrayCount)
        

def main() :
    filepath = r'c:/autodesk/objectarx/2012/inc-r'

    #operation very line
    dir_path = filepath
    hdrfiles = []
    allfiles = os.listdir(dir_path)
    for name in allfiles:
        if name.endswith('.h') :
            #print name
            hdrfiles.append(name)


    for name in hdrfiles :
        filename = os.path.join(filepath , name)
    #    print filename
        f = open(filename)
        line = f.readline()
        while True:
            if not line: break
            if isClassLine(line) :
                thisline = line
                line = f.readline()
                nextline = line
                process(thisline,nextline,filepath,name)
                #printclass(thisline)
            else :
                line = f.readline()
                
        f.close()


    print 'generate finished \n'
    return

# main func 
main()