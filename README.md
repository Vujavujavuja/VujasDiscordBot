# Vuja's Discord Bot

A small Discord music bot that plays MP3 playlists from a local folder into a voice channel. Built as a personal project for a private server.

Playlists are just folders: every subfolder of `mp3s/` is a playlist, and every `.mp3` inside it is a track. Names are matched fuzzily, so `!play ski` finds a folder called `Ski`.

## Commands

| Command | What it does |
| --- | --- |
| `!join` / `!leave` | Join or leave your voice channel |
| `!play` | List the available playlists |
| `!play <playlist>` | Shuffle and play a playlist |
| `!song <name>` | Find one song across all playlists and play it |
| `!pause` / `!resume` | Pause or resume playback |
| `!skip` | Skip the current song |
| `!stop` | Stop playback |
| `!lol <Champion>` | Look up a League of Legends champion (work in progress) |
| `!lolplayer <name>` | Look up a player's rank and win rate (needs a Riot API key) |
| `!commands` | Show the command list in Discord |

## Setup

You need Python 3.10+ and [FFmpeg](https://ffmpeg.org/) on your `PATH`.

```bash
pip install -r requirements.txt
cp .env.example .env
```

Put your bot token in `.env`. In the Discord developer portal, enable the **Message Content**, **Server Members** and **Presence** intents for the bot.

Add your music:

```
mp3s/
  Road trip/
    first song.mp3
    second song.mp3
  Focus/
    ...
```

Then run it:

```bash
python main.py
```

## Notes

- The music folder is ignored by git. Bring your own files, and only use audio you have the right to play.
- The League of Legends commands are unfinished: `!lol` returns placeholder win rate and build data.
