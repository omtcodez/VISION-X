import pandas as pd
from sentence_transformers import SentenceTransformer
import hdbscan
from transformers import pipeline

def cluster_and_summarize(posts):
    texts = [p.selftext or p.title for p in posts if p.is_self]
    if not texts:
        return {}
    embedder = SentenceTransformer('all-MiniLM-L6-v2')
    embeddings = embedder.encode(texts, show_progress_bar=True)
    clusterer = hdbscan.HDBSCAN(min_cluster_size=10)
    labels = clusterer.fit_predict(embeddings)
    df = pd.DataFrame({'text': texts, 'label': labels})
    summarizer = pipeline('summarization', model='facebook/bart-large-cnn')
    summary = {}
    for lbl in sorted(set(labels)):
        if lbl < 0: continue
        group = df[df.label == lbl].text.tolist()
        snippet = ' '.join(group[:10])
        out = summarizer(snippet, max_length=80, min_length=30, do_sample=False)[0]['summary_text']
        summary[lbl] = out
    return summary
 