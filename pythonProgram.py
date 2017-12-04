import sys
import operator
import rdflib
import csv

data = rdflib.Graph()
data.load(sys.argv[1])
historicalPersonalityName = sys.argv[1].rsplit('/',1)[-1].rsplit('.')[0].replace("_", " ")
textData = [[0 for x in range(3)] for y in range(len(data))]

#Storing the tuples from RDF graph as lists
i = 0
for subject, predicate, obj in data:
    textData[i][0] = subject.rsplit('/', 1)[-1].replace("_", " ")
    textData[i][1] = predicate.rsplit('/', 1)[-1].replace("_", " ")
    textData[i][2] = obj.rsplit('/', 1)[-1].replace("_", " ")
    i = i + 1
i = 0

#Sorting the data on the basis of subject and predicate columns
sortedTextData = sorted(textData, key = operator.itemgetter(0, 1))#lambda x:x[1])

fileWriter = csv.writer(open(historicalPersonalityName + ".csv","w"), delimiter=',', quoting=csv.QUOTE_ALL)
dataToWrite = [0 for x in range(3)]
numberOfBirthdates = 0;

#Checking number of birthdates
for subject, predicate, obj in sortedTextData:
    if predicate == "birthDate":
        numberOfBirthdates = numberOfBirthdates + 1
skipFlag = True

#Writing lists to a CSV file named as the historical figure
#print(historicalPersonalityName)
for subject, predicate, obj in sortedTextData:
   # print(subject, "||||", predicate, ">>>>", obj)  #if subject == historicalPersonalityName:
   if skipFlag == True: #To skip spurious birth dates
        if predicate == "birthDate" and numberOfBirthdates > 1:
            skipFlag = False
            continue
    dataToWrite[0] = subject
    dataToWrite[1] = predicate
    dataToWrite[2] = obj
    fileWriter.writerow(dataToWrite)
