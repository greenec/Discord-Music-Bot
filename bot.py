
import asyncio
from discord import FFmpegOpusAudio
from discord.ext import commands
from discord.utils import get
from dotenv import load_dotenv
import os


bot = commands.Bot(command_prefix='-')


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


def main():
    # load the .env file to get the bot's token (so it isn't checked into git)
    load_dotenv()
    token = os.getenv('DISCORD_TOKEN')

    bot.run(token)


if __name__ == "__main__":
    main()

