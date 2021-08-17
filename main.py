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
        return
    
    if message.content[:3] == "I\'m" or message.content[:3] == "i\'m":
        try:
            await message.channel.send("Hi {}, I'm dad!".format(message.content[4:]))
        except:
            print("poopoo")
        return

@client.event # doesn't work yet
async def on_member_join(member):
    print('member joined!')
    await member.send('welcome!', mention_author=True)

client.run(os.getenv('TOKEN'))