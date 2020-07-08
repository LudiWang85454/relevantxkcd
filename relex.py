import asyncio
import os
import random

import aiohttp
from discord import Game
from discord.ext import commands
from dotenv import load_dotenv

from newest_xkcd import latest_comic_num
from search import search

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

URL = 'https://xkcd.com/'

bot = commands.Bot(command_prefix='!')

@bot.event
async def on_connect():
    print(f'Bot connected as {bot.user}')
    # Setting `Playing ` status
    await bot.change_presence(activity=Game(name='Grand Theft Auto: Emily Dickinson Edition'))
    try:
        if bot.SESSION.closed:
            bot.SESSION = aiohttp.ClientSession()
    except AttributeError:
        bot.SESSION = aiohttp.ClientSession()


@bot.event
async def on_disconnect():
    await bot.SESSION.close()


@bot.command(name='number', pass_context=True, description='Get comic by number',aliases=['n'])
async def number(ctx, num: int):
    await ctx.send(ctx.message.author.mention + f' {URL}{num}/')


@number.error
async def number_error(ctx, error):
    if isinstance(error, commands.BadArgument):
        message_contents = ctx.message.content.split()
        await ctx.send(ctx.message.author.mention + f' Error: could not parse "{"".join(message_contents[1:])}"')


@bot.command(name='random_comic', pass_context=True, description='Get random comic', aliases=['random', 'rand', 'r'])
async def random_comic(ctx):
    newest_comic = await latest_comic_num(bot.SESSION)
    comic_num = random.randint(1, newest_comic)
    await ctx.send(ctx.message.author.mention + f' {URL}{comic_num}/')


@bot.command(name='search_phrase', pass_context=True, discription='Search by a word/phrase',
             aliases=['search', 's', 'find', 'f'])
async def search_phrase(ctx):
    split_phrase = ctx.message.content.split()
    # Remove command from message
    if len(split_phrase) > 1:
        phrase = ' '.join(split_phrase[1:])
    else:
        ctx.send(ctx.message.author.mention + ' Error: no phrase provided')
        return
    await ctx.send(ctx.message.author.mention + f' searching for the xkcd most relevant to the phrase \"{phrase}\".')
    loop = asyncio.get_running_loop()
    # `googlesearch` does not support async, so use executor to avoid blocking everything
    result = await loop.run_in_executor(None, search, phrase)
    await ctx.send(ctx.message.author.mention + ' ' + result)


@bot.command(name='newest', pass_context=True, description='Get newest comic',aliases=['latest', 'relex'])
async def newest(ctx):
    newest_comic = await latest_comic_num(bot.SESSION)
    await ctx.send(ctx.message.author.mention + f' The most recent xkcd is: {URL}{newest_comic}')


bot.run(TOKEN)
