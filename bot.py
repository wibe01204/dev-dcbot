import discord
import random
from discord import message
from discord import voice_client
from discord import channel
from discord.ext import commands
from discord.ext.commands import bot

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
async def clear(ctx, amount=10):
    await ctx.channel.purge(limit=amount)
    await ctx.send(f'已移除10則訊息!!')

@client.command()
async def rn(ctx):
    await ctx.send(f'我選擇的隨機號碼為: {random.randint(0,100)}')

client.run('ODg4MjUxMDc3MDI2MjY3MTc2.YUP-Rw.2X53VO2HtucTgPf-1nOw4JnavU0')