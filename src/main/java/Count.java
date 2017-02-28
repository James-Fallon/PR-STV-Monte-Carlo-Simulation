import java.util.*;
import java.util.stream.Collectors;

/**
 * Created by jamesfallon on 20/10/2016.
 */
public class Count {

    private int quota;
    private int numberOfSeats;
    private List<Ballot> ballots;
    private List<Candidate> candidates;
    private List<Candidate> electedCandidates;


    public Count (int numberOfSeats, List<Ballot> ballots, List<Candidate> candidates){

        this.numberOfSeats = numberOfSeats;
        this.ballots = ballots;
        this.candidates = candidates;
        electedCandidates = new ArrayList<>();
    }

    public List<Candidate> runCount ()
    {
        //TODO - Use stack for transferred ballots

        //Calculate quota
        quota = (ballots.size()/(numberOfSeats+1)) +1;

        System.out.println("Quota: " + quota + "\n");


        //Run first count
        for (Ballot ballot : ballots) {
            Candidate firstChoice = ballot.getNextPreference();
            firstChoice.addVote(ballot);
        }

        //Print first preferences

        System.out.println("First Preferences:");
        System.out.println("----------------------");
        for(Candidate candidate : candidates)
        {
            System.out.println(candidate.getSurname() + ": " + candidate.getVoteCount());
        }
        System.out.println("----------------------");


        int runNumber = 1;
        //Keep running counts until the seats are filled
        while(electedCandidates.size() < numberOfSeats) {

            Collections.sort(candidates);

            System.out.println("\nRun: " + runNumber );
            runNumber++;

            List<Ballot> ballotsToBeTransferred = new ArrayList<>();

            /**Check if any candidates have been elected:
             *
             * Loop through each candidate and see if they have reached the quota.
             * If they have reached the quota, we deem them elected and add them
             * to the electedCandidates list. We also add the candidate to a temporary 'electedOnThisCount' list
             * so that after the loop we can see if a surplus needs to be distributed.
             */


            boolean haveAnyCandidatesBeenElected = false;

            List<Candidate> electedOnThisCount = new ArrayList<>();

            Iterator<Candidate> candidateIterator = candidates.iterator();
            while (candidateIterator.hasNext()) {

                Candidate candidate = candidateIterator.next();

                if (candidate.getVoteCount() >= quota) {
                    candidate.setElected(true);

                    haveAnyCandidatesBeenElected = true;
                    System.out.println(candidate.getForename() + " " + candidate.getSurname() + " elected.");

                    electedOnThisCount.add(candidate);

                    //Redistribute ballots if required
                    int surplus = candidate.getVoteCount() - quota;
                    List<Ballot> votesToRedistribute = candidate.getBallots();

                    transferSurplus(votesToRedistribute, surplus);

                    electedCandidates.add(candidate);
                    candidateIterator.remove();
                    //TODO - Need to add ballots after count
                }

            }

            //Otherwise we eliminate the bottom candidate
            if(candidates.size() == (numberOfSeats - electedCandidates.size()))
            {
                electedCandidates.addAll(candidates);
            }
            else if(haveAnyCandidatesBeenElected == false){
                //If no candidate has reached the quota and there are still more candidates than seat vacancies,
                /*Eliminate the bottom candidate
                Candidate candidateToEliminate = candidates.get(0);
                candidateToEliminate.setEliminated(true);
                System.out.println(candidateToEliminate.getForename() + " " + candidateToEliminate.getSurname() + " eliminated.");
                transferEliminatedCandidatesVotes(candidateToEliminate.getBallots());
                candidates.remove(candidateToEliminate);*/


                /**
                 * Here we eliminate candidates until we have enough votes
                 * to transfer that could elect the highest candidate.
                 */

                int minimumRequiredVotesToElectCandidate = quota - candidates.get(candidates.size()-1).getVoteCount();
                int surplusAmount = 0;


                List<Candidate> eliminatedCandidates = new ArrayList<>();
                int i = 0;
                while(surplusAmount < minimumRequiredVotesToElectCandidate)
                {
                    Candidate candidate = candidates.get(i);
                    surplusAmount += candidate.getVoteCount();
                    ballotsToBeTransferred.addAll(candidate.getBallots());
                    candidate.setEliminated(true);
                    System.out.println(candidate.getForename() + " " + candidate.getSurname() + " eliminated.");
                    eliminatedCandidates.add(candidate);
                    i++;
                }

                candidates.removeAll(eliminatedCandidates);
                transferEliminatedCandidatesVotes(ballotsToBeTransferred);

            }



            //TODO - Transfer ballots + print relevant details.

        }

        return electedCandidates;
    }

    public void transferSurplus (List<Ballot> ballots, int surplus)
    {

        //Get all the transferable ballots

        List<Ballot> transferableBallots = ballots.stream().filter(Ballot::isTransferable).collect(Collectors.toList());


        if(surplus < transferableBallots.size())
        {

            //Split the transferable ballots into subparcels by the next preference

            Map<Candidate, List<Ballot>> parcels = new HashMap<>();

            for(Candidate candidate : candidates)
            {
                List<Ballot> votesForThisCandidate = new ArrayList<>();
                for(Ballot ballot : transferableBallots)
                {
                    if(ballot.getNextPreference().equals(candidate))
                    {
                        votesForThisCandidate.add(ballot);
                    }
                }
                parcels.put(candidate, votesForThisCandidate);
            }

            //Here we need to get the ratio of the number of transferable ballots to the surplus
            //and use that ratio to take a portion from each parcel

            List<Ballot> votesToTransfer = new ArrayList<>();

            for(Candidate parcel : parcels.keySet())
            {
                int numberOfVotesToTransfer = (int)Math.floor((parcels.get(parcel).size()*surplus)/ transferableBallots.size());
                votesToTransfer.addAll(parcels.get(parcel).subList(0, numberOfVotesToTransfer));
            }

            System.out.println("Transferring: " + votesToTransfer.size() + " ballots.");
            distributeVotes(votesToTransfer);
        }
        else {
            //If number of transferable ballots is equal to or greater than the surplus,
            //distribute all transferable ballots
            distributeVotes(transferableBallots);
        }

    }

    public void transferEliminatedCandidatesVotes (List<Ballot> votesToTransfer)
    {
        List<Ballot> transferableBallots = votesToTransfer.stream().filter(Ballot::isTransferable).collect(Collectors.toList());

        System.out.println("Transferring: " + transferableBallots.size() + " ballots");
        distributeVotes(transferableBallots);
    }

    public void distributeVotes (List<Ballot> votesToDistribute)
    {
        Map<Candidate, List<Ballot>> parcelsToTransfer = new HashMap<>();

        for(Candidate candidate : candidates)
        {
            List<Ballot> votesToTransferToThisCandidate = new ArrayList<>();

            for (Ballot ballot : votesToDistribute)
            {
                if(ballot.getNextPreference().equals(candidate))
                {
                    votesToTransferToThisCandidate.add(ballot);
                }
            }

            parcelsToTransfer.put(candidate, votesToTransferToThisCandidate);
        }

        for(Candidate candidate : parcelsToTransfer.keySet())
        {
            candidate.addVotes(parcelsToTransfer.get(candidate));
        }
    }

    public boolean isRedistributionRequired (int surplus)
    {
        for(Candidate candidate : candidates)
        {
            if(willSurplusElectCandidate(candidate, surplus) || willSurplusMoveCandidateFromBottomPlace(candidate,surplus))
            {
                return true;
            }
        }
        return false;
    }

    public boolean willSurplusElectCandidate (Candidate candidate, int surplus)
    {
        return (candidate.getVoteCount() + surplus) >= quota;
    }

    public boolean willSurplusMoveCandidateFromBottomPlace (Candidate candidate, int surplus)
    {
        Collections.sort(candidates);

        if(!candidates.get(0).equals(candidate))
        {
            return false;
        }
        else{
            int newVoteCountWithSurplus = candidate.getVoteCount() + surplus;
            return newVoteCountWithSurplus >= candidates.get(1).getVoteCount();
        }

    }

    //TODO - willSurplusRecoupElectionExpenses

}
