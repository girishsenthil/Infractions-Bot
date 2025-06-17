import asyncio
import nextcord
from nextcord.ext import commands
import logging

from infractions_bot.cogs.vote_view import VoteView
import infractions_bot.database_funcs as dbf

TEST_GUILD_ID = 1292283530415444000


class Ping(commands.Cog):
    '''
    Dev cog for testing components/features
    '''

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

    @nextcord.slash_command(name='dummy_embed', description='dummy embed for dev purposes', guild_ids=[TEST_GUILD_ID])
    async def dummy_embed(self, interaction: nextcord.Interaction):

        embed = nextcord.Embed(
            title=f"Testing embed in **{interaction.guild.name}**",
            description="Embed for testing",
            color=nextcord.Color.purple(),
        )

        view = VoteView(1, 2)
        await interaction.response.send_message(embed=embed, view=view)
        message = await interaction.original_message()

        await asyncio.sleep(15)
        view.stop()
        print('view has stopped')
        await message.edit(content=(f"button clicked {view.count} times\n"
                                    f"Votes: {''.join([f"<@{i}>\n" for i in view.approved])}"), embed=None, view=None)
        

    @nextcord.slash_command(name='clear_pending', description='Dev command to clear pending infractions', guild_ids=[TEST_GUILD_ID])
    @commands.is_owner()
    async def clear_pending(self, interaction):

        try:
            dbf.clear_pending_infractions()
        except Exception as e:
            logging.error('Error with clearing pending infractions', exc_info=True)
            await interaction.response.send_message('Error with clearing pending infractions', ephemeral=True)
        
        await interaction.response.send_message('Pending infractions cleared', ephemeral=True)

        return
    
        
    





def setup(bot):
    bot.add_cog(Ping(bot))