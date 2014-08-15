#file_operation.py

import fileinput,sys
import os
import glob
import re



def printclass(str):
    if str.startswith('class') :
        strArray = str.split(' ')
        arrayCount = 0
        for k,v in enumerate(strArray):
            #print k,v
            arrayCount += 1
            
        print ('split:', strArray ,arrayCount)
        

def remove_comments( str ) :
    #Rule1 = "(\/\*(\s|.)*?\*\/)|(\/\/.*)"
    comment_rule = r'(/[*](\s|.)*?[*]/)|(//.*)'
    str = re.sub(comment_rule,"",str)
    return str

def remove_whiteline( str ) :
    comment_rule = r'([\n]{2,})'
    str = re.sub(comment_rule,"\n",str)
    str = re.sub('[ ]*[\n]+',"\n",str)
    return str

def remove_invalid( str ) :
    #comment_rule = r'(/[*](\s|.)*?[*]/)|(//.*)'
    #str = re.sub(comment_rule,"",str)
    return str

def trim_space( str ) :
    #Rule1 = "(\/\*(\s|.)*?\*\/)|(\/\/.*)"
    comment_rule = r'([ \t]+)'
    str = re.sub(comment_rule," ",str)
    return str

def create_content( str ) :
    con = str
    return con

def write_file(fp, str ) :
    if len( str) != 0 :
        content =  str
        fo = open(fp,'w')
        fo.writelines(content)
        fo.close()
    return

def remove_class_declare( str ) :
    comment_rule = r'([ ]*(class)[ ]+[a-zA-z0-9_]*;\n)'
    str = re.sub(comment_rule,"",str)
    str = re.sub(r'[#]+.*\n',"",str)
    #str = re.sub(r'typedef.*;\n',"",str)
    return str


def remove_class_adj( str ) :
    str = re.sub(r'template.*>'," ",str)
    str = re.sub(r'[<>]'," ",str)
    str = re.sub(r'[&*]'," ",str)
    str = re.sub(r'__declspec\(novtable\)'," ",str)
    return str

def get_class_list( str ) :
    str = re.sub(r'\n'," ",str)
    comment_rule = r'class [a-zA-Z0-9_: ,]*{'
    str = re.findall(comment_rule,str)
    return str

def get_class_name( str ) :
    str = re.sub(r':.*{$',"",str)
    str = re.sub(r'[ ]*[{]*$',"",str)
    str = re.sub(r'^class ',"",str)
    comment_rule = r'AXAUTOEXP|CAMERADLLIMPEXP|SCENEDLLIMPEXP|LIGHTDLLIMPEXP|ISMDLLACCESS|GE_DLLEXPIMPORT|GX_DLLEXPIMPORT'
    str = re.sub(comment_rule,"",str)
    comment_rule = r'ADAF_PORT|ACAD_PORT|ACDB_PORT|ADESK_NO_VTABLE|ATL_NO_VTABLE|ACFDUI_PORT|ADESK_DEPRECATED|ACTC_PORT|ACTCUI_PORT|ACUI_PORT|ADUI_PORT|DLLIMPEXP|ANAV_PORT'
    str = re.sub(comment_rule,"",str)
    comment_rule = r' .*novtable. '
    str = re.sub(comment_rule," ",str)
    str = re.sub(r' ',"",str)
    #str = re.findall(comment_rule,str)
    return str

def get_group_name( str ) :
    prefix = str[0:4]
    #AcBr is empty
    comment_rule = r'^(AcAp|AcAx|AcBr|AcCm|AcDb|AcEd|AcFd|AcGe|AcGi|AcGs|AcLy|AcPl|AcRx)'
    comment_rule = comment_rule.lower()
    str = str.lower()
    if re.search(comment_rule,str) : groupn=str[0:4]
    elif re.search(r'^cacfdui',str) : groupn='acfd'
    elif re.search(r'constraint$',str) : groupn='acdb'
    elif re.search(r'^acconstrained',str) : groupn='acdb'
    elif re.search(r'^acautoconstrainevaluationcallback',str) : groupn='acdb'
#    elif re.search('^AcTransaction',str) : groupn='AcTransaction'
#    elif re.search('^AcTrayItem',str) : groupn='AcTrayItem'
    elif re.search('^acpublish',str) : groupn='acpublish'
    else : groupn='acmisc'

    return groupn

def get_group_name_by_file( str ) :
    #AcBr is empty
    comment_rule = r'^(AcAp|AcAx|AcBr|AcCm|AcDb|AcEd|AcFd|AcGe|AcGi|AcGs|AcLy|AcPl|AcRx)'
    comment_rule = comment_rule.lower()
    str = str.lower()
    if re.search(comment_rule,str) : groupn=str[0:4]
    elif re.search('^(db|ge|rx|ax',str) : groupn='ac'+ str[0:2]
#    elif re.search('^AcTransaction',str) : groupn='AcTransaction'
#    elif re.search('^AcTrayItem',str) : groupn='AcTrayItem'
#    elif re.search('^AcPublish',str) : groupn='AcPublish'
    else : groupn='acmisc'

    return groupn

def set_group( gdict,gname,gcontent ) :
    oldcon = gdict.get(gname, '')
    old = oldcon.lower();
    con = gcontent.lower();
    if old.find(con) < 0 :
        gdict[gname] = gcontent +"\n"+oldcon
    
    return gdict


def generate( filepath) :
 
    #operation very line
    dir_path = filepath
    hdrfiles = []
    allfiles = os.listdir(dir_path)
    for name in allfiles:
        if name.endswith('.h') :
            #print name
            hdrfiles.append(name)


    group_dict = {}
    group_str = {'AcAp','AcAx','AcBr','AcCm','AcDb','AcEd','AcFd','CAcFdUi','AcGe','AcGi','AcGs','AcLy','AcPl','AcRx','AcPublish','AcMisc'}
    for k, v in enumerate(group_str):
        nm = v.lower()
        group_dict[nm] = ''
    #group_dict = {'AcAp':'','AcAx':'','AcBr':'','AcCm':'','AcDb':'','AcEd':'','AcFd':'','CAcFdUi':'','AcGe':'','AcGi':'','AcGs':'','AcLy':'','AcPl':'','AcRx':'','AcPublish':'','AcMisc':''}
    cls_count = 0
    for inc_name in hdrfiles :
        filename = os.path.join(filepath , inc_name)
        fopath = filename + '.cpp';
    #    print filename
        f = open(filename)
        line = f.read()
        f.close()
        if not line: continue
        #
        line = remove_comments(line)
        line = remove_invalid(line)
        line = trim_space(line)
        line = remove_whiteline(line)
        line = remove_whiteline(line)
        #
        line = remove_class_declare(line)
        line = remove_class_adj(line)
        #
        line = get_class_list(line)
        #
        line_cnt =0
        arr = []
        for k, v in enumerate(line):
            line_cnt+=1
            cls_name= get_class_name(v)
            content = '#include "' + inc_name + '"'
            write_file(os.path.join(filepath , cls_name),content)
            line[k] =cls_name
            group_name = get_group_name(cls_name)
            group_name2 = get_group_name(inc_name)
            if group_name == 'acmisc' : group_name = group_name2
            group_dict = set_group(group_dict,group_name,content)

        cls_count += line_cnt

        print( filename)
        print (line)
        print( 'cls_count=',cls_count)
        #process(line)
        #write_file(fopath,line)


    spcfiles = ["acuiHeaderCtrl.h","acuiListCtrl.h","acuiListBox.h"]
    spcclasses = ["CAcUiHeaderCtrl","CAcUiListCtrl","CAcUiListBox"]
    line_cnt =0
    for k, v in enumerate(spcfiles):
        line_cnt+=1
        cls_name = spcclasses[k]
        content = '#include "' +spcfiles[k] + '"'
        write_file(os.path.join(filepath , cls_name),content)
        group_name = get_group_name(cls_name)
        group_dict = set_group(group_dict,group_name,content)
        
    cls_count += line_cnt
    print (spcclasses)
    print( 'cls_count=',cls_count)

    print(group_dict)
    for k, v in enumerate(group_dict.keys()):
        write_file(os.path.join(filepath , v),group_dict.get(v,''))
 

    print 'generate finished \n'
    return

def main() :
    filepath = r'c:/autodesk/objectarx/2012/inc-r'
    generate(filepath)

# main func 
main()