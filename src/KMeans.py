'''
Submitted for project requirement in CSE 601
K Means implementation in python for gene data set
  
@author1:     navinder
@contact:    navinder@buffalo.edu

@author2:     Kaushal
@contact:    sbondada@buffalo.edu
'''

import random
import re
import copy
import math
import sys
from DBSCAN_Clustering import calculateCorelation,calculateJaccardandRand,distance,gen_simlarity_mat

TotalClusters = 0
TotalGenes=0
centroids = []
genes = []

'''
class with centroid and gene information
'''
class gene:
    def __init__(self, geneNumber, totalValues):
        self.totalValues = totalValues
        self.geneNumber = geneNumber
        self.valueList = []
        self.centroidNumber=0
    def setList(self, valueList):
        self.valueList = valueList
    def getList(self):
        return self.valueList
    def setCentroidNum(self,num):
        self.centroidNumber=num
    def getCentroidNum(self):
        return self.centroidNumber
        
class centroid:
    def __init__(self, number, geneValueList):
        self.centroidNumber = number
        self.valueList = list(geneValueList)
        self.changeFlag = 0
        self.oldList = []
        self.totalGenes=0
    def getList(self):
        return self.valueList
    def setOldList(self):
        self.oldList=copy.deepcopy(self.valueList)
    def setListZero(self):
        for i in range(len(self.valueList)):
            self.valueList[i]=0

'''
 Method to read the input file 
 store the values of genes in an arrayList
 '''        
def readInputFile(filename):
    global genes, TotalGenes
    try:
        fileHandler = open(filename, 'r')
        
        for line in fileHandler:
            tokens = re.split('\t', line)
            totalValues = len(tokens)
# totalValues - 2 leaves the gene number and its next value
            geneObj = gene(tokens[0], totalValues - 2)
            tempList = []
            for i in range(2, totalValues):
                tempList.append(tokens[i].strip())
            geneObj.setList(tempList)
            genes.append(geneObj)
        TotalGenes= len(genes)
    except IOError:
        print "File doesn't exist"
        sys.exit()
        
def intializeCentroid(totalClusters):
    global TotalClusters ,genes, centroids, TotalGenes
    if totalClusters < 1:
        print "Cluster number should be greater than 1"
        sys.exit()
    TotalClusters = totalClusters
    for i in range(TotalClusters):
        rand = random.randint(1, TotalGenes)
        geneObj=genes[rand]
#         fixed_centroids=[3,53,175,261,419,344,208,183,199,422]
#         geneObj=genes[fixed_centroids[i]-1]
        lis=copy.deepcopy(geneObj.getList())
        centroidObj=centroid(i,lis)
        centroids.append(centroidObj)
    
    for i in range(len(centroids)):
        cenObj=centroids[i]

def runKMeans():
    global TotalClusters, centroids, genes

    for geneNum in range(TotalGenes):
        # temporary variables to calculate the values for min distance
        
        tempDist=0.0
        minDist= sys.maxint
        newCentroidNum = -1
        geneList=copy.deepcopy(genes[geneNum].getList())
     
        for centroidNum in range(TotalClusters):
            tempDist=0.0
            centroidList= centroids[centroidNum].getList()
            for valueNum in range(len(centroidList)):
                if geneList[valueNum] >= 0:
                    tempDist= tempDist +  pow((float(geneList[valueNum]) - float(centroidList[valueNum])),2)
            tempDist= math.sqrt(tempDist)
            if tempDist < minDist:
                minDist=tempDist
                newCentroidNum= centroidNum
        genes[geneNum].setCentroidNum(newCentroidNum)

# update the centroids value list once all the points are updated with new centroids
def updateCentroids():
    global TotalClusters, centroids, genes,TotalGenes

    for centroidNum in range(TotalClusters):
        del centroids[centroidNum].oldList[:]
        centroids[centroidNum].setOldList()
        centroids[centroidNum].setListZero()
        centroids[centroidNum].totalGenes=0

    for geneNum in range(TotalGenes):
        centroidNum= genes[geneNum].getCentroidNum()
        centroids[centroidNum].totalGenes=centroids[centroidNum].totalGenes+1
        for valueNum in range(genes[geneNum].totalValues):
            centroids[centroidNum].valueList[valueNum] = float(centroids[centroidNum].valueList[valueNum])+ float(genes[geneNum].valueList[valueNum])
        
          
    for centroidNum in range(TotalClusters):
        for count in range(len(centroids[centroidNum].valueList)):
            centroids[centroidNum].valueList[count]= (float(centroids[centroidNum].valueList[count])/float(centroids[centroidNum].totalGenes))

def utilKMeans():
    global TotalClusters, centroids, genes,TotalGenes
    loopCounter=0
    while 1:
        loopCounter+=1
        print "::::::::::::::::::::::::::::::::::::::"
        print "Iteration:",loopCounter,
        runKMeans()
        updateCentroids()
        counter=0
        print
        for centroidA in centroids:
            print "Centroid Number",centroidA.centroidNumber
            print "New Centroid: ",centroidA.valueList
            print "Old Centroid: ",centroidA.oldList
            if centroidA.valueList[1:]==centroidA.oldList[1:]:
                counter=counter+1
        if counter==len(centroids):
            print "Minima acheived"
            break
    print "Clusters are acheived"
    for cen in centroids:
        print "Centroid number:",cen.centroidNumber,"Elements",cen.totalGenes
    
def get_clusterno_list():
    global cluster_no_list
    global genes
    global cluster_map
    for gen in genes:
        cluster_no_list[int(gen.geneNumber)-1]=cluster_map[gen.centroidNumber]

def get_cluster_mapping():
    global cluster_map
    gene_set,inc=set(),0
    for gen in genes:
        gene_set.add(gen.centroidNumber)
    cluster_map={}
    for i in gene_set:
        inc=inc+1
        cluster_map[i]=inc
        
        
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
    
if __name__ == '__main__':
# two values to change as of now hardcoded
# 1.Name of file to read
# 2. Number of clusters needed    
#    readInputFile('/home/sean/workspace/first/src/project2/iyer.txt')
# here 5 is the k    
    global item_list,cluster_no_list,cluster_map
    readInputFile("/home/kaushal/Ubuntu One/subjects/semester_3/DATA_MINING/project2/iyer.txt")
    item_list=[]
    #specifiacally for the calculation of the jaccard and correlation values
    loadinput("/home/kaushal/Ubuntu One/subjects/semester_3/DATA_MINING/project2/iyer.txt")
    print item_list
    intializeCentroid(10)
    utilKMeans()
    print "Execution Finished"
    cluster_no_list=[0]*len(item_list)
    get_cluster_mapping()
    get_clusterno_list()
    print cluster_map.values()
    print cluster_no_list
    external_ind=calculateJaccardandRand(item_list, cluster_no_list)
    print external_ind
    sim_mat=gen_simlarity_mat(item_list,'euclidean')
    internal_ind=calculateCorelation(sim_mat,cluster_no_list)
    print internal_ind
    