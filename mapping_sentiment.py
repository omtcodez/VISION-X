import pandas as pd
import plotly.express as px
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

def map_and_sentiment(posts, video_info):
    sid = SentimentIntensityAnalyzer()
    recs = []
    for p in posts:
        if not p.coords: continue
        lat, lon = map(float, p.coords.split(','))
        content = p.selftext or ''
        recs.append({'lat': lat, 'lon': lon, 'type': 'text', 'content': content, 'sent': sid.polarity_scores(content)['compound']})
    for vid, info in video_info.items():
        # no geodata from videos—skip or borrow from original post
        pass
    df = pd.DataFrame(recs)
    fig = px.scatter_geo(df, lat='lat', lon='lon', color='sent', size=[8]*len(df),
                         title='Reddit Posts Sentiment by Location')
    fig.show()
