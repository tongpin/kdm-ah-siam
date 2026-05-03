import json, os
from config.settings import DATA_FILE

def ensure_file():
    folder = os.path.dirname(DATA_FILE)
    if folder: os.makedirs(folder, exist_ok=True)
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, "w", encoding="utf-8") as f: json.dump({}, f, ensure_ascii=False, indent=2)

def load_wiki():
    ensure_file()
    with open(DATA_FILE, "r", encoding="utf-8") as f: return json.load(f)

def save_wiki(data):
    ensure_file()
    with open(DATA_FILE, "w", encoding="utf-8") as f: json.dump(data, f, ensure_ascii=False, indent=2)

def search_wiki(query):
    query = query.lower().strip()
    words = [w for w in query.split() if len(w) > 1]
    wiki = load_wiki(); results=[]
    for slug, lesson in wiki.items():
        searchable = " ".join([slug, lesson.get("title",""), lesson.get("category",""), lesson.get("text",""), " ".join(lesson.get("keywords",[])), " ".join(lesson.get("aliases",[]))]).lower()
        score = 0
        if query and query in searchable: score += 5
        for w in words:
            if w in searchable: score += 1
        if score > 0:
            item = dict(lesson); item["slug"] = slug; item["score"] = score; results.append(item)
    return sorted(results, key=lambda x: x["score"], reverse=True)
