import discord
from discord.ext import commands
import random


client = commands.Bot(command_prefix="!a",help_command=None)

player1 = ""
player2 = ""
turn = ""
gameOver = True

board = []

winningConditions = [
    [0, 1, 2],
    [3, 4, 5],
    [6, 7, 8],
    [0, 3, 6],
    [1, 4, 7],
    [2, 5, 8],
    [0, 4, 8],
    [2, 4, 6]
]

@client.command()
async def ooxx(ctx, p1: discord.Member, p2: discord.Member):
    global count
    global player1
    global player2
    global turn
    global gameOver

    if gameOver:
        global board
        board = [":white_large_square:", ":white_large_square:", ":white_large_square:",
                 ":white_large_square:", ":white_large_square:", ":white_large_square:",
                 ":white_large_square:", ":white_large_square:", ":white_large_square:"]
        turn = ""
        gameOver = False
        count = 0

        player1 = p1
        player2 = p2

        # print the board
        line = ""
        for x in range(len(board)):
            if x == 2 or x == 5 or x == 8:
                line += " " + board[x]
                await ctx.send(line)
                line = ""
            else:
                line += " " + board[x]

        # determine who goes first
        num = random.randint(1, 2)
        if num == 1:
            turn = player1
            await ctx.send("由<@" + str(player1.id) + ">先開始!")
        elif num == 2:
            turn = player2
            await ctx.send("由<@" + str(player2.id) + ">先開始!")
    else:
        await ctx.send("一項遊戲進行中，請先結束!")

@client.command()
async def place(ctx, pos: int):
    global turn
    global player1
    global player2
    global board
    global count
    global gameOver

    if not gameOver:
        mark = ""
        if turn == ctx.author:
            if turn == player1:
                mark = ":regional_indicator_x:"
            elif turn == player2:
                mark = ":o2:"
            if 0 < pos < 10 and board[pos - 1] == ":white_large_square:" :
                board[pos - 1] = mark
                count += 1

                # print the board
                line = ""
                for x in range(len(board)):
                    if x == 2 or x == 5 or x == 8:
                        line += " " + board[x]
                        await ctx.send(line)
                        line = ""
                    else:
                        line += " " + board[x]

                checkWinner(winningConditions, mark)
                print(count)
                if gameOver == True:
                    await ctx.send(mark + " 贏了!!")
                elif count >= 9:
                    gameOver = True
                    await ctx.send("平手!")

                # switch turns
                if turn == player1:
                    turn = player2
                elif turn == player2:
                    turn = player1
            else:
                await ctx.send("請選擇 1 到 9（含）之間的整數和未選擇的區塊!")
        else:
            await ctx.send("現在不是你的回合!")
    else:
        await ctx.send("請使用 !aooxx 開始新遊戲!!")


def checkWinner(winningConditions, mark):
    global gameOver
    for condition in winningConditions:
        if board[condition[0]] == mark and board[condition[1]] == mark and board[condition[2]] == mark:
            gameOver = True

@ooxx.error
async def ooxx_error(ctx, error):
    print(error)
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("請標記兩個人來開始遊戲呦!")
    elif isinstance(error, commands.BadArgument):
        await ctx.send("請確定成員有標註成功! (ex. <@888251077026267176>).")

@place.error
async def place_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("請輸入一個有效的整數(1~9)")
    elif isinstance(error, commands.BadArgument):
        await ctx.send("你所選擇的地方有人選了")

@client.command(aliases=['nitro'])
async def string(ctx, p1, p2, p3, p4, p5, p6, p7, p8, p9, p10, p11, p12, p13, p14, p15, P16):
    選擇 = [p1, p2, p3, p4, p5, p6, p7, p8, p9, p10, p11, p12, p13, p14, p15, P16]
    await ctx.send(f'🎉恭喜 **{random.choice(選擇)}** 中獎!!')


client.run("ODg4MjUxMDc3MDI2MjY3MTc2.YUP-Rw.2X53VO2HtucTgPf-1nOw4JnavU0")