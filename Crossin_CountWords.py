#-*-coding:utf-8-*-
#!/usr/bin/python
import re
file='words.txt'
try:
    with open(file,'r') as f:
        content=f.read()
except FileNotFoundError:
    content=''
    print ('Can\'t find the %s file' %file)

if content:
    content=content.lower()
    result=re.findall(r'\b[A-z]+\b',content)
    print ('There are %d words in %s ' %(len(result),file))
    print ('There are %d words in %s(without repeat word) ' %(len(list(set(result))),file))