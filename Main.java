import java.io.IOException;
import java.sql.SQLException;
import java.text.ParseException;

import twitter4j.QueryResult;
import twitter4j.TwitterException;

public class Main {

	public static void main(String[] args) throws TwitterException, ParseException, IOException, SQLException, ClassNotFoundException {
		// TODO Auto-generated method stub
		TwitterSetup twitter = new TwitterSetup("", "",
				"", "");
		
		DBSetup connect = new DBSetup();
		connect.connectToDB();
		twitter.getTimeline("@MaastrichtU","01/01/2011", 1);
		connect.closeDB();
		System.out.println("Done");
	}

}
