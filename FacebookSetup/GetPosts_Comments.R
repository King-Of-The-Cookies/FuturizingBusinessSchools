getPostsComments <- function(pageID, token, since){
  universitypage <- getPage(pageID, n= 10000, token = token, since = since)
  comments <- data.frame()
  
  for(i in 1:nrow(universitypage)){
    comments_post <- getPost(universitypage[i, 7], token, comments = TRUE, likes=TRUE)$comments
    comments <- rbind(comments, comments_post)
  }
  
posts_comments = list("posts" = universitypage, "comments" = comments)
posts_comments
}