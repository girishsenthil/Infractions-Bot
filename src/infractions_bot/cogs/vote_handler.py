import asyncio
import nextcord
from nextcord.ext import commands

import infractions_bot.database_funcs as dbf

TEST_GUILD_ID = 1292283530415444000

class VoteHandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{__name__} is online")
    

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction: nextcord.Reaction, user: nextcord.Member):
        if user.bot:
            return
        
        