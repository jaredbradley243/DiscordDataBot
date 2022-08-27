# Reddit
from dotenv import load_dotenv
from discord.ext import commands
import discord
import random
import os
import re
import requests
subreddits = ['dataisbeautiful']

limit = 100
timeframe = 'month'  # hour, day, week, month, year, all
lisiting = 'top'  # hot, new, controversial, top, rising

developer_user_id = 691791864516444160

def get_reddit(subreddit, listing, limit, timeframe):
    try:
        base_url = f'https://www.reddit.com/r/{subreddit}/{listing}.json?limit={limit}&t={timeframe}'
        request = requests.get(
            base_url, headers={'User-agent': 'TheDataBot'})
    except:
        print('An Error Occured')
    return request.json()


def get_posts(subreddits):
    reddit_posts = []
    temp = {}
    for subreddit in subreddits:
        reddit_subreddit_json = get_reddit(
            subreddit, lisiting, limit, timeframe)
        for i, posts in enumerate(reddit_subreddit_json['data']['children']):
            temp = {'url': reddit_subreddit_json["data"]["children"][i]["data"]["url_overridden_by_dest"],
                    'link': 'https://reddit.com' + reddit_subreddit_json["data"]["children"][i]["data"]["permalink"],
                    'subreddit': 'https://reddit.com/' + reddit_subreddit_json["data"]["children"][i]["data"]["subreddit_name_prefixed"], }
            if not any("i.redd.it" in s for s in temp.values()):
                if not any("/gallery/" in s for s in temp.values()):
                    reddit_posts.append(temp)
    return reddit_posts


reddit_posts = get_posts(subreddits=subreddits)

# bot.py
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)


@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')
    for guild in bot.guilds:
        if guild.name == GUILD:
            break
    print(
        f'{bot.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})\n'
    )

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

   
    triggers = ['!databot']
    if any(t in message.content.lower().split() for t in triggers):
            random.shuffle(reddit_posts)
            chosen_post = random.choice(reddit_posts)
            image_url = chosen_post['url']
            post_link = chosen_post['link']
            subreddit = chosen_post['subreddit']
            embed = discord.Embed(title="TheDataBot",
                                  description="Here is your data from: " + subreddit, color=0x00ff00)
            embed.add_field(name="Post Link", value=post_link, inline=False)
            embed.add_field(name="Image", value=image_url, inline=False)
            embed.add_field(name="Developer Credit", value=f"<@{developer_user_id}>", inline=False)
            await message.channel.send(embed=embed)
            await message.channel.send(image_url)
    elif message.content == 'raise-exception':
        raise discord.DiscordException
        
bot.run(TOKEN)
