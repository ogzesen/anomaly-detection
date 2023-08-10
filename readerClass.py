import pandas as pd
import numpy as np

#For reading csv trafic data.

class Reader:

    #Takes the name of the table, opens it up and cleans it.
    def __init__(self, nameOfTable, mytype):
        self.name = nameOfTable
        self.counter = 0
        concString = "resources/CDN/" + self.name + ".csv"
        self.df=pd.read_csv(concString , on_bad_lines = 'skip')
        self.inboundData=self.df.loc[:,mytype].to_numpy()
        self.inboundData=self.inboundData/1000000000
        for counter in range(self.inboundData.size):
            if str(self.inboundData[counter])=="nan":
                self.inboundData[counter]=0  

    #Return entire day.
    def readEntireTable(self):
        return self.inboundData
    
    #Returns the next minute. Acts like a simulation.
    def getValue(self):
        self.counter=self.counter+1
        return self.inboundData[self.counter-1]
        