import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
import decprice as DP


load_dotenv("D:/Luke/CV WORK/PYTHON application/New Text Document.env")


TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True  

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"We have logged in as {bot.user}")

@bot.command()
async def Watch(ctx,*args ):
    IsSummary = False
    result = DP.Main(args,IsSummary)
    await ctx.send(result)
@bot.command()
async def watch(ctx,*args ):
    IsSummary = False
    result = DP.Main(args,IsSummary)
    await ctx.send(result)
    
@bot.command()    
async def Summary(ctx,*args ):
    IsSummary = True
    result = DP.Main(args,IsSummary)
    await ctx.send(result)

@bot.command()    
async def summary(ctx,*args ):
    IsSummary = True
    result = DP.Main(args,IsSummary)
    await ctx.send(result)
    
#@bot.command()
#async def Guild(ctx, *, GuildName: str = None):
#   result = DP.GuildData(GuildName)
#   await ctx.send(result)
#   

bot.run(TOKEN)
