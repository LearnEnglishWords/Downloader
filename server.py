#!/usr/bin/env python

from flask import Flask
from flask import render_template, request
import urllib, json


app = Flask(__name__)

@app.route('/')
def index():
    message = "Hello world!!"
    return render_template('index.html', message=message)


@app.route('/download/word', methods=['GET'])
def hello():
    text = request.args.get('text', '')
    voice = request.args.get('voice', 'en-GB')

    if text == '':
        return {"status": 400, "message": "Word text is missing."}
    if voice != "en-GB" and voice != "en-US":
        return {"status": 400, "message": "Voice is in wrong format."}

    data = bytes(json.dumps({"engine": "Google", "data": {"text": text, "voice": voice}}), encoding='utf-8')
    req =  urllib.request.Request("https://api.soundoftext.com/sounds", data=data)
    req.add_header('Content-Type', 'application/json')

    resp = urllib.request.urlopen(req)

    codeName = json.loads(resp.read())["id"]
    url = "https://soundoftext.nyc3.digitaloceanspaces.com/{0}.mp3".format(codeName)
    urllib.request.urlretrieve(url, "static/sounds/{0}-{1}.mp3".format(text, voice.split("-")[1].lower()))

    return {"status": 200}
