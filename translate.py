import os
from gtts import gTTS
from slugify import slugify
from threading import Thread
from deep_translator import GoogleTranslator
from googletrans import LANGUAGES, LANGCODES
from playsound import playsound

application_directory = os.getcwd()


# This class translate queries into the specified language.
# ------------------------------------------------------------------------------------------------------------
class Translate:
    def __init__(self, query, flag) -> None:
        self.query = query
        self.flag = flag
        self.processed_text = None
        self.detected_lang = None

    # This function is used to extract the specified language and eliminate any language-related entities from the query.
    def language_detection(self, query) -> list:
        exist_language = []
        languages = LANGUAGES.values()
        for word in query:
            if word in languages:
                exist_language.append(word)
        if len(exist_language) != 0:
            query.reverse()
            lang_idx = query.index(exist_language[-1])
            query = query[lang_idx + 1 :]
            query.reverse()
            self.processed_text = query.copy()
            self.detected_lang = exist_language[-1]

    # This function is used to process the query and remove irrelevant substrings.
    def text_processing(self):
        trans_idx, mean_idx, key_idx, flag = None, None, None, False
        query = self.query.split()
        thread = Thread(target=self.language_detection, args=(query.copy(),))
        thread.start()
        if "translate" in query:
            trans_idx = query.index("translate")
        if "meaning" in query:
            mean_idx = query.index("meaning")
        if trans_idx is not None and mean_idx is not None:
            if trans_idx > mean_idx:
                key_idx = mean_idx
                flag = True
            else:
                key_idx = trans_idx
        elif trans_idx is not None:
            key_idx = trans_idx
        else:
            key_idx = mean_idx
            flag = True

        thread.join()
        self.processed_text = self.processed_text[key_idx + 1 :]
        if self.processed_text[-1] == "in":
            self.processed_text.pop(-1)
        elif self.processed_text[-1] == "the" and self.processed_text[-2] == "in":
            self.processed_text.pop(-1)
            self.processed_text.pop(-1)
        if flag is True and self.processed_text[0] == "of":
            self.processed_text.pop(0)
        self.processed_text = " ".join(self.processed_text)

    def google_translate(self):
        if self.flag is False:
            self.text_processing()
            body, language = self.processed_text, self.detected_lang
        else:
            body = self.query["body"]
            language = str(self.query["language"]).lower()
        translated = GoogleTranslator(source="auto", target=language).translate(
            text=body
        )
        langCode = LANGCODES.get(language)
        slugified_text = slugify(translated)
        slugified_text = slugified_text.replace("-", " ").strip().capitalize()
        print(translated)
        print(slugified_text)
        try:
            tts = gTTS(translated, lang=langCode)
            tts.save(os.path.join(application_directory, "Data\\Cache\\voiceCache.mp3"))
            playsound(
                os.path.join(application_directory, "Data\\Cache\\voiceCache.mp3")
            )
            os.remove(
                os.path.join(application_directory, "Data\\Cache\\voiceCache.mp3")
            )
        except:
            tts = gTTS(slugified_text, lang="hi")
            tts.save(os.path.join(application_directory, "Data\\Cache\\voiceCache.mp3"))
            playsound(
                os.path.join(application_directory, "Data\\Cache\\voiceCache.mp3")
            )
            os.remove(
                os.path.join(application_directory, "Data\\Cache\\voiceCache.mp3")
            )
