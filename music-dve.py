from discord.ext import commands

bot = commands.Bot(command_prefix='!')

bot.lava_nodes = [
    {
        'host': 'lava.link',
        'port': 80,
        'rest_url': f'http://lava.link:80',
        'identifier': 'MAIN',
        'password': 'anything',
        'region': 'singapore'
    }
]

@bot.event
async def on_ready():
    print('Bot is online')
    bot.load_extension('dismusic')


bot.run("ODg4MjcyNzMzMjUzODEyMjQ0.YUQScg.V5BBm3wfLafT6hmQN0QWI4Da34Q")