# Libraries needed for NLP
import nltk
# nltk.download('punkt')
from nltk.stem.lancaster import LancasterStemmer
stemmer = LancasterStemmer()

#Libraries needed for Tensorflow Processing
import tensorflow.compat.v1 as tf
tf.disable_v2_behavior()
import numpy as np
import tflearn
import random
import json

#import our chat-bot intents file
with open("intent (Interview).json") as json_data:
  intents = json.load(json_data)
  
words = []
classes = []
documents = []
ignore = ['?']
#loop through each sentence in the intent's patterns
for intent in intents['intents']:  
  for pattern in intent['patterns']:
    #tokenize each and every word in the sentence
    w = nltk.word_tokenize(pattern)
    #addword to the words list
    #print(w)
    words.extend(w)
    #add word(s) to documents
    documents.append((w, intent['tag']))
    # add tags to our classes list
    if intent['tag'] not in classes:
      classes.append(intent['tag'])
print('documents: ',documents)
print('words: ',words)
print('classes: ',classes)    



#perform stemming and lower each word as well as remove duplicates
words = [stemmer.stem(w.lower()) for w in words if w not in ignore]
words = sorted(list(set(words)))

#remove duplicate classes
classes = sorted(list(set(classes)))

print(len(documents),"documents")
print(len(classes),"classes",classes)
print(len(words),"unique stemmed words",words)


#create training data
training = []
output = []
# create an empty array for output
output_empty = [0]*len(classes)


#create training set, bag of words for each sentence
for doc in documents:
  #initialize bag of words
  bag = []
  # list of tokenized words for the pattern
  pattern_words = doc[0]

  #stemming each word 
  pattern_words = [stemmer.stem(word.lower()) for word in pattern_words]

  #create bag of words array
  for w in words:
    bag.append(1) if w in pattern_words else bag.append(0)

  #output is '1' for current tag and '0' for rest of the other tags
  output_row = list(output_empty)
  output_row[classes.index(doc[1])] = 1

  training.append([bag, output_row])

#shuffling features and turning it into np.array
random.shuffle(training)
training = np.array(training)

#creating training lists 
train_x = list(training[:,0])
train_y = list(training[:,1])




#resetting underlying graph data
tf.reset_default_graph()

#building neural network
net = tflearn.input_data(shape = [None, len(train_x[0])])
net = tflearn.fully_connected(net, 10)
net = tflearn.fully_connected(net, 10)
net = tflearn.fully_connected(net, len(train_y[0]), activation = 'softmax')
net = tflearn.regression(net)

#defining model and setting up tensorboard

model  = tflearn.DNN(net, tensorboard_dir='tflearn_logs')

#start training
model.fit(train_x,train_y, n_epoch = 1000, batch_size = 8, show_metric = True)
model.save('model.tflearn')

import pickle
pickle.dump( {'words':words, 'classes':classes, 'train_x':train_x, 'train_y':train_y}, open( "training_data.pkl", "wb" ) )



