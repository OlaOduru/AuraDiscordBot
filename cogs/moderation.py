import discord
from discord import user
from discord.ext import commands
from discord.utils import get
from urllib.request import urlopen
import json
import string
import random


global botversion
botversion = "0.1"
versiondetails = "Currently the bot is in the beta stage and Hanashi is still trying to get more ideas before releasing a full version. Make sure to use the suggestion command to help!"

def load_json(filename):

  with open(filename, "r") as f:
    return json.load(f)

def save_json(o, fp):
  try:
    with open(fp, "w+") as f:
      json.dump(o, f, indent=4, sort_keys=True)
    return "Saved sucessfully."
  except Exception as e:
    return f"Error saving, {e}."

db = load_json("info.json")

db3 = load_json("nwords.json")
dblevels = load_json("levels.json")

async def save_db():
    with open("info.json", "w+") as f:
        json.dump(db, f, indent=4)
    
def pure_id(s):
    return ''.join([x for x in s if x in string.digits])

class moderation(commands.Cog):

    def __init__(self, client):
        self.client = client

    def is_it_me(self, ctx):
        return ctx.author.id == 345284566908403712

    # Events
    
    @commands.Cog.listener()
    async def on_ready(self):
        print("Bot is online")
        print("Moderation loaded")


    """
    Clear command
    """
    @commands.command()
    async def clear(self, ctx, amount: int = None):
        if ctx.message.author.guild_permissions.manage_messages:
            if not amount:
                embed = discord.Embed(title=f"Give me a number of messages to clear.", color = discord.Color.blue())
                embed.set_footer(text=f"{ctx.author}", icon_url=ctx.author.avatar_url)
                
                await ctx.send(embed=embed, delete_after = 5)
            else:
                await ctx.channel.purge(limit = amount)
                
                clear_embed = discord.Embed(title=f"{amount} message(s) have been cleared!", color = discord.Color.blue())
                clear_embed.set_footer(text=f"{ctx.author}", icon_url=ctx.author.avatar_url)
                
                await ctx.send(embed=clear_embed, delete_after = 5)
        else:
            inform_embed = discord.Embed(title=f"You dont have permissions to use this command!", color = discord.Color.blue())
            inform_embed.set_footer(text=f"{ctx.author}", icon_url=ctx.author.avatar_url)
            
            await ctx.send(embed=inform_embed, delete_after = 5)


    """
    Kick command
    """
    @commands.command()
    async def kick(self, ctx, member: discord.Member, *, reason = "No reason was given"):
        if ctx.message.author.guild_permissions.kick_members:
            if member.id == 345284566908403712:
                inform_embed = discord.Embed(title=f"You cant kick my owner bruh", color = discord.Color.blue())
                inform_embed.set_footer(text=f"{ctx.author}", icon_url=ctx.author.avatar_url)
                await ctx.send(embed=inform_embed)
            else:
                if member.id == ctx.author.id:
                    inform_embed = discord.Embed(title=f"You cant kick yourself!", color = discord.Color.blue())
                    inform_embed.set_footer(text=f"{ctx.author}", icon_url=ctx.author.avatar_url)
                    await ctx.send(embed=inform_embed)
                else:
                    await member.kick(reason=reason)
                    await ctx.message.delete()
                    
                    kick_embed = discord.Embed(title=f"{member.display_name} was kicked!", color = discord.Color.blue())
                    kick_embed.set_footer(text=f"They were kicked by {ctx.author}", icon_url=ctx.author.avatar_url)
                    
                    await ctx.send(embed=kick_embed)
        else:
            inform_embed = discord.Embed(title=f"You dont have permissions to use this command!", color = discord.Color.blue())
            inform_embed.set_footer(text=f"{ctx.author}", icon_url=ctx.author.avatar_url)
            
            await ctx.send(embed=inform_embed)


    """
    Ban command
    """
    @commands.command()
    async def ban(self, ctx, member: discord.Member, *, reason = "No reason was given"):
        if ctx.message.author.guild_permissions.ban_members:
            if member.id == 345284566908403712:
                inform_embed = discord.Embed(title=f"You cant ban my owner bruh", color = discord.Color.blue())
                inform_embed.set_footer(text=f"{ctx.author}", icon_url=ctx.author.avatar_url)
                await ctx.send(embed=inform_embed)
            else:
                if member.id == ctx.author.id:
                    inform_embed =discord.Embed(title=f"You cant ban yourself!", color = discord.Color.blue())
                    inform_embed.set_footer(text=f"{ctx.author}", icon_url=ctx.author.avatar_url)
                    
                    await ctx.send(embed=inform_embed)
                else:
                    await member.ban(reason=reason)
                    await ctx.message.delete()

                    ban_embed = discord.Embed(title=f"{member.display_name} has been banned", description = f"{reason}", color=discord.Color.blue())
                    ban_embed.set_footer(text=f"They were banned by {ctx.author}", icon_url=ctx.author.avatar_url)
                    
                    await ctx.send(embed=ban_embed)
        else:
            inform_embed = discord.Embed(title=f"You dont have permissions to use this command!", color = discord.Color.blue())
            inform_embed.set_footer(text=f"{ctx.author}", icon_url=ctx.author.avatar_url)
            
            await ctx.send(embed=inform_embed)


    # Command
def setup(client):
    client.add_cog(moderation(client))