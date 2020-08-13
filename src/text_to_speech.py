import urllib, json, hashlib
from time import sleep
from os import path, environ

class TextToSpeech:
    def __init__(self, logger):
        self.logger = logger

    def _text_to_speech(self, text, voice):
        data = bytes(json.dumps({"engine": "Google", "data": {"text": text, "voice": voice}}), encoding='utf-8')
        req =  urllib.request.Request("https://api.soundoftext.com/sounds", data=data)
        req.add_header('Content-Type', 'application/json')
        resp = urllib.request.urlopen(req)

        code_name = json.loads(resp.read())["id"]
        url = "https://soundoftext.nyc3.digitaloceanspaces.com/{0}.mp3".format(code_name)
        return url

    def _get_word_path(self, text, voice):
        return "static/sounds/words/{0}-{1}.mp3".format(text, voice.split("-")[1].lower())

    def _get_sentence_path(self, text, voice):
        return "static/sounds/examples/{0}.mp3".format(self.get_hash(text, voice))

    def _get_word_data(self, text):
        url = "{}/word/find?text={}".format(environ.get("BACKEND_URL"), text)
        resp = urllib.request.urlopen(url)
        word = json.loads(resp.read())["payload"]
        return word

    def get_hash(self, text, voice, speed='normal'):
        return hashlib.md5((text + voice + speed).encode()).hexdigest()

    def save_one_word_data(self, text, voice):
        url = self._text_to_speech(text, voice)
        sleep(2)
        try:
            urllib.request.urlretrieve(url, self._get_word_path(text, voice))
        except Exception:
            self.logger.error("Problem with download word: '" + text + "' with voice: '" + voice + "'")
            self.logger.info("Url is: " + url)
            try:
                url = self._text_to_speech(text, voice)
                sleep(5)
                urllib.request.urlretrieve(url, self._get_word_path(text, voice))
            except Exception:
                self.logger.error("Cannot download word: '" + text + "' with voice: '" + voice + "'")
                self.logger.info("Url is: " + url)
                return
        self.logger.info("Saved word: '" + text + "' with voice: '" + voice + "'")

    def save_one_sentence_data(self, text, voice):
        url = self._text_to_speech(text, voice)
        sleep(2)
        try:
            urllib.request.urlretrieve(url, self._get_sentence_path(text, voice))
        except Exception:
            self.logger.error("Problem with download sentence: \"" + text + "\" with voice: '" + voice + "' as: " + self.get_hash(text, voice) + ".mp3")
            self.logger.info("Url is: " + url)
            try:
                url = self._text_to_speech(text, voice)
                sleep(5)
                urllib.request.urlretrieve(url, self._get_sentence_path(text, voice))
            except Exception:
                self.logger.error("Cannot download sentence: \"" + text + "\" with voice: '" + voice + "' as: " + self.get_hash(text, voice) + ".mp3")
                self.logger.info("Url is: " + url)
                return

        self.logger.info("Saved sentence: \"" + text + "\" with voice: '" + voice + "' as: " + self.get_hash(text, voice) + ".mp3")


    def save_all_word_data(self, text):
        word = self._get_word_data(text)

        hashes = []

        # save word voice
        for voice in ['en-GB', 'en-US']:
            if (not path.exists(self._get_word_path(text, voice))): 
                self.save_one_word_data(text, voice)

        # save all examples of word voice
        for voice in ['en-GB', 'en-US']:
            for example in word["examples"]:
                if example == "": continue
                if (path.exists(self._get_sentence_path(example, voice))): continue
                sleep(15)
                self.save_one_sentence_data(example, voice)
                hashes.append(self.get_hash(example, voice))

        return hashes



