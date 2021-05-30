import requests
import json
import discord
from discord.ext import commands
import random
import os
from datetime import datetime

client = commands.Bot(command_prefix="++")



@client.event
async def on_ready():
    print("Bot is has started running")
    await client.change_presence(activity=discord.Game(name="cmd: ++search"))

@client.command()
async def search(ctx, arg):
    search_term = str(arg).replace(" ", "%")
    base_url = "https://www.googleapis.com/blogger/v3/blogs/your_id/posts/search"
    complete_url = base_url + "?q=" + search_term + \
        "&key=your_token"
    response = requests.get(complete_url)
    result = response.json()

    now = datetime.now()

    current_time = now.strftime("%H:%M:%S")

    embed = discord.Embed(title="List of Search results",
                          description="Checked on " + f"{current_time}\n", color=0x349bfc)
    embed.set_author(name="Gaming Forecast")
    embed.set_thumbnail(url="https://www.gamingforecast.com/favicon.ico")
    for count, value in enumerate(result["items"]):
        title = result["items"][count]["title"]
        url = result["items"][count]["url"]
        embed.description = embed.description + f"{count + 1}. [{title}]({url})\n"
    embed.set_footer(text='This message will be deleted in 1 Hour.')

    await ctx.send(embed=embed, delete_after=3600.0)

client.run("your_token")
