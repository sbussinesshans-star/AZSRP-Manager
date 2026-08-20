"""
User information commands
"""

import discord
from discord.ext import commands
from discord import app_commands
from utils.embeds import Embeds

class UserCommands(commands.Cog):
    """User information commands"""
    
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    
    @app_commands.command(name="roleinfo")
    @app_commands.describe(role="Role to check")
    async def roleinfo(
        self,
        interaction: discord.Interaction,
        role: discord.Role
    ):
        """Get role information"""
        embed = Embeds.info(
            f"Role: {role.name}",
            f"ID: {role.id}"
        )
        embed.add_field(name="Color", value=str(role.color), inline=True)
        embed.add_field(name="Position", value=str(role.position), inline=True)
        embed.add_field(name="Members", value=str(len(role.members)), inline=True)
        embed.add_field(name="Created", value=role.created_at.strftime('%Y-%m-%d'), inline=False)
        
        await interaction.response.send_message(embed=embed)
    
    @app_commands.command(name="membercount")
    async def membercount(self, interaction: discord.Interaction):
        """Get server member count"""
        guild = interaction.guild
        embed = Embeds.info(
            "Member Count",
            f"Total Members: {guild.member_count}"
        )
        embed.add_field(name="Humans", value=str(sum(1 for m in guild.members if not m.bot)), inline=True)
        embed.add_field(name="Bots", value=str(sum(1 for m in guild.members if m.bot)), inline=True)
        
        await interaction.response.send_message(embed=embed)
    
    @app_commands.command(name="joined")
    @app_commands.describe(member="Member to check")
    async def joined(
        self,
        interaction: discord.Interaction,
        member: discord.Member = None
    ):
        """Check when member joined"""
        member = member or interaction.user
        
        embed = Embeds.info(
            f"{member.name} Joined",
            f"Joined on: {member.joined_at.strftime('%Y-%m-%d %H:%M:%S')}"
        )
        embed.add_field(name="Account Created", value=member.created_at.strftime('%Y-%m-%d'), inline=False)
        
        await interaction.response.send_message(embed=embed)
    
    @app_commands.command(name="roles")
    async def roles(self, interaction: discord.Interaction):
        """List server roles"""
        guild = interaction.guild
        roles = sorted(guild.roles[1:], reverse=True)  # Skip @everyone
        
        role_list = "\n".join([f"{role.mention} - {len(role.members)} members" for role in roles[:25]])
        
        embed = Embeds.info("Server Roles", role_list)
        await interaction.response.send_message(embed=embed)

async def setup(bot: commands.Bot):
    await bot.add_cog(UserCommands(bot))
