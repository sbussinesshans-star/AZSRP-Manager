"""
Moderation commands
"""

import discord
from discord.ext import commands
from discord import app_commands
from utils.embeds import Embeds
import sqlite3

class Moderation(commands.Cog):
    """Moderation commands"""
    
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    
    @app_commands.command(name="ban")
    @app_commands.describe(
        member="Member to ban",
        reason="Reason for ban"
    )
    async def ban(
        self,
        interaction: discord.Interaction,
        member: discord.Member,
        reason: str = None
    ):
        """Ban a member from the server"""
        if not interaction.user.guild_permissions.ban_members:
            embed = Embeds.error("Permission Denied")
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
        
        try:
            await interaction.guild.ban(member, reason=reason)
            embed = Embeds.success(
                "Member Banned",
                f"{member.mention} has been banned\nReason: {reason or 'No reason provided'}"
            )
            await interaction.response.send_message(embed=embed)
        except Exception as e:
            embed = Embeds.error("Ban Failed", str(e))
            await interaction.response.send_message(embed=embed, ephemeral=True)
    
    @app_commands.command(name="kick")
    @app_commands.describe(
        member="Member to kick",
        reason="Reason for kick"
    )
    async def kick(
        self,
        interaction: discord.Interaction,
        member: discord.Member,
        reason: str = None
    ):
        """Kick a member from the server"""
        if not interaction.user.guild_permissions.kick_members:
            embed = Embeds.error("Permission Denied")
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
        
        try:
            await member.kick(reason=reason)
            embed = Embeds.success(
                "Member Kicked",
                f"{member.mention} has been kicked\nReason: {reason or 'No reason provided'}"
            )
            await interaction.response.send_message(embed=embed)
        except Exception as e:
            embed = Embeds.error("Kick Failed", str(e))
            await interaction.response.send_message(embed=embed, ephemeral=True)
    
    @app_commands.command(name="warn")
    @app_commands.describe(
        member="Member to warn",
        reason="Reason for warning"
    )
    async def warn(
        self,
        interaction: discord.Interaction,
        member: discord.Member,
        reason: str
    ):
        """Warn a member"""
        if not interaction.user.guild_permissions.moderate_members:
            embed = Embeds.error("Permission Denied")
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
        
        try:
            conn = sqlite3.connect('database.db')
            cursor = conn.cursor()
            cursor.execute(
                'INSERT INTO warnings (guild_id, user_id, moderator_id, reason) VALUES (?, ?, ?, ?)',
                (interaction.guild.id, member.id, interaction.user.id, reason)
            )
            conn.commit()
            conn.close()
            
            embed = Embeds.warning(
                "Member Warned",
                f"{member.mention} has been warned\nReason: {reason}"
            )
            await interaction.response.send_message(embed=embed)
        except Exception as e:
            embed = Embeds.error("Warning Failed", str(e))
            await interaction.response.send_message(embed=embed, ephemeral=True)
    
    @app_commands.command(name="warnings")
    @app_commands.describe(member="Member to check")
    async def warnings(
        self,
        interaction: discord.Interaction,
        member: discord.Member
    ):
        """Check member warnings"""
        try:
            conn = sqlite3.connect('database.db')
            cursor = conn.cursor()
            cursor.execute(
                'SELECT reason, timestamp FROM warnings WHERE guild_id = ? AND user_id = ?',
                (interaction.guild.id, member.id)
            )
            warnings = cursor.fetchall()
            conn.close()
            
            if not warnings:
                embed = Embeds.info(f"{member.name} Warnings", "No warnings found")
            else:
                embed = Embeds.info(f"{member.name} Warnings", f"Total: {len(warnings)}")
                for i, (reason, timestamp) in enumerate(warnings, 1):
                    embed.add_field(
                        name=f"Warning #{i}",
                        value=f"Reason: {reason}",
                        inline=False
                    )
            
            await interaction.response.send_message(embed=embed)
        except Exception as e:
            embed = Embeds.error("Error", str(e))
            await interaction.response.send_message(embed=embed, ephemeral=True)

async def setup(bot: commands.Bot):
    await bot.add_cog(Moderation(bot))
