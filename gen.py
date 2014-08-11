#file_operation.py

import fileinput,sys
import os

def getAlltree(dir_path):
    for name in os.listdir(dir_path):
        full_path = os.path.join(dir_path, name)
        if os.path.isfile(full_path):
            filesize=isLarge(full_path)           
            if filesize > 0:
               # print("path %s filesize%d" % (full_path,filesize))             
        #if os.path.isdir(full_path):
         #   getAlltree(full_path)
            
filename = r'c:/autodesk/objectarx/demo/inc-t/acpointcloud.h'
filepath = r'c:/autodesk/objectarx/demo/inc-t/'
fn = r'acpointcloud.h'
def process(str):
	if str.startswith('class') and str.endswith('{\n') : 
		strArray = str.split(' ')
		arrayCount = 0
		for k,v in enumerate(strArray):
			#print k,v
			arrayCount += 1
			
		print ('process:', strArray )
		if arrayCount == 4 and strArray[0] == 'class' and strArray[1] == 'ACDB_PORT' and strArray[3] == '{\n':
			classname = strArray[2]
		elif arrayCount == 3 and strArray[0] == 'class' and strArray[1] ==

		if classname != '':
			strline = '#include "' + fn + '"'
			fopath = filepath + classname;
			fo = open(fopath,'w')
			fo.writelines(strline)
			fo.close()
	if str.startswith('class')

#operation very line
f = open(filename)
print filename
while True:
    line = f.readline()
    if not line: break
    process(line)
f.close()
