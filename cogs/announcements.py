"""
Announcement and messaging commands
"""

import discord
from discord.ext import commands
from discord import app_commands
from utils.embeds import Embeds

class Announcements(commands.Cog):
    """Announcement commands"""
    
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    
    @app_commands.command(name="announce")
    @app_commands.describe(
        title="Announcement title",
        description="Announcement content",
        channel="Channel to send announcement (optional)"
    )
    async def announce(
        self,
        interaction: discord.Interaction,
        title: str,
        description: str,
        channel: discord.TextChannel = None
    ):
        """Send an announcement"""
        if not interaction.user.guild_permissions.administrator:
            embed = Embeds.error("Permission Denied")
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
        
        target_channel = channel or interaction.channel
        embed = Embeds.info(title, description)
        
        try:
            await target_channel.send(embed=embed)
            await interaction.response.send_message("✅ Announcement sent!", ephemeral=True)
        except Exception as e:
            embed = Embeds.error("Error", str(e))
            await interaction.response.send_message(embed=embed, ephemeral=True)
    
    @app_commands.command(name="embed")
    @app_commands.describe(
        title="Embed title",
        description="Embed description"
    )
    async def embed(
        self,
        interaction: discord.Interaction,
        title: str,
        description: str
    ):
        """Create a custom embed"""
        embed = discord.Embed(
            title=title,
            description=description,
            color=discord.Color.blue()
        )
        await interaction.response.send_message(embed=embed)
    
    @app_commands.command(name="say")
    @app_commands.describe(message="Message to send")
    async def say(
        self,
        interaction: discord.Interaction,
        message: str
    ):
        """Make the bot send a message"""
        if not interaction.user.guild_permissions.administrator:
            embed = Embeds.error("Permission Denied")
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
        
        await interaction.response.send_message(message)
    
    @app_commands.command(name="poll")
    @app_commands.describe(
        question="Poll question",
        option1="Option 1",
        option2="Option 2",
        option3="Option 3 (optional)",
        option4="Option 4 (optional)"
    )
    async def poll(
        self,
        interaction: discord.Interaction,
        question: str,
        option1: str,
        option2: str,
        option3: str = None,
        option4: str = None
    ):
        """Create a poll"""
        options = [option1, option2]
        if option3:
            options.append(option3)
        if option4:
            options.append(option4)
        
        description = "\n".join([f"{i}. {opt}" for i, opt in enumerate(options, 1)])
        embed = Embeds.neutral(f"📊 {question}", description)
        
        await interaction.response.send_message(embed=embed)

async def setup(bot: commands.Bot):
    await bot.add_cog(Announcements(bot))
