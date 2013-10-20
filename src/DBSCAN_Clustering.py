import math
import sys

item_list=[]

def loadinput(filename):
    f = open(filename)
    for line in f:
        temptrans=line.split("\t")
        temp_values=[]
        for i in range(len(temptrans)):
            if i<2:
                temp_values.append(int(temptrans[i]))
            else:
                temp_values.append(float(temptrans[i]))
        item_list.append([temp_values])
    print item_list

def distance(x,y,dtype):
    if(dtype=='euclidean'):
        sumsq=0
        for i in range(len(x)):
            sumsq=sumsq+math.pow((x[i]-y[i]),2)   
        dist=math.sqrt(sumsq)
    return dist
    
if __name__=="__main__":
        loadinput("/home/kaushal/Ubuntu One/subjects/semester_3/DATA_MINING/project2/cho.txt")
