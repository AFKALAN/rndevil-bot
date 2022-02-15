import discord
import os
import re
import random
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('TOKEN')

client = discord.Client()

def dice_roller(content):
    numregex = re.compile(r'(\d+)(d)(\d+)')
    totalroll = 0
    
    roller = numregex.search(content)
    dicenum = int(roller.group(1))
    dicelen = int(roller.group(3))

    if dicenum > 100:
      return ('no, fuck you')

    if dicelen > 100:
      return ('no, fuck you')
    
    while dicenum > 0:
        totalroll += random.randint(1, dicelen)
        dicenum -= 1

    return str(totalroll)


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    
    if message.author == client.user:
      return
    
    if message.content.startswith('RND bully'):
      await message.channel.send('New target aquired.')

    if message.content == ('RND help'):
      await message.channel.send('Only bot command is RNDice (number of dice)d(die faces)')

    if message.content.startswith('RNDice'):
      await message.channel.send('You rolled a total of ' + dice_roller(message.content))

client.run(TOKEN)