import discord
import random
from discord import message
from discord import voice_client
from discord import channel
from discord.ext import commands
from discord.ext.commands import bot
from discord.utils import get

client = commands.Bot(command_prefix='!a')

@client.event
async def on_ready():
    print('機器人已上線')

@client.command()
async def ping(ctx):
    await ctx.send(f'延遲 : {round(client.latency * 1000)}ms')

@client.command(aliases=['choose'])
async def _8ball(ctx, *, question):
    responses = ['要','不要']
    await ctx.send(f'問題: {question}\n回答: {random.choice(responses)}')

@client.command()
async def clear(ctx, amount=6):
    await ctx.channel.purge(limit=amount)
    await ctx.send(f'已移除5則訊息!!')

@client.command()
async def rn(ctx):
    await ctx.send(f'0~100中我選擇的隨機號碼為: {random.randint(0,100)}')

@client.command(pass_context=True, aliases=['j'])
async def join(ctx):
    global voice
    channel = ctx.message.author.voice.channel
    voice = get(client.voice_clients, guild=ctx.guild)

    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()

    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()
        print(f'Miyuki加入到 >> {channel} <<\n')

    await ctx.sent(f'Miyuki加入到 >> {channel} <<')

@client.command(pass_context=True, aliases=['l'])
async def leave(ctx):
    channel = ctx.message.author.voice.channel
    voice = get(client.voice_clients, guild=ctx.guild)

    if voice and voice.is_connected():
        await voice.disconnect()
        print(f'Miyuki離開了 >> {channel} <<')
        await ctx.send(f'Miyuki離開了 >> {channel} <<')
    else:
        print('Miyuki離開了')
        await ctx.send(f'Miyuki離開了頻道')


client.run('ODg4MjUxMDc3MDI2MjY3MTc2.YUP-Rw.2X53VO2HtucTgPf-1nOw4JnavU0')