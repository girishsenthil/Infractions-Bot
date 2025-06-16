import asyncio
import nextcord
from nextcord.ext import commands
import logging
import infractions_bot.database_funcs as dbf
from typing import Dict
from datetime import datetime

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

        user_infractions: Dict = dbf.get_user_infractions(interaction.guild.id, target_user.id)

        if not user_infractions:
            await interaction.response.send_message(
                f"{target_user.display_name} has no approved infractions in {interaction.guild.name}"
            )
            return
        
        embed = nextcord.Embed(
            title=f"📋 Infractions for {target_user.display_name}",
            description=f"**Server:** {interaction.guild.name}\n**Total approved infractions:** {len(user_infractions)}",
            color=nextcord.Color.blue()
        )
        
        recent_infractions = user_infractions[:5]
        for i, infraction in enumerate(recent_infractions, 1):
            timestamp = datetime.fromisoformat(infraction['timestamp'])
            embed.add_field(
                name=f"#{i} - {timestamp.strftime('%Y-%m-%d %H:%M')}",
                value=f"**Reason:** {infraction['reason']}\n**Reporter:** <@{infraction['reporter_id']}>",
                inline=False
            )
        
        if len(user_infractions) > 5:
            embed.set_footer(text=f"Showing 5 most recent of {len(user_infractions)} total infractions")
        
        await interaction.response.send_message(embed=embed)


    @nextcord.slash_command(name='infractionsleaderboard',
                            description='Top 3 users with the most approved infractions in the server',
                            guild_ids=[TEST_GUILD_ID])
    async def infractions_leaderboard(self, interaction: nextcord.Interaction):
        

        
        try:
            top_n_users: Dict = dbf.get_guild_leaderboard(interaction.guild.id)
        except Exception as e:
            logging.error('Error with getting guild infractions', exc_info=True)
        
        if not top_n_users:
            await interaction.response.send_message(
                f"No approved infractions yet in {interaction.guild.name}"
                )
            return

        embed = nextcord.Embed(
        title=f"🏆 Infraction Leaderboard - {interaction.guild.name}",
        description="Top 3 users with the most approved infractions in this server",
        color=nextcord.Color.gold()
    )

        # top_n_users = [dict((user_id, val), (username, val), (infraction_count, val))]
        
        for idx, user_dict in enumerate(top_n_users, 1):
            medal = "🥇" if idx == 1 else "🥈" if idx == 2 else "🥉"

            embed.add_field(
                name=f"{medal} {user_dict['target_username']}",
                value=f"{user_dict['count']} infractions",
                inline=False
            )
        
        await interaction.response.send_message(embed=embed)
    
    @nextcord.slash_command(name='pendinginfractions',
                            description='View all pending infractions for this server',
                            guild_ids=[TEST_GUILD_ID])
    async def pending_infractions(self, interaction: nextcord.Interaction):

        try:
            pending = dbf.get_pending_infractions(interaction.guild.id)
        except Exception as e:
            logging.error(f"Error with getting pending infractions for {interaction.guild.name}", exc_info=True)
            await interaction.response.send_message('Database error while grabbing infractions', ephemeral=True)
            return

        if not pending:
            await interaction.response.send_message(f"No pending infractions in {interaction.guild.name}")
            return
        
        embed = nextcord.Embed(
        title=f"⏳ Pending Infractions - {interaction.guild.name}",
        description=f"Currently {len(pending)} infractions awaiting votes",
        color=nextcord.Color.orange()
    )
    
        for infraction in pending:
            
            embed.add_field(
                name=f"ID: {infraction['id'][:8]}...",
                value=(
                f"**Target:**  {infraction['target_username']}\n"
                f"**Reporter:** {infraction['reporter_username']}\n"
                f"**Reason:** {infraction['reason']}\n"),
                inline=False
            )
        
        await interaction.response.send_message(embed=embed)


def setup(bot):
    bot.add_cog(InfractionInfo(bot))


        
