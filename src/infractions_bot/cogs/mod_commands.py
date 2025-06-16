import asyncio
import nextcord
from nextcord.ext import commands
import logging

import infractions_bot.database_funcs as dbf

TEST_GUILD_ID = 1292283530415444000

class ModeratorCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    

    @commands.Cog.listener()
    async def on_ready(self):
        logging.info(f"{__name__} is online")
        print(f"{__name__} is online")
    

    @nextcord.slash_command(name='infractionsettings', 
                            description='View current server settings for infraction voting', 
                            guild_ids=[TEST_GUILD_ID])
    @commands.has_permissions(manage_guild=True)
    async def get_guild_settings(self, interaction: nextcord.Interaction):

        try:
            settings = dbf.get_guild_settings(interaction.guild.id)
        except Exception as e:
            logging.error('Error getting guild settings', exc_info=True)

            await interaction.response.send_message('Error getting guild settings', ephemeral=True)
            return
        
        embed = nextcord.Embed(
        title=f"⚙️ Infraction Settings - {interaction.guild.name}",
        color=nextcord.Color.blue()
        )

        embed.add_field(name="Vote Duration", value=f"{settings['vote_duration']} seconds", inline=True)
        embed.add_field(name="Required Votes", value=settings['required_votes'], inline=True)
        embed.add_field(name="Approval Threshold", value=f"{settings['approval_threshold']*100}%", inline=True)
        
        minutes = settings['vote_duration'] // 60
        seconds = settings['vote_duration'] % 60
        duration_text = f"{minutes}m {seconds}s" if seconds > 0 else f"{minutes}m"
        
        embed.add_field(
            name="Info", 
            value=f"Voting lasts **{duration_text}** and needs **{settings['required_votes']}** votes with **{settings['approval_threshold']*100}%** approval to pass.",
            inline=False
        )
        
        await interaction.response.send_message(embed=embed, ephemeral=True)
        
    
    @nextcord.slash_command(name='modifyinfractionsettings',
                            description='Modify infraction settings',
                            guild_ids=[TEST_GUILD_ID])
    @commands.has_permissions(manage_guild=True)
    async def modify_settings(self, interaction:nextcord.Interaction, 
                              vote_duration: int = None,
                              required_votes: int = None,
                              approval_threshold: float = None):
        
        
        updated_settings = {}

        if vote_duration is not None:
            if vote_duration < 60 or vote_duration > 3600:
                await interaction.response.send_message(
                    "❌ Vote duration must be between 60 and 3600 seconds (1 minute to 1 hour)!", 
                    ephemeral=True
                )
                return
            
            updated_settings['vote_duration'] = vote_duration
        
        if required_votes is not None:
            if required_votes < 1 or required_votes > 20:
                await interaction.response.send_message(
                    "❌ Required votes must be between 1 and 20!", 
                    ephemeral=True
                )
                return
            
            updated_settings['required_votes'] = required_votes
        
        if approval_threshold is not None:
            if approval_threshold < 0.1 or approval_threshold > 1.0:
                await interaction.response.send_message(
                    "❌ Approval threshold must be between 0.1 and 1.0 (10% to 100%)!", 
                    ephemeral=True
                )
                return
            
            updated_settings['approval_threshold'] = approval_threshold
        
        if not updated_settings:
            await interaction.response.send_message(
                "❌ Please provide at least one setting to update!", 
                ephemeral=True
            )
            return

        dbf.configure_guild_settings(interaction.guild.id, updated_settings)
        settings = dbf.get_guild_settings(interaction.guild.id) #maybe construct embed from updated settings dict, only showing settings that were updated

        embed = nextcord.Embed(
            title="✅ Settings Updated",
            description=(f"**Vote Duration:** {settings['vote_duration']}s\n"
                         f"**Required Votes:** {settings['required_votes']}\n"
                         f"**Approval Threshold:** {settings['approval_threshold']*100}%"),
            color=nextcord.Color.green()
        )

        await interaction.response.send_message(embed=embed, ephemeral=True)



def setup(bot):
    bot.add_cog(ModeratorCommands(bot))
