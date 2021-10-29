from contextlib import ContextDecorator, contextmanager
from logging import Manager, error
from re import L, M, T, U
from typing import ContextManager
import discord
import random
from discord import message
from discord import voice_client
from discord import channel
from discord import guild
from discord import user
from discord import embeds
from discord import colour
from discord import member
from discord.errors import ClientException
from discord.ext import commands
from discord.ext.commands import bot
from discord.user import User
from discord.ext.commands import has_permissions, MissingPermissions
from datetime import datetime, timedelta
from discord.utils import get
datetime.now().timestamp()

client = commands.Bot(command_prefix='!a',help_command=None)
client.remove_command('help')

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
    if ctx.author.guild_permissions.manage_roles:
        await user.add_roles(role)
        await ctx.send(f"✅已將 `{user}` 新增 `{role}` 身分組!")

@addrole.error
async def addrole_error(ctx, error):
    await ctx.send("❌錯誤:請確認有管理權限或是指令使用是否正確>!aaddrole [身分組] [成員]") 

@client.command()
async def removerole(ctx, role: discord.Role, user: discord.Member):
    if ctx.author.guild_permissions.manage_roles:
        await user.remove_roles(role)
        await ctx.send(f"✅成功將 `{user}` 從 `{role}` 身分組中移除!")

@removerole.error
async def removerole_error(ctx, error):
    await ctx.send("❌錯誤 : 請確認有管理權限或是指令使用是否正確>!aremoverole [身分組] [成員]")

@client.command()
async def ban(ctx, user: discord.User, reason):
    guild = ctx.guild
    原因 = reason
    mbed = discord.Embed(
        title = '<BAN🪓>', timestamp=ctx.message.created_at,
        description = f"名稱 : {user} ({user.id})\n 原因 : <{原因}>\n 處理人員 : {ctx.author}"
    )
    if ctx.author.guild_permissions.ban_members:
        await ctx.message.delete()
        await ctx.send(embed=mbed)
        await guild.ban(user=user)

@ban.error
async def ban(ctx, error):
    await ctx.send("❌錯誤 : 請確認有管理權限或是指令使用是否正確>!aban [成員] [原因]")

@client.command()
async def unban(ctx, user: discord.User, reason):
    guild = ctx.guild
    原因 = reason
    mbed = discord.Embed(
        title = '<UNBAN🔁>', timestamp=ctx.message.created_at,
        description = f"名稱 : {user} ({user.id})\n 原因 : <{原因}>\n 處理w人員 : {ctx.author}"
    )
    if ctx.author.guild_permissions.ban_members:
        await ctx.message.delete()
        await ctx.send(embed=mbed)
        await guild.unban(user=user)

@unban.error
async def unban(ctx, error):
    await ctx.send("❌錯誤 : 請確認有管理權限或是指令使用是否正確>!aunban [成員] [原因]")

@client.command()
async def userinfo(ctx, member:discord.Member = None):
    member = ctx.author if not member else member
    roles = [role for role in member.roles]

    embed = discord.Embed(colour=member.colour ,timestamp=ctx.message.created_at)

    embed.set_author(name=f"個人資料 - {member}")
    embed.set_thumbnail(url=member.avatar_url)
    embed.set_footer(text=f"Requested by {ctx.author}",icon_url=ctx.author.avatar_url)

    embed.add_field(name="ID:", value=member.id,inline=False)
    embed.add_field(name="伺服器內名稱:", value=member.display_name,inline=False)

    embed.add_field(name="創建於:", value=member.created_at.strftime("%a, %#d %B %Y, %I:%M %p "),inline=False)
    embed.add_field(name="加入伺服器於:", value=member.joined_at.strftime("%a, %#d %B %Y, %I:%M %p "),inline=False)

    embed.add_field(name=f"身分組 ({len(roles)})", value=" ".join([role.mention for role in roles]),inline=False)
    embed.add_field(name=f"最高身分組:", value=member.top_role.mention,inline=False)

    embed.add_field(name="Bot?", value=member.bot, inline=False)

    await ctx.send(embed=embed)
@userinfo.error
async def userinfo(ctx, error):
    await ctx.send("❌錯誤 : 找不到指定的用戶或指令錯誤!")

@client.command(pass_context=True,aliases=['h'])
async def help(ctx):
    embed = discord.Embed(timestamp=ctx.message.created_at,
        colour = discord.Colour.green()
    )
    embed.set_author(name='一般指令🔻')
    embed.set_footer(text=f"Requested by {ctx.author}",icon_url=ctx.author.avatar_url)
    embed.add_field(name='!aj', value='加入語音頻道', inline=True)
    embed.add_field(name='!al', value='離開語音頻道', inline=True)
    embed.add_field(name='!aooxx', value='玩OOXX', inline=True)
    embed.add_field(name='!apick', value='三選一', inline=True)
    embed.add_field(name='!aclear', value='清除訊息', inline=True)
    embed.add_field(name='!auserinfo', value='群內成員資訊', inline=True)
    embed.add_field(name='!ah', value='指令列表', inline=True)
    embed.add_field(name='管理員指令🔻',value='(部分指令需有權限才可使用)',inline= False)
    embed.add_field(name='!aban', value='封鎖用戶', inline=True)
    embed.add_field(name='!aunban', value='解封用戶', inline=True)
    embed.add_field(name='!aaddrole', value='新增身分組', inline=True)
    embed.add_field(name='!aremoverole', value='移除身分組', inline=True)

    await ctx.send(embed=embed)

client.run('ODg4MjUxMDc3MDI2MjY3MTc2.YUP-Rw.2X53VO2HtucTgPf-1nOw4JnavU0')