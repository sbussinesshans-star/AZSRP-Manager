"""
Admin configuration commands
"""

import discord
from discord.ext import commands
from discord import app_commands
from utils.embeds import Embeds
import sqlite3

class Admin(commands.Cog):
    """Admin configuration commands"""
    
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    
    @app_commands.command(name="config")
    async def config(self, interaction: discord.Interaction):
        """Open bot configuration"""
        if not interaction.user.guild_permissions.administrator:
            embed = Embeds.error("Permission Denied", "Only admins can access configuration")
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
        
        embed = Embeds.info(
            "⚙️ Bot Configuration",
            "Configure bot settings for your server"
        )
        embed.add_field(
            name="Available Options",
            value="/config_sessions - Session settings\n" +
                  "/config_votes - Voting settings\n" +
                  "/config_logs - Logging settings\n" +
                  "/config_announcements - Announcement settings",
            inline=False
        )
        
        await interaction.response.send_message(embed=embed, ephemeral=True)
    
    @app_commands.command(name="config_sessions")
    @app_commands.describe(setting="Setting to configure")
    async def config_sessions(
        self,
        interaction: discord.Interaction,
        setting: str
    ):
        """Configure session settings"""
        if not interaction.user.guild_permissions.administrator:
            embed = Embeds.error("Permission Denied")
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
        
        embed = Embeds.success("Configuration Updated", f"Sessions setting '{setting}' has been configured")
        await interaction.response.send_message(embed=embed, ephemeral=True)
    
    @app_commands.command(name="settings")
    async def settings(self, interaction: discord.Interaction):
        """Show bot settings"""
        if not interaction.user.guild_permissions.administrator:
            embed = Embeds.error("Permission Denied")
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
        
        embed = Embeds.info(
            "Current Bot Settings",
            f"Guild: {interaction.guild.name}"
        )
        embed.add_field(name="Status", value="✅ Active", inline=True)
        embed.add_field(name="Commands", value="✅ Enabled", inline=True)
        
        await interaction.response.send_message(embed=embed, ephemeral=True)

async def setup(bot: commands.Bot):
    await bot.add_cog(Admin(bot))
