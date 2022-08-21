import asyncio
import discord
from discord.ext import commands, tasks
import os
import DiscordUtils
import random
import datetime


token = "bot-token here"
intents = discord.Intents.default().all()
prefix = "-"
bot = commands.AutoShardedBot(command_prefix=prefix, intents=intents)
music = DiscordUtils.Music()


bot.remove_command("help")


#-------------------------------------------------------------------------------------------
#// Events


@bot.event
async def on_ready():
    print(f"{bot.user.name} is ready.")
    bot.my_current_task = live_status.start()





@tasks.loop()
async def live_status(seconds=75):

    activity = discord.Activity(type=discord.ActivityType.watching, name=f' 🎙  Rhyme')
    await bot.change_presence(activity=activity)
    await asyncio.sleep(10)



    activity = discord.Activity(type=discord.ActivityType.playing, name=f'Rhyme | {prefix}help')
    await bot.change_presence(activity=activity)
    await asyncio.sleep(10)

    activity = discord.Activity(type=discord.ActivityType.watching, name=f'Made with ❤')
    await bot.change_presence(activity=activity)
    await asyncio.sleep(10)

    activity = discord.Activity(type=discord.ActivityType.playing, name=f'🎶🎵')
    await bot.change_presence(activity=activity)
    await asyncio.sleep(10)


#-------------------------------------------------------------------------------------------
#// Music Commands


@bot.command(aliases=["j"])
async def join(ctx):
    if ctx.author.voice is None:
        return await ctx.send("You are not connected to a voice channel, Please Connect to the Channel you want me to join.")

    if ctx.voice_client is not None:
        await ctx.voice_client.disconnect()

    await ctx.author.voice.channel.connect()


@bot.command(aliases=["l"])
async def leave(ctx):
    if ctx.voice_client is not None:
        return await ctx.voice_client.disconnect()

    await ctx.send("I have left the voice channel.")


@bot.command(aliases=["p"])
async def play(ctx, *, url):
    player = music.get_player(guild_id=ctx.guild.id)
    if not player:
        player = music.create_player(ctx, ffmpeg_error_betterfix=True)
        #await ctx.send("Cannot play Song because I am not in the Voice Channel.")
    if not ctx.voice_client.is_playing():
        await player.queue(url, search=True)
        song = await player.play()
        await ctx.send(f"Playing `{song.name}`.")
    else:
        song = await player.queue(url, search=True)
        await ctx.send(f"Added `{song.name}` to the Queue.")


@bot.command(aliases=["q"])
async def queue(ctx):
    player = music.get_player(guild_id=ctx.guild.id)
    newline = '\n'
    await ctx.send(f"{f'{newline}'. join([song.name for song in player.current_queue()])}\n")


@bot.command(aliases=["i"])
async def pause(ctx):
    player = music.get_player(guild_id=ctx.guild.id)
    song = await player.pause()
    await ctx.send(f"Paused `{song.name}`.")


@bot.command(aliases=["r"])
async def resume(ctx):
    player = music.get_player(guild_id=ctx.guild.id)
    song = await player.resume()
    await ctx.send(f"Unpaused `{song.name}`.")
    


@bot.command(aliases=["m"])
async def loop(ctx):
    player = music.get_player(guild_id=ctx.guild.id)
    song = await player.toggle_song_loop()
    if song.is_looping:
        return await ctx.send(f"`{song.name}` is Looping.")
    else:
        return await ctx.send(f"`{song.name}` has Stopped Looping.")


@bot.command(aliases=["s"])
async def song(ctx):
    player = music.get_player(guild_id=ctx.guild.id)
    song = player.now_playing()
    await ctx.send(f"Now Playing `{song.name}`.")


@bot.command(aliases=["k"])
async def remove(ctx, index):
    player = music.get_player(guild_id=ctx.guild.id)
    song = await player.remove_from_queue(int(index))
    await ctx.send(f"Removed `{song.name}` from Queue.")


@bot.command(aliases=["v"])
async def skip(ctx):
    player = music.get_player(guild_id=ctx.guild.id)
    data = await player.skip(force=True)
    if len(data) == 2:
        await ctx.send(f"Skipped from `{data[0].name}` to `{data[1].name}`.")
    else:
        await ctx.send(f"Skipped `{data[0].name}`.")


@bot.command(aliases=["c"])
async def stop(ctx):
    player = music.get_player(guild_id=ctx.guild.id)
    await player.stop()
    await ctx.send("Stopped Current Song.")


@bot.command(aliases=["g"])
async def volume(ctx, vol):
    player = music.get_player(guild_id=ctx.guild.id)
    song, volume = await player.change_volume(float(vol) / 100) # volume should be a float between 0 to 1
    await ctx.send(f"Changed volume for `{song.name}` to {volume*100}%")

#-------------------------------------------------------------------------------------------
#// Help Command


@bot.command(aliases=["h"])
async def help(ctx):  
    embed2 = discord.Embed(color=0xfff700).add_field(name=f"\nPlay Command", value="\nPlays the song⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀ ⠀⠀⠀⠀⠀⠀⠀\n\n```Usage:\n-play <song>\n-p <song> ```", inline=False).set_footer(text=f'Rhyme | Made with ❤')
    embed3 = discord.Embed(color=0xfff700).add_field(name=f"\nQueue Command", value="\nShows the Songs in the Queue⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n\n```Usage:\n-queue\n-q ```", inline=False).set_footer(text=f'Rhyme | Made with ❤')
    embed4 = discord.Embed(color=0xfff700).add_field(name=f"\nPause Command", value="\nPauses the Current Song⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n\n```Usage:\n-pause\n-i ```", inline=False).set_footer(text=f'Rhyme | Made with ❤')
    embed5 = discord.Embed(color=0xfff700).add_field(name=f"\nResume Command", value="\nResumes the Current Song⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n\n```Usage:\n-resume\n-r ```", inline=False).set_footer(text=f'Rhyme | Made with ❤')
    embed6 = discord.Embed(color=0xfff700).add_field(name=f"\nJoin Command", value="\nMakes the Bot join the Voice channel⠀⠀⠀⠀⠀⠀⠀⠀\n\n```Usage:\n-join\n-j ```", inline=False).set_footer(text=f'Rhyme | Made with ❤')
    embed7 = discord.Embed(color=0xfff700).add_field(name=f"\nLeave Command", value="\nMakes the Bot Leave the Voice Channel⠀⠀⠀⠀⠀⠀\n\n```Usage:\n-leave\n-l ```", inline=False).set_footer(text=f'Rhyme | Made with ❤')
    embed8 = discord.Embed(color=0xfff700).add_field(name=f"\nLoop Command", value="\nLoops the Current Song⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n\n```Usage:\n-loop\n-m ```", inline=False).set_footer(text=f'Rhyme | Made with ❤')
    embed9 = discord.Embed(color=0xfff700).add_field(name=f"\nSong Command", value="\nTells you What Song is Playing Now⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n\n```Usage:\n-song\n-s ```", inline=False).set_footer(text=f'Rhyme | Made with ❤')
    embed10 = discord.Embed(color=0xfff700).add_field(name=f"\nRemove Command", value="\nRemoves Song of Choice from the Queue⠀⠀⠀⠀⠀\n\n```Usage:\n-remove\n-k ```", inline=False).set_footer(text=f'Rhyme | Made with ❤')
    embed11 = discord.Embed(color=0xfff700).add_field(name=f"\nSkip Command", value="\nSkips the Current Song⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n\n```Usage:\n-skip\n-v ```", inline=False).set_footer(text=f'Rhyme | Made with ❤')
    embed12 = discord.Embed(color=0xfff700).add_field(name=f"\nStop Command", value="\nStops the Current Song⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n\n```Usage:\n-stop\n-c ```", inline=False).set_footer(text=f'Rhyme | Made with ❤')
    embed13 = discord.Embed(color=0xfff700).add_field(name=f"\nVolume Command", value="\nChanges the Volume⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n\n```Usage:\n-volume <1-100>\n-g <1-100> ```", inline=False).set_footer(text=f'Rhyme | Made with ❤')
    paginator = DiscordUtils.Pagination.AutoEmbedPaginator(ctx)
    embeds = [embed2, embed3, embed4, embed5, embed6, embed7, embed8, embed9,embed10, embed11, embed12, embed13]
    await paginator.run(embeds)



bot.run(token, bot=True, reconnect=True)
