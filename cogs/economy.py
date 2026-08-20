"""
Economy system commands
"""

import discord
from discord.ext import commands
from discord import app_commands
from utils.embeds import Embeds
import sqlite3
import random

class Economy(commands.Cog):
    """Economy system commands"""
    
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    
    def _get_or_create_account(self, guild_id: int, user_id: int):
        """Get or create user economy account"""
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        
        cursor.execute(
            'INSERT OR IGNORE INTO economy_balance (guild_id, user_id) VALUES (?, ?)',
            (guild_id, user_id)
        )
        conn.commit()
        
        cursor.execute(
            'SELECT wallet, bank FROM economy_balance WHERE guild_id = ? AND user_id = ?',
            (guild_id, user_id)
        )
        result = cursor.fetchone()
        conn.close()
        
        return result if result else (0, 0)
    
    @app_commands.command(name="balance")
    @app_commands.describe(member="Member to check (optional)")
    async def balance(
        self,
        interaction: discord.Interaction,
        member: discord.Member = None
    ):
        """Check wallet and bank balance"""
        member = member or interaction.user
        wallet, bank = self._get_or_create_account(interaction.guild.id, member.id)
        
        embed = Embeds.info(
            f"💰 {member.name}'s Balance",
            f"Wallet: ${wallet}\nBank: ${bank}\nTotal: ${wallet + bank}"
        )
        await interaction.response.send_message(embed=embed)
    
    @app_commands.command(name="daily")
    async def daily(self, interaction: discord.Interaction):
        """Claim your daily reward"""
        wallet, bank = self._get_or_create_account(interaction.guild.id, interaction.user.id)
        reward = random.randint(50, 200)
        
        new_wallet = wallet + reward
        
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute(
            'UPDATE economy_balance SET wallet = ? WHERE guild_id = ? AND user_id = ?',
            (new_wallet, interaction.guild.id, interaction.user.id)
        )
        conn.commit()
        conn.close()
        
        embed = Embeds.success(
            "📅 Daily Reward",
            f"You earned ${reward}!\nNew wallet balance: ${new_wallet}"
        )
        await interaction.response.send_message(embed=embed)
    
    @app_commands.command(name="work")
    async def work(self, interaction: discord.Interaction):
        """Work to earn coins"""
        wallet, bank = self._get_or_create_account(interaction.guild.id, interaction.user.id)
        jobs = [
            ("programmer", 150),
            ("teacher", 120),
            ("chef", 100),
            ("doctor", 200),
            ("artist", 90),
        ]
        
        job, earnings = random.choice(jobs)
        new_wallet = wallet + earnings
        
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute(
            'UPDATE economy_balance SET wallet = ? WHERE guild_id = ? AND user_id = ?',
            (new_wallet, interaction.guild.id, interaction.user.id)
        )
        conn.commit()
        conn.close()
        
        embed = Embeds.success(
            "💼 Work",
            f"You worked as a {job} and earned ${earnings}!"
        )
        await interaction.response.send_message(embed=embed)
    
    @app_commands.command(name="pay")
    @app_commands.describe(
        member="Member to send coins to",
        amount="Amount to send"
    )
    async def pay(
        self,
        interaction: discord.Interaction,
        member: discord.Member,
        amount: int
    ):
        """Send coins to another member"""
        if amount <= 0:
            embed = Embeds.error("Invalid Amount", "Amount must be greater than 0")
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
        
        sender_wallet, sender_bank = self._get_or_create_account(interaction.guild.id, interaction.user.id)
        
        if sender_wallet < amount:
            embed = Embeds.error("Insufficient Funds", f"You only have ${sender_wallet}")
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
        
        receiver_wallet, receiver_bank = self._get_or_create_account(interaction.guild.id, member.id)
        
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        
        cursor.execute(
            'UPDATE economy_balance SET wallet = ? WHERE guild_id = ? AND user_id = ?',
            (sender_wallet - amount, interaction.guild.id, interaction.user.id)
        )
        cursor.execute(
            'UPDATE economy_balance SET wallet = ? WHERE guild_id = ? AND user_id = ?',
            (receiver_wallet + amount, interaction.guild.id, member.id)
        )
        
        conn.commit()
        conn.close()
        
        embed = Embeds.success(
            "💸 Payment Sent",
            f"Sent ${amount} to {member.mention}"
        )
        await interaction.response.send_message(embed=embed)

async def setup(bot: commands.Bot):
    await bot.add_cog(Economy(bot))
