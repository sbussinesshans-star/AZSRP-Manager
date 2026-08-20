"""
Logging system - tracks server events
"""

import discord
from discord.ext import commands, tasks
from discord import app_commands
from utils.embeds import Embeds
import sqlite3
from datetime import datetime

class Logging(commands.Cog):
    """Logging system for server events"""
    
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    
    @app_commands.command(name="logs_setup")
    @app_commands.describe(channel="Channel for logs")
    async def logs_setup(
        self,
        interaction: discord.Interaction,
        channel: discord.TextChannel
    ):
        """Setup logging for the server"""
        if not interaction.user.guild_permissions.administrator:
            embed = Embeds.error("Permission Denied")
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
        
        try:
            conn = sqlite3.connect('database.db')
            cursor = conn.cursor()
            cursor.execute(
                'INSERT OR REPLACE INTO log_config (guild_id, log_channel_id) VALUES (?, ?)',
                (interaction.guild.id, channel.id)
            )
            conn.commit()
            conn.close()
            
            embed = Embeds.success("Logging Setup", f"Logs will be sent to {channel.mention}")
            await interaction.response.send_message(embed=embed)
        except Exception as e:
            embed = Embeds.error("Error", str(e))
            await interaction.response.send_message(embed=embed, ephemeral=True)
    
    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        """Log member join"""
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute(
            'SELECT log_channel_id FROM log_config WHERE guild_id = ? AND enabled = 1',
            (member.guild.id,)
        )
        result = cursor.fetchone()
        conn.close()
        
        if result:
            log_channel_id = result[0]
            log_channel = member.guild.get_channel(log_channel_id)
            if log_channel:
                embed = Embeds.info(
                    "Member Joined",
                    f"{member.mention} ({member.id})"
                )
                embed.add_field(name="Account Created", value=member.created_at.strftime('%Y-%m-%d'))
                await log_channel.send(embed=embed)
    
    @commands.Cog.listener()
    async def on_member_remove(self, member: discord.Member):
        """Log member leave"""
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute(
            'SELECT log_channel_id FROM log_config WHERE guild_id = ? AND enabled = 1',
            (member.guild.id,)
        )
        result = cursor.fetchone()
        conn.close()
        
        if result:
            log_channel_id = result[0]
            log_channel = member.guild.get_channel(log_channel_id)
            if log_channel:
                embed = Embeds.warning(
                    "Member Left",
                    f"{member.mention} ({member.id})"
                )
                await log_channel.send(embed=embed)

async def setup(bot: commands.Bot):
    await bot.add_cog(Logging(bot))
