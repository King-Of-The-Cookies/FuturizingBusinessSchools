import java.sql.Connection;
import java.sql.Date;
import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;
import static java.lang.Math.toIntExact;
public class DBSetup {

	
	
	
    public void sendToDB(long tweetID, int universityID, String tweetText, String tweetlanguage, String screenName, String tweetCreatedAt, int favoriteCount, String source, String isRetweeted, int retweetCount, Connection connection) throws SQLException{
    	try{
    		
//    		Class.forName("oracle.jdbc.driver.OracleDriver");
//    		Connection con2 = DriverManager.getConnection("");
//    		

    		
    		
    		String sql = "INSERT INTO FBSADMIN.TWITTER (TWEETID, UNIVERSITY_ID, TWEETTEXT, TWEETLANGUAGE, SCREENNAME, TWEETDATE, FAVORITECOUNT, SOURCE, ISRETWEETED, RETWEETCOUNT) VALUES (?,?,?,?,?,?,?,?,?,?)";
    		PreparedStatement pst = connection.prepareStatement(sql);
    		//pst.setLong(1, tweetID);
    		pst.setLong(1, tweetID);
    		pst.setInt(2, universityID);
    		pst.setString(3, tweetText);
    		pst.setString(4, tweetlanguage);
    		pst.setString(5, screenName);
    		pst.setString(6, tweetCreatedAt);
    		pst.setInt(7, favoriteCount);
    		pst.setString(8, source);
    		pst.setString(9, isRetweeted);
    		pst.setInt(10, retweetCount);

    		
    		pst.executeUpdate();
    		pst.close();
    		
    	} catch (Exception e){
    		System.out.println(e);
    }
    
    }
    
    
    
}
