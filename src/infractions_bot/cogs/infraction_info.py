import asyncio
import nextcord
from nextcord.ext import commands
import logging
import infractions_bot.database_funcs as dbf

TEST_GUILD_ID = 1292283530415444000


class InfractionInfo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
        logging.info(f"{__name__} is online")
        print(f"{__name__} is online")
    
    @nextcord.slash_command(name='infractions', 
                            description='Get infractions for a user (or for youself if user is blank',
                            guild_ids=[TEST_GUILD_ID])
    async def infractions(self, interaction: nextcord.Interaction, target_user: nextcord.Member):
        logging.info(f"Fetching infraction history for {target_user.name}")

