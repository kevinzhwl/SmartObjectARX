#file_operation.py

import fileinput,sys
import os
import glob


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
            

    if arrayCount == 4 :
        clsname = ''
#        if arrayCount == 4 and strArray[0] == 'class' and strArray[1] == 'ACDB_PORT' and strArray[3] == '{\n':
#            clsname = strArray[2]
#        elif arrayCount == 3 and strArray[0] == 'class' and strArray[2] == '{\n' :
#            clsname = strArray[1]
#        else :
#            clsname = ''
    if arrayCount == 3 :
        clsname = ''
    if arrayCount == 2 :
        clsname = ''
        if strArray[1] == '\n':
            clsname = ''
        else :
            strlen = len(strArray[1])
            strlast = strArray[1][strlen-2,2]
            if strlast == ';\n' :
                clsname = ''
            elif strlast[1,1] == '\n'
                clsname = strArray[1][0:strlen-1]
                



    if clsname == 'C' :
        print ('debug info c',strArray)

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