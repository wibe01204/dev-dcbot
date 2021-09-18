import discord
from discord.ext import commands

client = commands.Bot(command_prefix='!')

@client.event
async def on_ready():
    print('Bot is ready')

client.run('ODg4MjcyNzMzMjUzODEyMjQ0.YUQScg.V5BBm3wfLafT6hmQN0QWI4Da34Q')