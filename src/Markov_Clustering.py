import numpy as np
import math


def construct_inp_mat(filename):
    global input_matrix
    inpfile=open(filename)
    for line in inpfile:
        splitstr=line.split(" ")
        input_matrix[int(splitstr[0]),int(splitstr[1])]=input_matrix[int(splitstr[0]),int(splitstr[1])]+1

def write_mat_file(temp_mat,filename):
    write_file=open("/home/kaushal/Downloads/Data_For_HW3/"+filename,"w")
    for i in np.asarray(temp_mat):
        write_file.write(str(i))
        write_file.write(str("\n"))
        
        
def find_max_nodes(filename):
    maxnodes=0
    inpfile=open(filename)
    for line in inpfile:
        splitstr=line.split(" ")
        if(maxnodes<int(splitstr[0])):
            maxnodes=int(splitstr[0])
        if(maxnodes<int(splitstr[1])):
            maxnodes=int(splitstr[1])
    return maxnodes+1
    
def Mcl (e=2,r=2):
    global input_matrix
    #. Add self loops to each node to avoid divide by zero and not a number exceptions
    input_matrix=input_matrix+np.eye(input_matrix.shape[0])
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
    
    while( not(np.allclose(input_matrix,cmp_matrix))):
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
    write_mat_file(input_matrix,"input_matrix")
    write_mat_file(cmp_matrix,"cmp_matrix")
    write_mat_file(input_matrix.sum(axis=1),"input_sum")
    

if __name__== "__main__":
    global input_matrix
    maxnodes=find_max_nodes("/home/kaushal/Downloads/Data_For_HW3/attweb_net.txt")
    print maxnodes
    input_matrix=np.matrix(np.zeros((maxnodes,maxnodes)))
    construct_inp_mat("/home/kaushal/Downloads/Data_For_HW3/attweb_net.txt") 
#     input_matrix=np.matrix([[1,2,3],[4,5,6],[7,8,9]])
    Mcl(2, 2)