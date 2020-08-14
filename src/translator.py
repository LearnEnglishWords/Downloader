import json, subprocess
from logger import Logger
from urllib import request, parse

class Translator:
    def __init__(self, logger, engine):
        self.logger = logger
        self.engine = engine

    def _translate_with_microsoft(self, text, from_lang, to_lang):
        normal = subprocess.run(['curl', 'https://www.translate.com/translator/ajax_translate', '--data-raw', 'text_to_translate={}&source_lang={}&translated_lang={}&use_cache_only=false'.format(text, from_lang, to_lang) ],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            check=True)
        return json.loads(normal.stdout)["translated_text"]

    def _translate_with_google(self, text, from_lang, to_lang):
        normal = subprocess.run(['curl', 'https://www.webtran.eu/gtranslate/', '--data-raw', 'text={}&gfrom={}&gto={}&key=ABC'.format(text, from_lang, to_lang) ],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            check=True)
        return normal.stdout[3:].decode()
                                                          
    def translate(self, text, from_lang="en", to_lang="cs"):
        if (self.engine == "microsoft"):
            return self._translate_with_microsoft(text, from_lang, to_lang)
        else:
            return self._translate_with_google(text, from_lang, to_lang)

