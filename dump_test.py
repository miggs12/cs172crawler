import praw
import json
import time
import prawcore

#declaration of reddit instance
reddit = praw.Reddit(
    client_id="2-Aro9aRbE_Fq7l6WiSf3A",
    client_secret="7CGvg5-SanDwATMVY-dKpv958QfJvg",
    user_agent="test script by /u/Familiar-Fennel-6202",
    username = "Familiar-Fennel-6202",
    password = "securepassword101",
    ratelimit_second = 300
)

#array to store different subreddits
subreddits = ["gaming"]

for subreddit in subreddits:

    hot = reddit.subreddit(subreddit).hot(limit=500)
    new = reddit.subreddit(subreddit).new(limit=500)

    parsed_posts = [] #array to store posts

    hot_count = 1 #to keep track of crawling progress

    for post in hot: #goes through posts and stores variables
        try:
            print("Currently on hot post " + str(hot_count) + "\n")
            hot_count = hot_count+1
        
            self_text = (post.selftext)
            title = (post.title)
            id = (post.id)
            score = (post.score)
            url = (post.url)
            permalink = (post.permalink)

            parsed_comments = []
            post.comments.replace_more(limit=40)
            post_comments = post.comments.list()
            
            for comment in post_comments:
                try:
                    parsed_comments.append({
                        'comment_body' : comment.body
                    })
                except prawcore.exceptions.TooManyRequests as e:
                    sleeping = True
                    print(subreddit + "'s rate limit exceeded while crawling comments\n")
                    time.sleep(60)
            time.sleep(1)

            parsed_posts.append({ #appends variables to array
                'self_text' : self_text,
                'title' : title,
                'id' : id,
                'score' : score,
                'url' : url,
                'permalink' : permalink,
                'top_comments' : parsed_comments
            })
        except prawcore.exceptions.TooManyRequests as e:
            sleeping = True
            print(subreddit + "'s rate limit exceeded while crawling posts\n")
            time.sleep(60)

    new_count = 1 

    for post in new: #goes through top posts and stores variables

        try:
            print("Currently on new post " + str(new_count) + "\n")
            new_count = new_count + 1

            self_text = (post.selftext)
            title = (post.title)
            id = (post.id)
            score = (post.score)
            url = (post.url)
            permalink = (post.permalink)

            parsed_comments = []
            post.comments.replace_more(limit=30)
            post_comments = post.comments.list()

            for comment in post_comments:
                try:
                    parsed_comments.append({
                        'comment_body' : comment.body
                    })
                except prawcore.exceptions.TooManyRequests as e:
                    sleeping = True
                    print(subreddit + "'s rate limit exceeded while crawling posts\n")
            time.sleep(1)

            parsed_posts.append({
                'self-text' : self_text,
                'title' : title,
                 'id' : id,
                'score' : score,
                'url' : url,
                'permalink' : permalink,
                'top_comments' : parsed_comments
            })
        except prawcore.exceptions.TooManyRequests as e:
            sleeping = True
            print(subreddit + "'s rate limit exceeded while crawling posts\n")
            time.sleep(60)


    output_file_path = 'hot_new_posts/' + subreddit + '.json' #output file path
    with open(output_file_path, 'w', encoding='utf-8') as json_file:
        for chunk in parsed_posts:
            json.dump(chunk, json_file, ensure_ascii=False, indent=2)


