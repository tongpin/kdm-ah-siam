from flask import Flask, jsonify, request
from flask_cors import CORS
from storage.wiki_storage import load_wiki, search_wiki
app=Flask(__name__); CORS(app)
@app.get('/')
def home(): return jsonify({'status':'ok','message':'Minecraft Khmer Wiki API'})
@app.get('/api/wiki')
def api_wiki():
    items=[]
    for slug, lesson in load_wiki().items():
        item=dict(lesson); item['slug']=slug; items.append(item)
    return jsonify({'items':items})
@app.get('/api/search')
def api_search(): return jsonify({'items':search_wiki(request.args.get('q',''))})
