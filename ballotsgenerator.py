import csv, random, numpy, os, copy, cProfile


'CHOOSES A FIRST PREFERENCE'
def generateFirstPreferences (numberToGenerate, percentages):
    candidates = [x for x in range(len(percentages))]
    return numpy.random.choice(candidates,size=numberToGenerate, p=percentages)

'GENERATES A BALLOT'
def generateBallot(firstPreference,numberOfPreferences,voteTransferProportionsForCandidate):
    ballot = []
    ballot.append(firstPreference)
    nextPreferences = numpy.random.choice(voteTransferProportionsForCandidate[0], numberOfPreferences-1, replace=False, p=voteTransferProportionsForCandidate[1])
    for nextPreference in nextPreferences:
        ballot.append(int(nextPreference))

    return ballot

def generateBallots(numberOfBallots,candidateSupportProportions, voteTransferProportions):
    ballots = []
    firstPreferences = generateFirstPreferences(numberOfBallots, candidateSupportProportions)
    for firstPreference in firstPreferences:
        lengthOfBallot = random.randint(1, len(candidateSupportProportions))
        ballots.append(generateBallot(firstPreference,lengthOfBallot, voteTransferProportions[firstPreference]))
    return(ballots)
def calculateVoterTurnout(meanNumberOfBallots):
    return int(round(random.gauss(meanNumberOfBallots, meanNumberOfBallots/20)))

def main(candidateSupportProportions,voteTransferProportions):

    'CALCULATE VOTER TURNOUT'
    meanNumberOfBallots = 1000
    numberOfBallots = calculateVoterTurnout(meanNumberOfBallots)
    print('Number of ballots to generate: ')
    print(numberOfBallots)

    'GENERATE THE BALLOTS'
    ballots = generateBallots(numberOfBallots, candidateSupportProportions, voteTransferProportions)

    'PRINT BALLOTS TO A FILE'
    ballotsFile = open("./src/main/resources/ballots.csv", "w")
    ballotsFileWriter = csv.writer(ballotsFile)
    ballotsFileWriter.writerows(ballots)
    ballotsFile.close()
    return ballots
