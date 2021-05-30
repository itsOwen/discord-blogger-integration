import requests
import json
import discord
from discord.ext import commands
from discord.ext import tasks
import random
import os
from datetime import datetime
from googleapiclient.discovery import build

client = commands.Bot(command_prefix="++")

Key = "your_api_key" # Replace with your api key
BlogID = "your_blog_id" #Replace 

blog = build("blogger", "v3", developerKey=Key)

@client.event
async def on_ready():
    print("Bot has started running")
    await client.change_presence(activity=discord.Game(name="cmd: ++search"))

@client.command()
async def search(ctx, arg):
    search_term = str(arg).replace(" ", "%")
    base_url = "https://www.googleapis.com/blogger/v3/blogs/your_id/posts/search" # Replace your_id
    complete_url = base_url + "?q=" + search_term + \
        "&key=your_key" # Replace your_key
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

client.recentPosts = None

@tasks.loop(seconds=5.0)
async def fetchUpdates():
    posts = blog.posts()
    posts = posts.list(blogId=BlogID).execute()         
    if not client.recentPosts:
        client.recentPosts = posts
        print("no recents")
    elif client.recentPosts != posts:
        set1 = len(posts["items"])
        set2 = len(client.recentPosts["items"])
        value = set1 - set2
        if value < 0:
            client.recentPosts = posts
            value = 0
        elif value > 0:
            titleValue = str(posts["items"][0]["title"])
            urlValue = str(posts["items"][0]["url"])
            channel = client.get_channel(announcement_channel_id) # Replace
            embed = discord.Embed(title="New posts to the blog!", description=f"[{titleValue}]({urlValue})")
            embed.set_author(name="Gaming Forecast")
            embed.set_thumbnail(url="https://www.gamingforecast.com/favicon.ico")
            await channel.send(embed=embed)
            value = 0
            client.recentPosts = posts

fetchUpdates.start()


client.run("your_token") # Replace
