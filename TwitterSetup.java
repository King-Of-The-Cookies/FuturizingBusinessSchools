import java.io.FileWriter;
import java.io.IOException;
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;
import java.text.DateFormat;
import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.time.format.DateTimeFormatter;
import java.util.ArrayList;
import java.util.Date;
import java.util.List;
import java.util.Map;
import java.util.Properties;
import java.util.Set;

import au.com.bytecode.opencsv.CSVWriter;
import oracle.jdbc.pool.OracleDataSource;
import twitter4j.HashtagEntity;
import twitter4j.Paging;
import twitter4j.Query;
import twitter4j.QueryResult;
import twitter4j.RateLimitStatus;
import twitter4j.ResponseList;
import twitter4j.Status;
import twitter4j.Twitter;
import twitter4j.TwitterException;
import twitter4j.TwitterFactory;
import twitter4j.TwitterResponse;
import twitter4j.URLEntity;
import twitter4j.api.HelpResources;
import twitter4j.auth.OAuth2Token;
import twitter4j.conf.ConfigurationBuilder;

public class TwitterSetup {
	
	private Twitter twitter;
	private Status maxPost;
	private Paging pg;
	private Date maxDate;
	
	
	public TwitterSetup(String ConsumerKey, String ConsumerSecret, String AccessToken, String AccessTokenSecret) throws TwitterException{
		ConfigurationBuilder builder = new ConfigurationBuilder();
        //builder.setUseSSL(true);
        builder.setApplicationOnlyAuthEnabled(true);
        builder.setOAuthConsumerKey(ConsumerKey);
        builder.setOAuthConsumerSecret(ConsumerSecret);

        OAuth2Token token = new TwitterFactory(builder.build()).getInstance().getOAuth2Token();

        builder = new ConfigurationBuilder();
        //builder.setUseSSL(true);
        builder.setApplicationOnlyAuthEnabled(true);
        builder.setOAuthConsumerKey(ConsumerKey);
        builder.setOAuthConsumerSecret(ConsumerSecret);
        builder.setOAuth2TokenType(token.getTokenType());
        builder.setOAuth2AccessToken(token.getAccessToken());

        this.twitter = new TwitterFactory(builder.build()).getInstance();
		
		
		
		
//		ConfigurationBuilder cb = new ConfigurationBuilder();
//		cb.setOAuthConsumerKey(ConsumerKey);
//		cb.setOAuthConsumerSecret(ConsumerSecret);
//		cb.setOAuthAccessToken(AccessToken);
//		cb.setOAuthAccessTokenSecret(AccessTokenSecret);
//		TwitterFactory tf = new TwitterFactory(cb.build());
//		this.twitter = tf.getInstance();
	}
	
	
	public void searchTwitter(String searchTerm) throws TwitterException{
		Query query = new Query(searchTerm);
		QueryResult result = twitter.search(query);
		List<Status> tweets = result.getTweets();
		for (Status tweet:tweets){
			String text = tweet.getText();
			System.out.println(text);
		}
		
	}
	
	private void setMaxDate(String dateFull) throws ParseException{
		
		DateFormat format = new SimpleDateFormat("dd/MM/yyyy");
		Date date = format.parse(dateFull);
		this.maxDate = date;
	}
	
	public void getTimeline(String userName, String maxDateDDMMYYYY, int universityID) throws TwitterException, ParseException, IOException{
		DBSetup dbsetup = new DBSetup();

		setMaxDate(maxDateDDMMYYYY);
		this.pg = new Paging(1,1);
		List<Status> mostRecentPost = twitter.getUserTimeline(userName, pg);
		maxPost = mostRecentPost.get(0);
		CSVWriter writer = new CSVWriter(new FileWriter("data3.csv"), ';');
		while (true){
			this.pg = new Paging(1,500).maxId(maxPost.getId());
			List<Status> timelinePosts = twitter.getUserTimeline(userName, pg);
			System.out.println("Collected posts: " + timelinePosts.size());
			if(timelinePosts.size()==1){
				break;
			}
			
			Map<String, RateLimitStatus> ratelim = twitter.getRateLimitStatus();
			RateLimitStatus Applicationlim = ratelim.get("/application/rate_limit_status");
			RateLimitStatus Timelinelim = ratelim.get("/statuses/user_timeline");
			
			System.out.println("Application limit :" + Applicationlim.getRemaining() + "," + "Timelinelim: " + Timelinelim.getRemaining());
			
			if (Applicationlim.getRemaining() < 5 || Timelinelim.getRemaining() < 5){
				try {
					Thread.sleep(15*60*1000);
				} catch (InterruptedException e) {
	
					e.printStackTrace();
				}
				
			}
			
			
			this.maxPost = timelinePosts.get(timelinePosts.size()-1);
				if(maxPost.getCreatedAt().before(this.maxDate)){
					break;
				}
			
			for (Status post:timelinePosts){
				
				
				long tweetid = post.getId();
				String tweetText = post.getText();

				String tweetlanguage = post.getLang();
				String screenName = post.getUser().getScreenName();
				String tweetCreatedAt = post.getCreatedAt().toString();
				int favoriteCount = post.getFavoriteCount();
				String source = post.getSource();
				String isRetweeted = Boolean.toString(post.isRetweet());
				int retweetCount = post.getRetweetCount();
				
				
				
				
				try {
					dbsetup.sendToDB(tweetid, universityID, tweetText, tweetlanguage, screenName, tweetCreatedAt, favoriteCount, source, isRetweeted, retweetCount);
				} catch (SQLException e) {
					// TODO Auto-generated catch block
					e.printStackTrace();
				}
				
				
				
//				String[] record = {tweetText, Integer.toString(universityID), tweetlang, tweetCreatedAt, favoriteCount, source, isRetweeted, retweetCount, screenName};
//				
//				writer.writeNext(record);
//				
//				
//				writer.flush();
				
				//post.
				//System.out.println(tweetText);
			}
			
		}
		//writer.close();
				

		}

	
		
}
	

