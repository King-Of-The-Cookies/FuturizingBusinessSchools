import java.io.IOException;
import java.sql.SQLException;
import java.text.ParseException;

import twitter4j.QueryResult;
import twitter4j.TwitterException;

public class Main {

	public static void main(String[] args) throws TwitterException, ParseException, IOException, SQLException, ClassNotFoundException {
		// TODO Auto-generated method stub
		TwitterSetup twitter = new TwitterSetup("QYpCZW54iTLsciRrA950zhPov", "4FMGwrQHEzWLY7XAmOx9tf7ydVjiq29E4QJJt8SHwb3Uv1AIpc",
				"3515448134-0NWc5GRqLjv71smt72ux7kh57s09meZarnflFNw", "AdBATS664XDkMmRpaHNmKmDBTh9QMmCb3dT3a5LB10Cyq");
		
		DBSetup connect = new DBSetup();
		connect.connectToDB();
		twitter.getTimeline("@MaastrichtU","01/01/2011", 1);
		connect.closeDB();
		System.out.println("Done");
	}

}
