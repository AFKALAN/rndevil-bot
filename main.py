import discord
from discord.ext import commands
import os
import re
import random
from dotenv import load_dotenv

#Setup intents needed to run commands
intents = discord.Intents.default()
intents.message_content = True

#Set super secret token for bot login
load_dotenv()
TOKEN = os.getenv('TOKEN')

#Load bot instance
bot = commands.Bot(command_prefix='RND', intents=intents)

#bully target for bully command
bully_target = ''

#response for crazy number of dice or sides
randy_array = ['https://tenor.com/beRjI.gif', 'https://tenor.com/bepda.gif', 'https://tenor.com/bPnmo.gif', 'https://tenor.com/bPnmr.gif', 'https://tenor.com/bPnmv.gif']

#dice roller function that gets called by RNDroll (number of dice)d(how many sides each die has)
def dice_roller(content):
  numregex = re.compile(r'(\d+)(d)(\d+)')
  total_roll = 0

  roller = numregex.search(content)
  dice_num = int(roller.group(1))
  dice_len = int(roller.group(3))
  
  #won't calculate a roll if numbers are ridiculous
  if dice_num > 100 or dice_len > 100:
    return randy_array[random.randint(0, len(randy_array) - 1)]

  while dice_num > 0:
      total_roll += random.randint(1, dice_len)
      dice_num -= 1

  return 'You rolled a total of {}'.format(str(total_roll))

#bully function to set target
def bullyResponse(content):
  if len(content.message.mentions) != 1:
    return ('There can only be 1 bully target at a time. Please try again.')
  else:
    global bully_target
    bully_target = content.message.mentions[0]
    return ('{} has chosen to bully {}. Target acquired.'.format(content.author.name, bully_target.name))

#Login confirmation
@bot.event
async def on_ready():
  print('We have logged in as {0.user}'.format(bot))

#dice roller command
@bot.command()
async def roll(ctx, arg):
  await ctx.send(dice_roller(arg))

#select target to be bullied
@bot.command()
@commands.is_owner()
async def bully(ctx):
  await ctx.send(bullyResponse(ctx))

#listener for when bullied talks
@bot.event
async def on_message(message):
  if message.author == bot.user:
    return

  if message.author == bully_target:
    await message.channel.send('Shutup {}, you virgin'.format(bully_target.name))
  
  await bot.process_commands(message)

bot.run(TOKEN)