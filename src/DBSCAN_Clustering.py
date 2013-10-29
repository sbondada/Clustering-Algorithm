'''
Submitted for project requirement in CSE 601
DBSCAN implementation in python for gene data set
  
@author1:     navinder
@contact:    navinder@buffalo.edu

@author2:     Kaushal
@contact:    sbondada@buffalo.edu
'''
import math
import sys
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt

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
        item_list.append(temp_values)
    print item_list

def distance(x,y,dtype):
    if(dtype=='euclidean'):
        sumsq=0
        for i in range(len(x)):
            sumsq=sumsq+math.pow((x[i]-y[i]),2)   
        dist=math.sqrt(sumsq)
    return dist

def gen_simlarity_mat(item_list,sim_type):
    global sim_mat
    sim_mat=np.matrix(np.zeros((len(item_list),len(item_list))))
    for i in range(len(item_list)):
        for j in range(len(item_list)):
            sim_mat[i,j]=distance(item_list[i][2:],item_list[j][2:],sim_type)
    return sim_mat

def find_neighboring_points(point_pos,sim_mat,e):
    neighbour_pos_set=set()
    for i in range(len(item_list)):
        if(sim_mat[point_pos,i]<=e):
            neighbour_pos_set.add(i)
    return sorted(neighbour_pos_set)        

def DBSCAN(item_list,e,min_points):
    for i in range(len(item_list)):
        global visitor_list
        if(visitor_list[i]==-1):
            visitor_list[i]=1
            neighbour_pos_set=find_neighboring_points(i,sim_mat, e)
            if(len(neighbour_pos_set)<min_points):
                global cluster_no_list
                cluster_no_list[i]=-2
            else:
                global cluster_no
                cluster_no=cluster_no+1
                print cluster_no
                expand_Cluster(i,neighbour_pos_set,cluster_no,e,min_points)

def expand_Cluster(i,neighbor_pos_list,cluster_no,e,min_points):
    global cluster_no_list
    cluster_no_list[i]=cluster_no
    pending_neighbour_pos_list=list()
    for j in neighbor_pos_list:
        global visitor_list
        if visitor_list[j]==-1:
            visitor_list[j]=1
            new_neighbour_pos_list=find_neighboring_points(j,sim_mat,e)
            if(len(new_neighbour_pos_list)>=min_points):
                pending_neighbour_pos_list.extend(new_neighbour_pos_list)
                pending_neighbour_pos_list=sorted(set(pending_neighbour_pos_list))
                print pending_neighbour_pos_list
        if cluster_no_list[j]==-1:
            cluster_no_list[j]=cluster_no

def calculateJaccardandRand(item_list,cluster_no_list):
    clustering,groundTruth=np.matrix(np.zeros((len(item_list),len(item_list)))),np.matrix(np.zeros((len(item_list),len(item_list))))
    ss,sd,ds,dd=0,0,0,0
    for i in range(len(item_list)):
        for j in range(len(item_list)):   
            if(item_list[i][1]==item_list[j][1]):
                groundTruth[i,j]=1
            if(cluster_no_list[i]==cluster_no_list[j]):
                clustering[i,j]=1
    for i in range(len(item_list)):
        for j in range(len(item_list)):
            if(groundTruth[i,j]==1 and clustering[i,j]==1):
                ss=ss+1
            if(groundTruth[i,j]==1 and clustering[i,j]==0):
                sd=sd+1
            if(groundTruth[i,j]==0 and clustering[i,j]==1):
                ds=ds+1
            if(groundTruth[i,j]==0 and clustering[i,j]==0):
                dd=dd+1
    rand=float((ss+dd))/(ss+sd+ds+dd)
    jaccard=float((ss))/(ss+sd+ds)
    return [jaccard,rand]

def calculateCorelation(sim_mat,cluster_no_list):
    clustering=np.matrix(np.zeros((len(cluster_no_list),len(cluster_no_list))))
    for i in range(len(cluster_no_list)):
        for j in range(len(cluster_no_list)):   
            if(cluster_no_list[i]==cluster_no_list[j]):
                clustering[i,j]=1
    sim_mat_mean,cluster_mean=np.mean(sim_mat),np.mean(clustering)
    numer,denom1,denom2=0,0,0
    for i in range(len(cluster_no_list)):
        for j in range(len(cluster_no_list)):
            numer=numer+(sim_mat[i,j]-sim_mat_mean)*(clustering[i,j]-cluster_mean)
            denom1=denom1+math.pow((sim_mat[i,j]-sim_mat_mean), 2)
            denom2=denom2+math.pow(clustering[i,j]-cluster_mean, 2)
    correlation=float(numer)/(math.sqrt(denom1)*math.sqrt(denom2))
    return correlation

def get_TopN_values(inp_array,n):
    n_val_dict={}
    inc,max_val,pos=0,0,-1
    while(inc<n):
        for i in range(len(inp_array)):
            if(inp_array[i]>max_val):
                max_val=inp_array[i]
                pos=i
        inp_array[pos]=0
        n_val_dict[max_val]=pos
        max_val=0
        inc=inc+1
    return n_val_dict
    
    
def pca(item_list,nd):
    #removing the starting elements in the matrix so that the eigen values can be calculated only to the features
    org_data=np.compress([0]*2+[1]*(len(item_list[1])-2),np.matrix(item_list),axis=1)
    #print org_data.shape
    #calculating the mean of the matrix for each column so that the points are shifted to center
    org_mean=np.mean(org_data,axis=0)
    #subtracting the columns mean with each value in the matrix so that we shift the values
    adj_data=org_data-org_mean
    #calculating the co-variance among the 16 features of the each 300 or 500 samples
    cov_data=np.cov(np.transpose(adj_data))
    #calculating the eigen values for the square matrix
    eig_val,eig_vec=np.linalg.eig(cov_data)
    topN_Dict=get_TopN_values(list(eig_val),nd)
    condition=[0]*len(eig_val)
    for i in topN_Dict.values():
        condition[i]=1
    red_eig_vec=np.compress(condition,eig_vec,axis=1)
    #red_eig_vec=np.transpose(red_eig_vec)
    red_data=org_data*red_eig_vec
    return red_data
    
    
if __name__=="__main__":
    e=float(sys.argv[3])
    min_points=int(sys.argv[4])
    global cluster_no_list,visitor_list,item_list,cluster_no,sim_mat #visitor_list==-1 means the item_list point is unvisited by the algorithm
    item_list=[]
    loadinput("../dataset/dataset1.txt")#suppose to replace the test to the command line argument sys.argv[2] 
    cluster_no_list=[-1]*len(item_list)
    visitor_list=[-1]*len(item_list)
    sim_mat=gen_simlarity_mat(item_list, 'euclidean')
    cluster_no=0
    DBSCAN(item_list, e, min_points)
    print set(cluster_no_list)
    print cluster_no_list
    external_ind=calculateJaccardandRand(item_list,cluster_no_list)
    print external_ind
    internal_ind=calculateCorelation(sim_mat, cluster_no_list)
    print internal_ind
    red_item_list=pca(item_list,3)
    
    colorset=['r','b','g','c','m','y','k','w',(0.6,0.2,0.1),(0.1,0.3,0.6),(0.2,0.6,0.6),(0.15,0.4,0.7)]
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    for i in range(len(red_item_list[:,1])):
        ax.scatter(red_item_list[i,0],red_item_list[i,1],red_item_list[i,2],c=colorset[cluster_no_list[i]])
    ax.set_xlabel('X Label')
    ax.set_ylabel('Y Label')
    ax.set_zlabel('Z Label')

    plt.show()
