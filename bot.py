import discord
import random
from discord.ext import commands

client = commands.Bot(command_prefix='!a')

@client.event
async def on_ready():
    print('Bot is ready')

@client.command()
async def ping(ctx):
    await ctx.send(f'Ping: {round(client.latency * 1000)}ms')

@client.command(aliases=['8ball', ])
async def _8ball(ctx, *, question):
    responses = ['要','不要']
    await ctx.send(f'問題: {question}\n回答: {random.choice(responses)}')

@client.event
async def on_member_join(member):
    print(f'{member} 加入了伺服器')

@client.event
async def on_member_remover(member):
    print(f'{member} 退出了了伺服器')

client.run('ODg4MjcyNzMzMjUzODEyMjQ0.YUQScg.V5BBm3wfLafT6hmQN0QWI4Da34Q')