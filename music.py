from asyncio.queues import Queue
from asyncio import Event
from asyncio import sleep as async_sleep
from discord.ext import commands
from discord.ext import tasks
from discord import FFmpegPCMAudio
from yt_dlp import YoutubeDL
import song

song_queue = Queue()


class music(commands.Cog):
    def __init__(self):
        self.songs = Queue()
        self.next = Event()
        self.channel = None
        self.voice_client = None
        self.is_looped = False

    @tasks.loop(seconds=1)
    async def playersLoop(self):
        if song_queue.empty():
            await async_sleep(60)
            if not self.voice_client.is_playing() and song_queue.empty():
                await self.voice_client.disconnect()
                self.songs = Queue()
                self.playersLoop.stop()
        else:
            if not self.voice_client.is_playing():
                song_to_play = await song_queue.get()
                self.voice_client.play(song_to_play.source)
                await self.channel.send("Playing " + song_to_play.title + ", requested by " + song_to_play.played_by)
            else:
                await async_sleep(1)

    @commands.command()
    async def join(self, ctx):
        if ctx.author.voice is None:
            await ctx.send("Nie jesteś na kanale")
        voice_channel = ctx.author.voice.channel
        self.channel = ctx.channel
        if ctx.voice_client is None:
            await voice_channel.connect()
            self.voice_client = ctx.voice_client
            self.playersLoop.start()
        else:
            await ctx.voice_client.move_to(voice_channel)

    @commands.command()
    async def disconnect(self, ctx):
        await ctx.voice_client.disconnect()

    @commands.command()
    async def play(self, ctx, *, url):
        await self.join(ctx)
        FFMPEG_OPTIONS = {
            'before_options':
            '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
            'options': '-vn'
        }
        YDL_OPTIONS = {
            'format': "bestaudio",
            'default_search': 'auto',
            'noplaylist': True,
            'geo_bypass': True
        }
        vc = ctx.voice_client

        with YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(url, download=False)
            if 'entries' in info:
                url2 = info['entries'][0]['formats'][7]['url']
                title = info['entries'][0]['title']
                await ctx.send(title)
            else:
                url2 = info['formats'][4]['url']
                title = info['title']
            source = FFmpegPCMAudio(url2, **FFMPEG_OPTIONS)
            new_song = song.song(source, title, ctx.author.name)
            if vc.is_playing():
                await song_queue.put(new_song)
            else:
                vc.play(source)

    @commands.command()
    async def p(self, ctx, *, urlx):
        await self.play(ctx, url=urlx)

    @commands.command()
    async def skip(self, ctx):
        vc = ctx.voice_client
        if vc.is_playing():
            vc.stop()

    @commands.command()
    async def fs(self, ctx):
        await self.skip(ctx)

    @commands.command()
    async def loop(self, ctx):
        self.is_looped = not self.is_looped
        print("isLooped is ", self.is_looped)

    async def setup(client):
        await client.add_cog(music())
