'''
Submitted for project requirement in CSE 601
Hierarchical clustering implementation in python for gene data set
  
@author1:     navinder
@contact:    navinder@buffalo.edu

@author2:     Kaushal
@contact:    sbondada@buffalo.edu
'''
import math
import numpy as np
import sys
from DBSCAN_Clustering import calculateJaccardandRand
from DBSCAN_Clustering import calculateCorelation
from DBSCAN_Clustering import pca,get_TopN_values

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
        global item_list
        global item_list_org
        item_list.append([temp_values])
        item_list_org.append(temp_values)
    print item_list

def distance(x,y,dtype):
    if(dtype=='euclidean'):
        sumsq=0
        for i in range(len(x)):
            sumsq=sumsq+math.pow((x[i]-y[i]),2)   
        dist=math.sqrt(sumsq)
    return dist  

#item_list should be a list of list of lists to support hierarchical clustering
def gen_simlarity_mat(item_list,sim_type,merge_cond):
    sim_mat=np.matrix(np.zeros((len(item_list),len(item_list))))
    for i in range(len(item_list)):
        for j in range(len(item_list)):
            if merge_cond=='min':
                min_dist=100000
                for k in item_list[i]:
                    for l in item_list[j]:
                        temp_dist=distance(k[2:],l[2:],sim_type)
                        if(temp_dist<min_dist):
                            min_dist=temp_dist
                sim_mat[i,j]=min_dist
    return sim_mat

#quicker version of the sim mat generator.
def gen_similarity_mat1(sim_mat,item_list,sim_type,merge_cond,merge_r,merge_c):
    #shrinking the matrix
    minpos=min(merge_r,merge_c)
    maxpos=max(merge_r,merge_c)
    sim_filter=np.ones(sim_mat.shape[0])
    sim_filter[maxpos]=0
    #removing the row and column of the matrix and returning the new instance of the sim_mat
    sim_mat=np.compress(sim_filter,sim_mat,axis=0)
    sim_mat=np.compress(sim_filter,sim_mat,axis=1)
    #calculating the sim value of only the merged column and row
    for i in range(len(item_list)):
        if merge_cond=='min':
            min_dist=100000
            for k in item_list[minpos]:
                for l in item_list[i]:
                    temp_dist=distance(k[2:],l[2:],sim_type)
                    if(temp_dist<min_dist):
                        min_dist=temp_dist
            sim_mat[i,minpos]=min_dist
            sim_mat[minpos,i]=min_dist
#returning the sim matrix because the passed reference to the sim matrix is lost when the compress has reassigned the values to the variable again
    return sim_mat 
            
#get the positions of the 
def get_next_merges(curr_sim_mat,merge_cond):
    if(merge_cond=='min'):
        min_sim=100000
        posr,posc=-1,-1
        for i in range(curr_sim_mat.shape[0]):
            for j in range(curr_sim_mat.shape[1]):
                if(i!=j and curr_sim_mat[i,j]<min_sim):
                    min_sim=curr_sim_mat[i,j]
                    posr=i
                    posc=j
        print str(posr)+("-"*10)+str(posc)
        return [min_sim,posr,posc]      
    
def get_clusterno_list():
    global cluster_no_list
    cluster=0
    for clusters in item_list:
        cluster=cluster+1
        for lists in clusters:
            cluster_no_list[lists[0]-1]=cluster           
                
                 
if __name__=="__main__":
    global item_list,item_list_org,cluster_no_list
    item_list,item_list_org=[],[]
    loadinput("/home/kaushal/Ubuntu One/subjects/semester_3/DATA_MINING/project2/cho.txt")
    cluster_no_list=[0]*(len(item_list))
    ref_distance_mat=gen_simlarity_mat(item_list,sys.argv[4],sys.argv[5])
    curr_sim_mat=np.matrix(ref_distance_mat)
    k=int(sys.argv[3])
    while(len(item_list)!=k):
        mergeinfo=get_next_merges(curr_sim_mat,sys.argv[5])
        minpos=min(mergeinfo[1],mergeinfo[2])
        if(minpos==mergeinfo[1]):
            temp2=item_list.pop(mergeinfo[2])
            temp1=item_list.pop(mergeinfo[1])
            item_list.insert(minpos,temp1+temp2)
        else:
            temp1=item_list.pop(mergeinfo[1])
            temp2=item_list.pop(mergeinfo[2])
            item_list.insert(minpos,temp2+temp1)
        curr_sim_mat=gen_similarity_mat1(curr_sim_mat,item_list, sys.argv[4],sys.argv[5],mergeinfo[1],mergeinfo[2])
        #curr_sim_mat=gen_simlarity_mat(item_list,sys.argv[4],sys.argv[5])
    get_clusterno_list()
    print set(cluster_no_list)
    print cluster_no_list
    external_ind=calculateJaccardandRand(item_list_org, cluster_no_list)
    print external_ind
    internal_ind=calculateCorelation(ref_distance_mat,cluster_no_list)
    print internal_ind
    pca(item_list_org,2)
    
        