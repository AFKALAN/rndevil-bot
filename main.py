import discord
from discord.ext import commands
import os
import re
import random
from dotenv import load_dotenv

#Set super secret token for bot login
load_dotenv()
TOKEN = os.getenv('TOKEN')

#Load bot instance
bot = commands.Bot(command_prefix='RND')

#bully target for bully command
bullyTarget = ''

#response for crazy number of dice or sides
randyArray = ['https://tenor.com/beRjI.gif', 'https://tenor.com/bepda.gif', 'https://tenor.com/bPnmo.gif', 'https://tenor.com/bPnmr.gif', 'https://tenor.com/bPnmv.gif']

#dice roller function that gets called by RNDroll (number of dice)d(how many sides each die has)
def dice_roller(content):
  numregex = re.compile(r'(\d+)(d)(\d+)')
  totalroll = 0

  roller = numregex.search(content)
  dicenum = int(roller.group(1))
  dicelen = int(roller.group(3))
  
  #won't calculate a roll if numbers are ridiculous
  if dicenum > 100 or dicelen > 100:
    return randyArray[random.randint(0, len(randyArray) - 1)]

  while dicenum > 0:
      totalroll += random.randint(1, dicelen)
      dicenum -= 1

  return 'You rolled a total of {}'.format(str(totalroll))

#bully function to set target
def bullyResponse(content):
  if len(content.message.mentions) != 1:
    return ('There can only be 1 bully target at a time. Please try again.')
  else:
    global bullyTarget
    bullyTarget = content.message.mentions[0]
    return ('{} has chosen to bully {}. Target acquired.'.format(content.author.name, bullyTarget.name))

#Login confirmation
@bot.event
async def on_ready():
  print(f'We have logged in as {bot.user}')

#dice roller command
@bot.command()
async def roll(ctx, arg):
  await ctx.send(dice_roller(arg))

#select target to be bullied
@bot.command()
async def bully(ctx):
  await ctx.send(bullyResponse(ctx))

#listener for when bullied talks
@bot.event
async def on_message(message):
  if message.author == bot.user:
    return

  if message.author == bullyTarget:
    await message.channel.send(f'Shutup {bullyTarget.name}, you virgin')
  
  await bot.process_commands(message)


bot.run(TOKEN)