#!/usr/bin/env python3

from flask import Flask
from flask import render_template, request
import urllib, json, hashlib
from bs4 import BeautifulSoup
from time import sleep


def text_to_speech(text, voice):
    data = bytes(json.dumps({"engine": "Google", "data": {"text": text, "voice": voice}}), encoding='utf-8')
    req =  urllib.request.Request("https://api.soundoftext.com/sounds", data=data)
    req.add_header('Content-Type', 'application/json')
    resp = urllib.request.urlopen(req)

    code_name = json.loads(resp.read())["id"]
    url = "https://soundoftext.nyc3.digitaloceanspaces.com/{0}.mp3".format(code_name)
    return url


def get_hash(text, voice, speed='normal'):
    return hashlib.md5((text + voice + speed).encode()).hexdigest()



app = Flask(__name__)

@app.route('/')
def index():
    message = "Hello world!!"
    return render_template('index.html', message=message)


@app.route('/download/word', methods=['GET'])
def download_word():
    text = request.args.get('text', '')
    voice = request.args.get('voice', 'en-GB')

    if text == '':
        return {"status": 400, "message": "Word text is missing."}
    if voice != "en-GB" and voice != "en-US":
        return {"status": 400, "message": "Voice is in wrong format."}

    url = text_to_speech(text, voice)
    sleep(1)
    urllib.request.urlretrieve(url, "static/sounds/words/{0}-{1}.mp3".format(text, voice.split("-")[1].lower()))

    return {"status": 200}


@app.route('/download/sentence', methods=['POST'])
def download_sentence():
    text = request.form['text']
    voice = request.form['voice']

    if text == '':
        return {"status": 400, "message": "Sentence text is missing."}
    if voice != "en-GB" and voice != "en-US":
        return {"status": 400, "message": "Voice is in wrong format."}

    url = text_to_speech(text, voice)
    sleep(1)
    urllib.request.urlretrieve(url, "static/sounds/examples/{0}.mp3".format(get_hash(text, voice)))

    return {"status": 200}


