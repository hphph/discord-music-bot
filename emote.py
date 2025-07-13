from redis import Redis

from discord.ext import commands

class emote(commands.Cog):
    def __init__(self):
        self.redis = Redis(host='localhost', port=6379, decode_responses=True)

    @commands.command()
    async def sniper(self, ctx):
        await ctx.send("( -_･) ︻デ═一 ▸")

    @commands.command()
    async def nienawisc(self, ctx):
        await ctx.send("https://cdn.discordapp.com/attachments/801739925015756821/1105869150972289134/Mamm0nska_NIENAWISC_JGO-3SNU8pA.webm")
    
    @commands.command(aliases=["tag"])
    async def t(self, ctx : commands.Context, tag):
        content = self.redis.get(tag)
        if content is not None:
            await ctx.send(content)
            return
        if ctx.message.reference is None:
            await ctx.send("Tag pusty  <:Mikizoltamorda:912046984876146730>")
            return
        if len(ctx.message.reference.resolved.attachments) > 0:
            self.redis.set(tag, ctx.message.reference.resolved.attachments[0].url)
            await ctx.send("Zapisane  <:ZbychEZ:830032318466228296>👌")
        else:
            self.redis.set(tag, ctx.message.reference.resolved.content)
            await ctx.send("Zapisane  <:ZbychEZ:830032318466228296>👌")
    
    @commands.command(aliases=["tagi"])
    async def tags(self, ctx):
        keys = ""
        for key in self.redis.scan_iter("*"):
            keys += key + "\n"
        await ctx.send(keys)

    @commands.command(aliases=["removetag", "trm", "tagremove"])
    async def rmt(self, ctx, tag):
        content = self.redis.get(tag)
        if content is not None:
            self.redis.delete(tag)
            await ctx.send("Usunięte  <:ZbychEZ:830032318466228296>👌")
        else:
            await ctx.send("Tag pusty  <:Mikizoltamorda:912046984876146730>")

    @commands.command()
    async def rasizm(self, ctx):
        rasizm_moments = self.redis.get("rasizm:times")
        rasizm_moments = int(rasizm_moments) + 1
        await ctx.send("Na serwerze wypowiedziano " + str(rasizm_moments) + " razy coś rasistowskiego.")
        self.redis.set("rasizm:times", rasizm_moments)

    async def setup(client):
        await client.add_cog(emote())
