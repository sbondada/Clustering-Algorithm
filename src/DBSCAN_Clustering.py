import math
import sys
import numpy as np
from Hierarchical_Clustering import item_list

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
        if(visitor_list[i]==-1):
            visitor_list[i]=1
            neighbour_pos_set=find_neighboring_points(i,sim_mat, e)
            if(len(neighbour_pos_set)<min_points):
                cluster_no_list[i]=-2
            else:
                global cluster_no
                cluster_no=cluster_no+1
                print cluster_no
                expand_Cluster(i,neighbour_pos_set,cluster_no,e,min_points)

def expand_Cluster(i,neighbor_pos_list,cluster_no,e,min_points):
    cluster_no_list[i]=cluster_no
    pending_neighbour_pos_list=list()
    for j in neighbor_pos_list:
        if visitor_list[j]==-1:
            visitor_list[j]=1
            new_neighbour_pos_list=find_neighboring_points(j,sim_mat,e)
            if(len(new_neighbour_pos_list)>=min_points):
                pending_neighbour_pos_list.extend(new_neighbour_pos_list)
                pending_neighbour_pos_list=sorted(set(pending_neighbour_pos_list))
                print pending_neighbour_pos_list
        if cluster_no_list[j]==-1:
            cluster_no_list[j]=cluster_no
            
    
if __name__=="__main__":
    e=float(sys.argv[3])
    min_points=int(sys.argv[4])
    global cluster_no_list,visitor_list,item_list,cluster_no,sim_mat #visitor_list==-1 means the item_list point is unvisited by the algorithm
    item_list=[]
    loadinput("/home/kaushal/Ubuntu One/subjects/semester_3/DATA_MINING/project2/cho.txt")#suppose to replace thetest to the command line argument sys.argv[2] 
    cluster_no_list=[-1]*len(item_list)
    visitor_list=[-1]*len(item_list)
    sim_mat=gen_simlarity_mat(item_list, 'euclidean')
    cluster_no=0
    DBSCAN(item_list, e, min_points)
    print set(cluster_no_list)
    print cluster_no_list
