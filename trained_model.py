import tensorflow as tf
import numpy
import pickle
import nltk
import json
import random


from nltk.stem import WordNetLemmatizer

lemmatizer = WordNetLemmatizer()

with open("Data\\Files\\dataset.json", "r") as file:
    data = json.load(file)

with open("Data\\Files\\data.pickle", "rb") as file:
    words, labels, training, output = pickle.load(file)

model = tf.keras.models.load_model("Data\\Files\\model.tensorflow")


def bag_of_words(s, words):
    bag = [0 for _ in range(len(words))]
    s_words = nltk.word_tokenize(s)
    s_words = [lemmatizer.lemmatize(word.lower()) for word in s_words]

    for se in s_words:
        for i, w in enumerate(words):
            if w == se:
                bag[i] = 1
    return numpy.array(bag).reshape(1, len(words))


def chat(query: str):
    results = model.predict([bag_of_words(query, words)])[0]
    results_idx = numpy.argmax(results)
    tag = labels[results_idx]
    if results[results_idx] >= 0.98:
        for tg in data["intents"]:
            if tg["tag"] == tag:
                responses = tg["response"]
                context_set = tg["context_set"]
        if len(responses) != 0:
            response = random.choice(responses)
        else:
            response = None
        return response, context_set
    else:
        return None, None
