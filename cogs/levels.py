from os import name
import discord
from discord.ext import commands
from discord.utils import get
from urllib.request import urlopen
import json
import string


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

class levelscog(commands.Cog):

    def __init__(self, client):
        self.client = client

    def is_it_me(self, ctx):
        return ctx.author.id == 345284566908403712

    # Events
    
    @commands.Cog.listener()
    async def on_ready(self):
        print("Bot is online")
        print("Levels loaded")
    
    """
    @commands.Cog.listener()
    async def on_message(self, message):
        channel = self.client.get_channel(message.channel.id)
        
        username = message.author.display_name
        if int(message.author.id) == 886426953203216414:
            pass
        else:
            if str(message.author.id) not in dblevels["messages"]:
                dblevels["messages"][str(message.author.id)] = 0
                dblevels["levels"][str(message.author.id)] = 0
                save_json(dblevels, "levels.json")
                embed = discord.Embed(title=f"{username} Congrats on reaching level 1 ", color=discord.Color.blue())
                await channel.send(embed=embed)
            else:
                dblevels["messages"][str(message.author.id)] += 1
                save_json(dblevels, "levels.json")
        if int(message.author.id) == 886426953203216414:
            pass
        else:
            if dblevels["messages"][str(message.author.id)] % 25 == 0:

                dblevels["levels"][str(message.author.id)] += 1
                dblevels["messages"][str(message.author.id)] += 1
                save_json(dblevels, "levels.json")
                level = dblevels["levels"][str(message.author.id)]
                if dblevels["levels"][str(message.author.id)] == 1:
                    pass
                else:
                    embed = discord.Embed(title=f"{username}, You leveled up! You are now level {level}", color= discord.Color.blue())
                    await channel.send(embed=embed)
    """

    @commands.command()
    async def level(self, ctx, member: discord.Member = None):
        if not member:
            member = ctx.author

        member_name = member.display_name
        member_id = str(member.id)

        if member_id not in dblevels["levels"]:
            dblevels["levels"][member_id] = 1
            save_json(dblevels, "levels.json")
        level = dblevels["levels"][member_id]
        embed = discord.Embed(title=f"{member_name} is level {level}!", color = discord.Color.blue())
        await ctx.send(embed=embed)

    # Command
def setup(client):
    client.add_cog(levelscog(client))