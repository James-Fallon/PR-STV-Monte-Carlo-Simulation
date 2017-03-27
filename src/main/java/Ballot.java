import java.util.List;
import java.util.Map;

public class Ballot {

    private int id;
    private static int idCounter = 0;

    //List to store preferences of candidates.
    //index 0 is first choice, 1 is 2nd choice etc
    private List<Candidate> preferences;

    //Denotes whether or not this vote can be transferred

    public Ballot(List<Candidate> preferences)
    {
        this.id = ++idCounter;
        this.preferences = preferences;
    }

    public Candidate getNextPreference() {
        for (Candidate candidate : preferences)
        {
            if(candidate.isActive())
            {
                return candidate;
            }
        }

        return null;
    }

    public boolean isTransferable() {
        for (Candidate candidate : preferences)
        {
            if(candidate.isActive())
            {
                return true;
            }
        }
        return false;
    }

    @Override
    public String toString()
    {
        String string = "";
        for (int i = 1; i <= 12; i++) {

            if(preferences.get(i) == null)
            {
                string = string.concat(",");
            }
            else
            {
                string = string.concat(preferences.get(i).getId()+",");
            }

        }
        return string.substring(0,string.length()-1);
    }
}