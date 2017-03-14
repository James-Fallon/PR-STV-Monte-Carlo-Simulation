import java.io.*;
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
            bufferedReader.close();
        } catch (IOException e) {
            e.printStackTrace();
        }

        /**
         *
         * Parse ballots from file
         */

        if(args.length < 2 || !args[1].endsWith(".csv"))
        {
            throw new IllegalArgumentException();
        }

        String ballotsFilePath = args[1];

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
            ballotsBufferedReader.close();
        } catch (IOException e) {
            e.printStackTrace();
        }


        System.out.println("Candidates: " + candidates.size());
        System.out.println("Ballots: " + ballots.size());

        //Run count
        Count count = new Count(Integer.parseInt(args[0]), ballots, candidates);

        List<Candidate> electedCandidates = count.runCount();


        //Sort + print results

        Collections.sort(electedCandidates);
        Collections.reverse(electedCandidates);

        System.out.println();
        System.out.println("Elected Candidates: ");
        System.out.println("-----------------------");
        //File electedCandidatesFile = new File("/Users/jamesfallon/Documents/FYP/Vote Generator/results/electedCandidates.csv");
        //BufferedWriter bufferedWriter = null;

            //bufferedWriter = new BufferedWriter(new FileWriter(electedCandidatesFile));


            for(Candidate candidate : electedCandidates)
            {

                System.out.println(candidate.getId()+","+candidate.getForename() + " " + candidate.getSurname() + ": " + candidate.getVoteCount());
               // bufferedWriter.write(candidate.getId()+","+candidate.getSurname()+","+candidate.getForename()+","+candidate.getVoteCount());
               // bufferedWriter.newLine();
            }
           // bufferedWriter.close();
            System.out.println("-----------------------");


        /**
         * Print results in a format that our python script can eat
         */
        System.out.print("For python script:\n!!");
        for(Candidate candidate : electedCandidates)
        {
            System.out.println(candidate.getId() + ","+candidate.getVoteCount());
        }
        System.out.print("!!");

    }
}
