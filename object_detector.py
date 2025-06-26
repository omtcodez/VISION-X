from ultralytics import YOLO

MODEL = YOLO('your_dataset/best.pt')

def detect_objects(video_path):
    res = MODEL.predict(source=video_path, verbose=False)
    found = set()
    for r in res:
        for *_, conf, cls in r.boxes.data.tolist():
            found.add(MODEL.names[int(cls)])
    return found

def filter_important(video_texts):
    important = {}
    for vid, txt in video_texts.items():
        objs = detect_objects(vid)
        if objs:
            important[vid] = {'text': txt, 'objects': objs}
    return important
