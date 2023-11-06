from discord import FFmpegPCMAudio


class song():
    def __init__(self, source: FFmpegPCMAudio, title: str, played_by: str):
        self.source = source
        self.title = title
        self.played_by = played_by

    
