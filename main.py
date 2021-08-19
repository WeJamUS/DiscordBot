import discord
import enum
from joblib import dump, load
import numpy
import os
import random

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
im = ["i\'m", "i am", "i’m", "ima", "im"]

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

    lowercaseMsg = message.content.lower()

    if lowercaseMsg.startswith("where"):
        await message.channel.send("up your butt and around the corner")
        return

    prediction = gb.predict(vectorizer.transform([lowercaseMsg]))
    if prediction == ['whQuestion']:
        await message.channel.send(random.choice(your) + " " + random.choice(mom))
        return

    try:
        for s in im:
            idx = lowercaseMsg.rfind(s+" ")
            if idx == -1:
                continue
            else:
                await message.channel.send("Hi {}, I'm dad!".format(message.content[idx + len(s) + 1:]))
    except:
        print('poopoo')

    return

@client.event # doesn't work yet
async def on_member_join(member):
    print('member joined!')
    await member.send('welcome!', mention_author=True)

client.run(os.environ['BOT_TOKEN'])