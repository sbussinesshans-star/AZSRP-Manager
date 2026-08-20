"""
Utility commands
"""

import discord
from discord.ext import commands
from discord import app_commands
from utils.embeds import Embeds
import time
from datetime import datetime

class Utility(commands.Cog):
    """Utility commands"""
    
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.start_time = time.time()
    
    @app_commands.command(name="ping")
    async def ping(self, interaction: discord.Interaction):
        """Check bot latency"""
        latency = round(self.bot.latency * 1000)
        embed = Embeds.info(
            "🏓 Pong!",
            f"Latency: {latency}ms"
        )
        await interaction.response.send_message(embed=embed)
    
    @app_commands.command(name="uptime")
    async def uptime(self, interaction: discord.Interaction):
        """Check bot uptime"""
        current_time = time.time()
        uptime_seconds = int(current_time - self.start_time)
        
        days, remainder = divmod(uptime_seconds, 86400)
        hours, remainder = divmod(remainder, 3600)
        minutes, seconds = divmod(remainder, 60)
        
        uptime_str = f"{days}d {hours}h {minutes}m {seconds}s"
        
        embed = Embeds.info(
            "⏱️ Bot Uptime",
            f"Online for: {uptime_str}"
        )
        await interaction.response.send_message(embed=embed)
    
    @app_commands.command(name="userinfo")
    @app_commands.describe(member="Member to check (optional)")
    async def userinfo(
        self,
        interaction: discord.Interaction,
        member: discord.Member = None
    ):
        """Get user information"""
        member = member or interaction.user
        
        embed = Embeds.info(
            f"👤 {member.name}'s Info",
            f"ID: {member.id}"
        )
        embed.add_field(name="Username", value=member.name, inline=True)
        embed.add_field(name="Joined", value=member.joined_at.strftime('%Y-%m-%d'), inline=True)
        embed.add_field(name="Account Created", value=member.created_at.strftime('%Y-%m-%d'), inline=True)
        embed.set_thumbnail(url=member.display_avatar.url)
        
        await interaction.response.send_message(embed=embed)
    
    @app_commands.command(name="serverinfo")
    async def serverinfo(self, interaction: discord.Interaction):
        """Get server information"""
        guild = interaction.guild
        
        embed = Embeds.info(
            f"🏢 {guild.name}",
            f"ID: {guild.id}"
        )
        embed.add_field(name="Members", value=str(guild.member_count), inline=True)
        embed.add_field(name="Channels", value=str(len(guild.channels)), inline=True)
        embed.add_field(name="Roles", value=str(len(guild.roles)), inline=True)
        embed.add_field(name="Owner", value=f"{guild.owner.mention}", inline=False)
        embed.set_thumbnail(url=guild.icon.url if guild.icon else None)
        
        await interaction.response.send_message(embed=embed)
    
    @app_commands.command(name="avatar")
    @app_commands.describe(member="Member (optional)")
    async def avatar(
        self,
        interaction: discord.Interaction,
        member: discord.Member = None
    ):
        """Display a member's avatar"""
        member = member or interaction.user
        
        embed = discord.Embed(
            title=f"{member.name}'s Avatar",
            color=discord.Color.blue()
        )
        embed.set_image(url=member.display_avatar.url)
        
        await interaction.response.send_message(embed=embed)
    
    @app_commands.command(name="help")
    async def help(self, interaction: discord.Interaction):
        """Show all available commands"""
        embed = Embeds.info("📖 Help", "AZSRP Manager Bot Commands")
        
        embed.add_field(name="🎮 Sessions", value="/session_start, /session_end, /session_vote, /session_schedule", inline=False)
        embed.add_field(name="🛡️ Moderation", value="/ban, /kick, /warn, /warnings", inline=False)
        embed.add_field(name="📢 Announcements", value="/announce, /embed, /say, /poll", inline=False)
        embed.add_field(name="👤 User Commands", value="/userinfo, /serverinfo, /avatar", inline=False)
        embed.add_field(name="🔧 Utility", value="/ping, /uptime, /help", inline=False)
        
        await interaction.response.send_message(embed=embed)

async def setup(bot: commands.Bot):
    await bot.add_cog(Utility(bot))
