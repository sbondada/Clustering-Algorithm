import numpy as np
import math

def construct_inp_mat(filename,case):
    global input_matrix
    inpfile=open(filename)
    if case=='attweb_net':
        for line in inpfile:
            splitstr=line.split(" ")
            #print splitstr
            input_matrix[int(splitstr[0]),int(splitstr[1])]+=1
            input_matrix[int(splitstr[1]),int(splitstr[0])]+=1
    elif case =='yeast_undirected_metabolic' or case =='physics_collaboration_net':
        for line in inpfile:
            if case =='yeast_undirected_metabolic' :
                splitstr=line.split("\t")
            elif case =='physics_collaboration_net':
                splitstr=line.split(" ")
            #print splitstr
            tempfrststr=str(splitstr[0].strip())
            tempscndstr=str(splitstr[1].strip())
            input_matrix[itemdict[tempfrststr],itemdict[tempscndstr]]+=1
            input_matrix[itemdict[tempscndstr],itemdict[tempfrststr]]+=1

def write_mat_file(temp_mat,filename):
    write_file=open("/home/kaushal/Downloads/Data_For_HW3/"+filename,"w")
    for i in np.asarray(temp_mat):
        write_file.write(str(i))
        write_file.write(str("\n"))
        
        
def find_max_nodes(filename,case):
    maxnodes=0
    if case=='attweb_net':
        inpfile=open(filename)
        for line in inpfile:
            splitstr=line.split(" ")
            if(maxnodes<int(splitstr[0])):
                maxnodes=int(splitstr[0])
            if(maxnodes<int(splitstr[1])):
                maxnodes=int(splitstr[1])
        return maxnodes+1
    elif case =='yeast_undirected_metabolic' or case =='physics_collaboration_net' :
        inpfile=open(filename)
        global itemdict
        itemdict={}
        inc=0
        for line in inpfile:
            if case =='yeast_undirected_metabolic' :
                splitstr=line.split("\t")
            elif case =='physics_collaboration_net':
                splitstr=line.split(" ")
            #print splitstr
            tempfrststr=str(splitstr[0].strip())
            tempscndstr=str(splitstr[1].strip())
            if(tempfrststr not in itemdict):
                itemdict[tempfrststr]=inc
                #print tempfrststr
                inc+=1 
            if(tempscndstr not in itemdict):
                itemdict[tempscndstr]=inc
                #print tempscndstr
                inc+=1
        maxnodes=len(set(itemdict.keys()))
        #print sorted(itemdict.items(),key=lambda x : x[1])
        return maxnodes
    
def Mcl (e=2,r=2):
    global input_matrix
    #. Add self loops to each node to avoid divide by zero and not a number exceptions
    input_matrix=input_matrix+np.eye(input_matrix.shape[0],dtype='float16')
    #print input_matrix
    # finding the sum of each column for normalization
    norm_array=input_matrix.sum(axis=0)
    #print norm_array
    #applying norm to each column vector
    for i in range(input_matrix.shape[1]):
        input_matrix[:,i]=input_matrix[:,i]/norm_array[0,i]
    
    #print input_matrix
    
    cmp_matrix=np.eye(input_matrix.shape[1])
    
    loop_inc=0
    
    while( not(np.all(input_matrix==cmp_matrix))):
        #Expand by taking the eth power of the matrix
        cmp_matrix=np.matrix(input_matrix)
        input_matrix=input_matrix**e
        #print input_matrix
        #Inflate by taking inflation of the resulting matrix with parameter r
        for i in range(input_matrix.shape[1]):
            temp_col=np.asarray(input_matrix[:,i])**r
            #print temp_col
            #print temp_col.sum()
            input_matrix[:,i]=np.matrix(temp_col)/temp_col.sum()
        #print input_matrix
        loop_inc=loop_inc+1
    
    print input_matrix
    print loop_inc
    
    f=input_matrix.sum(axis=1)
    clusters=0
    for i in f:
        if i!=0:
            clusters+=1
    print clusters
    
    write_mat_file(input_matrix,"input_matrix")
    write_mat_file(cmp_matrix,"cmp_matrix")
    write_mat_file(input_matrix.sum(axis=1),"input_sum")
    

if __name__== "__main__":
    global input_matrix,itemdict
    #maxnodes=find_max_nodes("/home/kaushal/Downloads/Data_For_HW3/attweb_net.txt",'attweb_net')
    maxnodes=find_max_nodes("/home/kaushal/Downloads/Data_For_HW3/physics_collaboration_net.txt",'physics_collaboration_net')
    #maxnodes=find_max_nodes("/home/kaushal/Downloads/Data_For_HW3/yeast_undirected_metabolic.txt",'yeast_undirected_metabolic')
    print maxnodes
    input_matrix=np.matrix(np.zeros((maxnodes,maxnodes)))
    #construct_inp_mat("/home/kaushal/Downloads/Data_For_HW3/attweb_net.txt",'attweb_net')
    construct_inp_mat("/home/kaushal/Downloads/Data_For_HW3/physics_collaboration_net.txt",'physics_collaboration_net')
    #construct_inp_mat("/home/kaushal/Downloads/Data_For_HW3/yeast_undirected_metabolic.txt",'yeast_undirected_metabolic')
#     input_matrix=input_matrix.transpose()
#     input_matrix=np.matrix([[1,2,3],[4,5,6],[7,8,9]])
#     print input_matrix
#     print np.alltrue(input_matrix==input_matrix.transpose())
    Mcl(2, 2)