# import nltk
# from sklearn.feature_extraction.text import TfidfVectorizer
# # from sklearn.ensemble import GradientBoostingClassifier
# # from sklearn.metrics import classification_report

# # # nltk.download('nps_chat')
# posts = nltk.corpus.nps_chat.xml_posts()


# posts_text = [post.text for post in posts]

# # #divide train and test in 80 20
# train_text = posts_text[:int(len(posts_text)*0.8)]
# test_text = posts_text[int(len(posts_text)*0.2):]

# #Get TFIDF features
# vectorizer = TfidfVectorizer(ngram_range=(1,3),
#                              min_df=0.001,
#                              max_df=0.7,
#                              analyzer='word')

# X_train = vectorizer.fit_transform(train_text)
# X_test = vectorizer.transform(test_text)

# y = [post.get('class') for post in posts]

# y_train = y[:int(len(posts_text)*0.8)]
# y_test = y[int(len(posts_text)*0.2):]

# # Fitting Gradient Boosting classifier to the Training set
# gb = GradientBoostingClassifier(n_estimators = 400, random_state=0)
# #Can be improved with Cross Validation

# gb.fit(X_train, y_train)

# predictions_rf = gb.predict(X_test)

# #Accuracy of 86% not bad
# print(classification_report(y_test, predictions_rf))

import discord
from dotenv import load_dotenv
import enum
from joblib import dump, load
import numpy
import os
import random

load_dotenv()

class MessageTypes(enum.Enum):
    ACCEPT='Accept'
    BYE='Bye'
    CLARIFY='Clarify'
    CONTINUER='Continuer'
    EMOTION='Emotion'
    EMPHASIS='Emphasis'
    GREET='Greet'
    OTHER='Other'
    REJECT='Reject'
    STATEMENT='Statement'
    SYSTEM='System'
    NANSWER='nAnswer'
    WHQUESTION='whQuestion'
    YANSWER='yAnswer'
    YNQUESTION='ynQuestion'

your=['your', 'ur', 'yo', 'joe']
mom=['mom', 'momma', 'mother', 'mum', 'mama']

gb = load('gb.pkl')
vectorizer = load('vectorizer.pkl')

client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    prediction = gb.predict(vectorizer.transform([message.content]))
    if prediction == ['whQuestion']:
        await message.channel.send(random.choice(your) + " " + random.choice(mom))

@client.event # doesn't work yet
async def on_member_join(member):
    print('member joined!')
    await member.send('welcome!', mention_author=True)

client.run(os.getenv('TOKEN'))