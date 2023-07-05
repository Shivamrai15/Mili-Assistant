# Libraries
import re
import os
import imdb
import json
import time
import spacy
import pickle
import pyttsx3
import requests
import randfacts
import AppOpener
import wikipedia
import webbrowser
import subprocess
import urllib.parse
import urllib.request
from jokeapi import Jokes
from threading import Thread
from datetime import datetime
import speech_recognition as sr
from pymongo import MongoClient
from googlesearch import search
from encryption import Encryption
from random import randint, sample
from gnewsclient import gnewsclient
from gingerit.gingerit import GingerIt
from functions import CredentialManager
from translate import Translate


# importing interfaces
# ------------------------------------------------------------------------------------------------------
from app import GUI
from map import APP

# ------------------------------------------------------------------------------------------------------


# importing AI models
# ------------------------------------------------------------------------------------------------------
from trained_model import chat
from bard_model import bardResponse
from wit_model import witResponse

# ------------------------------------------------------------------------------------------------------


# -------------------------------------------------------------------------------------------------------

# Current directory of the application
application_directory = os.getcwd()

# object of the interface
map_interface = APP()


# Setting database connection
# -------------------------------------------------------------------------------------------------------
__ID__, __PASSWORD__ = CredentialManager().read_credential()
__database_url__ = Encryption(
    b"gAAAAABkeM77CniuvGNLTxhTXcvvxS4482UUd-YvStyomao17R01SW_7UrXKCjvUfjwrmYRZ-YEztP6Xpb02tF3mDqH42ECzrMYiw2d6hcw2ZeZuIQXzTNvl-ylfk39vReUEseO0KnAIsnkcdJQeHOTvhjufWM5yYEAShBSZ6g_E3qqcy9pWhlA="
).decrypt_text()
__client__ = MongoClient(__database_url__)
__database__ = __client__["Assistant"]
__collection__ = __database__["User Credentials"]


# -------------------------------------------------------------------------------------------------------

# -------------------------------------------------------------------------------------------------------

engine = pyttsx3.init("sapi5")
voices = engine.getProperty("voices")
engine.setProperty("volume", 1.0)
engine.setProperty("rate", 140)
engine.setProperty("voice", voices[1].id)

# -------------------------------------------------------------------------------------------------------


# -------------------------------------------------------------------------------------------------------
def defaultMiliGeneralSettings():
    defaultSettings = open(
        application_directory + "\\Data\\Cache\\Mili Settings.settings", "rb"
    )
    defaultSettings = pickle.load(defaultSettings)
    return defaultSettings


# -------------------------------------------------------------------------------------------------------


# -------------------------------------------------------------------------------------------------------
def speak(audio):
    print(audio)
    engine.say(audio)
    engine.runAndWait()


# -------------------------------------------------------------------------------------------------------


# -------------------------------------------------------------------------------------------------------
def onlySpeak(audio):
    engine.say(audio)
    engine.runAndWait()


# -------------------------------------------------------------------------------------------------------


# -------------------------------------------------------------------------------------------------------
# Function to remove all grammatical errors from the input voice text
def removeGrammaticalErrors(query) -> str:
    corrected_text = GingerIt().parse(query)
    result = corrected_text["result"]
    return result


# -------------------------------------------------------------------------------------------------------


# -------------------------------------------------------------------------------------------------------
def command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        # taking input from the microphone. It can be device's microphone or external microphone
        print("Listening...")
        # r.pause_threshold = 1
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)

    try:
        # Recognizing the input voice
        print("Recognizing...")
        # converting recognized voice into the string
        query = r.recognize_google(audio, language="en-in", pFilter=0)
        # removing all grammatical errors
        query = removeGrammaticalErrors(query).capitalize()
        print(f"User said: {query}\n")

    except Exception as e:
        speak("Say that again please...")
        return "None"
    return query


# -------------------------------------------------------------------------------------------------------


# -------------------------------------------------------------------------------------------------------
# Function that takes input until the input is not a null value
def takeCommand():
    exit = False
    while exit != True:
        query = command()
        if query != "None":
            exit = True
            break
    return query


# -------------------------------------------------------------------------------------------------------


# -------------------------------------------------------------------------------------------------------
class DATETIME:
    def current_date():
        today = datetime.now()
        current_date = today.strftime("%A, %d %B %Y")
        return current_date

    def currentTime():
        today = datetime.now()
        current_time = today.strftime("%I:%M %p")
        speak(current_time)
        print(DATETIME.currentDate())


# -------------------------------------------------------------------------------------------------------


# -------------------------------------------------------------------------------------------------------
# This function detects bad words, swear words by performing profanity check in a given text and return true or false value.
def profanityFilter(query):
    url = "https://neutrinoapi-bad-word-filter.p.rapidapi.com/bad-word-filter"
    payload = {"content": f"{query}", "censor-character": "*"}
    headers = {
        "content-type": "application/x-www-form-urlencoded",
        "X-RapidAPI-Key": Encryption(
            b"gAAAAABkdNLvCdK3P4kGRk1oGt8v3Def0i5tECK4SSBTz3PrwV3Dyy3xokcAOcJ-DoPBSWSzouAzvwxg6Qb_APIMjB0WDkos0l3oEE9ZvevH5TD6-p1qBA8AX2AeXWEqGzUN-RwofVkHWEo6iO4_g-Y2vk4mh829rQ=="
        ).decrypt_text(),
        "X-RapidAPI-Host": "neutrinoapi-bad-word-filter.p.rapidapi.com",
    }
    response = requests.post(url, data=payload, headers=headers).json()
    return response.get("is-bad")


# -------------------------------------------------------------------------------------------------------


# -------------------------------------------------------------------------------------------------------
# This function returns the sentiment of the text
# Return value positive, negative, neutral of type string
def sentimentAnalysis(query):
    url = "https://microsoft-text-analytics1.p.rapidapi.com/sentiment"

    payload = {"documents": [{"id": "1", "language": "en", "text": f"{query}"}]}
    headers = {
        "content-type": "application/json",
        "X-RapidAPI-Key": Encryption(
            b"gAAAAABkdNK73vwKyDgk_c2_s2Sm0lG9zsujkTo4em06gJvHDiNTpQTq32n2zx604UCe2fDB4zbTqZWnPva-dWhyT3x5dk4hzcAJ04Wubw-I5tW65a3N-Gt1dKmqMAsWtOc5t_3rNI2vHirZYxiSXDzEoyipt9hxvQ=="
        ).decrypt_text(),
        "X-RapidAPI-Host": "microsoft-text-analytics1.p.rapidapi.com",
    }

    response = requests.post(url, json=payload, headers=headers).json()
    sentiment = response.get("documents")[0].get("sentiment")
    return sentiment


# -------------------------------------------------------------------------------------------------------


# Sentiment Analysis by api ninjas
# ------------------------------------------------------------------------------------------------------
def sentimentAnalysisApiNinjas(query):
    api_url = "https://api.api-ninjas.com/v1/sentiment?text={}".format(query)
    response = requests.get(
        api_url,
        headers={
            "X-Api-Key": Encryption(
                b"gAAAAABkdNJcXSk6GKsHGRaM9yngyv6dtKYbo5x7Pkd30f0CdVl-gh7ab0GSUx7-k3KHf9-rPKbim88CewqDW0ncBEaldlKvCdIbVooBiG4_VZo8DxOoTnvA0jjX5DA47w86VS2faEr7"
            ).decrypt_text()
        },
    )
    if response.status_code == requests.codes.ok:
        response = response.json()
        return response.get("score")
    else:
        return 0


# ------------------------------------------------------------------------------------------------------


# Microsoft entity recoginition
# Returned value is list of dictionaries
# -------------------------------------------------------------------------------------------------------
def entity_recognition(query):
    url = (
        "https://microsoft-text-analytics1.p.rapidapi.com/entities/recognition/general"
    )
    payload = {"documents": [{"id": "1", "language": "en", "text": f"{query}"}]}
    headers = {
        "content-type": "application/json",
        "X-RapidAPI-Key": Encryption(
            b"gAAAAABkdNKRvYRgOggAA9V-85bLnWxrOc1cDCdTqanFOjx3Z6lCdDG_SqMvfUYmmq2kdnu3N2I7-0yYKac0kIoOLB6_J3sgRxEUaiB4NhLA4eT6EgMVTCxaAwGlP0o_fAoybeytpooClynlgZKY8LUTdOKc2NQLwQ=="
        ).decrypt_text(),
        "X-RapidAPI-Host": "microsoft-text-analytics1.p.rapidapi.com",
    }
    response = requests.post(url, json=payload, headers=headers)
    response = response.json()
    entities = response.get("documents")[0].get("entities")
    return entities


#  -------------------------------------------------------------------------------------------------------


# -------------------------------------------------------------------------------------------------------
class SearchQuery:
    def __init__(self, query, lang="en"):
        self.query = query
        self.lang = lang

    def googleResult(self):
        path = self.query.replace(" ", "+")
        url = f"https://www.google.com/search?q={path}&rlz="
        webbrowser.open_new_tab(url)

    # Returns a Wikipedia search for `query`.
    def wikkiSearch(self):
        wikipedia.set_lang(self.lang)
        response = wikipedia.summary("Salmaan Khan", sentences=3)
        return response

    def gptSearch(self):
        pass


# -------------------------------------------------------------------------------------------------------


# -------------------------------------------------------------------------------------------------------
def News(newsTopic):
    client = gnewsclient.NewsClient(
        language="english", location="india", topic=newsTopic, max_results=5
    )
    news_list = client.get_news()
    speak(f"Todays {newsTopic} news  are ")
    for item in news_list:
        speak(item["title"])


# -------------------------------------------------------------------------------------------------------


# -------------------------------------------------------------------------------------------------------
# Function that first check for application, if the application exists then it will open that application
# Otherwise it will open related application
def openAppWebsite(query):
    if ("mili" in query and "setting" in query) or "profile" in query:
        # Login().Interface().pageInterface(True)
        pass
    else:
        apps = AppOpener.give_appnames()
        goto = None
        try:
            for value in query:
                if value in apps:
                    goto = 1
                    AppOpener.run(value)
        except:
            speak("That may be beyond my abilities at the moment")
        if goto is None:
            try:
                query = " ".join(query)
                for web in search(query, tld="co.in", num=10, stop=10, pause=2):
                    link = web
                    break
                webbrowser.open_new_tab(link)
            except Exception as e:
                SearchQuery(query).googleResult()


# -------------------------------------------------------------------------------------------------------


# Class which suggest movies according to genre
# -------------------------------------------------------------------------------------------------------
class MoviesData:
    def __init__(self, query):
        self.query = query
        self.db = imdb.IMDb()

    def sortData(self, movieData):
        data = {}
        rand = sample(range(0, 25), 10)
        for element in movieData:
            if element.data.get("year") is not None:
                data.update(
                    {
                        f"{element.data.get('title')} {element.data.get('year')}": element.data.get(
                            "year"
                        )
                    }
                )
        data = sorted(data.items(), key=lambda x: x[1], reverse=True)
        sortedMovies = list(dict(data).keys())
        result = [sortedMovies[i] for i in rand]
        return "\n".join(result)

    def Movies(self):
        speak("Wait a moment")
        if "india" in self.query or "indian" in self.query or "bollywood" in self.query:
            topIndianMovies = self.db.get_top250_indian_movies()
            speak(self.sortData(topIndianMovies))
        elif "popular" in self.query:
            popularMovies = self.db.get_popular100_movies()
            speak(self.sortData(popularMovies))
        else:
            nlp = spacy.load("en_core_web_sm")
            doc = nlp(self.query)
            pos = {}
            for token in doc:
                pos.update({str(token.lemma_): (token.pos_, token.dep_)})
            key_list = list(pos.keys())
            val_list = list(pos.values())
            try:
                position = val_list.index(("NOUN", "compound"))
                gerne = key_list[position]
                moviesbygenres = self.db.get_top50_movies_by_genres([gerne])
                speak(self.sortData(moviesbygenres))
            except:
                topMovies = self.db.get_top250_movies()
                speak(self.sortData(topMovies))


# -------------------------------------------------------------------------------------------------------


#  Functions to return random jokes
# -------------------------------------------------------------------------------------------------------
async def randomJokes():
    value = defaultMiliGeneralSettings().get("Explicit content")
    if value == 0:
        value = True
    else:
        value = False
    j = await Jokes()
    joke = await j.get_joke(safe_mode=value)
    if joke["type"] == "single":
        speak(type(joke["joke"]))
    else:
        speak(joke["setup"])
        speak(joke["delivery"])


# -------------------------------------------------------------------------------------------------------


#  Functions to return random quotes
# -------------------------------------------------------------------------------------------------------
def random_quotes():
    rand = randint(0, 100)
    if rand % 3 == 0:
        speak("Here's a beautiful quote")
    elif rand % 3 == 1:
        speak("Sure")
    try:
        url = "https://api.quotable.io/random"
        r = requests.get(url)
        quote = r.json()
        content = quote["content"]
        author = quote["author"]
        print(content)
        print("-", author)
        onlySpeak(author + ", once said, " + content)
    except:
        ("Random quotes")


# -------------------------------------------------------------------------------------------------------


# -------------------------------------------------------------------------------------------------------
def maigicTrick():
    rand = randint(1, 100)
    if rand % 4 == 0:
        speak("Pick any number between 1 and 20.")
        time.sleep(2)
        speak("Now add 15 to it")
        time.sleep(2)
        speak("Now add 6 to it and subtract 8 from it")
        time.sleep(2)
        speak(
            "Finally, subtract  the number you  originally thought of from the number you have now."
        )
        time.sleep(2)
        speak("The answer you're thinking of is 13 😲")
    elif rand % 4 == 1:
        speak("Pick any number between 1 and 20.")
        time.sleep(2)
        speak("Now add 1 to it")
        time.sleep(2)
        speak("Now double the new number")
        time.sleep(2)
        speak("Now add 4 to it and divide it by 2")
        time.sleep(2)
        speak(
            "Finally, subtract  the number you  originally thought of from the number you have now."
        )
        time.sleep(2)
        speak("The answer you're thinking of is 3 😲")
    elif rand % 4 == 2:
        time.sleep(1)
        speak("Multiply the first digit of your age by 5")
        time.sleep(2)
        speak("Now add 4 to the answer")
        time.sleep(2)
        speak("Now double the answer and add the second digit of your age to it")
        time.sleep(2)
        speak("Now tell me your answer")
        query = takeCommand().lower()
        # age = getInteger(query)
        # your_age = int(age[0])
        # your_age -= 8
        # your_age = str(your_age)
        # speak("Your age is " + your_age+" 😲")
    elif rand % 4 == 3:
        speak(
            "Pick any number between 1 and 9 and write the same number 3 times to make a 3 digit number"
        )
        time.sleep(2)
        speak("Now add 3 digits together")
        time.sleep(2)
        speak("Divide the 3 digit number by the number you added a moment ago")
        time.sleep(2)
        speak("The answer you're thinking of is 37 😲")


# -------------------------------------------------------------------------------------------------------


# available wifi-networks
# -------------------------------------------------------------------------------------------------------
def availableWifiNetwork():
    devices = subprocess.check_output(["netsh", "wlan", "show", "network"])
    devices = devices.decode("ascii")
    devices = devices.replace("\r", "").split("\n")
    speak(devices[2].strip())
    available_devices = []
    for element in devices:
        if "SSID" in element:
            available_devices.append(element)
    available = "\n".join(available_devices)
    print(available)


# -------------------------------------------------------------------------------------------------------


# class Song Media
# -------------------------------------------------------------------------------------------------------
class Media:
    def __init__(self, query):
        self.query = query

    # playing songs from youtube music
    def youTubeMuisc(self):
        song_name = ""
        try:
            query_string = urllib.parse.urlencode({"search_query": song_name})
            formatUrl = urllib.request.urlopen(
                "https://www.youtube.com/search?" + query_string
            )
            search_results = re.findall(r"watch\?v=(\S{11})", formatUrl.read().decode())
            music_link = (
                "https://music.youtube.com/watch?v="
                + "{}".format(search_results[0])
                + "&feature=share"
            )
            speak(f"Ok, asking Youtube Music to play {song_name}")
            webbrowser.open_new_tab(music_link)
        except Exception as e:
            SearchQuery(song_name).googleResult()

    # playing media from youtube
    def youTube(self):
        if "play" in self.query:
            query = self.query.replace("play", "")
        query = query.strip()
        try:
            query_string = urllib.parse.urlencode({"search_query": query})
            formatUrl = urllib.request.urlopen(
                "https://www.youtube.com/results?" + query_string
            )
            search_results = re.findall(r"watch\?v=(\S{11})", formatUrl.read().decode())
            music_link = "https://www.youtube.com/watch?v=" + "{}".format(
                search_results[0]
            )
            speak("Ok, asking Youtube to play")
            webbrowser.open_new_tab(music_link)
        except Exception as e:
            SearchQuery(query).googleResult()


# -------------------------------------------------------------------------------------------------------


# This function serves the purpose of generating random facts.
# -------------------------------------------------------------------------------------------------------
def facts(query):
    if "fun" in query or "useless" in query:
        url = "https://uselessfacts.jsph.pl/random.json?language=en"
        response = requests.request("GET", url)
        data = json.loads(response.text)
        fun_fact = data["text"]
        speak(fun_fact)
    else:
        value = defaultMiliGeneralSettings().get("Explicit content")
        if value == 1:
            value = True
        else:
            value = False
        x = randfacts.get_fact(value, value)
        speak(x)


# -------------------------------------------------------------------------------------------------------


# --------------------------------------------------------------------------------------------------------
class Grocery:
    def __init__(self, query):
        self.query = query
        self.grocery_items = []
        self.filepath = "Data\\Files\\Grocery items.bin"

    # Extracting grocery items from the query using microsoft entity recognition
    # ---------------------------------------------------------------------------
    def extract_grocery_items(self):
        entities = entity_recognition(self.query)
        for entity in entities:
            if entity.get("category") == "Product" and entity.get("text") != "grocery":
                self.grocery_items.append(str(entity.get("text")).capitalize())

    # ---------------------------------------------------------------------------

    def showGroceryList(self, id):
        with open(self.filepath, "rb") as file:
            data = pickle.load(file)
            if id is True:
                speak(f"You have {len(data)} items on that list")
            for items in data:
                print(items)

    # Adding grocery items in the grocery list
    # ---------------------------------------------------------------------------
    def add_item(self):
        thread = Thread(target=self.extract_grocery_items)
        thread.start()
        if os.path.exists(self.filepath) is False:
            speak(
                "I couldn't find a list called 'Grocery'. Do you want me to make one?"
            )
            value = takeCommand().lower()
            sentiment = sentimentAnalysisApiNinjas(value)
            if sentiment > 0:
                thread.join()
                if len(self.grocery_items) == 0:
                    speak(f"Got it, I made a list called 'Grocery'")
                else:
                    if len(self.grocery_items) == 1:
                        speak(
                            f"Got it, I made a list called 'Grocery' and added {self.grocery_items[0]}."
                        )
                    else:
                        duplicate_list = self.grocery_items.copy()
                        last_item = duplicate_list.pop()
                        speak(
                            f"Got it, I made a list called 'Grocery' and added {','.join(duplicate_list)} and {last_item}."
                        )
                    with open(self.filepath, "wb") as file:
                        pickle.dump(set(self.grocery_items), file)
                        file.close()
                    print("List Updated")
                    self.showGroceryList(False)
            else:
                speak("Ok, nothing's been changed.")
        else:
            thread.join()
            with open(self.filepath, "rb+") as file:
                list = pickle.load(file)
                list.update(set(self.grocery_items))
                file.seek(0)
                pickle.dump(list, file)
                file.close()
                print("List Updated")
                self.showGroceryList(False)

    # ---------------------------------------------------------------------------

    # Removing grocery items from the list
    # ---------------------------------------------------------------------------
    def remove_grocery_item(self):
        thread = Thread(target=self.extract_grocery_items)
        thread.start()
        if os.path.exists(self.filepath) is False:
            speak("I couldn't find a list called 'Grocery'.")
        else:
            thread.join()
            if len(self.grocery_items) == 0:
                speak("Are you sure want to go ahead and delete it?")
                newQuery = takeCommand().lower()
                sentiment = sentimentAnalysisApiNinjas(newQuery)
                if sentiment > 0:
                    speak("Got it, I deleted the list called 'Grocery'")
                    os.remove(self.filepath)
                else:
                    speak("Ok, nothing's been changed.")
            else:
                with open("Data\\Files\\Grocery items.bin", "rb+") as file:
                    list = pickle.load(file)
                    for items in self.grocery_items:
                        try:
                            list.remove(items)
                            speak(f"Got it, I deleted {items}")
                        except:
                            speak(f"I couldn't find a grocery called {items}.")
                    file.seek(0)
                    pickle.dump(list, file)
                    file.close()

    # ---------------------------------------------------------------------------

    def handle_functions(self):
        if "add" in self.query:
            self.add_item()
        elif "delete" in self.query or "remove" in self.query:
            self.remove_grocery_item()
        else:
            print("Grocery List")
            self.showGroceryList(True)


# --------------------------------------------------------------------------------------------------------


# This class serves the purpose of generating random facts based on numbers.
# The givenNumberFact() function generates a random fact related to a given number
# While the randomNumberFact() function generates a random fact based on a randomly generated number.
# --------------------------------------------------------------------------------------------------------
class factsRelatedWithNumber:
    def __init__(self, query):
        self.query = query
        self.number = None

    def givenNumberFact(self):
        url = f"https://numbersapi.p.rapidapi.com/{self.number}/trivia"
        querystring = {"fragment": "true", "notfound": "floor", "json": "true"}
        headers = {
            "X-RapidAPI-Key": Encryption(
                b"gAAAAABkdNHwdK4torDYeqMGTc2jQ4Dil1d_2fFJiPeFuW4tpsuVinnMhbM5ypxHUp7kyy6VoYLfSw6TbAkpvKWOT0pX6HVb1SiCfAo4HwOuKSLVeQaShdILrS3rXCL-Goxc4ijFmv-Y5E5p6LbvKZgYmixShnpy6g=="
            ).decrypt_text(),
            "X-RapidAPI-Host": "numbersapi.p.rapidapi.com",
        }
        response = requests.request(
            "GET", url, headers=headers, params=querystring
        ).text
        response = json.loads(response)
        speak(response.get("text").capitalize())

    def randomNumberFact(self):
        url = "https://numbersapi.p.rapidapi.com/random/trivia"
        querystring = {"min": "10", "max": "20", "fragment": "true", "json": "true"}
        headers = {
            "X-RapidAPI-Key": Encryption(
                b"gAAAAABkdNHwdK4torDYeqMGTc2jQ4Dil1d_2fFJiPeFuW4tpsuVinnMhbM5ypxHUp7kyy6VoYLfSw6TbAkpvKWOT0pX6HVb1SiCfAo4HwOuKSLVeQaShdILrS3rXCL-Goxc4ijFmv-Y5E5p6LbvKZgYmixShnpy6g=="
            ).decrypt_text(),
            "X-RapidAPI-Host": "numbersapi.p.rapidapi.com",
        }
        response = requests.request(
            "GET", url, headers=headers, params=querystring
        ).text
        response = json.loads(response)
        result = f"{response.get('number')} is {response.get('text')}"
        speak(result)

    def chooseFunction(self):
        for element in self.query:
            if element.isdigit():
                self.number = element
                self.givenNumberFact()
                break
        if self.number is None:
            self.randomNumberFact()


# --------------------------------------------------------------------------------------------------------


# This function is designed to provide three important functionalities for the device:
#  shutting down the device, activating the hibernate mode, and restarting the device.
# --------------------------------------------------------------------------------------------------------
def deviceControl(val):
    speak("Do you confirmed")
    query = takeCommand().lower()
    sentiment = sentimentAnalysisApiNinjas(query)
    if sentiment > 1:
        if val == 1:
            speak("Hold a second. Your system is on its way to shut down")
            subprocess.call(["shutdown", "/s"])
        elif val == 2:
            speak("Restarting your device")
            subprocess.call(["shutdown", "/r"])
        elif val == 3:
            speak("Hibernating your device")
            subprocess.call(["shutdown", "/l"])
    else:
        speak("Ok...")


# --------------------------------------------------------------------------------------------------------


# This class serves the purpose of securely storing user secrets by employing encryption techniques.
# It encompasses four functions that facilitate various operations related to the secrets.
# --------------------------------------------------------------------------------------------------------
class Secret:
    def __init__(self):
        self.secret = None
        self.query_secret = None
        self.file_path = application_directory + "\\Data\\Files\\Secrets.bin"

    # This function is used to convert the secret from first person to the second person
    # --------------------------------------------------------------------------------------------------------
    def firstPersonToSecondPerson(self) -> str:
        pronouns = ("i", "you", "we", "my", "mine", "us", "me", "our", "ours")
        pronounsFirstPersonSubject = {
            "i": "you",
            "you": "i",
            "we": "you",
            "my": "your",
            "our": "your",
            "us": "you",
            "ours": "yours",
        }
        pronounsFirstPersonObject = {
            "you": "me",
            "mine": "your",
            "my": "your",
            "us": "you",
            "me": "you",
            "our": "your",
            "us": "you",
            "ours": "yours",
        }

        nlp = spacy.load("en_core_web_sm")
        doc = nlp(self.query_secret)
        query = self.query_secret.split()
        for i, token in enumerate(doc):
            if token.text in pronouns:
                if token.dep_ == "nsubj" and token.pos_ == "PRON":
                    query[i] = pronounsFirstPersonSubject.get(token.text)
                else:
                    query[i] = pronounsFirstPersonObject.get(token.text)

        query = " ".join(query)
        query = removeGrammaticalErrors(query)
        current_date = datetime.strftime(datetime.now(), "%d %B")
        self.secret = Encryption(
            f"On {current_date} you said, {query.capitalize()}."
        ).encrypt_text()

    # --------------------------------------------------------------------------------------------------------

    # This function takes secret query from the user and save it in secrets.bin file
    # User privacy is ensured by encrypting the secrets, alleviating any concerns or worries regarding their confidentiality.
    # Secrets are stored in th form of list of dictionaries
    # Dictionary have three keys -> 1) Date, 2) Time and 3) Secret
    # --------------------------------------------------------------------------------------------------------
    def add_secret(self):
        speak("Plese tell me your secret")
        speak("I keep this between us 🤫")
        self.query_secret = takeCommand().lower()
        thread = Thread(target=self.firstPersonToSecondPerson)
        thread.start()
        secret_date = datetime.strftime(datetime.now(), "Date: %A, %d %B, %Y")
        secret_time = datetime.strftime(datetime.now(), "Time: %I:%M %p")
        thread.join()
        data = {"Date": secret_date, "Time": secret_time, "Secret": self.secret}
        if os.path.exists(self.file_path):
            with open(self.file_path, "rb+") as file:
                list = pickle.load(file)
                list.append(data)
                file.seek(0)
                pickle.dump(list, file)
                file.close()
        else:
            with open(self.file_path, "wb") as file:
                pickle.dump([data], file)
                file.close()
        speak("Oh.. ok")

    # --------------------------------------------------------------------------------------------------------

    # This function is used to delete the secrets
    # --------------------------------------------------------------------------------------------------------
    def delete_secrets(self):
        if os.path.exists(self.file_path) is False:
            speak("Currently you have no secrets")
        else:
            os.remove(self.file_path)
            speak("Your secrets has been deleted")

    # --------------------------------------------------------------------------------------------------------

    # This function is used to retrieve the secrets from the encrypted file
    # --------------------------------------------------------------------------------------------------------
    def show_secrets(self):
        if os.path.exists(self.file_path) is False:
            speak("Currently you have no secrets")
        else:
            speak("Your secrets are ")
            with open(self.file_path, "rb") as file:
                data = pickle.load(file)
            for secret in data:
                print(secret.get("Date"))
                print(secret.get("Time"))
                decrypted_secret = Encryption(secret.get("Secret")).decrypt_text()
                speak(decrypted_secret)
                print()

    # --------------------------------------------------------------------------------------------------------


# --------------------------------------------------------------------------------------------------------


# mit model response
# --------------------------------------------------------------------------------------------------------
def wit_model(query):
    entities, intent = witResponse(query)
    if ("translate" in query or "meaning" in query) and intent == "translate":
        flag = True
        language = entities["language:language"]
        body = entities["wit$message_body:message_body"]
        if len(language) > 1 or len(body) > 1:
            flag = False
            Translate(query, flag).google_translate()
        else:
            flag = True
            language = language[0]["value"]
            body = body[0]["value"]
            query = {"body": body, "language": language}
            Translate(query, flag).google_translate()
        return True
    elif intent == "wit$get_weather":
        try:
            location = entities["wit$location:location"][0]["body"]
            # function of weather
        except:
            pass
            # function of weather
        return True
    elif intent == "map":
        try:
            locations = entities["wit$location:location"]
            if len(locations) == 2:
                origin = locations[0]["body"]
                destination = locations[1]["body"]
                map_interface.distanceAndRoute(origin, destination)
                map_interface.mainloop()
            else:
                destination = locations[0]["body"]
                map_interface.distanceAndRoute(None, destination)
                map_interface.mainloop()
        except:
            map_interface.currentLocation()
            map_interface.mainloop()
        return True
    elif intent == "grocery":
        # grocery function
        return True
    else:
        return False


# --------------------------------------------------------------------------------------------------------


# Executing all models here
def AI_models(query: str):
    wit_response = wit_model(query)
    if wit_response is False:
        pass


if __name__ == "__main__":
    flag = True
    while flag is not False:
        query = input("You : ")
        print()
        AI_models(query)
        flag = True
