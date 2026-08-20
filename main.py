"""
AZSRP Manager Bot - Main Entry Point
"""

import discord
from discord.ext import commands
import logging
from config import Config
from database import Database
import os

# Setup logging
logging.basicConfig(level=getattr(logging, Config.LOG_LEVEL))
logger = logging.getLogger(__name__)

# Initialize bot
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.guilds = True
intents.voice_states = True

bot = commands.Bot(
    command_prefix=Config.PREFIX,
    intents=intents,
    help_command=None
)

@bot.event
async def on_ready():
    """Bot is ready"""
    print(f"✅ {bot.user} is online!")
    print(f"Guilds: {len(bot.guilds)}")
    
    try:
        synced = await bot.tree.sync()
        print(f"✅ Synced {len(synced)} command(s)")
    except Exception as e:
        print(f"❌ Failed to sync commands: {e}")

@bot.event
async def on_command_error(ctx, error):
    """Handle command errors"""
    logger.error(f"Command error: {error}")
    await ctx.send(f"An error occurred: {error}")

async def load_cogs():
    """Load all cogs"""
    cogs_dir = "cogs"
    for filename in os.listdir(cogs_dir):
        if filename.endswith(".py"):
            cog_name = filename[:-3]
            try:
                await bot.load_extension(f"cogs.{cog_name}")
                print(f"✅ Loaded cog: {cog_name}")
            except Exception as e:
                print(f"❌ Failed to load cog {cog_name}: {e}")

async def main():
    """Main function"""
    # Validate configuration
    Config.validate()
    
    # Initialize database
    db = Database()
    db.init_tables()
    
    # Load cogs
    async with bot:
        await load_cogs()
        await bot.start(Config.TOKEN)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
