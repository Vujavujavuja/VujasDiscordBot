import os
from dotenv import load_dotenv

load_dotenv()


TOKEN = os.getenv('DISCORD_BOT_TOKEN')
RIOT_API_KEY = os.getenv('RIOT_API_KEY')
PREFIX = '!'
