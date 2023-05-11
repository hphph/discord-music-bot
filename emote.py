import discord
import asyncio
from redis import Redis

from discord.ext import commands
from discord.ext import tasks

class emote(commands.Cog):
    @commands.command()
    async def sniper(self, ctx):
        await ctx.send("( -_･) ︻デ═一 ▸")

    @commands.command()
    async def nienawisc(self, ctx):
        await ctx.send("https://cdn.discordapp.com/attachments/801739925015756821/1105869150972289134/Mamm0nska_NIENAWISC_JGO-3SNU8pA.webm")
    
    @commands.command()
    async def t(self, ctx, tag):
        await ctx.send(ctx.message.reference.resolved.content)

    async def setup(client):
        r = Redis(host='localhost', port=6797, decode_responses=True)
        await client.add_cog(emote())
