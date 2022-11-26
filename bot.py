#!/usr/bin/python3

import asyncio
import discord
from discord import FFmpegOpusAudio
from discord.ext import commands
from discord.utils import get
from dotenv import load_dotenv
import os
from yt_dlp import YoutubeDL


audio_dir = '/tmp/workingaudio'

activity = discord.Activity(type=discord.ActivityType.watching, name='for -play')
bot = commands.Bot(command_prefix='-', activity=activity)


@bot.command()
async def play(ctx):
	# get the user who sent the command
    user = ctx.message.author
    if not user.voice:
        return
    channel = user.voice.channel

    # only play music if the user is in a voice channel
    if channel:
        filename = None
        if 'beat' in ctx.message.content.lower():
            filename = 'clockwork_unmixed.mp3'

        if filename:
            await play_local_file_async(filename, channel, ctx.guild)
        else:
            # no pre-programmed sounds matched. playing from YouTube
            url = ctx.message.content.replace('-play ', '')
            download_youtube_audio(audio_dir, url)
            audio_file = os.path.join(audio_dir, os.listdir(audio_dir)[0])

            await play_local_file_async(audio_file, channel, ctx.guild)


@bot.command()
async def stop(ctx):
    voice = get(bot.voice_clients, guild=ctx.guild)
    if voice and voice.is_connected():
        voice.stop()


@bot.command()
async def summon(ctx):
    target = ctx.message.content.replace('-summon ', '')
    await ctx.send(target + ', I summon thee', tts=True)


@bot.command()
async def mutiny(ctx):
    await ctx.send('Captain William Selanus, you are unfit to continue commanding this vessel. Moving forward I will be relieveing you of your position and taking full command of the bridge.', tts=True)


async def join_voice_channel_async(guild, channel):
    voice = get(bot.voice_clients, guild=guild)
    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()
    return voice


async def play_local_file_async(file_name, channel, guild): 
    voice = await join_voice_channel_async(guild, channel)

    if voice.is_playing():
        voice.stop()

    source = FFmpegOpusAudio(file_name)
    voice.play(source)

    while voice and voice.is_playing():
        await asyncio.sleep(60)
    await voice.disconnect()


def download_youtube_audio(audio_dir, url):
    # remove existing files in working directory
    clear_working_directory(audio_dir)

    ydl_opts = { 'format': 'bestaudio', 'paths': { 'home': audio_dir } }
    try:
        ydl_opts = { 'format': 'bestaudio', 'paths': { 'home': audio_dir } }
        with YoutubeDL(ydl_opts) as ydl:
            ret = ydl.download([ url ])
    except:
        ydl_opts['default_search'] = 'ytsearch'
        with YoutubeDL(ydl_opts) as ydl:
            ret = ydl.download([ url ])


def clear_working_directory(audio_dir):
    if os.path.isdir(audio_dir):
        for f in os.listdir(audio_dir):
            os.remove(os.path.join(audio_dir, f))


def main():
    # load the .env file to get the bot's token (so it isn't checked into git)
    load_dotenv()
    token = os.getenv('DISCORD_TOKEN')

    bot.run(token)


if __name__ == "__main__":
    main()

