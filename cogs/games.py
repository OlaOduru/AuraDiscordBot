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

class gamescog(commands.Cog):

    def __init__(self, client):
        self.client = client

    def is_it_me(self, ctx):
        return ctx.author.id == 345284566908403712

    # Events
    
    @commands.Cog.listener()
    async def on_ready(self):
        print("Bot is online")
        print("Games loaded")  

    # Command
def setup(client):
    client.add_cog(gamescog(client))