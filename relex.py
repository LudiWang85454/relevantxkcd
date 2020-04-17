import asyncio
import concurrent.futures
import functools
import os
import random

import aiohttp
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
    try:
        if bot.SESSION.closed:
            bot.SESSION = aiohttp.ClientSession()
    except AttributeError:
        bot.SESSION = aiohttp.ClientSession()


@bot.event
async def on_disconnect():
    await bot.SESSION.close()


@bot.command(name='number', pass_context=True)
async def number(ctx, number):
    await ctx.send(f'{URL}{number}/')


@bot.command(name='random_comic', pass_context=True)
async def random_comic(ctx):
    newest_comic = await latest_comic_num(bot.SESSION)
    comic_num = random.randint(1, newest_comic)
    await ctx.send(f'{URL}{comic_num}/')


@bot.command(name='search_phrase', pass_context=True, aliases=['search'])
async def search_phrase(ctx, phrase):
    await ctx.send(f'Now searching for the xkcd most relevant to the phrase \"{phrase}\".')
    loop = asyncio.get_running_loop()
    result = await loop.run_in_executor(None, search, phrase)
    await ctx.send(result)


@bot.command(name='newest', pass_context=True)
async def newest(ctx):
    newest_comic = await latest_comic_num(bot.SESSION)
    await ctx.send(f'The most recent xkcd is: {URL}{newest_comic}')


bot.run(TOKEN)
