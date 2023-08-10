import readerClass
import numpy as np
from isOutOfRange import isOutOfRange, calculateAvg
import matplotlib.pyplot as plt
import math

#Define variables
name="cdn"
case="good"
mytype="Inbound"

upperBoundValue=[]
lowerBoundValue=[]

with open('parameters/'+name+'-learn.txt', 'r') as file:
    Lines = file.readlines()
    lineCounter=1
    
    for line in Lines:
        if lineCounter==1:
            avgTimer=int(line)
    
        elif lineCounter==2:
            n=int(line)
            
        elif lineCounter==3:
            rp=line
            
        else:
            upperBoundValue.append(int(line.split('-')[0]))
            lowerBoundValue.append(int(line.split('-')[1]))

        lineCounter+=1
        


tableReader=readerClass.Reader(name+"-"+case,mytype)
upperThreshold=np.zeros(avgTimer)
lowerThreshold=np.zeros(avgTimer)
memory=np.zeros(avgTimer)

#Get the initial data to compute the average.
for minute in range(avgTimer):
    memory[minute]=tableReader.getValue()
    upperThreshold[minute]=memory[minute]*2
    lowerThreshold[minute]=memory[minute]*-2
    
avgHistory=memory
#Graph stuff.
plotTime1=np.arange(avgTimer)
plotTime2=np.arange(tableReader.inboundData.size)
upperAnomalies=np.ones(tableReader.inboundData.size)*-10
lowerAnomalies=np.ones(tableReader.inboundData.size)*-10
plt.ion()
fig = plt.figure()
ax = fig.add_subplot(111)

line6, = ax.plot(plotTime1, avgHistory, color="blue", label="Average of Last "+ str(avgTimer)+" Minutes")
line1, = ax.plot(plotTime1, memory, color="red" ,linewidth=0.7, label=mytype + " Data")
line2, = ax.plot(plotTime2, upperAnomalies, 'x', color="#9404bf", markersize=7, label="Anomalies")
line3, = ax.plot(plotTime2, lowerAnomalies, 'x', color="#9404bf", markersize=7)
line4, = ax.plot(plotTime1, upperThreshold, color="white", linewidth=0.0) 
line5, = ax.plot(plotTime1, lowerThreshold, color="white", linewidth=0.0)


plt.ylim((-2,tableReader.inboundData.max()*3))
plt.xlim((0,1440))
plt.xlabel("Minutes Counting From 00:00 for 24 Hours (1440 Minutes)")
plt.ylabel("Gigabits")

if case=="good":
    titleCase=" With No Anomalies"
elif case=="bad":
    titleCase=" With Anomalies"
elif case=="learn":
    titleCase="-Training Set-"
plt.title("One Day of " + name.upper() + " Trafic" + titleCase + "\n Day Divided Into " + str(n) + " Pieces with R.P = " + rp)

#The day loop.
upperErrCount=0
lowerErrCount=0    
for minute in range(avgTimer,tableReader.inboundData.size):
    currentTrafic=tableReader.getValue() #Get the cuurent value that will be compared.
    currentAvg=calculateAvg(memory,currentTrafic,avgTimer)

    #Comparison.
    if isOutOfRange(memory,currentTrafic,avgTimer,upperBoundValue[math.floor((minute*n)/1440)],lowerBoundValue[math.floor((minute*n)/1440)]) == [1,'l']:
        lowerErrCount=lowerErrCount+1
        upperErrCount=0
    elif isOutOfRange(memory,currentTrafic,avgTimer,upperBoundValue[math.floor((minute*n)/1440)],lowerBoundValue[math.floor((minute*n)/1440)]) == [1,'u']:
        upperErrCount=upperErrCount+1
        lowerErrCount=0
    else:
        upperErrCount=0
        lowerErrCount=0
        
    if lowerErrCount>=3:
        lowerAnomalies[minute]=currentTrafic
    if upperErrCount>=3:
        upperAnomalies[minute]=currentTrafic
        
    #Plot every 10 instances.
    if minute % 10 == 0 or minute==tableReader.inboundData.size-1:
        line1.set_xdata(plotTime1)
        line1.set_ydata(memory)
        line2.set_ydata(upperAnomalies)
        line3.set_ydata(lowerAnomalies)
        line4.set_xdata(plotTime1)
        line4.set_ydata(upperThreshold)
        line5.set_xdata(plotTime1)
        line5.set_ydata(lowerThreshold)
        line6.set_xdata(plotTime1)
        line6.set_ydata(avgHistory)
        fig.canvas.draw() 
        fig.canvas.flush_events()
    
    #Update the variables.
    plotTime1=np.append(plotTime1,plotTime1[-1]+1)
    memory=np.append(memory,currentTrafic)
    avgHistory=np.append(avgHistory,currentAvg)
    lowerThreshold=np.append(lowerThreshold,currentTrafic*(1-lowerBoundValue[math.floor((minute*n)/1440)]/100))
    upperThreshold=np.append(upperThreshold,currentTrafic*(1+upperBoundValue[math.floor((minute*n)/1440)]/100))

plt.fill_between(plotTime1, upperThreshold, memory, where= plotTime1>avgTimer, color="#42f5a1", label="Aceptable Region")
plt.fill_between(plotTime1, memory, lowerThreshold, where= plotTime1>avgTimer, color="#42f5a1")
ax.legend()
plt.show()
    


