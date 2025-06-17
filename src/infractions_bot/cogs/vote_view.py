import nextcord
from nextcord.ext import commands

class VoteView(nextcord.ui.View):
    def __init__(self, reporter_id, target_id, timeout=None):
        super().__init__(timeout=timeout)
        self.parties = {reporter_id, target_id}
        self.approved, self.rejected = set(), set()
    
    @nextcord.ui.button(label='Approve', style=nextcord.ButtonStyle.green, emoji='👍')
    async def approve_callback(self, 
                               button: nextcord.ui.Button, 
                               interaction: nextcord.Interaction):
        

        if interaction.user.id in self.approved:
            await interaction.response.send_message('You have already approved this infraction', ephemeral=True)
            return
        
        elif interaction.user.id in self.rejected:
            await interaction.response.send_message('Your vote has been changed to **APPROVED**', ephemeral=True)
            self.rejected.remove(interaction.user.id)
            self.approved.add(interaction.user.id)
            return
        
        await interaction.response.send_message('You have **APPROVED** this infraction!', ephemeral=True)
        self.approved.add(interaction.user.id)

        return
        
    
    @nextcord.ui.button(label='Reject', style=nextcord.ButtonStyle.red, emoji='👎')
    async def reject_callback(self,
                              button: nextcord.ui.Button,
                              interaction: nextcord.Interaction):
        
        if interaction.user.id in self.rejected:
            await interaction.response.send_message('You have already **REJECTED** this infraction', ephemeral=True)
            return
        
        elif interaction.user.id in self.approved:
            await interaction.response.send_message('Your vote has been changed to **REJECTED**', ephemeral=True)
            self.approved.remove(interaction.user.id)
            self.rejected.add(interaction.user.id)

        await interaction.response.send_message('You have **REJECTED** this infraction!', ephemeral=True)
        self.rejected.add(interaction.user.id)
        
        return
    
    async def interaction_check(self, interaction):
        
        if interaction.user.id in self.parties:
            await interaction.response.send_message('You cannot vote on an infraction you are a party in!',
                                                    ephemeral=True)
            return False
        return True
    
    @property
    def count(self):
        return len(self.approved) + len(self.rejected)
    
    @property
    def approved_count(self):
        return len(self.approved)
    
    @property
    def rejected_count(self):
        return len(self.rejected)
    
        
        