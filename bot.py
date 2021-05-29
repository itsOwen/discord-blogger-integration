import requests
import json
import discord
import asyncio
import random
import os
from datetime import datetime

client = discord.Client()


@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game(name="cmd: ++meneed gamename"))


@client.event
async def on_message(message):
    if(message.author.id == your_bot_id_here):
        return
    search_term = message.content[9:len(message.content)].replace(" ", "%")
    base_url = "https://www.googleapis.com/blogger/v3/blogs/your_blog_id/posts/search"
    complete_url = base_url + "?q=" + search_term + \
        "&key=your_api_key_here"
    response = requests.get(complete_url)
    result = response.json()

    now = datetime.now()

    current_time = now.strftime("%H:%M:%S")

    embed = discord.Embed(title="List of Search results",
                          description="Checked on " + f"{current_time}\n", color=0x349bfc)
    embed.set_author(name="Gaming Forecast")
    embed.set_thumbnail(url="https://www.gamingforecast.com/favicon.ico")

    i = 0
    while i < len(result["items"]):
        title = result["items"][i]['title']
        url = result["items"][i]['url']
        embed.description = embed.description + f"{i+1}. [{title}]({url})\n"
        i = i+1
    embed.set_footer(text='This message will be deleted in 1 Hour.')

    if message.content.lower().startswith("++meneed"):
        await message.channel.send(embed=embed, delete_after=3600.0)

print("Bot is has started running")
client.run(' bot token ')
