import readerClass
from findParameter import findLowerParameter,findUpperParameter
from timeit import default_timer as timer
from splitDay import splitDay

#split the day into n pieces. Get the fittest parameters.
#Then add RP.
#Write the learned parameters.

name = "cdn-learn" #learn or bad or good
mytype="Inbound" #Inbound or Outbound
avgTimer = 30
n = 8
rp=13
tableReader=readerClass.Reader(name,mytype)

with open('parameters/'+name+'.txt', 'w+') as file:
    file.write(str(avgTimer)+"\n")
    file.writelines(str(n)+"\n")
    file.writelines(str(rp)+"\n")
    
    partsOfDay=splitDay(tableReader.readEntireTable(), n)

    for counter in range(n):
        start = timer()
        file.write(str(findUpperParameter(partsOfDay[counter],avgTimer)+rp)+"-"
                   +str(findLowerParameter(partsOfDay[counter],avgTimer)+rp)+"\n")
        end = timer()
        print("Learned:" + str(counter+1) + "/" + str(n) + " in "  
              + str(end - start) + " seconds")
    
    