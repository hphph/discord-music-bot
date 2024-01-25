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
        self.retry_queue = 0

    @tasks.loop(seconds=1)
    async def playersLoop(self):
        if song_queue.empty():
            self.retry_queue += 1
            if not self.voice_client.is_playing() and song_queue.empty() and self.retry_queue > 60:
                await self.voice_client.disconnect()
                self.retry_queue = 0
                self.songs = Queue()
                self.playersLoop.stop()
        else:
            self.retry_queue = 0
            if not self.voice_client.is_playing():
                song_to_play = await song_queue.get()
                try:
                    self.voice_client.play(song_to_play.source)
                except Exception as e:
                    await self.channel.send(type(e))
                    await self.channel.send(e.args)
                    await self.channel.send(e)
                    return
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
                formats = info['entries'][0]['formats'] 
            else:
                formats = info['formats']

            best_format = None
            for f in formats:
                if f['format_id'] == '251':
                    best_format = f
                    break
                elif f['resolution'] == 'audio only':
                    best_format = f

            if best_format is None:
                    best_format = formats[0]

            url2 = best_format['url']
            title = info['title']
            await ctx.send(title)
            try:
                source = FFmpegPCMAudio(url2, **FFMPEG_OPTIONS)
                await ctx.send(url2)
            except:
                await ctx.send("FFMPEG error")
                return
            new_song = song.song(source, title, ctx.author.name)
            await song_queue.put(new_song)

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
