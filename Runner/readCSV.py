#!/usr/bin/env python
# coding: utf-8

# In[213]:


import os
import csv

def removeChar(input:str)->str:
    input=list(input)
    result=[]
    for i in range(len(input)):
        if not input[i].isalpha():
            result.append(input[i])
    return ''.join(result)

def readFromOut(direct:str,ep:int)->list:
    result=[]
    f=open(direct)
    flist=f.readlines()
    for i in range(len(flist)-1,-1,-1):
        tmp=flist[i]
        if 'Epoch' in tmp and len(result)!=2:
            tmp=tmp.split(' ')
            epl=tmp.index('[Epoch')+1
            if tmp[epl]==ep:
                if 'accuracy:' in tmp:
                    pointer=tmp.index('accuracy:')
                    accuracy=tmp[pointer+1].strip(')\n')
                    result.append(accuracy)
                if 'time' in tmp:
                    time=tmp[-2].strip()
                    result.append(time)
            else:
                break
    f.close()
    if len(result)!=2:
        print('invalid file!')
        return None
    return result
    

def readToCSV(dirct:str):
    os.system('rm ./experiments.csv')
    files=os.listdir(dirct)
    row_list =[['NO.','learning rate','number of epoch','number of executor','size','accuracy/%','time/ms']]
    no=1
    for f in files:
        if os.path.isdir(dirct + '/'+f):
            print('now processing directory %s:'%f)
            tmp=f.split('_')[1:]
            for i in range(len(tmp)):
                tmp[i]=removeChar(tmp[i])
            lr,ep,ex,s=tmp
            #write into csv
            outlist=os.listdir(dirct+'/'+f)
            outlist.sort()
            pointer=len(outlist)-1
            while pointer>=0:
                if len(open(dirct + '/'+f+'/'+ outlist[pointer-1]).readlines())==0:
                    accuracy,time=readFromOut(dirct + '/'+f+'/'+ outlist[pointer],ep)
                    break
                pointer-=2
            row_list.append([no,float(lr),int(ep),int(ex),int(s),float(accuracy),float(time)])
            no+=1
    with open('experiments.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(row_list)


# In[214]:


def sortCSV(dirct:str,column:int):
    reader = csv.reader(open(dirct))
    sortedlist = sorted(reader, key=lambda row: row[column], reverse=True)
    no=1
    for i in range(1,len(sortedlist)):
        sortedlist[i][0]=no
        no+=1
    with open(dirct, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(sortedlist)


# In[225]:


def main():
    readToCSV("./Result")
    sortCSV("./experiments.csv",2)
    print('csv writing finished\n --------------------------------')


# In[226]:


if __name__=="__main__":
    main()

