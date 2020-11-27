from discord.ext import commands
from discord.utils import get
import discord.member
import discord.mentions

import discord
import asyncio
import os
import re

votea = []
votecreater = ''
votenum = 0

try:
    game = discord.Game("help is ~명령어")
    bot = commands.Bot(command_prefix='~',Status=discord.Status.online,activity=game)

    client = discord.Client()

    msg_nl = "\n"

    def box(msg):
        return "@everyone" + msg_nl + msg

    @bot.event
    async def on_ready():
        print("login...")
        print(bot.user.name)
        print(bot.user.id)
        print("ready!")
        print("----------------")

    @bot.event
    async def on_message(message):
        await bot.process_commands(message)

    @bot.command()
    async def 명령어(ctx):
        await ctx.send(f"""{ctx.author.mention}
~명령어 : 해당 봇의 명령어를 보여 줍니다.

~votecreate <옵션 개수> <투표 이름> <옵션1> <옵션2> .... : 투표를 생성합니다.
~vc <옵션 개수> <투표 이름> <옵션1> <옵션2> .... : 투표를 생성합니다.

~vote <투표 번호> <옵션 번호> : <투표 번호>에 해당하는 생성된 투표에 <옵션 번호>에 투표합니다.
~v <투표 번호> <옵션 번호> : <투표 번호>에 해당하는 생성된 투표에 <옵션 번호>에 투표합니다.

~notice <channel tag> <message> : 해당 <Channel tag>한 곳에 <message>를 공지합니다.
~n <channel tag> <message> : 해당 <Channel tag>한 곳에 <message>를 공지합니다.

~kick <member tag> <reason> : 해당 <member tag>된 사람을 <reason>(이유)이라는 사유로 킥합니다.
~k <member tag> <reason> : 해당 <member tag>된 사람을 <reason>(이유)이라는 사유로 킥합니다.

~ban <member tag> <reason> : 해당 <member tag>된 사람을 <reason>(이유)이라는 사유로 벤합니다.
~b <member tag> <reason> : 해당 <member tag>된 사람을 <reason>(이유)이라는 사유로 벤합니다.""")

    @bot.command(aliases=['n'])
    async def notice(ctx, *args):
        if ctx.author.guild_permissions.manage_messages:
            try:
                output = ''
                channel = ''
                cnt = 1
                for tmp in args:
                    if cnt == 1:
                        channel += str(tmp).replace("<", "").replace(">", "").replace("#", "")
                    else:
                        output += str(tmp)
                        output += " "
                    cnt += 1
                await bot.get_channel(int(str(channel))).send(box(output))
                print("'notice' Command executed successfully.\n" + box(output)+"\n")
            except Exception as e:
                print(e)
                print("An error occurred in executing the 'notice' Command.\n" + box(output)+"\n")
        else:
            await ctx.send(f"{ctx.author.mention}\n이 명령을 사용할 수 있는 권한이 없습니다.")

    @bot.command(aliases=['k'], pass_context=True)
    async def kick(ctx, member: discord.Member, *, reason=None):
        if ctx.author.guild_permissions.kick_members == True:
            try:
                embed = discord.Embed(title=f"{member.name}님 {ctx.guild.name}에서 추방되셨습니다.", color=0xF21C00)
                embed.add_field(name="이름", value=member.mention)
                if reason == None:
                    reason = '없음.'
                embed.add_field(name="사유", value=reason)
                await bot.get_channel(781585624339709962).send(embed=embed)
                await bot.get_channel(672105952681525261).send(embed=embed)
                await bot.get_user(member.id).send(embed=embed)
            except Exception as e:
                print(e)
            await member.kick(reason=reason)
            print("'kick' Command executed successfully.\nMember : " + str(member) + "\nReason : "+ str(reason) +"\nUsing User : "+ str(ctx.message.author)+"\n")
        else:
            embed=discord.Embed(title="에러", description=f"{ctx.message.author.mention}님께서는 유저를 추방시킬 권한이 없습니다. 권한을 추가하신 후 다시 시도해주십시오.", color=0xFFE146)
            await ctx.send(embed=embed)
            await bot.get_channel(781585624339709962).send(embed=embed)
            await bot.get_channel(672105952681525261).send(embed=embed)
            print("An error occurred in executing the 'kick' Command.\nMember : " + str(member) + "\nReason : "+ str(reason) +"\nUsing User : "+ str(ctx.message.author)+"\n")


    @bot.command(aliases=['b'], pass_context=True)
    async def ban(ctx, member: discord.Member, *, reason=None):
        if ctx.author.guild_permissions.ban_members == True:
            try:
                embed = discord.Embed(title=f"{member.name}님 {ctx.guild.name}에서 차단되셨습니다.", color=0xF21C00)
                embed.add_field(name="이름", value=member.mention)
                if reason == None:
                    reason = '없음.'
                embed.add_field(name="사유", value=reason)
                await bot.get_channel(781585624339709962).send(embed=embed)
                await bot.get_channel(672105952681525261).send(embed=embed)
                await bot.get_user(member.id).send(embed=embed)
            except Exception as e:
                print(e)
            await member.ban(reason=reason)
            print("'ban' Command executed successfully.\nMember : " + str(member) + "\nReason : "+ str(reason) +"\nUsing User : "+ str(ctx.message.author)+"\n")
        else:
            embed=discord.Embed(title="에러", description=f"{ctx.message.author.mention}님께서는 유저를 차단시킬 권한이 없습니다. 권한을 추가하신 후 다시 시도해주십시오.", color=0xFFE146)
            await ctx.send(embed=embed)
            await bot.get_channel(781585624339709962).send(embed=embed)
            await bot.get_channel(672105952681525261).send(embed=embed)
            print("An error occurred in executing the 'ban' Command.\nMember : " + str(member) + "\nReason : "+ str(reason) +"\nUsing User : "+ str(ctx.message.author)+"\n")

    @bot.command(aliases=['c'], pass_context=True)
    async def clear(ctx, number:int=None):
        if ctx.guild:
            if ctx.message.author.guild_permissions.manage_messages:
                try:
                    if number == None:
                        await ctx.send('숫자를 입력해주세요.')
                    elif 100<number:
                        await ctx.message.delete()
                        await ctx.send(f"{ctx.message.author.mention} `100`보다 큰 수는 입력할 수 없습니다.", delete_after=5)
                    else:
                        deleted = await ctx.message.channel.purge(limit=number)
                        await ctx.send(f"{ctx.message.author.mention}에 의해 `{len(deleted)}`개의 메세지가 삭제되었습니다.")
                except Exception as e:
                    print(e)
                    await ctx.send("삭제가 불가합니다.")
            else:
                await ctx.send('이 명령을 사용할 수 있는 권한이 없습니다.')
        else:
            await ctx.send('DM에선 불가합니다.')
    @bot.command(aliases=['vc'], pass_context=True)
    async def votecreate(ctx, *args):
        
        if ctx.guild:
            try:
                global votenum
                global vote
                global votecreater
                cnt = 1
                title = ''
                options_num = args[0]
                tmp = int('-'+str(options_num))
                options = []
                for i in args[:tmp]:
                    if cnt == 1:
                        # options_num = int(i)
                        pass
                    else:
                        title += str(i)+' '
                    # else:
                    #     options.append(str(i))
                    cnt += 1
                
                for j in args[cnt-1:]:
                    options.append(str(j))
                cnt = 1
                embed = discord.Embed(title=f"{title}", color=0x00FFFF)
                embed.add_field(name="생성자", value=ctx.author.mention)
                embed.add_field(name="번호", value=str(votenum), inline=True)
                for k in options:
                    embed.add_field(name=f"Option {cnt}", value=k, inline=False)
                    cnt+=1
                await ctx.send(embed=embed)
                votecreater = ctx.author
                tmp = [votenum, title, votecreater]
                
                for k in options:
                    tmp.append([k, 0])
                votea.append(tmp)
                print(votea)
                votenum += 1
            except Exception as e:
                print(e)
        else:
            await ctx.send('DM에선 불가합니다.')

    @bot.command(aliases=['v'], pass_context=True)
    async def vote(ctx, *args):
        if ctx.guild:
            try:
                global votenum
                global votea
                global votecreater
                
                votenum_tmp = votea[int(args[0])]
                if str(args[0]) == str(votenum_tmp[0]):
                    cnt = 1
                    for k in votenum_tmp[3:]:
                        if cnt == int(args[1]):
                            tmp = int(k[1])+1
                            k[1] = tmp
                            embed = discord.Embed(title=F"\"{votenum_tmp[1]}\"에 대한 투표 현황", color=0x00FF00)
                            embed.add_field(name="생성자", value=votenum_tmp[2].mention)
                            embed.add_field(name="번호", value=votenum_tmp[0], inline=True)
                            cnt_ = 1
                            for row in votenum_tmp[3:]:
                                embed.add_field(name=f"Option {cnt_}", value=row[0]+" : "+str(row[1]), inline=False)
                                cnt_ += 1
                        cnt+=1
                else:
                    pass
                await ctx.send(embed=embed)
            except Exception as e:
                print(e)

    token = os.environ["BOT_TOKEN"]
    print("Token_key : ", token)
    bot.run(token)
except Exception as e:
    print(e)
