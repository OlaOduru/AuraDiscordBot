import os
import string
import discord
from discord.ext import commands, tasks
import json
import asyncio
from itertools import cycle
import io
import chat_exporter


def get_prefix(client, message):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)


    return prefixes[str(message.guild.id)]

def load_json(filename):

  with open(filename, "r") as f:
    return json.load(f)

def save_json(o, fp):
  try:
    with open(fp, "w+") as f:
      json.dump(o, f, indent=4, sort_keys=True)
    return "Saved sucessfully."
  except Exception as e:
    return print("GG")

db = load_json("info.json")

db3 = load_json("nwords.json")

async def save_db():
    with open("info.json", "w+") as f:
        json.dump(db, f, indent=4)
    
def pure_id(s):

    return ''.join([x for x in s if x in string.digits])

client = commands.Bot(command_prefix=get_prefix, help_command=None, case_insensitive=True, intents=discord.Intents.all(), owner_ids=[345284566908403712])

@client.event
async def on_ready():
  await client.change_presence(activity=discord.Game("(*)"))
  print("Le bot is ready")

@client.event
async def on_guild_join(guild):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)

    prefixes[str(guild.id)] = '!'

    with open('prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent = 4)

@client.event
async def on_guild_remove(guild):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)

    prefixes.pop(str(guild.id))

    with open('prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent = 4)

@client.command()
async def test(ctx):
    for message in ctx.channel:
        await ctx.send(message)

@client.command()
@commands.is_owner()
async def load(ctx, *, extension):
    client.load_extension(f"cogs.{extension}")
    embed = discord.Embed(title = f"{extension} has been loaded!", color=0x00aeef)
    embed.set_footer(text= f"{ctx.author}", icon_url=ctx.author.avatar_url)
    await ctx.send(embed=embed)
    print(f"{extension} has been loaded")


@client.command()
@commands.is_owner()
async def unload(ctx, *,  extension):
    
    client.unload_extension(f"cogs.{extension}")
    embed = discord.Embed(title = f"{extension} has been unloaded!", color=0x00aeef)
    embed.set_footer(text= f"{ctx.author}", icon_url=ctx.author.avatar_url)
    await ctx.send(embed=embed)
    print(f"{extension} has been unloaded")

@client.command()
@commands.is_owner()
async def reload(ctx, *,  extension):
    client.unload_extension(f"cogs.{extension}")
    client.load_extension(f"cogs.{extension}")
    embed = discord.Embed(title = f"{extension} has been reloaded!", color=0x00aeef)
    embed.set_footer(text= f"{ctx.author}", icon_url=ctx.author.avatar_url)
    await ctx.send(embed=embed)
    print(f"{extension} has been reloaded")


for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        try:
            client.load_extension(f'cogs.{filename[:-3]}')
        except Exception as e:
            print(f"Error loading {filename}: {e}")

@load.error
async def load_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        if error.param.name == 'extension':
            embed = discord.Embed(title = "Please mention a valid cog", color=0x00aeef)
            embed.set_footer(text= f"{ctx.author}", icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed)

@unload.error
async def unnload_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        if error.param.name == 'extension':
            embed = discord.Embed(title = "Please mention a valid cog", color=0x00aeef)
            embed.set_footer(text= f"{ctx.author}", icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed)

@reload.error
async def reload_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        if error.param.name == 'extension':
            embed = discord.Embed(title = "Please mention a valid cog", color=0x00aeef)
            embed.set_footer(text= f"{ctx.author}", icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed)

client.run("")
