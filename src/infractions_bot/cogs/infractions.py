import asyncio
from datetime import datetime, timedelta
from typing import Any, Dict
import uuid
import logging
import nextcord
from nextcord.ext import commands

import infractions_bot.database_funcs as dbf

TEST_GUILD_ID = 1292283530415444000


class Infractions(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.emojis = {
            'approve': '✅',
            'reject': '❌'
            }
    

    @commands.Cog.listener()
    async def on_ready(self):
        logging.info(f"{__name__} is online")
        print(f"{__name__} is online")
    
    @nextcord.slash_command(name='infraction', description='Create new infraction', guild_ids=[TEST_GUILD_ID])
    async def infraction(self, interaction: nextcord.Interaction, target_user: nextcord.Member, reason: str):
        
        MAX_REASON_LENGTH = 500
        
        if interaction.user.id == target_user.id:
            await interaction.response.send_message("You cannot report yourself!", ephemeral=True)
            return
        
        if len(reason) > MAX_REASON_LENGTH:
            await interaction.response.send_message(f"Reason can be up to {MAX_REASON_LENGTH} characters")
            return

        try:
            settings = dbf.get_guild_settings(interaction.guild_id)
        except Exception as e:
            await interaction.response.send_message("ERROR")
            logging.error('Error with grabbing guild settings', exc_info=True)
            return
        
        infraction_id = str(uuid.uuid4())

        end_time = datetime.now() + timedelta(seconds=settings['vote_duration'])

        logging.debug(f'creating new infraction with reporter: {interaction.user} and target: {target_user}')



        infraction = {
            'id': infraction_id,
            'guild_id': interaction.guild.id,
            'target_user_id': target_user.id,
            'target_username': str(target_user),
            'reporter_id': interaction.user.id,
            'reporter_username': str(interaction.user),
            'reason': reason,
            'channel_id': interaction.channel_id,
            'timestamp': datetime.now().isoformat(),
            'status': 'pending',
            'end_time': end_time.isoformat(),
        }

        logging.debug('creating infraction embed')

        infraction_embed = await self.create_infraction_embed(interaction.user.id, 
                                                              target_user.id, 
                                                              reason, 
                                                              infraction_id)

        logging.debug('Sending message')
        await interaction.response.send_message(embed=infraction_embed)
        message = await interaction.original_message()
        
        await message.add_reaction('✅')
        await message.add_reaction('❌')

        infraction['message_id'] = message.id

        try:
            logging.debug('saving infraction')
            dbf.save_infraction(infraction)
        
        except Exception as e:
            logging.error('Error with saving infraction in database', exc_info=True)
        
        logging.debug('Creating async timer for infraction')
        asyncio.create_task(self._infraction_timer(infraction))
    
    async def create_infraction_embed(self,
                                reporter_id: int, 
                                target_user_id: int, 
                                reason: str, infraction_id: str) -> nextcord.Embed:
        
        embed = nextcord.Embed(
            title="🚨 New Infraction Report 🚨",
            description=f"**Target:** <@{target_user_id}>\n**Reason:** {reason}\n**Reporter:** <@{reporter_id}>",
            color=nextcord.Color.orange(),
            timestamp=datetime.now()
    )
        
        embed.add_field(name="Voting", value="React with ✅ to approve or ❌ to reject", inline=False)
        # embed.add_field(name="Votes", value="✅ 0 | ❌ 0", inline=True)
        embed.add_field(name="Status", value="🕐 Voting in progress...", inline=False)
        embed.set_footer(text=f"Infraction ID: {infraction_id}")

        return embed
    
    async def _infraction_timer(self, infraction: Dict[str, Any]):

        try:
            voting_duration = (datetime.fromisoformat(infraction['end_time']) - datetime.now()).total_seconds()
            logging.debug(f"Async timer created for {voting_duration}")
        except:
            logging.debug('voting_duration calc error', exc_info=True)

        await asyncio.sleep(voting_duration) 

        # await asyncio.sleep(5)

        logging.debug('Async timer complete, going into finalize func')
        await self.finalize(infraction)
    
    async def get_message(self, channel_id: int, message_id: int):
        logging.debug("Getting message")

        try:

            channel = self.bot.get_channel(channel_id)
            if channel is None:
                channel = await self.bot.fetch_channel(channel_id)
            message = await channel.fetch_message(message_id)
        
        except:
            logging.debug('Error grabbing message', exc_info=True)

        return message

    async def finalize(self, infraction: Dict[str, Any]):

        try:

            logging.debug('Grabbing message')
            channel_id, message_id = infraction['channel_id'], infraction['message_id']

            try:

                channel = self.bot.get_channel(channel_id)
                infraction_message = await channel.fetch_message(message_id)

            except Exception as e:
                logging.error('Error with loading original infraction message', exc_info=True)
            
            guild_settings = dbf.get_guild_settings(infraction['guild_id'])

            logging.debug('counting reactions')
            for reaction in infraction_message.reactions:
                if str(reaction.emoji) == self.emojis['approve']:
                    approve_votes = reaction.count - 1
                elif str(reaction.emoji) == self.emojis['reject']:
                    reject_votes = reaction.count - 1
            
            logging.debug('Creating final embed')
            embed, outcome = self.create_finalization_embed(infraction, guild_settings, approve_votes, reject_votes)

            await infraction_message.edit(embed=embed)
            await infraction_message.clear_reactions()

            logging.debug('Finalizing infraction and saving in db')
            dbf.finalize_infraction(infraction['id'], outcome, approve_votes, reject_votes)

        except Exception as e:
            logging.error('Error with finalizing infraction', exc_info=True)
            return

    def create_finalization_embed(self, infraction, guild_settings, approve_votes, reject_votes) -> nextcord.Embed:
        
        outcome, outcome_text, color = self.get_infraction_result(approve_votes, reject_votes,
                                                                  guild_settings['required_votes'],
                                                                  guild_settings['approval_threshold'],)
        
        embed = nextcord.Embed(
            title="🚨 Infraction Report - Final Result",
            description=(
                f"**Target:** <@{infraction['target_user_id']}>\n"
                f"**Reason:** {infraction['reason']}\n"
                f"**Reporter:** <@{infraction['reporter_id']}>"
            ),
            color=color,
            timestamp=datetime.now()
        )

        guild_name = self.bot.get_guild(infraction['guild_id']).name

        embed.add_field(name="Final Votes", value=f"✅ {approve_votes} | ❌ {reject_votes}", inline=True)
        embed.add_field(name="Result", value=outcome_text, inline=True)
        embed.add_field(name="Server", value=guild_name, inline=False)
        embed.set_footer(text=f"Infraction ID: {infraction['id']}")

        return embed, outcome

    def get_infraction_result(self, approve_votes: int, reject_votes: int,
                              required_votes: int, approval_threshold: float):
        
        total_votes = approve_votes + reject_votes

        if total_votes < required_votes:
            outcome = 'rejected'
            outcome_text = "❌ **REJECTED** - Not enough votes"
            color = nextcord.Color.red()
        
        elif total_votes == 0:
            outcome = 'rejected'
            outcome_text = "❌ **REJECTED** - No votes received"
            color = nextcord.Color.red()
        
        elif approve_votes / total_votes >= approval_threshold:
            outcome = 'approved'
            outcome_text = "✅ **APPROVED**"
            color = nextcord.Color.green()
        
        else:
            outcome = 'rejected'
            outcome_text = "❌ **REJECTED** - Not enough approval"
            color = nextcord.Color.red()
        
        return outcome, outcome_text, color
        


def setup(bot):
    bot.add_cog(Infractions(bot))

# async def setup(bot):
#     await bot.add_cog(Infractions(bot))