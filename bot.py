
import asyncio
from discord import FFmpegPCMAudio
from discord.ext import commands
from discord.utils import get

bot = commands.Bot(command_prefix='-')


@bot.command()
async def play(ctx):
	# grab the user who sent the command
    user = ctx.message.author
    channel = user.voice.channel

    # only play music if user is in a voice channel
    if channel:
        filename = None
        if 'beat' in ctx.message.content:
            filename = 'clockwork_unmixed.mp3'

        if filename:
            await play_local_file_async(filename, channel, ctx.guild)


@bot.command()
async def stop(ctx):
    voice = get(bot.voice_clients, guild=ctx.guild)
    if voice and voice.is_connected():
        voice.stop()


async def play_local_file_async(file_name, channel, guild): 
    voice = get(bot.voice_clients, guild=guild)
    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()

    source = FFmpegPCMAudio(file_name)
    voice.play(source)


bot.run('')

