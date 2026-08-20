"""
Ticket system commands
"""

import discord
from discord.ext import commands
from discord import app_commands
from utils.embeds import Embeds
import sqlite3

class Tickets(commands.Cog):
    """Ticket system commands"""
    
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    
    @app_commands.command(name="ticket_create")
    @app_commands.describe(reason="Reason for creating ticket")
    async def ticket_create(
        self,
        interaction: discord.Interaction,
        reason: str
    ):
        """Create a support ticket"""
        guild = interaction.guild
        
        # Create ticket channel
        try:
            ticket_channel = await guild.create_text_channel(
                name=f"ticket-{interaction.user.name}",
                overwrites={
                    guild.default_role: discord.PermissionOverwrite(read_messages=False),
                    interaction.user: discord.PermissionOverwrite(read_messages=True)
                }
            )
            
            # Save to database
            conn = sqlite3.connect('database.db')
            cursor = conn.cursor()
            cursor.execute(
                'INSERT INTO tickets (guild_id, channel_id, creator_id, status) VALUES (?, ?, ?, ?)',
                (guild.id, ticket_channel.id, interaction.user.id, 'open')
            )
            conn.commit()
            conn.close()
            
            embed = Embeds.success(
                "Ticket Created",
                f"Your ticket has been created: {ticket_channel.mention}\nReason: {reason}"
            )
            await interaction.response.send_message(embed=embed)
            
        except Exception as e:
            embed = Embeds.error("Error", str(e))
            await interaction.response.send_message(embed=embed, ephemeral=True)
    
    @app_commands.command(name="ticket_close")
    async def ticket_close(self, interaction: discord.Interaction):
        """Close a ticket"""
        if not interaction.user.guild_permissions.administrator:
            embed = Embeds.error("Permission Denied")
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
        
        try:
            conn = sqlite3.connect('database.db')
            cursor = conn.cursor()
            cursor.execute(
                'UPDATE tickets SET status = ?, closed_at = CURRENT_TIMESTAMP WHERE channel_id = ?',
                ('closed', interaction.channel.id)
            )
            conn.commit()
            conn.close()
            
            await interaction.channel.delete()
            
        except Exception as e:
            embed = Embeds.error("Error", str(e))
            await interaction.response.send_message(embed=embed, ephemeral=True)

async def setup(bot: commands.Bot):
    await bot.add_cog(Tickets(bot))
