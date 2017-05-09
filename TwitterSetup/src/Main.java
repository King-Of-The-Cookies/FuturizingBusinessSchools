import java.io.FileReader;
import java.io.IOException;
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.SQLException;
import java.text.ParseException;
import java.util.ArrayList;
import java.util.List;

import au.com.bytecode.opencsv.CSVReader;
import twitter4j.QueryResult;
import twitter4j.TwitterException;

public class Main {
	
	private static Connection con;
	
	public static void main(String[] args) throws TwitterException, ParseException, IOException, SQLException, ClassNotFoundException {
		// TODO Auto-generated method stub
		
		TwitterSetup twitter = new TwitterSetup();
		
		List<String> usernames = readcsv("");
		
		
		
		connectToDB();
		for(int i=0; i < usernames.size(); i++){
			twitter.getTimeline(usernames.get(i),"01/01/2011", i+1, con);
			
		}
		
		closeDB();
		
		System.out.println("Done");
	}

	
	public static void connectToDB(){
		Connection con1 = null;
		try{
		Class.forName("oracle.jdbc.driver.OracleDriver");
		con1 = DriverManager.getConnection();
		}catch(Exception e){
			System.out.println(e);
		}
		con = con1;
		
	}
	public static void closeDB(){
    	try{
    	con.close();
    	}catch(Exception e){
    		System.out.println(e);
    	}
    }
	
	public static List<String> readcsv(String file_path) throws IOException{
		CSVReader reader = new CSVReader(new FileReader(file_path));
		List<String> twitterUsernames = new ArrayList<String>();
		
		String[] record = null;
		while((record = reader.readNext()) != null){
			twitterUsernames.add(record[0]);
		}
		return twitterUsernames;
		
		
	}
}
