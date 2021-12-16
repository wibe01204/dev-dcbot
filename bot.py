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
import asyncio
import keep_alive

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

##@client.command(pass_context=True, aliases=['l'])
##async def leave(ctx):
    ##channel = ctx.message.author.voice.channel
    #voice = get(client.voice_clients, guild=ctx.guild)

    #if voice and voice.is_connected():
        #await voice.move_to(channel)
    #else:
        #voice = await channel.connect()

    #if voice and voice.is_connected():
        #await voice.move_to(channel)
    #else:
        #voice = await channel.connect()
        #print(f'Miyuki加入到 >> {channel} <<\n')

        #await ctx.sent(f'Miyuki加入到 >> {channel} <<')

    #if voice and voice.is_connected():
        #await voice.disconnect()
        #print(f'Miyuki離開了 >> {channel} <<')
        #await ctx.send(f'Miyuki離開了 >> {channel} <<')
    #else:
        #print('Miyuki離開了')
        #await ctx.send(f'Miyuki離開了頻道')

@client.command()
async def sayd(ctx, *,msg):
    await ctx.message.delete()
    await ctx.send(msg)

@client.command()
async def clean(ctx ,num:int):
    await ctx.channel.purge(limit=num+1)
    await ctx.send(f'❌已刪除{num}則訊息!')

@clean.error
async def clean_error(ctx, error):
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
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason=None):
    await member.ban(reason=reason)
    await ctx.send(f"{member} 因為**{reason}**被封鎖了!")

@ban.error
async def ban(ctx, error):
    await ctx.send("❌錯誤 : 請確認有管理權限或是指令使用是否正確>!aban [成員] [原因]")

@client.command()
@commands.has_permissions(ban_members=True)
async def unban(ctx, *, member):
    bannedUsers = await ctx.guild.bans()
    name, discriminator = member.split("#")

    for ban in bannedUsers:
        user = ban.user

        if(user.name, user.discriminator) == (name, discriminator):
            await ctx.guild.unban(user)
            await ctx.send(f"{user.mention} 被伺服器解封!")
            return

@unban.error
async def unban(ctx, error):
    await ctx.send("❌錯誤 : 請確認有管理權限或是指令使用是否正確>!aunban [成員]")

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
    embed.add_field(name='!aooxx', value='玩OOXX', inline=True)
    embed.add_field(name='!aplace', value='OOXX放置',inline=True)
    embed.add_field(name='!apick', value='三選一', inline=True)
    embed.add_field(name='!aclear', value='清除訊息', inline=True)
    embed.add_field(name='!auserinfo', value='群內成員資訊', inline=True)
    embed.add_field(name='!ah', value='指令列表', inline=True)
    embed.add_field(name='管理員指令🔻',value='(部分指令需有權限才可使用)',inline= False)
    embed.add_field(name='!aban', value='封鎖用戶', inline=True)
    embed.add_field(name='!aunban', value='解封用戶', inline=True)
    embed.add_field(name='!aaddrole', value='新增身分組', inline=True)
    embed.add_field(name='!aremoverole', value='移除身分組', inline=True)
    embed.add_field(name='!akick', value='踢出成員', inline=True)
    embed.add_field(name='!amute' ,value='將成員靜音' ,inline=True)
    embed.add_field(name='!aunmute' ,value='將成員解除靜音' ,inline=True)

    await ctx.send(embed=embed)

@client.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason=None):
    await member.kick(reason=reason)
    await ctx.send(f"{member} 因為 {reason}被踢出伺服器!")

@client.command(description="Mutes the specified user.")
@commands.has_permissions(manage_messages=True)
async def mute(ctx, member: discord.Member, *, reason=None):
    guild = ctx.guild
    mutedRole = discord.utils.get(guild.roles, name="Muted")

    if not mutedRole:
        mutedRole = await guild.create_role(name="Muted")

        for channel in guild.channels:
            await channel.set_permissions(mutedRole, speak=False, send_messages=False, read_message_history=True, read_messages=False)

    await member.add_roles(mutedRole, reason=reason)
    await ctx.send(f"**{member}** 因為 **{reason}** 被伺服器管理員靜音!")
    await member.send(f"你已被 **{guild.name}**靜音! 原因: **{reason}**")

@client.command(description="Unmutes a specified user.")
@commands.has_permissions(manage_messages=True)
async def unmute(ctx, member: discord.Member):
    mutedRole = discord.utils.get(ctx.guild.roles, name="Muted")

    await member.remove_roles(mutedRole)
    await ctx.send(f"伺服器管理員已解除 **{member}** 的靜音!")
    await member.send(f"**{ctx.guild.name}** 已解除你的靜音!")

keep_alive.keep_alive()

client.run('')
