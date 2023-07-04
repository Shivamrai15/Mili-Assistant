import numpy
import tflearn
import json
import nltk
import pickle

from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()

with open("Data\\Files\\dataset.json", "r") as file:
    data = json.load(file)

words = []
labels = []
docs_x = []
docs_y = []

for intent in data['intents']:
    for pattern in intent['patterns']:
        wds = nltk.word_tokenize(pattern)
        words.extend(wds)
        docs_x.append(wds)
        docs_y.append(intent['tag'])

        if intent['tag'] not in labels:
            labels.append(intent['tag'])

words = [lemmatizer.lemmatize(w.lower()) for w in words]
words = sorted(list(set(words)))
labels = sorted(labels)


training = []
output = []

out_empty = [0 for _ in range(len(labels))]

for x, doc in enumerate(docs_x):
    bag = []
    wrds = [lemmatizer.lemmatize(w) for w in doc]
    for w in words:
        if w in wrds:
            bag.append(1)
        else:
            bag.append(0)

    output_row = out_empty.copy()
    output_row[labels.index(docs_y[x])] = 1
    training.append(bag)
    output.append(output_row)


training = numpy.array(training)
output = numpy.array(output)

with open("Data\\Files\\data.pickle", "wb") as file:
    pickle.dump((words, labels, training, output), file)

net = tflearn.input_data(shape=[None, len(training[0])])
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, len(output[0]), activation="softmax")
net = tflearn.regression(net)


model = tflearn.DNN(net)
model.fit(training, output, n_epoch=2000, batch_size=8, show_metric=True)
model.save("model.tflearn")