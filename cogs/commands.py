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

class basiccommands(commands.Cog):

    def __init__(self, client):
        self.client = client

    def is_it_me(self, ctx):
        return ctx.author.id == 345284566908403712

    # Events
    
    @commands.Cog.listener()
    async def on_ready(self):
        print("Bot is online")
        print("Commands loaded")
    
    
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        embed = discord.Embed(title = "❌ Error ❌", color=0x00aeef)
        embed.set_footer(text= f"{ctx.author}", icon_url=ctx.author.avatar_url)

        if isinstance(error, commands.CommandNotFound):
            embed.description = "That command does not exist"
        else:
            embed.description = str(error)

        await ctx.send(embed=embed)

    @commands.command()
    async def pfp(self ,ctx, member: discord.Member = None):
        if not member:
            member = ctx.author.id
            
        member_name = member.display_name
        profile_pic = member.avatar_url
        embed = discord.Embed(title=f"{member_name}'s profile picture", color = discord.Color.blue())
        embed.set_image(url=profile_pic)
        await ctx.send(embed=embed)

    @commands.command()
    async def embed(self, ctx, url = None):
        await ctx.message.delete()
        member = ctx.author
        member_name = member.display_name
        if not url:
            embed = discord.Embed(title="Give me a URL to embed.", color = discord.Color.blue())
            await ctx.send(embed=embed)
        
        embed = discord.Embed(title=f"{member_name}'s embed", color = discord.Color.blue())
        embed.set_footer(text="fuck steven for not allowing embeds")
        embed.set_image(url=url)
        await ctx.send(embed=embed)
    
    @commands.command()
    async def help(self, ctx):
        member = ctx.author
        member_name = member.display_name
        help_embed = discord.Embed(title=f"Aura Commands", color = discord.Color.blue())
        help_embed.add_field(name=f"Basic Commands", value=f"`embed` --- Pass in a url to embad a picture through the bot. \n" +
                                                        "`pfp` --- Get the profile picture of a mentioned user, or yourself. \n", inline=False)
        help_embed.add_field(name=f"Moderation", value=f"`ban` --- Ban a mentioned user \n" +
                                                        "`clear`--- Clear a given amount of messages in a channel. \n" +
                                                        "`kick` --- Kick a mentioned user from the server", inline=False)
        help_embed.add_field(name=f"Idle Mining", value=f"`mine` --- Start mining coins idely through the fun built in game! \n" +
                                                        "`balance` --- Check how many coins you have \n"+
                                                        "`price` --- Check the price of an item in the shop \n"+
                                                        "`buy` --- Buy an item in the shop \n"+
                                                        "`sell` --- Sell an item in your inventory (Chance of value depreciation) \n"+
                                                        "`inventory` --- Check the current items in your inventory \n"+
                                                        "`shop` --- View all the possible items you can buy \n"+
                                                        "`pay` --- Pay a given user a certain amount of money \n" +
                                                        "`daily chest` --- Open up a daily chest and get a random amount of money! \n" +
                                                        "`beg` --- Beg for money! Be careful, you might get robbed! ", inline=False)
        help_embed.set_footer(text=f"Requested by {member_name}", icon_url=ctx.author.avatar_url)

        
        await ctx.send(embed=help_embed)

    
    @commands.command()
    async def loop(self, ctx):
        counter = 0
        #channel = ctx.channel.id

        messages = await ctx.channel.history(limit=None).flatten()
        print(len(messages))

        for message in messages:
            counter += 1
            if message.author.id != 345284566908403712:
                pass
            else:
                if len(message.attachments) > 0:
                    await message.attachments[0].save(fp=f"{counter}.png")
                    print("Downloaded An Image")
                    await message.delete()


    @commands.command()
    async def testloop(self, ctx):
        counter = 0
        channel_ids = [871611203724673036]

        for id in channel_ids:
            channel = discord.utils.get(ctx.guild.text_channels, id=id)
            messages = await channel.history(limit=None).flatten()

            for message in messages:
                counter +=1
                if message.author.id != 345284566908403712:
                    pass
                else:
                    if len(message.attachments) > 0:
                        await message.attachments[0].save(fp=f"{counter}.png")
                        print("Downloaded An Image")
                        await message.delete()
        
        print("Done")

    

    # Command
def setup(client):
    client.add_cog(basiccommands(client))