#The function to compute whether the current trafic is in range or not.

import numpy as np

def isOutOfRange(KnownArray,TestPoint,avgTimer,upperBoundValue,lowerBoundValue):
        averageValue=np.average(KnownArray[KnownArray.size-avgTimer:KnownArray.size])
        if TestPoint >= averageValue*(1+(upperBoundValue/100)):
            return [1,'u']
        elif TestPoint <= averageValue*(1-(lowerBoundValue/100)):
            return [1,'l']
        else:
            return 0
        
def calculateAvg(KnownArray,TestPoint,avgTimer):
        averageValue=np.average(KnownArray[KnownArray.size-avgTimer:KnownArray.size])
        return averageValue