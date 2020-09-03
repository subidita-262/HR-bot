import nltk
from nltk.stem.lancaster import LancasterStemmer
stemmer = LancasterStemmer()
#nltk.download('punkt')
#Libraries needed for Tensorflow Processing
import tensorflow as tf
tf.disable_v2_behavior()
import numpy as np
import tflearn
import random
import json
import pickle
import warnings
warnings.filterwarnings("ignore")





# restoring all the data structures
data = pickle.load( open( "training_data.pkl", "rb" ) )
words = data['words']
classes = data['classes']
train_x = data['train_x']
train_y = data['train_y']


#Neural Network architechture
tf.reset_default_graph()

net = tflearn.input_data(shape = [None, len(train_x[0])])
net = tflearn.fully_connected(net, 10)
net = tflearn.fully_connected(net, 10)
net = tflearn.fully_connected(net, len(train_y[0]), activation = 'softmax')


#defining model and setting up tensorboard

model  = tflearn.DNN(net, tensorboard_dir='tflearn_logs')

with open('intent (Interview).json') as json_data:
    intents = json.load(json_data)
#classes


#importing the trained model
model.load('model.tflearn', weights_only = True)



def clean_up_sentence(sentence):
    # tokenizing the pattern
    sentence_words = nltk.word_tokenize(sentence)
    # stemming each word
    sentence_words = [stemmer.stem(word.lower()) for word in sentence_words]
    return sentence_words

# returning bag of words array: 0 or 1 for each word in the bag that exists in the sentence
def bow(sentence, words, show_details=False):
    # tokenizing the pattern
    sentence_words = clean_up_sentence(sentence)
    # generating bag of words
    bag = [0]*len(words)  
    for s in sentence_words:
        for i,w in enumerate(words):
            if w == s: 
                bag[i] = 1
                if show_details:
                    print ("found in bag: %s" % w)

    return(np.array(bag))


ERROR_THRESHOLD = 0.30
def classify(sentence):
    # generate probabilities from the model
    results = model.predict([bow(sentence, words)])[0]
    # filter out predictions below a threshold
    results = [[i,r] for i,r in enumerate(results) if r>ERROR_THRESHOLD]
    # sort by strength of probability
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append((classes[r[0]], r[1]))
    # return tuple of intent and probability
    return return_list

def response(sentence, userID='123', show_details=False):
    results = classify(sentence)
    # if we have a classification then find the matching intent tag
    if results:
        # loop as long as there are matches to process
        while results:
            for i in intents['intents']:
                # find a tag matching the first result            
                      
                if i['tag'] == results[0][0]:
                    # a random response from the intent                    
                    return random.choice(i['responses'])               
    
            results.pop(0)
    else:
      return 'HR_bot: Sorry, Your input is not understanble or acceptable for us'



        
        
   

  
