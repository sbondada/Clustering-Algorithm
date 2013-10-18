import math
import numpy as np

true_cluster=[]
gene_list=[]

def loadinput(filename):
    f = open(filename)
    for line in f:
        temptrans=line.split("\t")
        gene_feature_values=[]
        for i in range(1,len(temptrans)):
            if i==1:
                true_cluster.append(int(temptrans[i]))
            else:
                gene_feature_values.append(float(temptrans[i]))
        gene_list.append(gene_feature_values)

def distance(x,y,dtype):
    if(dtype=='euclidean'):
        sumsq=0
        for i in range(len(x)):
            sumsq=sumsq+math.pow((x[i]-y[i]),2)   
        dist=math.sqrt(sumsq)
    return dist  

def gen_simlarity_mat(item_list,sim_type):
    sim_mat=np.matrix(np.zeros((len(item_list),len(item_list))))
    for i in range(len(item_list)):
        for j in range(len(item_list)):
            sim_mat[i,j]=distance(item_list[i],item_list[j],sim_type)
    return sim_mat
             
                 
if __name__=="__main__":
    loadinput("/home/kaushal/Ubuntu One/subjects/semester_3/DATA_MINING/project2/cho.txt")
    a=gen_simlarity_mat(gene_list,'euclidean')
    print a
    
    
        