import praw
import json
import time
import prawcore
#for grabbing urls
import re
import requests
from bs4 import BeautifulSoup
import os
import sys
#import schedule

#Testing this code so that it stores the data after each post so that when it crashes, not everything is lost
#also trying to see if i can make it so that running it multiple times will get new uniquen posts
#also added top posts of all time

def load_seen_ids():
    if os.path.exists("seen_ids.json"):
        with open("seen_ids.json", "r") as f:
            return set(json.load(f))
    return set()

def save_seen_ids(seen_ids):
    with open("seen_ids.json", "w") as f:
        json.dump(list(seen_ids), f)

#declaration of reddit instance
reddit = praw.Reddit(
    client_id="8Vmluj2uH8MbE_-b4LvBlw",
    client_secret="iLaamxRCVlDSow20Ek4-mtrosPlK0A",
    user_agent="test script by /u/TurbulentBandicoot98",
    username = "TurbulentBandicoot98",
    password = "password101!",
    ratelimit_second = 300
)

seen_ids = load_seen_ids()

def get_html_title(url):
    try:
        response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            return soup.title.text if soup.title else 'No title found'
    except requests.RequestException:
        return 'Failed to retrieve title'

def find_html_links(text):
    return re.findall(r'https?://\S+', text)

#array to store different subreddits
def crawl_and_store():    
    subreddits = ["Helldivers", "leagueoflegends", "GlobalOffensive"]
    for subreddit in subreddits:
        output_file_path = f'mig_{subreddit}.json'
        with open(output_file_path, 'w', encoding='utf-8') as json_file:
            json_file.write('[')
            first_post = True

            for submission_set in ['hot', 'new', 'top']: #crawls hot, then new, then top with no limit
                new_count = 1;
                if submission_set == 'top':
                    post_limit = 120  #used to adjust top post limits
                    posts = getattr(reddit.subreddit(subreddit), submission_set)(limit=post_limit)  # Fetch top posts from all time
                else:
                    posts = getattr(reddit.subreddit(subreddit), submission_set)(limit=None)  # Fetch hot and new posts, limit can be adjusted

                for post in posts:
                    if post.id not in seen_ids:
                        seen_ids.add(post.id)

                        print(f"Currently on {submission_set} post {new_count} in {subreddit}\n") #output statement to show progress ofm crawler
                        new_count += 1

                        #check text for urls and save if exist
                        html_links = find_html_links(post.selftext)
                        linked_html_titles = {url: get_html_title(url) for url in html_links}

                        try:
                            post.comments.replace_more(limit=450) #adjust comments here
                        except prawcore.exceptions.TooManyRequests:
                            print(f"{subreddit}'s rate limit exceeded. \n")
                            time.sleep(60)
                            continue
                        except prawcore.exceptions.PRAWException as e:
                            print(f"An error occurred while expanding comments \n")
                            continue

                        parsed_comments = [{'comment_body': comment.body} for comment in post.comments.list()]

                        post_data = {  #appends variables to array
                            'self_text': post.selftext,
                            'title': post.title,
                            'id': post.id,
                            'score': post.score,
                            'url': post.url,
                            'permalink': post.permalink,
                            'top_comments': parsed_comments,
                            'linked_html_titles': linked_html_titles
                        }

                        if not first_post:
                            json_file.write(',')
                        else:
                            first_post = False

                        json.dump(post_data, json_file, ensure_ascii=False, indent=2)

                        time.sleep(1)  #Used to avoid hitting rate limits

            json_file.write(']')
            print(f"Data collection for {subreddit} completed \n")

        save_seen_ids(seen_ids)
        print("-------------------------------------------- \n")
#first call to crawl and store
crawl_and_store()

#scheduler loop
#schedule.every(3).hours.do(crawl_and_store)

 #Run scheduler loop
#while True:
 #   schedule.run_pending()
 #   time.sleep(1)