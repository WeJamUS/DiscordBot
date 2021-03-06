import discord
import enum
from joblib import dump, load
import numpy
import os
import random
import sys

# Constants
DEBUGGING = False
MENTION_WEJAMUS = "<@339859157404614657>"
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
CHARACTER_LIMIT = 2000
your=['your', 'ur', 'yo', 'joe']
mom=['mom', 'momma', 'mother', 'mum', 'mama']
dad=['dad', 'daddy']
im = ["i\'m", "i am", "i’m", "im", "ima", "i`m"]

# Load question classification model
gb = load('gb.pkl')
vectorizer = load('vectorizer.pkl')

client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

# Handle message responses
@client.event
async def on_message(message):
    # Don't respond to a message from ourselves
    if message.author == client.user:
        return

    # Convert message to lowercase before parsing
    lowercaseMsg = message.content.lower()

    # Respond to command messages that begin with $
    if lowercaseMsg.startswith("$"):
        commandMsg = lowercaseMsg[1:].split(" ", 1)
        commandOptions = ""
        if (len(commandMsg) > 1 and commandMsg[1].startswith("-")):
            separateCmd = commandMsg[1].split(" ", 1)
            commandOptions = separateCmd[0]
            commandMsg[1] = separateCmd[1]
        if commandMsg[0] == "repeat" or commandMsg[0] == "r":
            sentMsg = ""
            spacing = ""
            if commandOptions.find("s") != -1:
                spacing = " "
            for i in range(int(CHARACTER_LIMIT/(len(commandMsg[1]) + len(spacing)))):
                sentMsg += commandMsg[1] + spacing
            await message.channel.send(sentMsg)
        else:
            await message.channel.send("unknown command: \"" + commandMsg[0] + "\"")

    # Respond to messages containing daddy
    if "daddy" in lowercaseMsg:
        await message.channel.send(MENTION_WEJAMUS + " is my daddy!")
        return

    # Respond to a 'where' type question
    if "where" in lowercaseMsg:
        await message.channel.send("up your butt and around the corner")
        return

    # Respond to 'wei shen me'
    if "shen me" in lowercaseMsg:
        await message.channel.send(random.choice(your) + " " + random.choice(mom))
        return

    # Respond to a who/what/when/why/how type question
    prediction = gb.predict(vectorizer.transform([lowercaseMsg]))
    if prediction == ['whQuestion']:
        await message.channel.send(random.choice(your) + " " + random.choice(mom))
        return

    try:
        for s in im:
            idx = lowercaseMsg.rfind(s + " ")
            if not idx == 0:
                idx = lowercaseMsg.rfind(" " + s + " ")
                if idx == -1:
                    continue
                idx += 1
            if idx == -1:
                continue
            else:
                await message.channel.send("Hi {}, I'm dad!".format(message.content[idx + len(s) + 1:]))
                break
    except:
        print('poopoo')

    if (DEBUGGING):
        # Flush stdout stream so print statements actually show up when debugging locally
        sys.stdout.flush()

    return

@client.event # doesn't work yet
async def on_member_join(member):
    print('member joined!')
    await member.send('welcome!', mention_author=True)

# Start bot
client.run(os.environ['BOT_TOKEN'])