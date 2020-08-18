#Hyliter bot
#do not copy my code
#if u do ur gay

import discord
from discord.ext import commands
import os
from time import sleep
import youtube_dl
from discord.utils import get

TOKEN = 'NzQ0MzQ0ODE5MzYyNjkzMTUx.Xzh3Ig.FNAHmURAhEZoZ8B-pTMXPkkbrMU'


time_convert = {"s": 1, "m": 60, "h": 3600, "d": 86400}

players = {}

def ctts(t):
    try:
        return int(t[:-1]) * time_convert[t[-1]]
    except:
        return t


client = commands.Bot(command_prefix = '!h ')



@client.command(pass_context=True, aliases=['j', 'joi'])
async def join(ctx):
    channel = ctx.message.author.voice.channel
    voice = get(client.voice_clients, guild=ctx.guild)

    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()

    await voice.disconnect()

    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()
        print(f"The bot has connected to {channel}\n")

    await ctx.send(f"Joined {channel}")


@client.command(pass_context=True, aliases=['l', 'lea'])
async def leave(ctx):
    channel = ctx.message.author.voice.channel
    voice = get(client.voice_clients, guild=ctx.guild)

    if voice and voice.is_connected():
        await voice.disconnect()
        print(f"The bot has left {channel}")
        await ctx.send(f"Left {channel}")
    else:
        print("Bot was told to leave voice channel, but was not in one")
        await ctx.send("Don't think I am in a voice channel")


@client.command(pass_context=True, aliases=['p', 'pla'])
async def play(ctx, url: str):

    song_there = os.path.isfile("song.mp3")
    try:
        if song_there:
            os.remove("song.mp3")
            print("Removed old song file")
    except PermissionError:
        print("Trying to delete song file, but it's being played")
        await ctx.send("ERROR: Music playing")
        return

    await ctx.send("Getting everything ready now")

    voice = get(client.voice_clients, guild=ctx.guild)

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        print("Downloading audio now\n")
        ydl.download([url])

    for file in os.listdir("./"):
        if file.endswith(".mp3"):
            name = file
            print(f"Renamed File: {file}\n")
            os.rename(file, "song.mp3")

    voice.play(discord.FFmpegPCMAudio("song.mp3"), after=lambda e: print("Song done!"))
    voice.source = discord.PCMVolumeTransformer(voice.source)
    voice.source.volume = 0.07

    nname = name.rsplit("-", 2)
    await ctx.send(f"Playing: {nname[0]}")
    print("playing\n")


kicknoerror = False
@client.command()
@commands.has_permissions(administrator=True)
async def kick(ctx, member : discord.Member, *, reason=None):
    await member.kick(reason=reason)
    await ctx.send(f"{member.mention} was kicked for {reason}.")
@kick.error
async def kick_error(ctx,error):
    if isinstance(error, discord.ext.commands.errors.CommandInvokeError):
        await ctx.send("I don't have permissions to do that.")
    elif isinstance(error, discord.ext.commands.errors.BadArgument):
        await ctx.send("That person does not exist.")



@client.command()
@commands.has_permissions(administrator=True)
async def ban(ctx, member : discord.Member, *, reason=None):
    await member.ban(reason=reason)
    await ctx.send(f"{member.mention} was banned for {reason}.")
@ban.error
async def ban_error(ctx,error):
    if isinstance(error, discord.ext.commands.errors.CommandInvokeError):
        await ctx.send("I don't have permissions to do that.")
    elif isinstance(error, discord.ext.commands.errors.BadArgument):
        await ctx.send("That person does not exist.")



@client.command()
@commands.has_permissions(administrator=True)
async def mute(ctx, member: discord.Member, *, reason='Treason'):
    role = discord.utils.get(ctx.guild.roles, name="Muted")
    await member.add_roles(role)
    await ctx.send(f"{member.mention} has been muted for {reason}")
@mute.error
async def mute_error(ctx,error):
    if isinstance(error, discord.ext.commands.errors.CommandInvokeError):
        await ctx.send("I don't have permissions to do that.")
    elif isinstance(error, discord.ext.commands.errors.BadArgument):
        await ctx.send("That person does not exist.")



@client.command()
@commands.has_permissions(administrator=True)
async def pmute(ctx,member:discord.Member, *, reason='Ping'):
    role = discord.utils.get(ctx.guild.roles, name="Muted")
    await member.add_roles(role)
    await ctx.send(f"{member.mention} has been muted(10 mins) for ping.")
    sleep(6000)
    role = discord.utils.get(ctx.guild.roles, name="Muted")
    await member.remove_roles(role)
    await ctx.send(f"{member.mention} has been unmuted")
@pmute.error
async def pmute_error(ctx,error):
    if isinstance(error, discord.ext.commands.errors.CommandInvokeError):
        await ctx.send("I don't have permissions to do that.")
    elif isinstance(error, discord.ext.commands.errors.BadArgument):
        await ctx.send("That person does not exist.")



@client.command()
@commands.has_permissions(administrator=True)
async def unmute(ctx, member: discord.Member, *, reason=None):
    role = discord.utils.get(ctx.guild.roles, name="Muted")
    await member.remove_roles(role)
    await ctx.send(f"{member.mention} has been unmuted")
@unmute.error
async def unmute_error(ctx,error):
    if isinstance(error, discord.ext.commands.errors.CommandInvokeError):
        await ctx.send("I don't have permissions to do that.")
    elif isinstance(error, discord.ext.commands.errors.BadArgument):
        await ctx.send("That person does not exist.")



@client.command()
@commands.has_permissions(administrator=True)
async def unban(ctx, *,member):
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split('#')
    
    for ban_entry in banned_users:
        user = ban_entry.user

        if (user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            await ctx.send(f'Unbanned {user.mention}')
            return
@unban.error
async def unban_error(ctx,error):
    if isinstance(error, discord.ext.commands.errors.CommandInvokeError):
        await ctx.send("I don't have permissions to do that.")
    elif isinstance(error, discord.ext.commands.errors.BadArgument):
        await ctx.send("That person does not exist.")

@client.command()
@commands.has_permissions(administrator = True)
async def softban(ctx, member:discord.Member, *, reason=None):
    role = discord.utils.get(ctx.guild.roles, name="SoftBanned")
    await member.add_role(role)
    await ctx.send(f'{user.mention} has been softbanned.')
@softban.error
async def softban_error(ctx,error):
    if isinstance(error, discord.ext.commands.errors.CommandInvokeError):
        await ctx.send("I don't have permissions to do that.")
    elif isinstance(error, discord.ext.commands.errors.BadArgument):
        await ctx.send("That person does not exist.")

@client.command()
@commands.has_permissions(administrator = True)
async def softunban(ctx, member:discord.Member, *, reason=None):
    role = discord.utils.get(ctx.guild.roles, name="SoftBanned")
    await member.remove_role(role)
    await ctx.send(f'{user.mention} has been softunbanned.')
@softban.error
async def softban_error(ctx,error):
    if isinstance(error, discord.ext.commands.errors.CommandInvokeError):
        await ctx.send("I don't have permissions to do that.")
    elif isinstance(error, discord.ext.commands.errors.BadArgument):
        await ctx.send("That person does not exist.")


'''
@client.command()
async def load(ctx, extension):
    client.load_extension(f'cogs.extension')

@client.command()
async def unload(ctx, extension):
    client.unload_extension(f'cogs.extension')
'''


import praw
import random

reddit = praw.Reddit(client_id='744344819362693151',
                     client_secret='ERXMAkQ-tg45ekKFK_r3XW9xo3y5dBAI',
                     user_agent='Mozilla/5.0 (compatible; Discordbot/2.0; +https://discord.com)')

@client.command()
async def meme(ctx):
    memes_submissions = reddit.subreddit('memes').hot()
    post_to_pick = random.randint(1, 10)
    for i in range(0, post_to_pick):
        submission = next(x for x in memes_submissions if not x.stickied)
    
    await ctx.send(submission.url)

@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.online, activity=discord.Game('Hyliting'))
    print('bot is ready')


@client.event
async def on_member_join(ctx,member):
    await ctx.send(f'{member} has joined the Hyliters! Welcome, and we hope you enjoy your stay! We have splashes and giveaways sometimes! Have fun!')


@client.event
async def on_member_remove(ctx,member):
    await ctx.send(f'{member} has left the server. Press F to pay respects.')


@client.command()
async def ping(ctx):
    await ctx.send(f'Your ping is: {round(client.latency * 1000)}ms')


'''
for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')
'''

client.run(TOKEN)


