#!/usr/bin/env python3

from flask import Flask
from flask import render_template, request
import urllib, json, hashlib
from time import sleep
from os import path


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

def get_word_path(text, voice):
    return "static/sounds/words/{0}-{1}.mp3".format(text, voice.split("-")[1].lower())

def get_sentence_path(text, voice):
    return "static/sounds/examples/{0}.mp3".format(get_hash(text, voice))

def save_word(text, voice):
    url = text_to_speech(text, voice)
    sleep(2)
    try:
        urllib.request.urlretrieve(url, get_word_path(text, voice))
    except Exception:
        print("Problem with download word: " + text + " with voice: " + voice)
        print("Url is: " + url)
        try:
            url = text_to_speech(text, voice)
            sleep(5)
            urllib.request.urlretrieve(url, get_word_path(text, voice))
        except Exception:
            print("ERROR: Cannot download word: " + text + " with voice: " + voice)
            print("Url is: " + url)
            return
    print("Saved word: " + text + " with voice: " + voice)

def save_sentence(text, voice):
    url = text_to_speech(text, voice)
    sleep(2)
    try:
        urllib.request.urlretrieve(url, get_sentence_path(text, voice))
    except Exception:
        print("Problem with download sentence: \"" + text + " with voice: " + voice + "\" as: " + get_hash(text, voice) + ".mp3")
        print("Url is: " + url)
        try:
            url = text_to_speech(text, voice)
            sleep(5)
            urllib.request.urlretrieve(url, get_sentence_path(text, voice))
        except Exception:
            print("ERROR: Cannot download sentence: \"" + text + " with voice: " + voice + "\" as: " + get_hash(text, voice) + ".mp3")
            print("Url is: " + url)
            return

    print("Saved sentence: \"" + text + " with voice: " + voice + "\" as: " + get_hash(text, voice) + ".mp3")


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

    save_word(text, voice)

    return {"status": 200}


@app.route('/download/sentence', methods=['POST'])
def download_sentence():
    text = request.form['text']
    voice = request.form['voice']

    if text == '':
        return {"status": 400, "message": "Sentence text is missing."}
    if voice != "en-GB" and voice != "en-US":
        return {"status": 400, "message": "Voice is in wrong format."}

    save_sentence(text, voice)

    return {"status": 200}


@app.route('/download/all', methods=['GET'])
def download_all():
    voice = request.args.get('voice', 'en-GB')
    limit = request.args.get('limit', 1000)

    resp = urllib.request.urlopen("https://drakeman.cz/api/word/list?page=1&limit=20000&state=correct")
    words = json.loads(resp.read())["payload"]["words"]

    counter = 0
    for word in words:
        counter += 1
        if (counter == limit): break
        if (path.exists(get_word_path(word["text"], voice))): continue

        save_word(word["text"], voice)
        sleep(10)
        for example in word["examples"]:
            save_sentence(example, voice)
            sleep(20)
        print()


    return "ok"
