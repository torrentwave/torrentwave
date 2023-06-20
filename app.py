from flask import Flask, render_template, request, g
import sqlite3
from youtubesearchpython import VideosSearch
import random
import qbittorrentapi
import re
import json
import sqlite3
import pandas as pd
import requests
with open('torrents.csv', "ab") as torrents:
    rn = requests.get("https://git.torrents-csv.ml/heretic/torrents-csv-data/raw/branch/main/torrents.csv") 
    torrents.write(rn.text.encode('utf-8'))
    
df = pd.read_csv('torrents.csv')
df.columns = df.columns.str.strip()
connection = sqlite3.connect("demo.db")
df.to_sql('titles',connection, if_exists='replace',)
connection.close() 

with open('config.json', 'r') as config_file:
    config = json.load(config_file)

DATABASE = config['database']
app = Flask(__name__)

def convert_bytes_to_gb(bytes):
    gb = bytes / (1024 * 1024 * 1024)
    return round(gb, 2)



def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()
background_images = ["image1.jpg","image2.jpg","image3.jpg","image4.jpg","image5.jpg","image6.jpg","image7.jpg","image8.jpg","image9.jpg"]
@app.route('/')
def index():
    global background_image
    # Pick a random background image
    random_index = random.randint(0, len(background_images) - 1)
    background_image = background_images[random_index]
    
    return render_template('index.html', background_image=background_image)

@app.route('/search', methods=['GET', 'POST'])
def search():
    results = []
    if request.method == 'GET':
        query = request.args.get('query')

        conn = get_db()
        c = conn.cursor()

        strings_to_remove = ["1080p", "720p", "480p"]
        pattern = r"\b19[0-9][0-9]|20[0-9][0-9]\b"
        years = re.findall(pattern, query)

        c.execute("SELECT infohash, name, seeders, size_bytes FROM titles WHERE name LIKE ? AND seeders > 10 ORDER BY seeders DESC", ('%' + query + '%',))

        results = c.fetchall()
        results = [{'hash': 'magnet:?xt=urn:btih:' + row[0], 'title': row[1], 'seeders': row[2], 'filesize_gb': convert_bytes_to_gb(row[3]), 'years': re.findall(pattern, row[1])} for row in results]

    return render_template('search.html', results=results)





@app.route('/video-preview', methods=['GET'])
def video_preview():
    
    query = request.args.get('query')
    new_text = query
    strings_to_remove = ["1080p", "720p", "480p"]
    pattern = r"\b19[0-9][0-9]|20[0-9][0-9]\b"
    years = re.findall(pattern, new_text)

    if years:
        print("Found years:", years)
    

    for string in strings_to_remove:
        if string in new_text:
            new_text = new_text.split(string)[0]
       

            print(new_text)
            results = VideosSearch(new_text, limit=1)
            print(results.result())
            results2 = results.result()
            video_info = results2['result'][0]
            video_title = video_info['title']
            video_id = video_info['id']
            video_url = f'https://www.youtube.com/embed/{video_id}'
            return render_template('videopreview.html', video_title=video_title, video_url=video_url)
        elif years:
            print(new_text)
            results = VideosSearch(new_text, limit=1)
            print(results.result())
            results2 = results.result()
            video_info = results2['result'][0]
            video_title = video_info['title']
            video_id = video_info['id']
            video_url = f'https://www.youtube.com/embed/{video_id}'
            return render_template('videopreview.html', video_title=video_title, video_url=video_url)
    else:
        return 'Requested video is not a movie or tv show.. <a href="/">Back</a>'
    


app.run(host='0.0.0.0', port=8031)
