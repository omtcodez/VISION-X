import praw
import time
from pushshift_py import PushshiftAPI

def fetch_posts(subreddit, hashtag, start_ts, end_ts, limit=10000):
    api = PushshiftAPI()
    reddit = praw.Reddit(client_id='YOUR_ID', client_secret='YOUR_SECRET', user_agent='reddit-m2')
    posts = []
    for submission in api.search_submissions(after=start_ts, before=end_ts, subreddit=subreddit, filter=['id','title','selftext','created_utc','is_self','url','coords'], q=hashtag):
        posts.append(submission)
        if len(posts) >= limit:
            break
    return posts

def count_hashtag(posts, hashtag):
    return sum(((p.title or '') + (p.selftext or '')).lower().count(hashtag.lower()) for p in posts)

if __name__ == "__main__":
    import time
    # example dates: June 1–25, 2025
    start_ts = int(time.mktime(time.strptime('2025-06-01', '%Y-%m-%d')))
    end_ts   = int(time.mktime(time.strptime('2025-06-25', '%Y-%m-%d')))
    posts = fetch_posts('all', '#Example', start_ts, end_ts)
    print(f"Fetched {len(posts)} posts")
    print("Hashtag count:", count_hashtag(posts, '#Example'))
