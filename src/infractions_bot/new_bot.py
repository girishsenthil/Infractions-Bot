import nextcord
from nextcord.ext import commands
from utils import logging_config
import logging

intents = nextcord.Intents.default()
intents.message_content = True
intents.reactions = True

import infractions_bot.database_funcs as dbf

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    logging.info(f'{bot.user} has connected to Discord!')
    logging.info(f'Bot ID: {bot.user.id}')
    logging.info(f'Connected to {len(bot.guilds)} guilds')
    
    dbf.init_database()
    print('Bot Ready!')




