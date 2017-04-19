import java.sql.Connection;
import java.sql.Date;
import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;

public class DBSetup {

	private Connection con;
	
	public void connectToDB(){
		try{
		Class.forName("oracle.jdbc.driver.OracleDriver");
		this.con = DriverManager.getConnection("jdbc:oracle:thin:@um003089.unimaas.nl:1521:FBSDB","FBSADMIN","FA8skhg6");
		}catch(Exception e){
			System.out.println(e);
		}
		
	}
	
	
    public void sendToDB(long tweetID, int universityID, String tweetText, String tweetlanguage, String screenName, String tweetCreatedAt, int favoriteCount, String source, String isRetweeted, int retweetCount ) throws SQLException{
    	try{
    		
    		String sql = "INSERT INTO twitter VALUES (?,?,?,?,?,?,?,?,?,?)";
    		PreparedStatement pst = con.prepareStatement(sql);
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
    		
    		
    	} catch (Exception e){
    		System.out.println(e);
    }
    
    }
    
    public void closeDB(){
    	try{
    	this.con.close();
    	}catch(Exception e){
    		System.out.println(e);
    	}
    }
    
}
