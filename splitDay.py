#The code to split the day.

import numpy as np
def splitDay(arrayToBeSplit,n):

    if int(arrayToBeSplit.size) % n != 0:
        print(int(arrayToBeSplit.size) % n)
        raise Exception("Array not divisible")

    return np.split(arrayToBeSplit,n)