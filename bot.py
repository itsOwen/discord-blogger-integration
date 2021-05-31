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

Key = "#"  # Replace with your API key
BlogID = "#"  # Replace your BlogId here.

blog = build("blogger", "v3", developerKey=Key)

blog = build("blogger", "v3", developerKey=Key)

@client.event
async def on_ready():
    print("Bot is has started running")
    await client.change_presence(activity=discord.Game(name="cmd: ++search"))


@client.command()
async def search(ctx, arg):
    search_term = str(arg).replace(" ", "%")
    base_url = "https://www.googleapis.com/blogger/v3/blogs/" + BlogID + "/posts/search"
    complete_url = base_url + "?q=" + search_term + \
        "&key=" + Key
    response = requests.get(complete_url)
    result = response.json()

    now = datetime.now()

    current_time = now.strftime("%H:%M:%S")

    embed = discord.Embed(title="List of Search results",
                          description="Checked on " + f"{current_time}\n", color=0x349bfc)
    embed.set_author(name="Your Website Here")
    embed.set_thumbnail(url="https://www.gamingforecast.com/favicon.ico")
    try:
        for count, value in enumerate(result["items"]):
            title = result["items"][count]["title"]
            url = result["items"][count]["url"]
            embed.description = embed.description + \
                f"{count + 1}. [{title}]({url})\n"
        embed.set_footer(text='This message will be deleted in 1 Hour.')

        await ctx.send(embed=embed, delete_after=3600.0)
    except:
        await ctx.send("There is something wrong with the response.")

client.recentPosts = None


@tasks.loop(seconds=5.0)
async def fetchUpdates():
    posts = blog.posts().list(blogId=BlogID).execute()
    postsList = posts["items"]
    postTime = postsList[0]["published"]
    if not client.recentPosts:
        client.recentPosts = postTime
    elif client.recentPosts != postTime:
        titleValue = str(posts["items"][0]["title"])
        urlValue = str(posts["items"][0]["url"])
        channel = client.get_channel(your_Channel_id_here)  # Add channel ID
        embed = discord.Embed(title="New posts to the blog!",
                              description=f"[{titleValue}]({urlValue})")
        embed.set_author(name="Your Website Name")
        embed.set_thumbnail(url="https://www.gamingforecast.com/favicon.ico")
        await channel.send(embed=embed)
        client.recentPosts = postTime

fetchUpdates.start()

client.run("#") # Your discord bot token here
