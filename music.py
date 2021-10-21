import discord 
from discord.ext import commands 
import os
import nacl
import music
import youtube_dl


#client = commands.Bot(command_prefix = '!')


#TOKEN = 'ODM4OTgwNzE5MzcyMDA5NDgy.YJC_rw.8sTGnOib-Dlrs99s96s7vOSrU9E'


'''
@client.event
async def on_ready(): 
    print('Music bot online')



@client.command()
async def play(ctx, url: str):
    song = os.path.isfile("song.mp3")
    try:
        if song:
            os.remove("song.mp3")
    except PermissionError:
        await ctx.send("Pls wait til current song ends or use 'stop' command")
        return

    voiceChannel = discord.utils.get(ctx.guild.voice_channels, name = "General")
    await voiceChannel.connect()
    voice = discord.utils.get(client.voice_clients, guild = ctx.guild)

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'prefferedquality': '192',

        }]
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    for file in os.listdir("./"):
        if file.endswith(".mp3"):
            os.rename(file, "song.mp3")
    
    voice.play(discord.FFmpegPCMAudio("song.mp3"))


@client.command()
async def pause(ctx):
    voice = discord.utils.get(client.voice_clients, guild = ctx.guild)
    if voice.is_playing():
        voice.pause();

@client.command()
async def resume(ctx):
    voice = discord.utils.get(client.voice_clients, guild = ctx.guild)
    if voice.is_paused():
        voice.resume()

@client.command()
async def stop(ctx):
    voice = discord.utils.get(client.voice_clients, guild = ctx.guild)
    voice.stop()


@client.command()
async def leave(ctx):
    await ctx.voice_client.disconnect()



#client.run(TOKEN)
'''

class bot(commands.Cog):
    def __init__(self, client):
        self.client = client;

    @commands.command()
    async def join(self, ctx):
        if ctx.author.voice is None:
            await ctx.send("Not in vc")
        voice_channel = ctx.author.voice.channel

        if ctx.voice_client is None:
            await voice_channel.connect()
        else: 
            ctx.voice_client.move_to(voice_channel)

    @commands.command()
    async def disconnect(self, ctx):
        await ctx.voice_client.disconnect()

    @commands.command()
    async def play(self, ctx, url):
        ctx.voice_client.stop()
        FFMPEG_OPTIONS = {
            'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'
        }

        YDL_Options = {'format': 'bestaudio'}

        vc = ctx.voice_client

        with youtube_dl.YoutubeDL(YDL_Options) as ydl:
            info = ydl.extract_info(url, download = False)
            url2 = info['format'][0][url]
            source = await discord.FFmpegOpusAudio.from_probe(url2, **FFMPEG_OPTIONS)
            vc.play(source)

    @commands.command()
    async def pause(self, ctx):
        await ctx.voice_client.pause()
        await ctx.send("paused")

    @commands.command()
    async def resume(self, ctx):
        await ctx.voice_client.resume()
        await ctx.send("resumed")

    @commands.command()
    async def stop(self, ctx):
        await ctx.voice_client.stop()
        await ctx.send("stopped")

def setup(client):
    client.add_cog(music(client))