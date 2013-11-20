'''
Submitted for Homework3 requirement in CSE 601
Markov Clustering Analysis for Complex Data in python for gene data set
  
@author1:     navinder
@contact:    navinder@buffalo.edu

@author2:     Kaushal
@contact:    sbondada@buffalo.edu
'''
import numpy as np

def construct_inp_mat(filename,case):
    global input_matrix
    inpfile=open(filename)
    for line in inpfile:
        if case =='attweb_net':
            splitstr=line.split(" ")
        elif case =='yeast_undirected_metabolic' :
            splitstr=line.split("\t")
        elif case =='physics_collaboration_net':
            splitstr=line.split(" ")
        #print splitstr
        tempfrststr=str(splitstr[0].strip())
        tempscndstr=str(splitstr[1].strip())
        input_matrix[itemdict[tempfrststr],itemdict[tempscndstr]]+=1
        input_matrix[itemdict[tempscndstr],itemdict[tempfrststr]]+=1

def write_mat_file(TOTnodes,filename):
    Clusterlist=[-1]*TOTnodes
    Clusterno=-1
    for i in range(input_matrix.shape[0]):
        if input_matrix[i].sum()!=0:
            Clusterno+=1
        for j in range(input_matrix.shape[1]):
            if input_matrix[i,j]!=0:
                Clusterlist[j]=Clusterno   
    print Clusterlist        
    write_file=open("/home/kaushal/Downloads/Data_For_HW3/"+filename+".clu","w")
    write_file.write("*Vertices "+str(TOTnodes)+'\n')
    for item in Clusterlist:
        write_file.write(str(item)+'\n')
    write_file.close()         
    
def find_max_nodes(filename,case):
    print "Dataset being used:",case
    inpfile=open(filename)
    global itemdict
    itemdict={}
    inc=0
    for line in inpfile:
        if case =='attweb_net':
            splitstr=line.split(" ")
        elif case =='yeast_undirected_metabolic' :
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
    print "No of Iterations:", loop_inc
    
    f=input_matrix.sum(axis=1)
    clusters=0
    for i in f:
        if i!=0:
            clusters+=1
    print "No of Clusters:", clusters
    return (loop_inc,clusters)

if __name__== "__main__":
    global input_matrix,itemdict
    #TOTnodes=find_max_nodes("/home/kaushal/Downloads/Data_For_HW3/attweb_net.txt",'attweb_net')
    #TOTnodes=find_max_nodes("/home/kaushal/Downloads/Data_For_HW3/physics_collaboration_net.txt",'physics_collaboration_net')
    TOTnodes=find_max_nodes("/home/kaushal/Downloads/Data_For_HW3/yeast_undirected_metabolic.txt",'yeast_undirected_metabolic')
    print "Total no of Nodes:",TOTnodes
    input_matrix=np.matrix(np.zeros((TOTnodes,TOTnodes)))
    #construct_inp_mat("/home/kaushal/Downloads/Data_For_HW3/attweb_net.txt",'attweb_net')
    #construct_inp_mat("/home/kaushal/Downloads/Data_For_HW3/physics_collaboration_net.txt",'physics_collaboration_net')
    construct_inp_mat("/home/kaushal/Downloads/Data_For_HW3/yeast_undirected_metabolic.txt",'yeast_undirected_metabolic')
#     input_matrix=input_matrix.transpose()
#     input_matrix=np.matrix([[1,2,3],[4,5,6],[7,8,9]])
#     print input_matrix
#     print np.alltrue(input_matrix==input_matrix.transpose())
    NoOfIterations,Clusters=Mcl(2, 2)
    write_mat_file(TOTnodes,'yeast')
    
    
    
    
    