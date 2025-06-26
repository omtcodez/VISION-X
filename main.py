from reddit_scraper import fetch_posts, count_hashtag
from text_cluster import cluster_and_summarize
from video_processor import process
from object_detector import filter_important
from mapping_sentiment import map_and_sentiment

if __name__ == "__main__":
    # Set your parameters
    start_ts =  int(__import__('time').mktime(__import__('time').strptime('2025-06-01','%Y-%m-%d')))
    end_ts   =  int(__import__('time').mktime(__import__('time').strptime('2025-06-25','%Y-%m-%d')))
    
    posts = fetch_posts('all', '#ExampleTag', start_ts, end_ts)
    print("Total posts:", len(posts))
    print("Hashtag count:", count_hashtag(posts, '#ExampleTag'))

    clusters = cluster_and_summarize(posts)
    print("Text clusters and summaries:", clusters)

    video_texts = process(posts)
    important = filter_important(video_texts)
    print("Important videos:", important)

    map_and_sentiment(posts, important)
