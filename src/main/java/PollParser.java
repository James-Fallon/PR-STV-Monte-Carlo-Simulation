import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.IOException;
import java.util.*;

/**
 * Created by jamesfallon on 09/01/2017.
 */
public class PollParser {

    public static void main (String args[])
    {
        /**
         * Parse 'candidates' file to create Candidate objects
         */

        String candidatesFilePath = "/Users/jamesfallon/Documents/FYP/Vote Generator/data/GalwayWestCandidates.csv";

        List<Candidate> candidates = new ArrayList<>();

        File candidateFile = new File(candidatesFilePath);

        BufferedReader bufferedReader = null;

        Map<Integer, Candidate> candidateIds = new HashMap<>();
        try {
            bufferedReader = new BufferedReader(new FileReader(candidateFile));
            String line;

            while((line = bufferedReader.readLine()) != null)
            {
                String[] lineEntries = line.split(",");

                Candidate candidate = new Candidate(Integer.valueOf(lineEntries[0]),lineEntries[2],lineEntries[1],Party.valueOf(lineEntries[3]));

                candidateIds.put(Integer.valueOf(lineEntries[0]), candidate);
                candidates.add(candidate);
            }
        } catch (IOException e) {
            e.printStackTrace();
        }

        /**
         *
         * Parse ballots from file
         */



        String ballotsFilePath = "/Users/jamesfallon/Documents/FYP/Vote Generator/results/EliminationTestBallots.csv";

        List<Ballot> ballots = new ArrayList<>();

        File ballotsFile = new File(ballotsFilePath);

        BufferedReader ballotsBufferedReader = null;

        try {
            ballotsBufferedReader = new BufferedReader(new FileReader(ballotsFile));
            String line;

            while((line = ballotsBufferedReader.readLine()) != null)
            {
                String[] lineEntries = line.split(",");

                List<Candidate> preferences = new ArrayList<>();

                for(String lineEntry : lineEntries)
                {
                    Integer candidateID = Integer.valueOf(lineEntry);
                    preferences.add(candidateIds.get(candidateID));
                }

                ballots.add(new Ballot(preferences));
            }
        } catch (IOException e) {
            e.printStackTrace();
        }


        System.out.println("Candidates: " + candidates.size());
        System.out.println("Ballots: " + ballots.size());
        //Run count

        Count count = new Count(2, ballots, candidates);

        List<Candidate> electedCandidates = count.runCount();


        //Sort + print results

        Collections.sort(electedCandidates);
        Collections.reverse(electedCandidates);

        System.out.println();
        System.out.println("Elected Candidates: ");
        System.out.println("-----------------------");

        for(Candidate candidate : electedCandidates)
        {
            System.out.println(candidate.getForename() + " " + candidate.getSurname() + ": " + candidate.getVoteCount());
        }

        System.out.println("-----------------------");

    }
}
