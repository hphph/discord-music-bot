from discord import Intents
from os import getenv
from music import music
from emote import emote
from discord.ext import commands

intents = Intents.default()
intents.message_content = True
intents.voice_states = True
intents.message_content = True

client = commands.Bot(command_prefix='!', intents=intents)

@client.event
async def on_ready():
    await music.setup(client)
    await emote.setup(client)


discord_token = getenv('DISCORD_TOKEN')
client.run(discord_token)
