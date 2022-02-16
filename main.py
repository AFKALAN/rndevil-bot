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

#dice roller function that gets called by RNDroll (number of dice)d(how many sides each die has)
def dice_roller(content):
  numregex = re.compile(r'(\d+)(d)(\d+)')
  totalroll = 0

  roller = numregex.search(content)
  dicenum = int(roller.group(1))
  dicelen = int(roller.group(3))
  
  #won't calculate a roll if numbers are ridiculous
  if dicenum > 100 or dicelen > 100:
    return ('no, fuck you')

  while dicenum > 0:
      totalroll += random.randint(1, dicelen)
      dicenum -= 1

  return str(totalroll)

#bully function to set target
def bullyResponse(content):
  if len(content.message.mentions) != 1:
    return ('There can only be 1 bully target at a time. Please try again.')
  else:
    global bullyTarget
    bullyTarget = content.message.mentions[0]
    return ('{} has chosen to bully {}'.format(content.author, bullyTarget.name))

#Login confirmation
@bot.event
async def on_ready():
  print('We have logged in as {0.user}'.format(bot))

#dice roller command
@bot.command()
async def roll(ctx, arg):
  await ctx.send(ctx.author.name + ' rolled a total of ' + dice_roller(arg))

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
    await message.channel.send('Shutup {}, you virgin'.format(bullyTarget.name))
  
  await bot.process_commands(message)


bot.run(TOKEN)