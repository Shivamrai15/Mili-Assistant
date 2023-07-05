import tflearn
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

net = tflearn.input_data(shape=[None, len(training[0])])
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, len(output[0]), activation="softmax")
net = tflearn.regression(net)

model = tflearn.DNN(net)
model.load("model.tflearn")


def bag_of_words(s, words):
    bag = [0 for _ in range(len(words))]
    s_words = nltk.word_tokenize(s)
    s_words = [lemmatizer.lemmatize(word.lower()) for word in s_words]

    for se in s_words:
        for i, w in enumerate(words):
            if w == se:
                bag[i] = 1
    return numpy.array(bag)


def chat(query: str):
    results = model.predict([bag_of_words(query, words)])[0]
    results_idx = numpy.argmax(results)
    tag = labels[results_idx]
    print(results[results_idx])
    for tg in data["intents"]:
        if tg["tag"] == tag:
            responses = tg["response"]
            context_set = tg["context_set"]
    if len(responses) != 0:
        response = random.choice(responses)
    else:
        response = None
    return response, context_set
