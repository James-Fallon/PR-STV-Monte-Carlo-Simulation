import java.util.ArrayList;
import java.util.List;

/**
 * Created by jamesfallon on 13/10/2016.
 */
public class Candidate implements Comparable<Candidate> {

    private int id;

    private final String forename, surname;

    private Party party;
    private List<Ballot> ballots = new ArrayList<>();
    private boolean isElected = false;
    private boolean isEliminated = false;

    public Candidate (int id, String forename, String surname, Party party)
    {
        this.id = id;
        this.forename = forename;
        this.surname = surname;
        this.party = party;
    }

    public int getId()
    {
        return id;
    }

    public String getForename (){
        return forename;
    }

    public String getSurname (){
        return surname;
    }

    public void addVote (Ballot ballot)
    {
        ballots.add(ballot);
    }

    public void addVotes (List<Ballot> votesToAdd)
    {
        ballots.addAll(votesToAdd);
    }

    public Integer getVoteCount()
    {
        return ballots.size();
    }

    public boolean isElected() {
        return isElected;
    }

    public void setElected (boolean elected)
    {
        isElected = elected;
    }

    public boolean isEliminated() {
        return isEliminated;
    }

    public void setEliminated(boolean eliminated) {
        isEliminated = eliminated;
    }

    public boolean isActive ()
    {
        return !(isElected || isEliminated);
    }

    @Override
    public String toString ()
    {
        return id + "," + forename + "," + surname + "," + party;
    }

    @Override
    public int compareTo(Candidate c) {
        if (this.getVoteCount() == c.getVoteCount()) {
            return 0;
        } else {
            return this.getVoteCount() > c.getVoteCount() ? 1 : -1;
        }
    }

    public List<Ballot> getBallots() {
        return ballots;
    }
}
