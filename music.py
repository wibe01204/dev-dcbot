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

    await voice.disconnect()

    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()
        print(f'Miyuki加入到 {channel}\n')

    await ctx.send(f'Miyuki加入到 {channel}')


@bot.command(pass_context=True, aliases=['l'])
async def leave(ctx):
    channel = ctx.message.author.voice.channel
    voice = get(bot.voice_clients, guild=ctx.guild)

    if voice and voice.is_connected():
        await voice.disconnect()
        print(f'Miyuki離開了 {channel}')
        await ctx.send(f'Miyuki離開了 {channel}')
    else:
        print('Miyuki離開了頻道')
        await ctx.send('Miyuki離開了頻道')






bot.run(TOKEN)
