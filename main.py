import discord
from os import getenv
from dotenv import load_dotenv
from music import music
from emote import emote
import asyncio
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True

client = commands.Bot(command_prefix='!', intents=intents)

@client.event
async def on_ready():
    await music.setup(client)
    await emote.setup(client)

load_dotenv()
discord_token = getenv('DISCORD_TOKEN')
client.run(discord_token)
