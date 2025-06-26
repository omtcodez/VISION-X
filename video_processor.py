import os, hashlib, requests
from moviepy.editor import VideoFileClip
import whisper

def download_videos(urls, out_dir='data/videos'):
    os.makedirs(out_dir, exist_ok=True)
    paths = []
    for u in urls:
        fn = u.split('/')[-1].split('?')[0]
        dest = os.path.join(out_dir, fn)
        if not os.path.exists(dest):
            resp = requests.get(u)
            open(dest,'wb').write(resp.content)
        paths.append(dest)
    return paths

def dedupe(paths):
    seen, uniq = set(), []
    for p in paths:
        h = hashlib.md5(open(p,'rb').read()).hexdigest()
        if h not in seen:
            seen.add(h)
            uniq.append(p)
    return uniq

def extract_audio(video_path, audio_path):
    clip = VideoFileClip(video_path)
    clip.audio.write_audiofile(audio_path)
    clip.close()

def transcribe(audio_path):
    model = whisper.load_model('base')
    return model.transcribe(audio_path)['text']

def process(posts):
    video_urls = [p.url for p in posts if 'reddit_video' in p.url]
    paths = download_videos(video_urls)
    unique = dedupe(paths)
    texts = {}
    for vp in unique:
        ap = vp.replace('.mp4', '.wav').replace('.webm','.wav')
        extract_audio(vp, ap)
        texts[vp] = transcribe(ap)
    return texts
