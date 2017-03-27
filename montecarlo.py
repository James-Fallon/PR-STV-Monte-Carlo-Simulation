import ballotsgenerator, printresults
import numpy as np,csv,os.path,subprocess,operator,copy
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.plotly as pltly
import plotly.graph_objs as go
import pylab
import webbrowser
from subprocess import STDOUT,PIPE

'Parse Candidate Data'
'-------------------------------------------------------------------------------'

#Parse candidate support poll
candidateDataFile = open('./src/main/resources/candidates-GalwayWest.csv', 'r')
candidateData = list(csv.reader(candidateDataFile))
candidateDataFile.close()
#Get the raw percentages from the data
originalCandidateSupportProportions = [float(row[4]) for row in candidateData]

parties = {x[3] for x in candidateData}

#Create dictionary with candidates per party
#Parse data into a dictionary
candidatesPerParty = {}
for party in parties:
    candidatesInThisParty = []
    for candidate in candidateData:
        if candidate[3] == party:
            candidatesInThisParty.append(candidate[0])
    candidatesPerParty[party] = candidatesInThisParty

def generateCandidateSupportProportions():
    #Account for simple random sampling error
    #candidateSupportProportions = [np.random.normal(x, np.sqrt((x*(1-x))/samplesize)) for x in originalCandidateSupportProportions]
    candidateSupportProportions = [np.random.normal(x, marginOfError) for x in originalCandidateSupportProportions]

    #If any of drawn values are < 0, set them to 0
    candidateSupportProportions = [x if x > 0 else 0.0 for x in candidateSupportProportions]
    #Normalise so the sum is still 1
    return[x/sum(candidateSupportProportions) for x in candidateSupportProportions]

'Vote Transfer Proportions'
'-------------------------------------------------------------------------------'

#Parse voteTransferData
voteTransferDataFile = open('./src/main/resources/transfers-GalwayWest.csv', 'r')
voteTransferData = list(csv.reader(voteTransferDataFile))
voteTransferDataFile.close()
#Remove the header and store it for later
voteTransferDataHeader = voteTransferData.pop(0)
voteTransferDict = {}
for row in voteTransferData:
    partyToTransfer = row[0]
    for index in range(1,len(row)):
        voteTransferDict[partyToTransfer+','+voteTransferDataHeader[index]] = row[index]

def getWeightedNextPreferencesForCandidate(firstPrefCandidate):
    possibleCandidates = list(range(0,len(candidateData)))
    possibleCandidates.remove(firstPrefCandidate)
    weightedNextPreferencesForCandidate = np.ndarray(shape=(2,len(possibleCandidates)))
    percentagesForRandomChoice = {}
    transferringParty = candidateData[int(firstPrefCandidate)][3]
    partiesToTransferTo = copy.deepcopy(parties)

    for party in partiesToTransferTo:
        partyPercentage = float(voteTransferDict[transferringParty+','+party])
        percentagePerPartyMember = partyPercentage/float(len(candidatesPerParty[party]))

        candidatesInThisParty = copy.deepcopy(candidatesPerParty[party])
        if(firstPrefCandidate in candidatesInThisParty):
            candidatesInThisParty.remove(firstPrefCandidate)

        for candidateInThisParty in candidatesInThisParty:
            percentagesForRandomChoice[int(candidateInThisParty)] = percentagePerPartyMember

    percentages = []
    for candidate in possibleCandidates:
        percentages.append(percentagesForRandomChoice[candidate])

    #If the sum doesn't equal 1, numpy.random.choice will throw an exception
    #This is more than likely to occur because we are splitting percentages among each party
    #To compensate for this we get the difference and add it to one random candidate in the list

    percentages = [x/sum(percentages) for x in percentages]


    weightedNextPreferencesForCandidate[0] = possibleCandidates
    weightedNextPreferencesForCandidate[1] = percentages

    return weightedNextPreferencesForCandidate


#Creating an ndarray for each candidate.
#This ndarray has 2 rows. The first row contains the ids of all the other candidates.
#The second row contains the vote transfer percentage to each of these candidates.
#The rows are indexed the same. i.e The vote transfer percentage for the candidate in cell 1,1 will be in cell 2,1

weightedNextPreferencesPerCandidate = {}
for index in range(len(candidateData)):
    weightedNextPreferencesPerCandidate[index] = getWeightedNextPreferencesForCandidate(index)

def generateVoteTransferProportions():

    voteTransferProportionsPerCandidate = copy.deepcopy(weightedNextPreferencesPerCandidate)

    for key in voteTransferProportionsPerCandidate:

        #Account for simple random sampling error
        voteTransferProportionsPerCandidate[key][1] = [np.random.normal(x, marginOfError*2) for x in voteTransferProportionsPerCandidate[key][1]]
        #If any of drawn values are < 0, set them to 0.001 (np.random.choice will throw an error if theyre not)
        voteTransferProportionsPerCandidate[key][1] = [x if x > 0 else 0.001 for x in voteTransferProportionsPerCandidate[key][1]]
        #Normalise so the sum is still 1
        voteTransferProportionsPerCandidate[key][1] = [x/sum(voteTransferProportionsPerCandidate[key][1]) for x in voteTransferProportionsPerCandidate[key][1]]


    return voteTransferProportionsPerCandidate


'-------------------------------------------------------------------------------'

#samplesize = 515
marginOfError = 0.028
numberOfRuns = 30
numberOfWinsPerCandidate = {candidate[0]:0 for candidate in candidateData}

outcomeFrequencys = {}

for i in range(numberOfRuns):

    candidateSupportProportions = generateCandidateSupportProportions()
    voteTransferProportions = generateVoteTransferProportions()

    #Generate ballots
    ballots = ballotsgenerator.main(candidateSupportProportions, voteTransferProportions)

    #Run the java simulation
    cmd = ['mvn','test', '-Pgalway-west']
    proc = subprocess.Popen(cmd, stdin=PIPE, stdout=PIPE, stderr=STDOUT)
    stdout,stderr = proc.communicate()
    #print ('This was "' + stdout + 'STOPPED')
    results = stdout.split("!!")

    outcome = set()
    #Get the results of the simulation
    electedCandidates = results[1].split("\n")
    electedCandidates.pop()
    for electedCandidate in electedCandidates:
        candidateID,voteCount = electedCandidate.split(",")
        outcome.add(candidateID)
        numberOfWinsPerCandidate[candidateID] = numberOfWinsPerCandidate[candidateID]+1

    outcome = frozenset(outcome)
    #Add this outcome to the outcome frequencys list if its not already there
    if outcome in outcomeFrequencys.keys():
        outcomeFrequencys[outcome] = outcomeFrequencys[outcome] + 1
    else:
        outcomeFrequencys[outcome] = 1

'-------------------------------------------------------------------------------'

sorted_numberOfWinsPerCandidate = sorted(numberOfWinsPerCandidate.items(), key=operator.itemgetter(1), reverse=True)
print 'Chance of winning a seat:'

percentageOfWinsPerCandidate = [0.0] * len(candidateData)
for candidate in sorted_numberOfWinsPerCandidate:
    name = candidateData[int(candidate[0])][2] + " " + candidateData[int(candidate[0])][1]
    numberOfWins = float(candidate[1])
    percentageOfWins = float((numberOfWins/float(numberOfRuns))*100.0)
    percentageOfWinsPerCandidate[int(candidate[0])] = percentageOfWins
    print(percentageOfWins)
    print name + ": %" + str(percentageOfWins)

'-------------------------------------------------------------------------------'

highestOutcomeFrequency = 0

for key in outcomeFrequencys:
    if outcomeFrequencys[key] > highestOutcomeFrequency:
        highestOutcomeFrequency = outcomeFrequencys[key]
        mostCommonOutcome = key

outcomeResult = "Most common outcome: \n%r\n with %r occurrences" % (mostCommonOutcome,outcomeFrequencys[mostCommonOutcome])

print outcomeResult

mostCommonOutcome = list(mostCommonOutcome)

candidates = [x[2] + ' ' + x[1] for x in candidateData]


printresults.main(candidateData, percentageOfWinsPerCandidate, mostCommonOutcome)
