
import asyncio
import discord
from discord.ext import commands

bot = commands.Bot(command_prefix='-')

#@bot.command()
#async def ping(ctx):
#    await ctx.send('pong')

@bot.command()
async def play(ctx):
	# grab the user who sent the command
    user = ctx.message.author
    voice_channel = user.voice.voice_channel
    channel = None

    # only play music if user is in a voice channel
    if voice_channel != None:
        play_local_file('clockwork_unmixed.mp3', voice_channel)

async def play_local_file(file_name, voice_channel):
    # create StreamPlayer
        channel = await client.join_voice_channel(voice_channel)
        player = channel.create_ffmpeg_player(file_name)
        player.start()
        while not player.is_done():
            await asyncio.sleep(1)

        # disconnect after the player has finished
        player.stop()
        await channel.disconnect()

bot.run('')

