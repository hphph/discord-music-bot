import discord


class song():
    def __init__(self, source: discord.FFmpegPCMAudio, title: str, played_by: str):
        self.source = source
        self.title = title
        self.played_by = played_by

    
