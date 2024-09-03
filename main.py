import discord
import requests
from discord.ext import commands
import os
import random
from fuzzywuzzy import process
import asyncio
import config

intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
intents.message_content = True
intents.voice_states = True
intents.members = True
intents.presences = True

bot = commands.Bot(command_prefix=config.PREFIX, intents=intents)


@bot.command()
async def join(ctx):
    """Joins the voice channel."""
    channel = ctx.author.voice.channel
    if not ctx.voice_client:
        await channel.connect()


@bot.command()
async def leave(ctx):
    """Leaves the voice channel."""
    if ctx.voice_client:
        await ctx.voice_client.disconnect()


@bot.command()
async def play(ctx, *, playlist_name=None):
    """Plays a playlist or lists available playlists."""
    playlists = os.listdir('mp3s')
    if not playlist_name:
        # List available playlists
        playlists_str = '\n'.join(playlists)
        await ctx.send(f"Available playlists:\n{playlists_str}\nUse '!play PLAYLISTNAME' to play a playlist.")
        return

    closest_match = process.extractOne(playlist_name, playlists)[0]
    playlist_path = os.path.join('mp3s', closest_match)
    songs = [os.path.join(playlist_path, f) for f in os.listdir(playlist_path) if f.endswith('.mp3')]
    random.shuffle(songs)

    voice_channel = ctx.author.voice.channel
    if not ctx.voice_client:
        await voice_channel.connect()

    for song in songs:
        if ctx.voice_client.is_playing():
            ctx.voice_client.stop()
        ctx.voice_client.play(discord.FFmpegPCMAudio(song))
        await ctx.send(f"Now playing: {os.path.basename(song)}")
        while ctx.voice_client.is_playing():
            await asyncio.sleep(1)


@bot.command()
async def song(ctx, *, song_name):
    """Searches for a song across all playlists and plays it."""
    for root, dirs, files in os.walk('mp3s'):
        songs = [f for f in files if f.endswith('.mp3')]
        song_path = process.extractOne(song_name, songs, score_cutoff=70)
        if song_path:
            full_path = os.path.join(root, song_path[0])
            break
    else:
        await ctx.send("Song not found.")
        return

    voice_channel = ctx.author.voice.channel
    if not ctx.voice_client:
        await voice_channel.connect()

    if ctx.voice_client.is_playing():
        ctx.voice_client.stop()
    ctx.voice_client.play(discord.FFmpegPCMAudio(full_path))
    await ctx.send(f"Now playing: {os.path.basename(full_path)}")


@bot.command()
async def skip(ctx):
    """Skips the current song."""
    if ctx.voice_client:
        ctx.voice_client.stop()
        await ctx.send("Song skipped.")


@bot.command()
async def pause(ctx):
    """Pauses the current song."""
    if ctx.voice_client:
        ctx.voice_client.pause()
        await ctx.send("Song paused.")


@bot.command()
async def resume(ctx):
    """Resumes the current song."""
    if ctx.voice_client:
        ctx.voice_client.resume()
        await ctx.send("Song resumed.")


@bot.command()
async def stop(ctx):
    """Stops the current song and clears the queue."""
    if ctx.voice_client:
        ctx.voice_client.stop()
        await ctx.send("Queue cleared.")


@bot.command()
async def commands(ctx):
    """Displays the help message."""
    help_message = """
    Available commands:
    !join - Joins the voice channel.
    !leave - Leaves the voice channel.
    !play [playlist_name] - Plays a playlist. If no playlist_name is provided, lists available playlists.
    !song [song_name] - Searches for a song across all playlists and plays it.
    !skip - Skips the current song.
    !pause - Pauses the current song.
    !resume - Resumes the current song.
    !stop - Stops the current song and clears the queue.
    !help - Displays this help message.
    """
    await ctx.send(help_message)


@bot.command()
async def basa(ctx):
    await ctx.send('Debeljanko')


@bot.command()
async def basaragin(ctx):
    await ctx.send('Vladimir Basa Basaragin poznatiji kao debeljakno.')


@bot.command()
async def lol(ctx, *, champion_name):
    """Fetches and displays information about a League of Legends champion."""
    url = f"https://ddragon.leagueoflegends.com/cdn/12.10.1/data/en_US/champion/{champion_name}.json"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        champion_data = data['data'][champion_name]
        win_rate = "50%"  # Placeholder, real win rate needs another API or data source
        best_build = "Item1, Item2, Item3"  # Placeholder, real build needs another API or data source
        await ctx.send(f"**{champion_name}** - Win Rate: {win_rate}, Best Build: {best_build}")
    else:
        await ctx.send("Champion not found.")


@bot.command()
async def lolplayer(ctx, *, player_name):
    """Fetches and displays information about a League of Legends player."""
    region = "na1"  # Example region, this should be dynamic based on the player or command
    url = f"https://{region}.api.riotgames.com/lol/summoner/v4/summoners/by-name/{player_name}?api_key={config.RIOT_API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        summoner_data = response.json()
        summoner_id = summoner_data['id']
        # Fetch rank information
        rank_url = f"https://{region}.api.riotgames.com/lol/league/v4/entries/by-summoner/{summoner_id}?api_key={config.RIOT_API_KEY}"
        rank_response = requests.get(rank_url)
        if rank_response.status_code == 200:
            rank_data = rank_response.json()[0]
            rank = rank_data['tier'] + " " + rank_data['rank']
            win_rate = f"{(rank_data['wins'] / (rank_data['wins'] + rank_data['losses'])) * 100:.2f}%"
            await ctx.send(f"**{player_name}** - Rank: {rank}, Win Rate: {win_rate}")
        else:
            await ctx.send("Rank information not available.")
    else:
        await ctx.send("Player not found.")

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

bot.run(config.TOKEN)
