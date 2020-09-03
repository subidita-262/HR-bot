# HR_Bot

Abstract:
The growing need of machine learning and AI can effectively be applied to the recruitment process to ease the human life and make the process more cost effective, quick and unbiased. As the recruitment process is being perplexed day by day, sometimes it becomes really tough for a company to go through the all the entire resumes manually and shortlist the candidates based on company requirements for personal interviews. Eventually companies sometimes hire agencies to do this, and end up spending a huge amount of time and money. Here the interview chatbots come into play. 
We have built the HR-BOT to automate the initial screening process by chatting with the candidates online and asking relevant questions so that a company can spend less time going through thousands of resumes and shortlist them faster. It’s not possible for human recruiters to work 24/7 while a chatbot can serve the queries and effectively takes interviews of several candidates at a time without asking for a leave.  

What is Chatbot?
A chatbot is an intelligent piece of software that is capable of communicating and performing actions similar to a human. Chatbots are used a lot in customer interaction, marketing on social network sites and instantly messaging the client. There are two basic types of chatbot models based on how they are built; Retrieval based and Generative based models.

          1. Retrieval based Chatbots: A retrieval-based chatbot uses predefined input patterns and responses. It then uses some type of heuristic approach to select the appropriate response. It is widely used in the industry to make goal-oriented chatbots where we can customize the tone and flow of the chatbot to drive our customers with the best experience.
          2. Generative based Chatbots: Generative models are not based on some predefined responses.They are based on seq 2 seq neural networks. It is the same idea as machine translation. In machine translation, we translate the source code from one language to another language but here, we are going to transform input into an output. It needs a large amount of data and it is based on Deep Neural networks.


#Methodology:
 	The basic training tools that will be used are:
                               - Python 3
              	- Natural Language Processing Tool-kit (nltk)
               	- Tensorflow 1.15
                     - Tflearn
                     - SQlite
    • The platform used for training the model is Google Colab . 
    • We are using tflearn(a wrapper above tensorflow) to create this chatbot. .
    • The language which we used primarily is python3.

*PREPROCESSING THE DATA:* For training the model we have created a .JSON file(i.e the intents file) containing a bunch of messages related to interview purpose that the user is likely to type and mapped them to a group of appropriate responses.
With this data we will be training a neural network to take the words in a sentence and classify it as one of the tags in our file.
Then simply one response from this tag will be shown to the user as a reply.
This in short describes the context/concept of the query and provides answers accordingly.
The golden rule here applies, more data, better results.
We have also used the concepts of Natural Language Processing like word stemming, word tokenizing and creating bag_of_words  to make our “HR-BOT” more accurate in finding general meaning behind the question asked.

*DEVELOPING AND TRAINING THE MODEL:* 
We will be using tensorflow deep neural networks with 2 hidden layers. The goal of our network will be to look at a bag of words and give a class that they belong to.
After setting up the model, we will fit the data to our model, defining the number of epochs.

*MAKING PREDICTIONS:*
Ideally we want to generate a response to any sentence the user types in . To do this, during the actual execution of our “HR-BOT” the process to generate a response will look like the following:-

Get some input from the user ➤ Convert it to a bag of words ➤ Get a prediction from our model ➤ Find the most probable class ➤ Pick a response from that class ➤ Show as response.


Youtube link for demo:

https://youtu.be/ECqabrjyoV4


Project has been deployed and live on:


http://ec2-13-234-38-210.ap-south-1.compute.amazonaws.com:8080/




Done By
1. Swapnadeep Sarkar
2. Subidita Maity
3. Tirtha Paul Chowdhury
