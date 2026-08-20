"""
Helper functions and utilities
"""

import discord
from discord.ext import commands
from datetime import datetime, timedelta
import sqlite3

def is_staff():
    """Check if user has staff role"""
    async def predicate(ctx):
        return ctx.author.guild_permissions.administrator
    return commands.check(predicate)

def is_admin():
    """Check if user is admin"""
    async def predicate(ctx):
        return ctx.author.guild_permissions.administrator
    return commands.check(predicate)

def get_database():
    """Get database connection"""
    return sqlite3.connect('database.db')

def format_duration(seconds: int) -> str:
    """Format seconds to readable duration"""
    duration = timedelta(seconds=seconds)
    days = duration.days
    hours, remainder = divmod(duration.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    
    parts = []
    if days:
        parts.append(f"{days}d")
    if hours:
        parts.append(f"{hours}h")
    if minutes:
        parts.append(f"{minutes}m")
    if seconds or not parts:
        parts.append(f"{seconds}s")
    
    return " ".join(parts)

def format_timestamp(dt: datetime) -> str:
    """Format datetime to Discord timestamp"""
    return f"<t:{int(dt.timestamp())}:f>"

def paginate_text(text: str, max_length: int = 2000) -> list:
    """Split text into pages"""
    pages = []
    current_page = ""
    
    for line in text.split('\n'):
        if len(current_page) + len(line) + 1 > max_length:
            if current_page:
                pages.append(current_page)
            current_page = line
        else:
            current_page += line + '\n'
    
    if current_page:
        pages.append(current_page)
    
    return pages
