from operator import mul
import discord
from discord import user
from discord import member
from discord import colour
from discord.embeds import Embed
from discord.ext import commands
from discord.utils import get
from urllib.request import urlopen
import json
import string
import random
from datetime import datetime, time
from time import time



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
dbidle = load_json("idle.json")
dbshop = load_json("shop.json")

async def save_db():
    with open("info.json", "w+") as f:
        json.dump(db, f, indent=4)
    
def pure_id(s):
    return ''.join([x for x in s if x in string.digits])

def pure_items(s):
    return ''.join([x for x in s if x not in string.digits])

def get_speed_multipier(memberid):
    value = 0
    for item in dbidle["inventory"][str(memberid)]:
        multiplier = dbshop["speed_multiply"][str(item)]
        value += multiplier
    return value

def get_coin_multipier(memberid):
    value = 0
    for item in dbidle["inventory"][str(memberid)]:
        multiplier = dbshop["coin_multiply"][str(item)]
        value += multiplier
    return value


def get_item_speed(item_name):
    for item in dbshop["speed_multiply"]:
        multiplier = dbshop["speed_multiply"][str(item_name)]
    return multiplier

def get_item_coin(item_name):
    for item in dbshop["coin_multiply"]:
        multiplier = dbshop["coin_multiply"][str(item_name)]
    return multiplier
            

class idlecog(commands.Cog):

    def __init__(self, client):
        self.client = client

    def is_it_me(self, ctx):
        return ctx.author.id == 345284566908403712

    # Events
    
    @commands.Cog.listener()
    async def on_ready(self):
        print("Bot is online")
        print("Idle Game loaded")  

    # Command
    @commands.command()
    @commands.cooldown(1, 60, commands.BucketType.user)
    async def mine(self, ctx):
        t = datetime.now().time()
        member_id = ctx.author.id
        seconds = int(time())

        if str(member_id) not in dbidle["time"]:
            dbidle["time"][str(member_id)] = str(seconds)
            dbidle["money"][str(member_id)] = 0
            dbidle["inventory"][str(member_id)] = []
            save_json(dbidle, "idle.json")
            inform_embed = discord.Embed(title="💤 Idle Miner", description=f"You have just begun your mining jounrey, you currently have $0",color=discord.Color.blue())
            await ctx.send(embed=inform_embed)
        else:
            multiplier = get_speed_multipier(str(member_id))
            coin_multiplier = get_coin_multipier(str(member_id))
            if multiplier == 0:
                multiplier = 1
        
            if coin_multiplier == 0:
                coin_multiplier = 1

            last_mine_time = dbidle["time"][str(member_id)]
            time_away = seconds - int(last_mine_time)
            coins = (time_away / 8) * int(multiplier)
            rounded = round(coins * coin_multiplier)
            dbidle["time"][str(member_id)] = str(seconds)
            dbidle["money"][str(member_id)] += rounded
            save_json(dbidle, "idle.json")
            value = dbidle["money"][str(member_id)]

            inform_embed = discord.Embed(title="💤 Idle Miner", description=f"While you were gone you mined ⛏️ {rounded} coins 💰 \n You were gone for {time_away} seconds",color=discord.Color.blue())
            inform_embed.add_field(name=f"Balance", value=f"Your new balance is ${value} 💰")
            inform_embed.add_field(name=f"Stats", value=f"With your current items, you have a speed multiplier of x{multiplier} \n And a coin multiplier of x{coin_multiplier}", inline=False)

            await ctx.send(embed=inform_embed)

    @commands.command()
    async def bal(self, ctx, member: discord.Member = None):
        if not member:
            member = ctx.author
        
        t = datetime.now().time()
        seconds = int(time())
        username = member.display_name
        member_id = str(member.id)

        if str(member_id) not in dbidle["time"]:
            inform_embed = discord.Embed(title=f"💤 Idle Miner", description =f"{username} has no money \n Start mining with the `*mine` ⛏️ command!", color=discord.Color.blue())
            await ctx.send(embed=inform_embed)
        else:
            value = dbidle["money"][str(member_id)]
            inform_embed = discord.Embed(title=f"💤 Idle Miner", description =f"{username} has ${value} 💰", color=discord.Color.blue())
            await ctx.send(embed=inform_embed)

    @commands.command()
    async def price(self, ctx, *, item):
        if str(item.lower()) not in dbshop["items"]:
            inform_embed = discord.Embed(title=f"That item does not exist", color=discord.Color.blue())
            await ctx.send(embed=inform_embed)
        else:
            price_item = dbshop["items"][str(item.lower())]
            speed = dbshop["speed_multiply"][str(item.lower())]
            coin_multiple = dbshop["coin_multiply"][str(item.lower())]
            inform_embed = discord.Embed(title=f"Shop", color=discord.Color.blue())
            inform_embed.add_field(name=f"{item.title()}", value=f"Costs: $**{price_item}** 💰", inline=False)
            inform_embed.add_field(name=f"Features", value=f"Speed: x**{speed} 💨** \n Coin Multiplier: **{coin_multiple}** 💥", inline= False)
            await ctx.send(embed=inform_embed)

    @commands.command()
    async def buy(self, ctx, *, item):
        price_item = dbshop["items"][str(item.lower())]
        member = ctx.author
        member_id = str(member.id)
        if str(item.lower()) not in dbshop["items"]:
            inform_embed = discord.Embed(title=f"That item does not exist", color=discord.Color.blue())
            await ctx.send(embed=inform_embed)
        else:
            if str(item.lower()) in dbidle["inventory"][str(member_id)]:
                inform_embed = discord.Embed(title=f"Purchase Error", description=f"You cant buy more than 1 of this item!", color = discord.Color.blue())
                await ctx.send(embed=inform_embed)
            else:
                if price_item > dbidle["money"][str(member_id)]:
                    await ctx.send("You dont have enough money to buy this item.")
                else:
                    dbidle["inventory"][str(member_id)].append(str(item.lower()))
                    save_json(dbidle, "idle.json")
                    dbidle["money"][str(member_id)] = dbidle["money"][str(member_id)] - price_item
                    save_json(dbidle, "idle.json")
                    new_balance = dbidle["money"][str(member_id)]
                    inform_embed = discord.Embed(title="Purchase Successful", colour = discord.Color.blue())
                    inform_embed.add_field(name=f"Item bought: {item.title()}", value=f"Price: $**{price_item}** 💰", inline=False)
                    inform_embed.add_field(name=f"New Balance", value=f"$**{new_balance}** 💰", inline=False)
                    await ctx.send(embed=inform_embed)

    @commands.command()
    async def pay(self ,ctx, member: discord.Member, *, amount: int):

        username = member.display_name
        member_id = str(member.id)
        balance = dbidle["money"][str(ctx.author.id)]

        if member_id == ctx.author.id:

            inform_embed = discord.Embed(title=f"You cant pay yourself!", color = discord.Color.blue())
            await ctx.send(embed=inform_embed)
        else:
            if amount < 0:
                inform_embed = discord.Embed(title=f"You cant send negative amounts!", color=discord.Color.blue())
                await ctx.send(embed=inform_embed)
            else:
                if amount > balance:
                    inform_embed = discord.Embed(title=f"You dont have that much money!", description = f"Your balance is {balance}", color = discord.Color.blue())
                    await ctx.send(embed=inform_embed)
                else:
                    if str(member_id) not in dbidle["money"]:
                        inform_embed = discord.Embed(title=f"{username} is not in the database!", description =f"Tell them to start mining with `*mine`!⛏️", color=discord.Color.blue())
                        await ctx.send(embed=inform_embed)
                    else:
                        dbidle["money"][str(ctx.author.id)] = dbidle["money"][str(ctx.author.id)] - amount
                        save_json(dbidle, "idle.json")
                        new_balance = dbidle["money"][str(ctx.author.id)]
                        dbidle["money"][str(member_id)] += amount
                        save_json(dbidle, "idle.json")
                        inform_embed = discord.Embed(title=f"Payment Successful", color=discord.Color.blue())
                        inform_embed.add_field(name=f"You sent ${amount} to {username}", value=f"Your new balance is: ${new_balance}💰")
                        await ctx.send(embed=inform_embed)
                



    @commands.command()
    async def sell(self, ctx, *, item):
        depreciation = random.randint(1,5)
        price_item = dbshop["items"][str(item.lower())]
        new_item_value = price_item / depreciation
        member = ctx.author
        member_id = str(member.id)
        if str(item.lower()) not in dbshop["items"]:
            inform_embed = discord.Embed(title=f"That item does not exist", color=discord.Color.blue())
            await ctx.send(embed=inform_embed)
        else:
            if str(item.lower()) not in dbidle["inventory"][str(member_id)]:
                inform_embed = discord.Embed(title=f"Sale Error", description = f"You dont own that item!", color = discord.Color.blue())
                await ctx.send(embed=inform_embed)
            else:
                dbidle["inventory"][str(member_id)].remove(str(item.lower()))
                save_json(dbidle, "idle.json")
                dbidle["money"][str(member_id)] = dbidle["money"][str(member_id)] + new_item_value
                save_json(dbidle, "idle.json")
                new_balance = dbidle["money"][str(member_id)]
                inform_embed = discord.Embed(title="Item Sale Successful", colour = discord.Color.blue())
                inform_embed.add_field(name=f"Item sold: {item.title()}", value=f"Sold for: $**{new_item_value}** 💰", inline=False)
                inform_embed.add_field(name=f"New Balance", value=f"$**{new_balance}** 💰", inline=False)
                await ctx.send(embed=inform_embed)

    @commands.command()
    async def inventory(self, ctx):
        slot = 0
        member = ctx.author
        username = member.display_name
        member_id = str(member.id)

        embed = discord.Embed(title=f"Your Inventory", color = discord.Color.blue())
        inform_embed = discord.Embed(title=f"Your Inventory", description=f"You have no items, maybe you should buy some?",color = discord.Color.blue())
        for item in dbidle["inventory"][str(member_id)]:
            slot += 1
            embed.add_field(name=f"Slot {slot}:", value = item.title())
        if not dbidle["inventory"][str(member_id)]:
            await ctx.send(embed=inform_embed)
        else:
            await ctx.send(embed=embed)
    @commands.command()
    async def shop(self, ctx):
        member = ctx.author
        username = member.display_name
        member_id = str(member.id)
        embed = discord.Embed(title=f"Idle Miner Shop 💰", color = discord.Color.blue())
        for item in dbshop["items"]:
            item_price = dbshop["items"][str(item.lower())]
            embed.add_field(name=f"{item.title()}", value=f"Costs: $**{item_price}** \n Speed Multiplier: **x{get_item_speed(str(item.lower()))}** \n Coin Multiplier **x{get_item_coin(str(item.lower()))}**")
        await ctx.send(embed=embed)
    
    @commands.group(invoke_without_command = True)
    @commands.is_owner()
    async def add(self, ctx):
        inform_embed = discord.Embed(title=f"Give me something to add!", color=discord.Color.blue())
        await ctx.send(embed=inform_embed)

    @add.command()
    @commands.is_owner()
    async def item(self, ctx, price, speed, coin, *, name):
        dbshop["items"][str(name.lower())] = int(price)
        dbshop["speed_multiply"][str(name.lower())] = float(speed)
        dbshop["coin_multiply"][str(name.lower())] = float(coin)
        save_json(dbshop, "shop.json")

        inform_embed = discord.Embed(title=f"Item Added", color = discord.Color.blue())
        inform_embed.add_field(name=f"Item with name {name.title()} has been added to the databse", value=f"Stats: \n Costs: **${price}** 💰\n Speed Multiplier: **x{speed}** \n Coin Multiplier: **x{coin}** 💥")
        await ctx.send(embed=inform_embed)

    @add.command()
    @commands.is_owner()
    async def balance(self, ctx, amount, member: discord.Member = None):
        if not member:
            member = ctx.author
        username = member.display_name
        member_id = str(member.id)

        dbidle["money"][str(member_id)] += int(amount)
        save_json(dbidle, "idle.json")
        inform_embed = discord.Embed(title=f"You have given {username} ${amount} 💰", color=discord.Color.blue())
        await ctx.send(embed=inform_embed)


    @commands.command()
    @commands.is_owner()
    async def remove(self, ctx, *, name):
        dbshop["items"].pop(str(name.lower()))
        dbshop["coin_multiply"].pop(str(name.lower()))
        dbshop["speed_multiply"].pop(str(name.lower()))
        save_json(dbshop, "shop.json")

        inform_embed = discord.Embed(title=f"{name.title()} has been removed from the databse!", color=discord.Color.blue())
        await ctx.send(embed=inform_embed)


    @commands.group(invoke_without_command = True)
    @commands.is_owner()
    async def daily(self, ctx):
        inform_embed = discord.Embed(title=f"You are missing some arguments! Try again.", color=discord.Color.blue())
        await ctx.send(embed=inform_embed)

    @daily.command()
    async def chest(self, ctx):

        t = datetime.now().time()
        seconds = int(time())
        reward = random.randint(1000, 10000)
        next_chest = seconds + 86400
        member = ctx.author
        member_id = str(member.id)
        if seconds < int(dbidle["daily_chest"][str(member_id)]):
            inform_embed = discord.Embed(title=f"You already opened your daily chest! Try again later.", color = discord.Color.blue())
            await ctx.send(embed=inform_embed)
        else:
            dbidle["daily_chest"][str(member_id)] = str(next_chest)
            dbidle["money"][str(member_id)] += reward
            save_json(dbidle, "idle.json")
            new_balance = dbidle["money"][str(member_id)]
            inform_embed = discord.Embed(title=f"Daily Chest", color=discord.Color.blue())
            inform_embed.add_field(name=f"Reward", value=f"You opened a chest and recieved {reward} coins!💰", inline=False)
            inform_embed.add_field(name=f"New Balance", value=f"Your new balance is: **{new_balance}**💰")
            await ctx.send(embed=inform_embed)

    @commands.command()
    async def beg(self, ctx):
        t = datetime.now().time()
        seconds = int(time())
        member = ctx.author
        member_id = str(member.id)
        chance = random.randint(1,3)
        amount = random.randint(1, 5000)
        next_beg = seconds + 1200
        if seconds < int(dbidle["beg_counter"][str(member_id)]):
            inform_embed = discord.Embed(title=f"You can only beg every 20 minutes! Try again later.", color = discord.Color.blue())
            await ctx.send(embed=inform_embed)
        else:
            if chance == 1:
                if dbidle["money"][str(member_id)] <= amount:
                    dbidle["beg_counter"][str(member_id)] = str(next_beg)
                    dbidle["money"][str(member_id)] = dbidle["money"][str(member_id)] = 0
                    save_json(dbidle, "idle.json")
                    inform_embed = discord.Embed(title=f"You got robbed!", description=f"You begged for money and got robbed!", color=discord.Color.blue())
                    inform_embed.add_field(name=f"Amount lost:", value=f"You lost ${amount}!💰", inline=False)
                    inform_embed.add_field(name=f"New Balance:", value=f"Your new balance is: **$0**💰", inline=False)
                    await ctx.send(embed=inform_embed)
                else:
                    dbidle["beg_counter"][str(member_id)] = str(next_beg)
                    dbidle["money"][str(member_id)] = dbidle["money"][str(member_id)] - amount
                    save_json(dbidle, "idle.json")
                    new_balance = dbidle["money"][str(member_id)]
                    inform_embed = discord.Embed(title=f"You got robbed!", description=f"You begged for money and got robbed!", color=discord.Color.blue())
                    inform_embed.add_field(name=f"Amount lost:", value=f"You lost ${amount}!💰", inline=False)
                    inform_embed.add_field(name=f"New Balance:", value=f"Your new balance is: **${new_balance}**💰", inline=False)
                    await ctx.send(embed=inform_embed)
            elif chance == 2:
                dbidle["beg_counter"][str(member_id)] = str(next_beg)
                inform_embed = discord.Embed(title=f"You got nothing!", description=f"No one was feeling genorous today...", color=discord.Color.blue())
                await ctx.send(embed=inform_embed)
            elif chance == 3:
                dbidle["beg_counter"][str(member_id)] = str(next_beg)
                dbidle["money"][str(member_id)] += amount
                save_json(dbidle, "idle.json")
                new_balance = dbidle["money"][str(member_id)]
                inform_embed = discord.Embed(title=f"You begged and got some money!", color=discord.Color.blue())
                inform_embed.add_field(name=f"You got:", value=f"$**{amount}**💰", inline=False)
                inform_embed.add_field(name=f"New Balance:", value=f"$**{new_balance}**💰")
                await ctx.send(embed=inform_embed)
    
    @commands.command(aliases=['lb','top'])
    async def leaderboard(self, ctx):
        for user in dbidle["money"]:
            intid = int(user)
            username = intid.display_name
            await ctx.send(username)
                
        
        






    @commands.command()
    async def get_time(self, ctx):
        await ctx.send(int(time()))

    



        


def setup(client):
    client.add_cog(idlecog(client))