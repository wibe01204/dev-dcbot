import discord
from discord import channel
from discord.ext import commands
from discord.utils import get
import youtube_dl
import os

TOKEN = 'ODg4MjcyNzMzMjUzODEyMjQ0.YUQScg.V5BBm3wfLafT6hmQN0QWI4Da34Q'
BOT_PREFIX = '!'

bot = commands.Bot(command_prefix=BOT_PREFIX)

@bot.event
async def on_ready():
    print('機器人已上線: ' + bot.user.name + '\n')

@bot.command(pass_context=True, aliases=['j'])
async def join(ctx):
    global voice
    channel = ctx.message.author.voice.channel
    voice = get(bot.voice_clients, guild=ctx.guild)

    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()

    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()
        print(f'Miyuki加入到 >> {channel} <<\n')

    await ctx.send(f'Miyuki加入到 >> {channel} <<')


@bot.command(pass_context=True, aliases=['l'])
async def leave(ctx):
    channel = ctx.message.author.voice.channel
    voice = get(bot.voice_clients, guild=ctx.guild)

    if voice and voice.is_connected():
        await voice.disconnect()
        print(f'Miyuki離開了 >> {channel} <<')
        await ctx.send(f'Miyuki離開了 >> {channel} <<')
    else:
        print('Miyuki離開了')
        await ctx.send(f'Miyuki離開了頻道')

@bot.command(pass_context=True, aliases=['p'])
async def play(ctx, url: str):
    song_there = os.path.isfile("song.mp3")
    try:
        if song_there:
            os.remove("song.mp3")
            print("Remove old song file")
    except PermissionError:
        print("Trying to delete song fils, but it's bing played")
        await ctx.send("錯誤:音樂正在撥放")
        return
    await ctx.send(f"歌曲正在播放")

    voice = get(bot.voice_clients, guild=ctx.guild)

    ydl_opts = {
        'format':'bestaudio/beat',
        'postproprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '320',
        }],
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        print("Downloading audio now\n")
    ydl.download([url])

    for file in os.listdir("./"):
         if file.endswith(".mp3"):
            name = file
            print(f"Renamed File: {file}\n")
            os.rename(file, "song.mp3")

    voice.play(discord.FFmpegPCMAudio("song.mp3"), after=lambda e: print(f"{name} has finished playing"))
    voice.source = discord.PCMVolumeTransformer(voice.source)
    voice.source.volume = 0.07

    nname = name.rsplit()
    await ctx.send(f"正在播放: {nname}")
    print('playing\n')


bot.run(TOKEN)
