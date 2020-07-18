import discord
from discord.ext import commands
import asyncio
from datetime import datetime as dt
import os

script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
rel_path = "conf/discord_token.txt"
abs_file_path = os.path.join(script_dir, rel_path)

with open(abs_file_path, 'r') as f:
	TOKEN = f.read()
	TOKEN = TOKEN.strip()

client = discord.Client()

bot = commands.Bot(command_prefix='!')
#bot.remove_command('help')

@bot.event
async def on_ready():
  #activity = discord.activity(type=discord.ActivityType.listening, name='!help')
  #await bot.change_presence(activity=activity)
  print(f'{bot.user} has connected to Discord!')

@bot.command(name='test', description='Replies if bot is up and running.')
async def test(ctx):
  await ctx.send('I\'m working!')

@bot.command(name='setup', description='Setup new 10-mans session.')
async def setup(ctx):
  await ctx.send('Initializing setup!')

@bot.command(name='ping', description='Displays ping time of bot.')
async def ping(ctx):
  await ctx.send(f'Ping = {round(bot.latency * 1000)}ms')

#@bot.command(name='help', description='Returns all available commands.')
#async def help(ctx):
#    helptext = '```'
#    for command in bot.commands:
#        helptext += f'{command} - {command.description}\n'
#    helptext += '```'
#    await ctx.send(helptext)

@bot.event
async def on_command_error(ctx, error):
  if isinstance(error, commands.errors.CheckFailure):
    await ctx.send(error)

bot.run(TOKEN)
