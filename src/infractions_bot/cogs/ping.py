import asyncio
import nextcord
from nextcord.ext import commands
import logging

TEST_GUILD_ID = 1292283530415444000
print('test cog loading')
class Ping(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        logging.info(f"{__name__} is online")
        print(f"{__name__} is online")

    @nextcord.slash_command(name='ping', description='testing pings/mentions', guild_ids=[TEST_GUILD_ID])
    async def ping(self, interaction: nextcord.Interaction, target_user: nextcord.Member):

        logging.info(f"Pinging user from Ping Cog: {target_user.name}")
        
        logging.debug(type(target_user.id))
        await interaction.response.send_message(f"using exclam: <@!{target_user.id}>\nusing no exclam: <@{target_user.id}>")
    
    @nextcord.slash_command(name='print_message_cache', description='debug func to print bot message cache', guild_ids=[TEST_GUILD_ID])
    async def print_message_cache(self, interaction: nextcord.Interaction):
        
        guild = self.bot.get_guild(interaction.guild.id)
        await interaction.response.send_message(f"GUILD ID: {guild.id}; GUILD_NAME: {guild.name}")



def setup(bot):
    bot.add_cog(Ping(bot))