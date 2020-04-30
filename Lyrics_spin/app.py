import os
from flask import Flask, url_for, redirect, request, render_template
from flask_pymongo import PyMongo

from .form import Lyrics_info 
from .engine import engine
from .script import get_lyrics_text



MONGO_URL = os.environ.get('MONGO_URL')
if not MONGO_URL:
    MONGO_URL = "mongodb://localhost:27017/art_lyric"


app = Flask(__name__)
app.debug = False
app.secret_key = os.environ.get('SECRET_KEY')
app.config['MONGO_URI'] = MONGO_URL

mongo = PyMongo(app)


@app.route('/lyrics', methods=['POST'])
def lyrics():
    artist = request.form['artist']
    album = request.form['album']
    lines = int(request.form['lines'])
    cache = mongo.db.lyrics_col.find_one({"_id":'{artist}_{album}'.format(artist=artist, album=album)})
    if cache:
        lyrics = cache['lyrics']
        result = engine(lyrics, lines)
    
    else:
        lyrics = get_lyrics_text(artist, album)
        if type(lyrics,) == str:
            x = mongo.db.lyrics_col.insert({"_id":'{artist}_{album}'.format(artist=artist, album=album), "lyrics":lyrics})
            result = engine(lyrics, lines)
        else:
            result = lyrics

    if len(result) == lines:
        return render_template('lyrics.html', result=result, artist=artist)
    else:
        return render_template('lyrics.html', result=result, artist='Wrong Input')



@app.route('/', methods=['GET', 'POST'])
def index():
    form = Lyrics_info()


    return render_template('index.html', form=form)


