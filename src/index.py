#!/usr/bin/env python3

from flask import Flask
from flask import render_template, request
from logging.config import dictConfig
import urllib, json, hashlib
from time import sleep
from os import path, environ
from text_to_speech import TextToSpeech

dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'stream': 'ext://flask.logging.wsgi_errors_stream',
        'formatter': 'default'
    }},
    'root': {
        'level': 'INFO',
        'handlers': ['wsgi']
    }
})

app = Flask(__name__)
tts = TextToSpeech(app.logger)


@app.route('/')
def index():
    message = "Hello world!!"
    return render_template('index.html', message=message)


@app.route('/hash', methods=['GET'])
def hash():
    text = request.args.get('text', '')
    voice = request.args.get('voice', 'en-GB')

    if text == '':
        return {"status": 400, "message": "Word text is missing."}
    if voice != "en-GB" and voice != "en-US":
        return {"status": 400, "message": "Voice is in wrong format."}


    return {"status": 200, "hash": tts.get_hash(text, voice)}


@app.route('/download/word/all', methods=['GET'])
def download_word_all():
    text = request.args.get('text', '')

    if text == '':
        return {"status": 400, "message": "Word text is missing."}

    hashes = tts.save_all_word_data(text)
    
    return {"status": 200, "hashes": hashes}


@app.route('/download/word', methods=['GET'])
def download_word():
    text = request.args.get('text', '')
    voice = request.args.get('voice', 'en-GB')

    if text == '':
        return {"status": 400, "message": "Word text is missing."}
    if voice != "en-GB" and voice != "en-US":
        return {"status": 400, "message": "Voice is in wrong format."}

    tts.save_one_word_data(text, voice)

    return {"status": 200}


@app.route('/download/sentence', methods=['POST'])
def download_sentence():
    text = request.form['text']
    voice = request.form['voice']

    if text == '':
        return {"status": 400, "message": "Sentence text is missing."}
    if voice != "en-GB" and voice != "en-US":
        return {"status": 400, "message": "Voice is in wrong format."}

    tts.save_one_sentence_data(text, voice)
    app.logger.info("Generated hash is: " + tts.get_hash(text, voice))

    return {"status": 200}


