"""
Embed templates and utilities
"""

import discord
from datetime import datetime

class Embeds:
    """Embed template collection"""
    
    # Colors
    SUCCESS = discord.Color.green()
    ERROR = discord.Color.red()
    INFO = discord.Color.blue()
    WARNING = discord.Color.orange()
    NEUTRAL = discord.Color.greyple()
    
    @staticmethod
    def success(title: str, description: str = None) -> discord.Embed:
        """Create a success embed"""
        embed = discord.Embed(
            title=f"✅ {title}",
            description=description,
            color=Embeds.SUCCESS,
            timestamp=datetime.utcnow()
        )
        return embed
    
    @staticmethod
    def error(title: str, description: str = None) -> discord.Embed:
        """Create an error embed"""
        embed = discord.Embed(
            title=f"❌ {title}",
            description=description,
            color=Embeds.ERROR,
            timestamp=datetime.utcnow()
        )
        return embed
    
    @staticmethod
    def info(title: str, description: str = None) -> discord.Embed:
        """Create an info embed"""
        embed = discord.Embed(
            title=f"ℹ️ {title}",
            description=description,
            color=Embeds.INFO,
            timestamp=datetime.utcnow()
        )
        return embed
    
    @staticmethod
    def warning(title: str, description: str = None) -> discord.Embed:
        """Create a warning embed"""
        embed = discord.Embed(
            title=f"⚠️ {title}",
            description=description,
            color=Embeds.WARNING,
            timestamp=datetime.utcnow()
        )
        return embed
    
    @staticmethod
    def neutral(title: str, description: str = None) -> discord.Embed:
        """Create a neutral embed"""
        embed = discord.Embed(
            title=title,
            description=description,
            color=Embeds.NEUTRAL,
            timestamp=datetime.utcnow()
        )
        return embed
