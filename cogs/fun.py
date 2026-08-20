"""
Fun commands
"""

import discord
from discord.ext import commands
from discord import app_commands
from utils.embeds import Embeds
import random

class Fun(commands.Cog):
    """Fun commands"""
    
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    
    @app_commands.command(name="8ball")
    @app_commands.describe(question="Your question")
    async def eightball(
        self,
        interaction: discord.Interaction,
        question: str
    ):
        """Ask the magic 8 ball"""
        responses = [
            "Yes, definitely!", "No, not likely.", "Maybe...",
            "Ask again later.", "Don't count on it.", "It is certain.",
            "Absolutely!", "Very doubtful.", "Outlook good!", "Concentrate and ask again."
        ]
        
        response = random.choice(responses)
        embed = Embeds.neutral("🎱 Magic 8 Ball", f"Q: {question}\nA: {response}")
        
        await interaction.response.send_message(embed=embed)
    
    @app_commands.command(name="coinflip")
    async def coinflip(self, interaction: discord.Interaction):
        """Flip a coin"""
        result = random.choice(["Heads 👑", "Tails 🪙"])
        embed = Embeds.neutral("🪙 Coin Flip", f"Result: {result}")
        await interaction.response.send_message(embed=embed)
    
    @app_commands.command(name="roll")
    @app_commands.describe(sides="Number of sides (default: 6)")
    async def roll(
        self,
        interaction: discord.Interaction,
        sides: int = 6
    ):
        """Roll a dice"""
        if sides < 2:
            sides = 6
        
        result = random.randint(1, sides)
        embed = Embeds.neutral(f"🎲 Dice Roll (1-{sides})", f"Result: **{result}**")
        await interaction.response.send_message(embed=embed)
    
    @app_commands.command(name="ship")
    @app_commands.describe(
        member1="First member",
        member2="Second member"
    )
    async def ship(
        self,
        interaction: discord.Interaction,
        member1: discord.Member,
        member2: discord.Member
    ):
        """Rate the compatibility of two members"""
        percentage = random.randint(0, 100)
        embed = Embeds.neutral(
            "💕 Ship Rating",
            f"{member1.mention} + {member2.mention}\nCompatibility: **{percentage}%** {'❤️' if percentage > 50 else '💔'}"
        )
        await interaction.response.send_message(embed=embed)
    
    @app_commands.command(name="rps")
    @app_commands.describe(choice="Rock, Paper, or Scissors")
    async def rps(
        self,
        interaction: discord.Interaction,
        choice: str
    ):
        """Play Rock Paper Scissors with the bot"""
        choice = choice.lower()
        if choice not in ["rock", "paper", "scissors"]:
            embed = Embeds.error("Invalid choice", "Please choose: rock, paper, or scissors")
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
        
        bot_choice = random.choice(["rock", "paper", "scissors"])
        
        if choice == bot_choice:
            result = "It's a tie!"
        elif (choice == "rock" and bot_choice == "scissors") or \
             (choice == "paper" and bot_choice == "rock") or \
             (choice == "scissors" and bot_choice == "paper"):
            result = "You win!"
        else:
            result = "I win!"
        
        embed = Embeds.neutral(
            "✋ Rock Paper Scissors",
            f"You chose: {choice.capitalize()}\nI chose: {bot_choice.capitalize()}\n{result}"
        )
        await interaction.response.send_message(embed=embed)
    
    @app_commands.command(name="rate")
    @app_commands.describe(thing="What to rate")
    async def rate(
        self,
        interaction: discord.Interaction,
        thing: str
    ):
        """Rate something"""
        rating = random.randint(1, 10)
        stars = "⭐" * rating
        embed = Embeds.neutral(
            f"⭐ Rating: {thing}",
            f"Rating: {rating}/10\n{stars}"
        )
        await interaction.response.send_message(embed=embed)

async def setup(bot: commands.Bot):
    await bot.add_cog(Fun(bot))
