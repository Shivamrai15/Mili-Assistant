import tensorflow as tf
import numpy as np
import json
import nltk
import pickle
from nltk.stem import WordNetLemmatizer

# Load the dataset
with open(r"Data\Files\dataset.json", "r") as file:
    data = json.load(file)

# Initialize WordNetLemmatizer
lemmatizer = WordNetLemmatizer()

words = []
labels = []
docs_x = []
docs_y = []

# Process the dataset
for intent in data["intents"]:
    for pattern in intent["patterns"]:
        wds = nltk.word_tokenize(pattern)
        words.extend(wds)
        docs_x.append(wds)
        docs_y.append(intent["tag"])
        if intent["tag"] not in labels:
            labels.append(intent["tag"])

words = [lemmatizer.lemmatize(w.lower()) for w in words]
words = sorted(list(set(words)))
labels = sorted(labels)

training = []
output = []
out_empty = [0 for _ in range(len(labels))]

# Create training and output data
for x, doc in enumerate(docs_x):
    bag = []
    wrds = [lemmatizer.lemmatize(w) for w in doc]
    for w in words:
        bag.append(1) if w in wrds else bag.append(0)

    output_row = out_empty.copy()
    output_row[labels.index(docs_y[x])] = 1

    training.append(bag)
    output.append(output_row)

training = np.array(training)
output = np.array(output)

# Save preprocessed data
with open("Data\\Files\\data.pickle", "wb") as file:
    pickle.dump((words, labels, training, output), file)

# Define the neural network model
model = tf.keras.Sequential(
    [
        tf.keras.layers.Dense(8, activation="relu", input_shape=(len(training[0]),)),
        tf.keras.layers.Dense(8, activation="relu"),
        tf.keras.layers.Dense(len(output[0]), activation="softmax"),
    ]
)

# Compile the model
model.compile(optimizer="adam", loss="categorical_crossentropy", metrics=["accuracy"])

# Train the model
model.fit(training, output, epochs=500, batch_size=8, verbose=1)

# Save the trained model
model.save("Data\\Files\\model.tensorflow")
