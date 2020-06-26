import nltk
from nltk.stem.lancaster import LancasterStemmer
stemmer = LancasterStemmer()

#Libraries needed for Tensorflow Processing
import tensorflow as tf
import numpy as np
import tflearn
import random
import json
import pickle
import sqlite3


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

#initial points of the candidate
#p = 0

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
                    return print('\nHR_bot: ',random.choice(i['responses']))               
    
            results.pop(0)
    else:
      return print('HR_bot: Sorry, Your input is not understanble or acceptable for us')

name = str(input("Enter Your Full Name: "))
mail = str(input("Your Email Id: "))

#Initializing the points variables
jr = 0
skill_pts = 0
exp_pts = 0
project_pts = 0
total_pts = 0

#Storing Datas into the Database
def insert_into_db(name,mail,jr,exp_pts,skill_pts, project_pts,total_pts):
    db = sqlite3.connect('HR_bot.db')
    cr = db.cursor()
    
    cr.execute('''INSERT INTO applicants_data(Name, Mail_id, Prefd_Jobrole, Exp_pts, Skills_pts,Projects_pts,Total_pts)
                   VALUES(?,?,?,?,?,?,?);''',(name,mail,jr,exp_pts,skill_pts, project_pts,total_pts))
    db.commit()
    db.close()
    return

    
print('\nHR_bot: Hi, I am HR-bot, Nice to meet you', name)

while True:
    
    s = str(input('you: '))
    
    if classify(s)[0][0] == "Exp_Fresher_level":
        exp_pts = 2
    elif classify(s)[0][0] == "Exp_Intermediate_level":
        exp_pts = 5
    elif classify(s)[0][0] == "Exp_Pro_level":
        exp_pts = 8
    elif classify(s)[0][0] == "Basic_proj":
        project_pts = 2
    elif classify(s)[0][0] == "Intermediate_proj":
        project_pts = 4
    elif classify(s)[0][0] == "Exp_proj_lvl1":
        project_pts = 6
    elif classify(s)[0][0] == "Exp_proj_lvl2":
        project_pts = 8
    elif classify(s)[0][0] == "Skill_Basic":
        skill_pts = 3
    elif classify(s)[0][0] == "Skill_Int":
        skill_pts = 6
    elif classify(s)[0][0] == "Skill_Pro":
        skill_pts = 10
    elif classify(s)[0][0] == "Acceptable_role":
        jr = s
        
    elif s == ('exit' or 'Exit'):
        total_pts = exp_pts + skill_pts + project_pts
        insert_into_db(name,mail,jr,exp_pts,skill_pts, project_pts,total_pts)
        break
        
    response(s)
    