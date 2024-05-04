import praw
import json
import time
import prawcore
#for grabbing urls
import re
import requests
from bs4 import BeautifulSoup

#declaration of reddit instance
reddit = praw.Reddit(
    client_id="8Vmluj2uH8MbE_-b4LvBlw",
    client_secret="iLaamxRCVlDSow20Ek4-mtrosPlK0A",
    user_agent="test script by /u/TurbulentBandicoot98",
    username = "TurbulentBandicoot98",
    password = "password101!",
    ratelimit_second = 300
)

def get_html_title(url):
    try:
        response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            title = soup.title.text if soup.title else 'No title found'
            return title
    except requests.RequestException:
        return 'Failed to retrieve title'

def find_html_links(text):
    urls = re.findall(r'https?://\S+', text)
    return urls

#array to store different subreddits
subreddits = ["gaming"]
seen_ids = set()

for subreddit in subreddits:

    hot = reddit.subreddit(subreddit).hot(limit=500)
    new = reddit.subreddit(subreddit).new(limit=500)

    parsed_posts = [] #array to store posts

    hot_count = 1 #to keep track of crawling progress

    for post in hot: #goes through posts and stores variables
        if(post.id) not in seen_ids:
            seen_ids.add(post.id)
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
                #check text for urls and save if exist
                html_links = find_html_links(post.selftext)
                linked_html_links = {url: get_html_title(url) for url in html_links}
                #comments
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
                #puts all into .json
                parsed_posts.append({ #appends variables to array
                    'self_text' : self_text,
                    'title' : title,
                    'id' : id,
                    'score' : score,
                    'url' : url,
                    'permalink' : permalink,
                    'top_comments' : parsed_comments,
                    'linked_html_titles' : linked_html_links
                })

            except prawcore.exceptions.TooManyRequests as e:
                sleeping = True
                print(subreddit + "'s rate limit exceeded while crawling posts\n")
                time.sleep(60)

    new_count = 1 

    for post in new: #goes through top posts and stores variables
        if(post.id) not in seen_ids:
            seen_ids.add(post.id)
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
                #for urls in text
                html_links = find_html_links(post.selftext)
                linked_html_links = {url: get_html_title(url) for url in html_links}
                #comments
                for comment in post_comments:
                    try:
                        parsed_comments.append({
                            'comment_body' : comment.body
                        })
                    except prawcore.exceptions.TooManyRequests as e:
                        sleeping = True
                        print(subreddit + "'s rate limit exceeded while crawling posts\n")
                time.sleep(1)
                #append all into json
                parsed_posts.append({
                    'self-text' : self_text,
                    'title' : title,
                    'id' : id,
                    'score' : score,
                    'url' : url,
                    'permalink' : permalink,
                    'top_comments' : parsed_comments,
                    'linked_html_titles' : linked_html_links
                })
            except prawcore.exceptions.TooManyRequests as e:
                sleeping = True
                print(subreddit + "'s rate limit exceeded while crawling posts\n")
                time.sleep(60)


    output_file_path = 'hot_new_posts/' + subreddit + '.json' #output file path
    with open(output_file_path, 'w', encoding='utf-8') as json_file:
        for chunk in parsed_posts:
            json.dump(chunk, json_file, ensure_ascii=False, indent=2)
