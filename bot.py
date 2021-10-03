from contextlib import ContextDecorator, contextmanager
from logging import Manager, error
from re import T, U
from typing import ContextManager
import discord
import random
from discord import message
from discord import voice_client
from discord import channel
from discord import guild
from discord.errors import ClientException
from discord.ext import commands
from discord.ext.commands import bot
from discord.user import User
from discord.utils import get, time_snowflake
from discord.ext.commands import has_permissions, MissingPermissions

client = commands.Bot(command_prefix='!a')

@client.event
async def on_ready():
    print('BOT已上線')

@client.command()
async def ping(ctx):
    await ctx.send(f'總系統平均延遲 : {round(client.latency * 1000)}ms')

@client.command(aliases=['choose'])
async def _8ball(ctx, *, question):
    responses = ['要','不要','不知道','我無法回答']
    await ctx.send(f'問題: {question}\n回答: {random.choice(responses)}')

@client.command(aliases=['pick'])
async def string(ctx, msg1, msg2, msg3):
    選擇 = [msg1, msg2, msg3]
    await ctx.send(f'🤔我選這個好了>>{random.choice(選擇)}')

@string.error
async def string_error(ctx, error):
    await ctx.send(f'❌錯誤，請確認指令為:!apick <1> <2> <3>。')

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
        await voice.move_to(channel)
    else:
        voice = await channel.connect()

    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()
        print(f'Miyuki加入到 >> {channel} <<\n')

        await ctx.sent(f'Miyuki加入到 >> {channel} <<')

    if voice and voice.is_connected():
        await voice.disconnect()
        print(f'Miyuki離開了 >> {channel} <<')
        await ctx.send(f'Miyuki離開了 >> {channel} <<')
    else:
        print('Miyuki離開了')
        await ctx.send(f'Miyuki離開了頻道')

@client.command()
async def sayd(ctx, *,msg):
    await ctx.message.delete()
    await ctx.send(msg)

@client.command()
async def clear(ctx ,num:int):
    await ctx.channel.purge(limit=num+1)
    await ctx.send(f'❌已刪除{num}則訊息!')

@clear.error
async def clear_error(ctx, error):
    await ctx.send(f'❌錯誤，請確認指令為:!aclear <要清除的行數>。')  

@client.command()
async def addrole(ctx, role: discord.Role, user: discord.Member):
    if ctx.author.guild_permissions.administrator:
        await user.add_roles(role)
        await ctx.send(f"✅已將 {user.mention} 新增 {role.mention} 身分組!")

@addrole.error
async def addrole_error(ctx, error):
    await ctx.send("❌錯誤:請確認有管理權限或是指令使用是否正確>!aaddrole [身分組] [成員]")

@client.command()
async def removerole(ctx, role: discord.Role, user: discord.Member):
    if ctx.author.guild_permissions.administrator:
        await user.remove_roles(role)
        await ctx.send(f"✅成功將 {user.mention} 從 {role.mention} 身分組中移除!")

@removerole.error
async def removerole_error(ctx, error):
    await ctx.send("❌錯誤 : 請確認有管理權限或是指令使用是否正確>!aremoverole [身分組] [成員]")

@client.command()
async def ban(ctx, user: discord.User, reason, GM):
    guild = ctx.guild
    原因 = reason
    mbed = discord.Embed(
        title = '<BAN🪓>',
        description = f"名稱 : {user} ({user.id})\n 原因 : <{原因}>\n 處理人員 : {GM} "
    )
    if ctx.author.guild_permissions.ban_members:
        await ctx.message.delete()
        await ctx.send(embed=mbed)
        await guild.ban(user=user)

@ban.error
async def ban(ctx, error):
    await ctx.send("❌錯誤 : 請確認有管理權限或是指令使用是否正確>!aban [成員] [原因] [處理人員]")

@client.command()
async def unban(ctx, user: discord.User, reason, GM):
    guild = ctx.guild
    原因 = reason
    mbed = discord.Embed(
        title = '<UNBAN🔁>',
        description = f"名稱 : {user} ({user.id})\n 原因 : <{原因}>\n 處理人員 : {GM} "
    )
    if ctx.author.guild_permissions.ban_members:
        await ctx.message.delete()
        await ctx.send(embed=mbed)
        await guild.unban(user=user)

@unban.error
async def unban(ctx, error):
    await ctx.send("❌錯誤 : 請確認有管理權限或是指令使用是否正確>!aunban [成員] [原因] [處理人員]")

client.run('ODg4MjUxMDc3MDI2MjY3MTc2.YUP-Rw.2X53VO2HtucTgPf-1nOw4JnavU0')