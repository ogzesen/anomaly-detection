import readerClass
import numpy as np
from isOutOfRange import isOutOfRange

#Run the detection algorithm in an iteration to determine the fittest 
#results that do not produce anomalies.
def findLowerParameter(myArray,avgTimer):
    currValue=0
    for lowerBoundValue in range(40,0,-1):
        selfCounter=0
        upperErrCount=0
        lowerErrCount=0    
        upperBoundValue=100
        memory=np.zeros(avgTimer)
        
        for minute in range(avgTimer):
            memory[minute]=myArray[selfCounter]
            selfCounter+=1
        
    
        for minute in range(avgTimer,myArray.size-1):
            currentTrafic=myArray[selfCounter]#Get the cuurent value that will be compared.
            selfCounter+=1
            weGood=True
            
            #Comparison.
            if isOutOfRange(memory,currentTrafic,avgTimer,upperBoundValue,lowerBoundValue) == [1,'l']:
                lowerErrCount=lowerErrCount+1
                upperErrCount=0
            elif isOutOfRange(memory,currentTrafic,avgTimer,upperBoundValue,lowerBoundValue) == [1,'u']:
                upperErrCount=upperErrCount+1
                lowerErrCount=0
            else:
                upperErrCount=0
                lowerErrCount=0
                
            if lowerErrCount>=3:
                weGood=False
                
            if weGood==False:
                currValue=lowerBoundValue
                return currValue+1
            memory=np.append(memory,currentTrafic)
    return 0
            
def findUpperParameter(myArray,avgTimer):

    currValue=0
    for upperBoundValue in range(40,0,-1):
        selfCounter=0
        upperErrCount=0
        lowerErrCount=0    
        avgTimer=30
        lowerBoundValue=100
        memory=np.zeros(avgTimer)
        
        for minute in range(avgTimer):
            memory[minute]=myArray[selfCounter]
            selfCounter+=1
        
    
        for minute in range(avgTimer,myArray.size-1):
            currentTrafic=myArray[selfCounter]
            selfCounter+=1 #Get the cuurent value that will be compared.
            weGood=True
            
            #Comparison.
            if isOutOfRange(memory,currentTrafic,avgTimer,upperBoundValue,lowerBoundValue) == [1,'l']:
                lowerErrCount=lowerErrCount+1
                upperErrCount=0
            elif isOutOfRange(memory,currentTrafic,avgTimer,upperBoundValue,lowerBoundValue) == [1,'u']:
                upperErrCount=upperErrCount+1
                lowerErrCount=0
            else:
                upperErrCount=0
                lowerErrCount=0
                
            if upperErrCount>=3:
                weGood=False
                
            if weGood==False:
                currValue=upperBoundValue
                return currValue+1
            
            memory=np.append(memory,currentTrafic)
    return 0
