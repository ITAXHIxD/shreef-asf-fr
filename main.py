import asyncio
import io
import json
import os
import random
import string
import traceback
from threading import Thread
import venv
import discord
from discord.ext.commands.core import bot_has_any_role
import requests
import youtube_dl
from discord.ext import commands
from discord.ext.commands import bot
from flask import Flask
import typing
from discordemoji import *
from emoji_utils import *
import time
import datetime
import aiohttp
from quotes import *
from discord_webhook import DiscordWebhook, DiscordEmbed
from PIL import Image, ImageDraw, ImageFont
import sys


error_webhook = os.environ['error_url']
dm_webhook = os.environ['dm_url']
start_hook = os.environ['start_url']


async def create_session():
  return aiohttp.ClientSession()


# Install ffmpeg on Replit


def is_server_owner():

  async def check(ctx):
    return ctx.guild and ctx.guild.owner == ctx.author.id

  return commands.check(check)


intents = discord.Intents.default()
intents.message_content = True
intents.typing = False
intents.presences = False

# Owner's Discord ID
owner = [1013851779886231685, 1095605756008611900, 1171117313945243708, 1152510743032377405, 1111276567038005309]

# Allowed User's
allowed_users = [1013851779886231685, 1095605756008611900, 1171117313945243708,1152510743032377405]


class CustomContext(commands.Context):

  @property
  def message(self):
    # Override the message.content property to always include the bot's mention at the beginning
    if not self._message.content.startswith(f'<@{self.bot.user.id}> '):
      self._message.content = f'<@{self.bot.user.id}> {self._message.content}'
    return self._message


class MyBot(commands.Bot):

  def __init__(self):
    super().__init__(command_prefix=self.get_prefix, self_bot=True)


@commands.before_invoke
async def get_prefix(self, message):
  user_id = message.author.id
  if user_id in allowed_users:
    self.message.content = f'{get_prefix}{message}'
    return self.message
  else:
    return '!!'


# Define a global dictionary to store guild-specific prefixes
prefixes = {}


def get_prefix(bot, message):
  # Check if the guild ID exists in the prefixes dictionary
  guild_id = str(message.guild.id)
  if guild_id in prefixes:
    return prefixes[guild_id]
  else:
    # If not, use a default prefix
    return "!!"


# Load prefixes from the JSON file on bot startup
def load_prefixes():
  try:
    with open("prefixes.json", "r") as f:
      global prefixes
      prefixes = json.load(f)
  except FileNotFoundError:
    print("No prefixes file found. Using default prefixes.")


load_prefixes()

# Example usage:
# In your bot setup:
# bot = commands.Bot(command_prefix=get_prefix)

# Make sure to handle the setup of the command prefix properly when initializing your bot.

ALLOWED_USER_IDS = [
    1013851779886231685, 1013851779886231685, 1095605756008611900,
    1171117313945243708,1152510743032377405
]

yellowish = 0xe7c770
prefix = "!!"
# In your bot setup, set the custom help command

bot = commands.Bot(command_prefix=["!!"], intents=intents)
bot.launch_time = time.time()
app = Flask(__name__)
bot.http_session = aiohttp.ClientSession()

# Suppress noise about console usage from errors
youtube_dl.utils.bug_reports_message = lambda: ''

tenor_api_key = "AIzaSyCzj4UzAYXEHD0PyxTGfkcSazl0PjcHZPQ"

giphy_api_key = "ToFp55XoqCKDI6ZxmZ3coN4LseCexs05"


@bot.event
async def on_ready():
  for i in range(7):
    print(".")
    time.sleep(0.1)
  print(f'''Logged in as {bot.user.name}''')
  print(f"lesh goo.....🙃")
  activity = discord.Activity(
      name=f'with {bot.command_prefix}help with {len(bot.commands)}cmds',
      type=discord.ActivityType.playing,
      details='A bot by itaxhi_xd',
      state=f'Serving {len(bot.commands)} commands with {bot.command_prefix}',
      assets={
          'large_image': 'https://cdn.discordapp.com/avatars/116746460262.png',
          'large_text': 'shreef asf',
          'small_image':
          'https://cdn.discordapp.com/emojis/1058245384251641916.png ',
          'small_text': 'ITAXHI_xD'
      })

  #webhook send
  webhook = DiscordWebhook(url=start_hook)
  embed = DiscordEmbed(title="shreef asf reports:",
                       description=f"bot started {uwudance_emoji}",
                       color=(yellowish))
  embed.set_timestamp()
  webhook.add_embed(embed)
  response = webhook.execute()


# print('Bot Commands:')

@bot.event
async def on_ready():
  channel = bot.get_channel(1195042340490973204)
  time.sleep(1800)
  await channel.send("!!restart")

#24/7 time spam
@bot.event
async def on_ready():
  channel = bot.get_channel(1195042340490973204)
  await channel.send("bot started lesh go")
  while True:
    utc_now = datetime.datetime.utcnow()
    # Add the UTC offset for India Standard Time (IST)
    rtime = utc_now + datetime.timedelta(hours=5, minutes=30)
    await channel.send(
        rtime.strftime(''' ``
........................
time = %H:%M:%S
------------------------
date = %d-%m-%Y 
........................``'''))
    time.sleep(0.5)


# for command in bot.commands:
#    print(command.name)


@bot.event
async def on_disconnect():
  channel = bot.get_channel(1195042340490973204)
  await channel.send(f"bot disconnected {sad_cry}")
  await bot.http_session.close()


@bot.event
async def on_command_error(ctx, error):
  if isinstance(error, commands.MissingPermissions):
    # Check if the error is due to missing permissions
    missing_permissions = ', '.join(error.missing_permissions)
    await ctx.send(
        f"Sorry, you don't have the required permissions ({missing_permissions}) to run this command."
    )
  elif isinstance(error, commands.MissingRequiredArgument):
    # Check if the error is due to missing required arguments
    await ctx.send(
        "Missing required arguments. Please provide all the necessary arguments."
    )
  elif isinstance(error, commands.CommandNotFound):
    # Handle command not found error
    await ctx.send("Command not found. Please use a valid command.")


#  elif isinstance(error, commands.cooldown):
# Handle cooldown error
#    await ctx.send(f"you are on cooldown for {error.retry_after: 2f} seconds.")

  else:
    # Handle other errors by printing the error to console
    webhook = DiscordWebhook(url=error_webhook)
    embed = DiscordEmbed(title="error found:",
                         description=f"**{error}**",
                         color=(yellowish))
    embed.set_timestamp()
    webhook.add_embed(embed)
    response = webhook.execute()
    print(error)


@bot.event
async def on_message(message):
  if isinstance(message.channel,
                discord.DMChannel) and message.author != bot.user:
    print(f"DM from {message.author}: {message.content}")
    webhook = DiscordWebhook(url=dm_webhook)
    embed = DiscordEmbed(title="direct message found",
                         description=f"DM from {message.author}",
                         value=f"{message.content}",
                         color=(yellowish))
    embed.set_timestamp()
    webhook.add_embed(embed)
    response = webhook.execute()


@bot.event
async def on_message(message):
  if message.author.bot:
    return

  # Check if the message content matches any autoresponder trigger
  server_id = str(message.guild.id)
  if (server_id in autoresponders_by_server
      and message.content.lower() in autoresponders_by_server[server_id]):
    response = autoresponders_by_server[server_id][message.content.lower()]
    await message.channel.send(response)

  # Check if the response contains the trigger for reaction
  if "{react:" in message.content and ":}" in message.content:
    # Extract the emoji from the response
    start_index = message.content.find("{react:") + len("{react:")
    end_index = message.content.find(":}", start_index)
    emoji_text = message.content[start_index:end_index].strip()

    # Check if the emoji_text is an emoji name
    emoji = discord.utils.get(bot.emojis, name=emoji_text)

    # If not, check if it's a custom emoji (assuming it starts and ends with colons)
    if not emoji and emoji_text.startswith(":") and emoji_text.endswith(":"):
      emoji_text = emoji_text[1:-1]
      emoji = discord.utils.get(bot.emojis, name=emoji_text)

    # If it's still not found, assume emoji_text is a Unicode emoji
    if not emoji:
      emoji = emoji_text

    # React to the original message if the emoji is found
    await message.add_reaction(emoji)

  if isinstance(message.channel,
                discord.DMChannel) and message.author != bot.user:
    print(f"DM from {message.author}: {message.content}")
    webhook = DiscordWebhook(url=dm_webhook)
    embed = DiscordEmbed(title="direct message found",
                         description=f"DM from   {message.author}",
                         value=f"{message.content}",
                         color=(yellowish))
    embed.set_timestamp()
    webhook.add_embed(embed)
    response = webhook.execute()

  # Continue with other on_message event functionality
  await bot.process_commands(message)


def format_help(help_text):

  return help_text

# Remove default 'help' command
bot.remove_command('help')


# Custom help command
@bot.command(name='help')
async def send_help(ctx):
  embed = discord.Embed(title="Bot Commands",
                        description=f'''
                        Here are my commands.
                        use {prefix} to use this.
                        
                        ''',
                        color=discord.Color(0xe7c770))

  # Exclude commands with "bot owner only" permission
  commands_list = [
      cmd for cmd in bot.commands if not hasattr(cmd,'owner_only')
  ]

  # Sort commands alphabetically
  commands_list = sorted(commands_list, key=lambda x: x.name.lower())

  page = 1
  per_page = 10  # Two rows with 7 commands per row
  total_pages = (len(commands_list) + per_page - 1) // per_page

  start_index = (page - 1) * per_page
  end_index = min(start_index + per_page, len(commands_list))
  commands_page = commands_list[start_index:end_index]

  for i in range(0, len(commands_page), 2):
    row = commands_page[i:i + 2]
    if len(row) == 1:
      embed.add_field(name=f"{prefix}{row[0].name}",
                      value=f"** **",
                      inline=True)
    else:
      embed.add_field(name=f"{prefix}{row[0].name}",
                      value=f"** **",
                      inline=True)
      embed.add_field(name=f"{prefix}{row[1].name}",
                      value=f"** **",
                      inline=True)

  embed.set_footer(text=f"Page {page}/{total_pages}")
  embed.set_author(name="shreef asf", icon_url=bot.user.avatar.url)
  embed.set_thumbnail(url=bot.user.avatar.url)
  embed.set_footer(text=f"Requested by {ctx.author.name}",
                   icon_url=ctx.author.avatar.url)

  message = await ctx.send(embed=embed)
  await message.add_reaction(previous_emoji)
  await message.add_reaction(next_emoji)

  def check(reaction, user):
    return user == ctx.author and str(
        reaction.emoji) in [previous_emoji, next_emoji]

  while True:
    try:
      reaction, user = await bot.wait_for("reaction_add",
                                          timeout=60,
                                          check=check)
      if str(reaction.emoji) == previous_emoji:
        page = (page - 1) % total_pages
      elif str(reaction.emoji) == next_emoji:
        page = (page + 1) % total_pages

      start_index = (page - 1) * per_page
      end_index = min(start_index + per_page, len(commands_list))
      commands_page = commands_list[start_index:end_index]

      embed.clear_fields()
      for i in range(0, len(commands_page), 2):
        row = commands_page[i:i + 2]
        if len(row) == 1:
          embed.add_field(name=f"{prefix}{row[0].name}",
                          value=format_help(row[0].help),
                          inline=True)
        else:
          embed.add_field(name=f"{prefix}{row[0].name}",
                          value=format_help(row[0].help),
                          inline=True)
          embed.add_field(name=f"{prefix}{row[1].name}",
                          value=format_help(row[1].help),
                          inline=True)

      embed.set_footer(text=f"Page {page}/{total_pages}")
      await message.edit(embed=embed)
      await message.remove_reaction(reaction, user)
    except asyncio.TimeoutError:
      await message.clear_reactions()
      break


@bot.command(name='ownerhelp', aliases=['ohelp'], owner_only=True)
@commands.is_owner()
async def owner_help(ctx):
  prefix = ctx.prefix
  embed = discord.Embed(
      title="Owner Commands",
      description="Here are commands only available to the bot owner.",
      color=discord.Color(0xe7c770))

  # Include only commands with "owner only" permission
  owner_commands = [cmd for cmd in bot.commands if hasattr(cmd, 'owner_only')]

  # Sort owner commands alphabetically
  owner_commands = sorted(owner_commands, key=lambda x: x.name.lower())

  page = 1
  per_page = 14  # Two rows with 7 commands per row
  total_pages = (len(owner_commands) + per_page - 1) // per_page

  start_index = (page - 1) * per_page
  end_index = min(start_index + per_page, len(owner_commands))
  commands_page = owner_commands[start_index:end_index]

  for cmd in commands_page:
    embed.add_field(name=f"{prefix}{cmd.name}",
                    value=format_help(cmd.help),
                    inline=False)

  embed.set_footer(text=f"Page {page}/{total_pages}")
  embed.set_author(name="shreef asf", icon_url=bot.user.avatar.url)
  embed.set_footer(text=f"Requested by {ctx.author.name}",
                   icon_url=ctx.author.avatar.url)

  message = await ctx.send(embed=embed)
  await message.add_reaction(previous_emoji)
  await message.add_reaction(next_emoji)

  def check(reaction, user):
    return user == ctx.author and str(
        reaction.emoji) in [previous_emoji, next_emoji]

  while True:
    try:
      reaction, user = await bot.wait_for("reaction_add",
                                          timeout=60,
                                          check=check)
      if str(reaction.emoji) == previous_emoji:
        page = (page - 1) % total_pages
      elif str(reaction.emoji) == next_emoji:
        page = (page + 1) % total_pages

      start_index = (page - 1) * per_page
      end_index = min(start_index + per_page, len(owner_commands))
      commands_page = owner_commands[start_index:end_index]

      embed.clear_fields()
      for cmd in commands_page:
        embed.add_field(name=f"{prefix}{cmd.name}",
                        value=format_help(cmd.help),
                        inline=False)

      embed.set_footer(text=f"Page {page}/{total_pages}")
      await message.edit(embed=embed)
      await message.remove_reaction(reaction, user)
    except asyncio.TimeoutError:
      await message.clear_reactions()
      break


# Example owner-only command


@bot.command(name="guess", description="Guess the number game")
async def guess_command(ctx):
  await ctx.send("I'm thinking of a number between 1 and 10. Take a guess!")

  def check(m):
    return m.author == ctx.author and m.channel == ctx.channel

  answer = random.randint(1, 10)

  try:
    guess = await bot.wait_for("message", check=check, timeout=10.0)
    if not guess.content.isdigit():
      await ctx.send("Invalid input. Please enter a number.")
      return

    if int(guess.content) == answer:
      await ctx.send("You guessed it correctly!")
    else:
      await ctx.send(
          f"Wrong guess. The number was {answer}. Better luck next time!")
  except asyncio.TimeoutError:
    await ctx.send("Time's up! You took too long to guess.")


@bot.command(name="dance", description="Sends a dance GIF")
async def dance_command(ctx):
  # Make a request to Giphy API to get a random GIF of anime dance
  url = f"https://api.giphy.com/v1/gifs/random?api_key={giphy_api_key}&tag=anime-dance"
  response = requests.get(url)
  data = json.loads(response.text)

  if response.status_code == 200 and "data" in data:
    gif_url = data["data"].get("images", {}).get("original", {}).get("url")

    # Send the GIF URL to the Discord channel
    if gif_url:
      await ctx.send(gif_url)
  else:
    await ctx.send("Failed to fetch the dance GIF.")


@bot.command(name="random", description="Sends a random GIF")
async def random_command(ctx):
  # Make a request to Giphy API to get a random GIF of anime laughter
  url = f"https://api.giphy.com/v1/gifs/random?api_key={giphy_api_key}&tag=anime"
  response = requests.get(url)
  data = json.loads(response.text)

  if response.status_code == 200 and "data" in data:
    gif_url = data["data"].get("images", {}).get("original", {}).get("url")
    if gif_url:
      await ctx.send(gif_url)
    else:
      await ctx.send("Sorry, I couldn't find an random GIF at the moment.")
  else:
    await ctx.send("Sorry, I couldn't find an random GIF at the moment.")


@bot.command(name="ghost", description="Sends a ghost GIF")
async def ghost_command(ctx):
  # Make a request to Giphy API to get a random GIF of anime laughter
  url = f"https://api.giphy.com/v1/gifs/random?api_key={giphy_api_key}&tag=ghost+bhoot+aatma"
  response = requests.get(url)
  data = json.loads(response.text)

  if response.status_code == 200 and "data" in data:
    gif_url = data["data"].get("images", {}).get("original", {}).get("url")
    if gif_url:
      await ctx.send(gif_url)
    else:
      await ctx.send("Sorry, I couldn't find an ghost GIF at the moment.")
  else:
    await ctx.send("Sorry, I couldn't find an ghost GIF at the moment.")


@bot.command(name="kill", description="Sends a kill GIF")
async def kill_command(ctx):
  # Make a request to Giphy API to get a random GIF of anime laughter
  url = f"https://api.giphy.com/v1/gifs/random?api_key={giphy_api_key}&tag=anime+killing+scene+anime+murder+scene"
  response = requests.get(url)
  data = json.loads(response.text)

  if response.status_code == 200 and "data" in data:
    gif_url = data["data"].get("images", {}).get("original", {}).get("url")
    if gif_url:
      await ctx.send(gif_url)
    else:
      await ctx.send("Sorry, I couldn't find an kill GIF at the moment.")
  else:
    await ctx.send("Sorry, I couldn't find an kill GIF at the moment.")


@bot.command(name="roll",
             description="Roll and get a random number between 1-10")
async def roll_command(ctx):
  dice = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
  result = random.choice(dice)
  await ctx.send(f"You rolled a {result}!")


@bot.command(
    name="ping",
    description="Get the bot's latency."  # Put your server's ID here.
)
async def ping_command(ctx):
  random_member = random.choice(ctx.guild.members)
  icon_url = random_member.avatar._url
  latency = bot.latency * 1000  # Convert to milliseconds
  embed = discord.Embed(title="Pong!",
                        description=f"Latency: {latency:.2f}ms",
                        color=discord.Color(0xe7c770))
  embed.set_footer(text=f"{random_member.name}", icon_url=str(icon_url))
  embed.set_thumbnail(url=str(icon_url))
  embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar._url)
  await ctx.send(embed=embed)


def check_user_id(ctx):
  return str(ctx.author.id) in allowed_user_ids


@bot.command(name="say", description="Make the bot say something")
@commands.has_permissions(manage_messages=True)
async def say_command(ctx, *, message):
  await ctx.send(message)
  await ctx.message.delete()


@bot.command(name="ship", description="Ship two users")
async def ship_command(ctx,
                       user1: typing.Optional[discord.User] = None,
                       user2: typing.Optional[discord.User] = None):
  if not user1 and not user2:
    # If no users are mentioned, ship the message author with a random user
    members = ctx.guild.members
    user1, user2 = ctx.author, random.choice(members)
  elif user1 and not user2:
    # If only one user is mentioned, ship the message author with that mentioned user
    user2 = ctx.author

  # Calculate ship percentage
  percentage = random.randint(0, 100)

  # Combine names to create ship name
  ship_name = user1.name[:len(user1.name) // 2] + user2.name[len(user2.name) //
                                                             2:]

  # Get avatars
  avatar1_url = user1.avatar_url_as(size=1024)
  avatar2_url = user2.avatar_url_as(size=1024)

  # Create the ship embed
  embed = discord.Embed(title="Shipping", color=discord.Color(0xe7c770))
  embed.set_footer(text=f"Requested by {ctx.author.name}",
                   icon_url=ctx.author.avatar_url)
  embed.add_field(name="Ship Name", value=ship_name)
  embed.add_field(name="Ship Percentage", value=f"{percentage}%")
  embed.set_thumbnail(url=avatar1_url)
  embed.set_image(
      url=
      "https://cdn.discordapp.com/attachments/858900678247456778/858901609254768660/heart.png"
  )
  embed.set_footer(text=f"{user1.name}'s Avatar", icon_url=avatar1_url)
  embed.set_thumbnail(url=avatar2_url)
  embed.set_footer(text=f"{user2.name}'s Avatar", icon_url=avatar2_url)

  await ctx.send(embed=embed)


@ship_command.error
async def ship_command_error(ctx, error):
  if isinstance(error, commands.BadArgument):
    await ctx.send("Invalid user. Please mention valid users.")


@bot.command(name="nickname",
             aliases=['nick'],
             description="Change the nickname of yourself or a mentioned user")
async def nickname_command(ctx,
                           member: discord.Member = None,
                           *,
                           new_nickname: str = None):
  if member is None:
    member = ctx.author

  if new_nickname is None:
    await member.edit(nick=None)

  try:
    await member.edit(nick=new_nickname)
    await ctx.send(
        f"The nickname of {member.mention} has been changed to {new_nickname}.{updown}"
    )
  except discord.Forbidden:
    await ctx.send(f"I don't have permission to change the nickname.{sad_cry}")


@nickname_command.error
async def nickname_command_error(ctx, error):

  if isinstance(error, commands.BadArgument):
    await ctx.send("Invalid user. Please mention a valid user.")


@bot.command(name="serverinfo",
             aliases=["si"],
             description="Display server information")
async def serverinfo_command(ctx):
  guild = ctx.guild
  embed = discord.Embed(title="Server Information",
                        color=discord.Color(0xe7c770))
  embed.set_thumbnail(url=guild.icon._url)  # Set server icon as thumbnail
  embed.set_image(url=guild.banner._url)
  embed.add_field(name="Server Name", value=guild.name, inline=False)
  embed.add_field(name="Server ID", value=guild.id, inline=False)
  embed.add_field(name="Owner", value=guild.owner, inline=False)
  embed.add_field(name="Region", value=guild.region, inline=False)
  embed.add_field(name="Total Members", value=guild.member_count, inline=False)
  embed.add_field(name="Creation Date",
                  value=guild.created_at.strftime("%Y-%m-%d"),
                  inline=False)
  embed.set_footer(text=f"Requested by {ctx.author.name}",
                   icon_url=ctx.author.avatar._url)
  await ctx.send(embed=embed)


@bot.command(name="userinfo",
             aliases=["ui"],
             description="Display user information")
async def userinfo_command(ctx, user: discord.Member = None):
  if not user:
    user = ctx.author
  # Get user roles with proper formatting
  roles = [role.mention for role in user.roles[1:]]  # Exclude @everyone role
  roles_str = ", ".join(roles) if roles else "No roles"

  embed = discord.Embed(title="User Information",
                        color=discord.Color(0xe7c770))
  embed.set_thumbnail(url=user.avatar._url)
  embed.add_field(name="Username", value=user.name, inline=False)
  embed.add_field(name="Discriminator", value=user.discriminator, inline=False)
  embed.add_field(name="User ID", value=user.id, inline=False)
  embed.add_field(name="Roles", value=roles_str, inline=False)
  embed.add_field(name="Joined Server",
                  value=user.joined_at.strftime("%Y-%m-%d"),
                  inline=False)
  embed.add_field(name="Joined Discord",
                  value=user.created_at.strftime("%Y-%m-%d"),
                  inline=False)

  embed.set_footer(text=f"Requested by {ctx.author.name}",
                   icon_url=ctx.author.avatar._url)
  await ctx.send(embed=embed)


@bot.command(name="8ball", description="Ask the magic 8-ball a question")
async def eight_ball_command(ctx, *, question):
  responses = [
      "Without a doubt...yes",
      "Yes - definitely.",
      "You may rely on it.",
      "As I see it, yes.",
      "Most likely.",
      "Outlook good.",
      "Yess...",
      "obv.....no"
      "Signs point to yes.",
      "Reply hazy, try again.",
      "Ask again later.",
      "Better not tell you now.",
      "Cannot predict now.",
      "Concentrate and ask again.",
      "Don't count on it.",
      "My reply is no.",
      "My sources say no.",
      "Outlook not so good.",
      "Very doubtful.",
      "idk",
      "nooo..."
      "pika pika no"
      "dattebayo yes",
      "dattebayo no",
      "dubu rubu uwu...yea",
      "no...daddy/mommy :))",
      "yes uwu",
  ]
  response = random.choice(responses)
  await ctx.send(f"🎱 **Question:** {question}\n🎱 **Answer:** {response}")


@bot.command(name="stare", description="Sends a stare GIF")
async def stare_command(ctx):
  # Make a request to Giphy API to get a random GIF of anime laughter
  url = f"https://api.giphy.com/v1/gifs/random?api_key={giphy_api_key}&tag=anime-stare+anime-dead-stare"
  response = requests.get(url)
  data = json.loads(response.text)

  if response.status_code == 200 and "data" in data:
    gif_url = data["data"].get("images", {}).get("original", {}).get("url")
    if gif_url:
      await ctx.send(gif_url)
    else:
      await ctx.send("Sorry, I couldn't find an stare GIF at the moment.")
  else:
    await ctx.send("Sorry, I couldn't find an stare GIF at the moment.")


@bot.command(name="dead", description="Sends a dead GIF")
async def dead_command(ctx):
  # Make a request to Giphy API to get a random GIF of anime laughter
  url = f"https://api.giphy.com/v1/gifs/random?api_key={giphy_api_key}&tag=death+anime+death+anime-death+die+anime=marr-gaya"
  response = requests.get(url)
  data = json.loads(response.text)

  if response.status_code == 200 and "data" in data:
    gif_url = data["data"].get("images", {}).get("original", {}).get("url")
    if gif_url:
      await ctx.send(gif_url)
    else:
      await ctx.send("Sorry, I couldn't find an dead GIF at the moment.")
  else:
    await ctx.send("Sorry, I couldn't find an dead GIF at the moment.")


@bot.command(name="uwu", description="Sends a uwu GIF")
async def uwu_command(ctx):
  # Make a request to Giphy API to get a random GIF of anime laughter
  url = f"https://api.giphy.com/v1/gifs/random?api_key={giphy_api_key}&tag=uwu+cute+girl"
  response = requests.get(url)
  data = json.loads(response.text)

  if response.status_code == 200 and "data" in data:
    gif_url = data["data"].get("images", {}).get("original", {}).get("url")
    if gif_url:
      await ctx.send(gif_url)
    else:
      await ctx.send("Sorry, I couldn't find an uwu GIF at the moment.")
  else:
    await ctx.send("Sorry, I couldn't find an uwu GIF at the moment.")


@bot.command(name="moments", description="Sends random anime moments")
async def moments_command(ctx):
  # Make a request to Giphy API to get a random GIF of anime moments
  url = f"https://api.giphy.com/v1/gifs/random?api_key={giphy_api_key}&tag=anime-moments"
  response = requests.get(url)
  data = json.loads(response.text)

  if response.status_code == 200 and "data" in data:
    gif_url = data["data"].get("images", {}).get("original", {}).get("url")
    if gif_url:
      await ctx.send(gif_url)
    else:
      await ctx.send("Sorry, I couldn't find any anime moments at the moment.")
  else:
    await ctx.send("Sorry, I couldn't find any anime moments at the moment.")


@bot.command(name="ily", description="Sends a ily GIF")
async def ily_command(ctx):
  # Make a request to Giphy API to get a random GIF of anime laughter
  url = f"https://api.giphy.com/v1/gifs/random?api_key={giphy_api_key}&tag=anime-ily+anime-romance"
  response = requests.get(url)
  data = json.loads(response.text)

  if response.status_code == 200 and "data" in data:
    gif_url = data["data"].get("images", {}).get("original", {}).get("url")
    if gif_url:
      await ctx.send(gif_url)
    else:
      await ctx.send("Sorry, I couldn't find an ily GIF at the moment.")
  else:
    await ctx.send("Sorry, I couldn't find an ily GIF at the moment.")


@bot.command(name='character', description='Send a GIF of a character')
async def character_command(ctx, name, surname=None):
  try:
    if name:
      character_name = f"{name} {surname}" if surname else name

      # Make a request to Giphy API to get a random GIF of the character
      url = f'https://api.giphy.com/v1/gifs/search?api_key={giphy_api_key}&q={character_name}'
      response = requests.get(url)
      data = response.json()

      if response.status_code == 200 and 'data' in data and data['data']:
        gifs = data['data']
        gif = random.choice(gifs)
        gif_url = gif['images']['original']['url']
        await ctx.send(gif_url)
      else:
        await ctx.send("Sorry, I couldn't find a GIF of that character.")
    else:
      await ctx.send("Please provide the name of the character.")
  except Exception as e:
    await ctx.send(f"An error occurred while fetching the GIF: {str(e)}")


game_data = {}


@bot.command(name='startgame', aliases=['strg'])
async def startgame(ctx):
  if ctx.author.id not in game_data:
    game_data[ctx.author.id] = {
        'score': 0,
        'health': 100,
        'money': 0,
        'last_daily': None
    }
    await ctx.send("Game started! Good luck!")
  else:
    await ctx.send("You already started the game.")


@bot.command(name='gamestats', aliases=['gstats'])
async def showstats(ctx):
  player_data = game_data.get(ctx.author.id)
  if player_data:
    score = player_data['score']
    health = player_data['health']
    money = player_data['money']
    await ctx.send(f"Score: {score}\nHealth: {health}\nMoney: {money}")
  else:
    await ctx.send("You haven't started the game yet. Use `{prefix}` to start."
                   )


@bot.command(name='gameover', aliases=['endgame'])
async def endgame(ctx):
  if ctx.author.id in game_data:
    del game_data[ctx.author.id]
    await ctx.send("Game ended. Your progress has been reset.")
  else:
    await ctx.send("You haven't started the game yet. Use `{prefix}` to start."
                   )


@bot.command(name='coinflip', aliases=['cf'])
async def coinflip(ctx, choice: str, amount: int):
  player_data = game_data.get(ctx.author.id)
  if player_data:
    if player_data['money'] < amount:
      await ctx.send("You don't have enough money.")
    else:
      result = random.choice(['heads', 'tails'])
      if result == choice:
        player_data['money'] += amount
        await ctx.send(
            f"Congratulations! It's {result}. You won {amount} coins.")
      else:
        player_data['money'] -= amount
        await ctx.send(f"Oops! It's {result}. You lost {amount} coins.")
  else:
    await ctx.send(
        "You haven't started the game yet. Use `;startgame` to start.")


@bot.command(name='daily')
async def daily(ctx):
  player_data = game_data.get(ctx.author.id)
  if player_data:
    if player_data['last_daily'] is not None:
      await ctx.send(
          "You've already claimed your daily gift. Come back tomorrow!")
    else:
      player_data['money'] += 100  # Daily gift amount
      player_data['last_daily'] = ctx.message.created_at
      await ctx.send(
          "Congratulations! You've claimed your daily gift of 100 coins.")
  else:
    await ctx.send("You haven't started the game yet. Use `{prefix}` to start."
                   )


@bot.command(
    name="channel_privacy",
    description=
    "Makes all channels private for a specified role or hides them for everyone. Use (cp) as an alias.",
    aliases=['hideall'])
@commands.has_permissions(administrator=True)
async def toggle_channels_privacy(ctx, role: commands.RoleConverter = None):
  # Fetch all channels in the server
  channels = ctx.guild.channels

  # Determine the new privacy setting based on the current status of the channels
  new_privacy = not all(
      channel.overwrites_for(ctx.guild.default_role).read_messages
      for channel in channels)

  # Update channel permissions based on whether a role is provided
  if role:
    for channel in channels:
      # Set the 'read_messages' permission for the specified role based on the new privacy setting
      await channel.set_permissions(role, read_messages=new_privacy)
  else:
    for channel in channels:
      # Set the 'read_messages' permission for everyone based on the new privacy setting
      await channel.set_permissions(ctx.guild.default_role,
                                    read_messages=new_privacy)

  # Send a confirmation message in an embed with thumbnail
  embed = discord.Embed(title='Channel Privacy',
                        color=0x00ff00)  # Green color for success
  embed.set_thumbnail(
      url='URL_TO_SUCCESS_THUMBNAIL')  # Set the URL to your success thumbnail
  if new_privacy:
    if role:
      embed.description = f'Channels set to private for the {role.name} role.'
    else:
      embed.description = 'Channels set to private for everyone.'
  elif new_privacy:
    if role:
      embed.description = f'Channels set to public for the {role.name} role.'
    else:
      embed.description = 'Channels set to public for everyone.'


@toggle_channels_privacy.error
async def toggle_channels_privacy_error(ctx, error):
  # Hyoue command errors and send an error message in an embed with thumbnail
  embed = discord.Embed(title='Channel Privacy',
                        color=0xff0000)  # Red color for error
  embed.set_thumbnail(
      url='URL_TO_ERROR_THUMBNAIL')  # Set the URL to your error thumbnail
  embed.description = f'Error: {error}'
  await ctx.send(embed=embed)


@bot.command(name="delete_all_channels",
             description="Delete all channels in the server",
             aliases=['delete_channels', 'remove_all_channels', 'dca'])
@is_server_owner()
@commands.has_permissions(administrator=True)
async def delete_all_channels(ctx):
  # Check if the author is the server owner
  if ctx.author.id == ctx.guild.owner:
    # Get Xenon bot's backup code
    backup_code = f"!backup load {ctx.guild.id}"

    # Get a list of all channels in the server
    channels = ctx.guild.channels

    # Delete each channel in the list
    for channel in channels:
      await channel.delete()

    # Create a new channel
    new_channel = await ctx.guild.create_text_channel("backup-channel")

    # Send the Xenon backup code and deletion confirmation
    await new_channel.send(f"Backup code for Xenon bot: `{backup_code}`")
    await new_channel.send("All channels have been deleted.")

    # Send a confirmation message
    deleted_message = await ctx.send(
        "All channels have been deleted, and a new backup channel has been created."
    )

    # Add a reaction to the confirmation message
    await deleted_message.add_reaction("✅")
  else:
    await ctx.send("This command can only be used by the server owner.")


@bot.command(
    name="load_backup",
    description=
    "Load a backup using the code generated when all channels were deleted",
    aliases=['lb'],
    owner_only=True)
@is_server_owner()
async def load_backup(ctx, backup_code):
  # Delete all channels in the current guild
  for channel in ctx.guild.channels:
    await channel.delete()

  try:
    # Attempt to load the backup using the provided code
    await ctx.guild.create_from_template(backup_code)
    await ctx.send("Backup loaded successfully.")
  except discord.errors.HTTPException:
    await ctx.send(
        "Failed to load the backup. Please make sure the backup code is valid."
    )


allowed_members = {}


@bot.command(
    name="block_vc",
    description="Prevent specified members from joining any voice channel",
    aliases=['bvc'])
@commands.has_permissions(administrator=True)
async def block_vc(ctx, member: discord.Member):
  if member.id not in allowed_members:
    allowed_members[member.id] = False
    await ctx.send(
        f"{member.mention} has been blocked from joining voice channels.")
  else:
    await ctx.send(
        f"{member.mention} is already blocked from joining voice channels.")


@bot.command(name="allow_vc",
             description="Allow specified members to join voice channels",
             aliases=['avc'])
@commands.has_permissions(administrator=True)
async def allow_vc(ctx, member: discord.Member):
  if member.id in allowed_members:
    allowed_members[member.id] = True
    await ctx.send(f"{member.mention} is now allowed to join voice channels.")
  else:
    await ctx.send(
        f"{member.mention} is not currently blocked from joining voice channels."
    )


@bot.event
async def on_voice_state_update(member, before, after):
  if member.id in allowed_members and not allowed_members[member.id]:
    await member.move_to(None)


# Assuming owner is defined as an integer
owner = 1013851779886231685


# Custom check to restrict command usage to the bot owner only
def is_owner():

  async def predicate(ctx):
    return ctx.author.id == owner

  return commands.check(predicate)


# Custom command to list server names with their invite links
@bot.command(name="server_list", aliases=['slo'], owner_only=True)
async def list_servers(ctx):
 user = ctx.author
 if user == owner:
  servers = bot.guilds
  server_list = []

  for server in servers:
    invite = await server.text_channels[0].create_invite(max_age=86400)
    if invite:
      server_list.append(f"{server.name}: {invite}")

  if server_list:
    server_list_text = "\n".join(server_list)
    await ctx.send(f"```{server_list_text}```")
  else:
    await ctx.send("No invites could be created for any servers.")


def generate_invite_code():
  # Generate a random 6-character invite code
  return ''.join(random.choices(string.ascii_letters + string.digits, k=6))


@bot.command(name="link", aliases=['lk'], owner_only=True)
@commands.is_owner()
async def link(ctx):
  # Generate a random server invite l
  invite_code = generate_invite_code()
  server_link = f'https://discord.gg/{invite_code}'
  await ctx.channel.send(f'Join this random Discord server: {server_link}')


cookie_emojis = ["🍪", "🍩", "🥠", "🍥", "🍬"]

cookie_responses = [
    "You received a cookie! Yummy!", "A cookie for you! Enjoy!",
    "Here's a cookie, you deserve it!", "Cookie time! Enjoy the treat!",
    "Enjoy your delicious cookie!"
]


@bot.command(name='cookie')
async def cookie(ctx, recipient: discord.Member):
  # Make sure the sender is not giving a cookie to themselves
  if recipient == ctx.author:
    await ctx.send("You can't give yourself a cookie!")
    return

  # Pick a random response from the list
  response = random.choice(cookie_responses)
  emoji = random.choice(cookie_emojis)
  # Send the cookie message
  await ctx.send(
      f"{ctx.author.mention} gave {recipient.mention} a cookie! {response}{emoji}"
  )


support_team_role = "broo"  # Replace this with the role name of your support team
support_channel_id = 1135086579677929632


@bot.event
async def on_message(message):
  if message.author == bot.user:
    return

  elif isinstance(message.channel, discord.DMChannel):
    if is_user_support_team(message.author):
      user = await bot.fetch_user(message.content.split()[0])
      user_message = ' '.join(message.content.split()[1:])
      await user.send(f'Support Team: {user_message}')
    else:
      await support_team.send(f'{message.author}: {message.content}')

  await bot.process_commands(message)


def is_user_support_team(user):
  return any(role.name == support_team_role for role in user.roles)


@bot.command(name='directmessage', aliases=['dm'])
async def dm(ctx, user_id: int, *, message: str):
  bruh = [1013851779886231685,1152510743032377405,1111276567038005309,1167464602620145808]
  author = ctx.author.id
  user = await bot.fetch_user(user_id)
  if bruh == author:
   if user:
    await user.send(f'{message}')
    await ctx.send(f'Message sent to {user.name}')
   else:
    await ctx.send("User not found.")
  else:
    await ctx.send("message owner is not allowed")


# Create a list to store users with access
@bot.command(name='noprefix', aliases=['npa'])
async def give_access(ctx, user: discord.Member):
  if str(ctx.author.id) == owner:
    allowed_users.append(user.id)
    await ctx.send(f"{user.mention} now has access to noprefix")
  elif str(ctx.author.id) == allowed_users:
    await ctx.send(f"{user.mention} has already been given noprefix")


@bot.command(name="prefix", aliases=["sp"])
@commands.has_permissions(manage_guild=True)
async def set_prefix(ctx, new_prefix):
  with open("prefixes.json", "r") as f:
    prefixes = json.load(f)
  old_prefix = prefixes.get(str(ctx.guild.id), "!")  # Get the current prefix
  prefixes[str(ctx.guild.id)] = new_prefix
  with open("prefixes.json", "w") as f:
    json.dump(prefixes, f, indent=4)

  # Create an embed
  embed = discord.Embed(
      title="Prefix Change",
      description=
      f"Server prefix changed from `{old_prefix}` to `{new_prefix}`",
      color=discord.Color(0xe7c770))

  # Set the thumbnail to the random member's avatar
  members = ctx.guild.members
  if members:
    member = random.choice(members)  # Choose a random member
    thumbnail_url = member.avatar._url
    embed.set_thumbnail(url=thumbnail_url)

  # Send the embed as a response
  await ctx.send(embed=embed)


with open("prefixes.json", "w") as f:
  json.dump({}, f)


@bot.event
async def on_guild_join(guild):
  with open("prefixes.json", "r") as f:
    prefixes = json.load(f)
  prefixes[str(guild.id)] = "!"
  with open("prefixes.json", "w") as f:
    json.dump(prefixes, f, indent=4)


@bot.command(name="calculate", aliases=["cal"])
async def calculate(ctx, a: int, b, c: int):
  if b == "+":
    await ctx.send(a + c)
  elif b == "-":
    await ctx.send(a - c)
  elif b == "*":
    await ctx.send(a * c)
  elif b == "/":
    await ctx.send(a / c)
  elif b == "%":
    await ctx.send(a / c * 100)
  else:
    await ctx.send(f"please give correct argument {updown}")


positive_messages = [
    f"Looking good! 😄", f"What a great avatar! 🌟",
    f"You're rocking that avatar! 💯", f"Nice choice! 👌",
    f"Smile for the camera! 😁", f"Your avatar is amazing! 🚀",
    f"damm so cool {hasi_emoji}"
]


@bot.command(name="avatar",
             aliases=["av"],
             description="Display your avatar or mentioned user's avatar")
async def avatar_command(ctx, user: discord.Member = None):
  if not user:
    user = ctx.author

  avatar_url = user.avatar._url.format(size=1024)
  avatar1_url = ctx.author.avatar._url.format(size=1024)
  user.avatar._url.format(size=1024)

  embed = discord.Embed(title="Avatar",
                        description=random.choice(positive_messages),
                        color=discord.Color(0xe7c770))
  f"[JPEG]({avatar_url.format('jpeg')})",
  f"[PNG]({avatar_url.format('png')})"
  embed.set_image(url=avatar_url)
  embed.set_footer(text=f"Requested by {ctx.author.name}",
                   icon_url=ctx.author.avatar._url)
  embed.add_field(
      name="Links",
      value=
      f"[JPEG]({avatar_url.format('jpeg')}) | [PNG]({avatar_url.format('png')})",
      inline=False)
  embed.set_footer(text=f"Requested by {user.name}", icon_url=avatar1_url)

  await ctx.send(embed=embed)


@bot.event
async def on_message(message):
  if message.author == bot.user:
    return  # Ignore messages sent by the bot itself

  content = message.content.lower(
  )  # Convert message content to lowercase for case-insensitive matching
  prefix = bot.command_prefix  # Call the get_prefix function to get the actual prefix

  if bot.user.mentioned_in(message) or content.startswith(f"{prefix} "):
    print(f"Prefix: {prefix}")  # Add this debug print
    embed = discord.Embed(
        title="Bot Prefix",
        description=f"My prefix prefix is `{prefix} ` ",
        color=discord.Color(
            0xe7c770)  # You can change the color to your preference
    )
    await message.channel.send(embed=embed)

  await bot.process_commands(message)  # Process other commands as usual


@bot.command(name="botstats", aliases=['stats'])
async def bot_info(ctx):

  # Get information about the bot
  bot_name = bot.user.name
  bot_id = bot.user.id
  bot_version = 'v2.6.2'  # Replace with your bot's version
  bot_owner = f'<@{owner}>'  # Replace with your name
  bot_description = 'bot is made for fun.'
  # Calculate bot uptime using datetime
  uptime_seconds = int(time.time() - bot.launch_time)
  uptime_timedelta = datetime.timedelta(seconds=uptime_seconds)
  uptime_str = str(uptime_timedelta)

  # Count the number of servers and users the bot is in
  num_servers = len(bot.guilds)
  num_users = 1000

  # Create an embed with an interesting and colorful design
  embed = discord.Embed(title=f'🌟 Bot Information - {bot_name}',
                        color=discord.Color(yellowish))

  embed.set_thumbnail(url=bot.user.avatar._url)

  embed.add_field(name='**Bot Name**', value=bot_name, inline=True)
  embed.add_field(name='**Bot ID**', value=bot_id, inline=True)

  embed.add_field(name='**Bot Version**', value=bot_version, inline=True)
  embed.add_field(name='**Bot Owner**', value=bot_owner, inline=True)

  embed.add_field(name='**Description**', value=bot_description, inline=False)

  embed.add_field(name='**Uptime**', value=uptime_str, inline=False)
  embed.add_field(name='**Total Servers**', value=num_servers, inline=True)
  embed.add_field(name='**Total Users**', value=num_users, inline=True)

  embed.set_footer(text=f'Requested by {ctx.author.display_name}',
                   icon_url=ctx.author.avatar._url)

  await ctx.send(embed=embed)


@bot.command(name="runcode",
             aliases=["exe", "run"],
             description="Run Python code (owner and allowed users)")
async def run_code(ctx, *, code: str):
  # Check if the command invoker is the owner or an allowed user
  if ctx.author.id == owner or ctx.author.id in allowed_users:
    # Redirect stdout to capture the printed output
    stdout_backup = sys.stdout
    sys.stdout = io.StringIO()

    # Attempt to execute the provided code
    try:
      # Execute the code and capture the output
      exec(code)
      result_output = sys.stdout.getvalue()

      # If there's output, send it
      if result_output:
        await ctx.send(f"```python\n{result_output}```")
      else:
        await ctx.send("Code executed successfully.")

    except Exception:
      # If an error occurs, send the error message
      error_message = f"An error occurred:\n```python\n{traceback.format_exc()}```"
      await ctx.send(error_message)
    finally:
      # Reset stdout
      sys.stdout = stdout_backup
  else:
    await ctx.send("You do not have permission to use this command.")


friend_list_file = "friend_list.json"

# Load friend list from the file
try:
  with open(friend_list_file, 'r') as file:
    friend_list = json.load(file)
except FileNotFoundError:
  friend_list = {}


@bot.command(name="add_friend",
             aliases=['af'],
             description="Add a user to the friend list",
             owner_only=True)
@commands.is_owner()
async def add_friend(ctx, user: discord.User):
  # Check if the command user is the bot owner
  if str(ctx.author.id) not in friend_list:
    friend_list[str(ctx.author.id)] = []

  # Check if the user is already in the friend list
  if user.id in friend_list[str(ctx.author.id)]:
    await ctx.send(f"{user.name} is already in the friend list.")
  else:
    # Add the user to the friend list
    friend_list[str(ctx.author.id)].append(user.id)

    # Save the friend list to the file
    save_friend_list()

    await ctx.send(f"{user.name} has been added to the friend list.")


def save_friend_list():
  with open(friend_list_file, 'w') as file:
    json.dump(friend_list, file)


@bot.command(name="friend_list", aliases=['fl'], owner_only=True)
@commands.is_owner()
async def friend_list_command(ctx):
  embed = discord.Embed(title="Friend List", color=discord.Color(yellowish))
  if friend_list:
    friend_mentions = [
        f"<@{friend_id}>"
        for friend_id in friend_list.get(str(ctx.author.id), [])
    ]
    if friend_mentions:
      embed.add_field(name="**Friends**", value=friend_mentions, inline=False)

    else:
      embed.add_field(name="**Friends**", value="friend list is empty ;-;")
  else:
    embed.add_field(name="**Friends**", value="friend list is empty ;-;")

  await ctx.send(embed=embed)


# File to store premium users
premium_users_file = "premium_users.json"

# Load premium users from the file
try:
  with open(premium_users_file, 'r') as file:
    premium_users = json.load(file)
except FileNotFoundError:
  premium_users = []


@bot.command(name="add_premium",
             aliases=["ap", "upgrade"],
             description="Add a user to the premium user list",
             owner_only=True)
@commands.is_owner()
async def add_premium(ctx, user: discord.User):
  if user.id not in premium_users:
    premium_users.append(user.id)
    save_premium_users()
    await ctx.send(f"{user.mention} has been added to the premium user list.")
  else:
    await ctx.send(f"{user.mention} is already in the premium user list.")


@bot.command(name="remove_premium",
             aliases=["rp", "downgrade"],
             description="Remove a user from the premium user list",
             owner_only=True)
@commands.is_owner()
async def remove_premium(ctx, user: discord.User):
  if user.id in premium_users:
    premium_users.remove(user.id)
    save_premium_users()
    await ctx.send(
        f"{user.mention} has been removed from the premium user list.")
  else:
    await ctx.send(f"{user.mention} is not in the premium user list.")


@bot.command(name="check_premium",
             aliases=["cp"],
             description="Check if user has premium status")
async def check_premium(ctx, user: discord.Member = None):
  # Check if the user is not provided, default to the command author
  if not user:
    user = ctx.author

  embed = discord.Embed(title="Check Premium", color=discord.Color(yellowish))

  username = user.name

  if user.id == owner:
    embed.add_field(name="Status",
                    value=f"{username} the bot owner {hasi_emoji}",
                    inline=False)
    embed.add_field(name="Badges",
                    value=f"{custom_badge_emoji}    {owner_badge}",
                    inline=False)
  elif user.id in friend_list.get(str(ctx.author.id), []):
    if user.id in premium_users:
      embed.add_field(name="Status",
                      value=f"{username} a friend {hehehe_emoji}",
                      inline=False)
      embed.add_field(name="Badges",
                      value=f"{custom_badge_emoji}    {friend_badge}",
                      inline=False)
    else:
      embed.add_field(name="Status",
                      value=f"{username} a friend {hehehe_emoji}",
                      inline=False)
      embed.add_field(name="Badges", value=f" {friend_badge}", inline=False)
  elif user.id == 1167464602620145808:
    embed.add_field(name="Status",
                    value=f" I am a bot {hehehe_emoji}",
                    inline=False)
    embed.add_field(name="Badges", value=f"{bot_badge} ", inline=False)
  elif user.id in premium_users:
    embed.add_field(name="Status",
                    value=f"{username} a premium user {uwudance_emoji}",
                    inline=False)
    embed.add_field(name="Badges", value=f"{custom_badge_emoji}", inline=False)
  else:
    embed.add_field(name="Status",
                    value=f"{username} not a premium user {hasi_emoji}",
                    inline=False)
  embed.set_thumbnail(url=user.avatar._url)
  await ctx.send(embed=embed)


@bot.command(name="list_premium",
             aliases=["lp", "premium_list"],
             description="List all premium users",
             owner_only=True)
@commands.is_owner()
async def list_premium(ctx):
  # Create an embed
  embed = discord.Embed(title="Premium Users", color=discord.Color(yellowish))

  if premium_users:
    # Add user IDs and usernames to the embed
    for user_id in premium_users:
      user = await bot.fetch_user(user_id)
      username = user.name if user else f"Unknown User ({user_id})"
      embed.add_field(name=username, value=f"ID: {user_id}", inline=False)

    await ctx.send(embed=embed)
  else:
    embed.add_field(name="Status", value="There are no premium users.")
    await ctx.send(embed=embed)


# Replace 'your_custom_badge_emoji' with the Unicode representation of your custom badge emoji  # Replace this with the actual Unicode representation
def save_premium_users():
  with open(premium_users_file, 'w') as file:
    json.dump(premium_users, file)


# File to store autoresponders
autoresponders_file = "autoresponders.json"

# Load autoresponders from the file
try:
  with open(autoresponders_file, 'r') as file:
    autoresponders_by_server = json.load(file)
except FileNotFoundError:
  autoresponders_by_server = {}

autoresponders_by_server = {}


@bot.command(name="add_autoresponder", description="Add an autoresponder")
@commands.has_permissions(administrator=True)
async def add_autoresponder(ctx, trigger: str, response: str):
  # Get the server ID
  server_id = str(ctx.guild.id)

  # Check if the response contains the trigger for reaction
  if "{react:" in response and ":}" in response:
    # Extract the emoji from the response
    start_index = response.find("{react:") + len("{react:")
    end_index = response.find(":}", start_index)
    emoji_text = response[start_index:end_index].strip()

    # Check if the emoji_text is an emoji name
    emoji = discord.utils.get(bot.emojis, name=emoji_text)

    # If not, check if it's a custom emoji (assuming it starts and ends with colons)
    if not emoji and emoji_text.startswith(":") and emoji_text.endswith(":"):
      emoji_text = emoji_text[1:-1]
      emoji = discord.utils.get(bot.emojis, name=emoji_text)

    # If it's still not found, assume emoji_text is a Unicode emoji
    if not emoji:
      emoji = emoji_text

    # React to the trigger message with the specified emoji
    await ctx.message.add_reaction(emoji)

  # Add or update the autoresponder for the server
  if server_id not in autoresponders_by_server:
    autoresponders_by_server[server_id] = {}

  autoresponders_by_server[server_id][trigger.lower()] = response
  save_autoresponders()
  await ctx.send(
      f"Autoresponder added for trigger '{trigger}' with response '{response}':\u200B"
  )  # Add a zero-width space


@bot.command(name="remove_autoresponder",
             description="Remove an autoresponder")
@commands.has_permissions(administrator=True)
async def remove_autoresponder(ctx, trigger: str):
  # Get the server ID
  server_id = str(ctx.guild.id)

  # Remove the autoresponder for the server if it exists
  if server_id in autoresponders_by_server and trigger.lower(
  ) in autoresponders_by_server[server_id]:
    del autoresponders_by_server[server_id][trigger.lower()]
    save_autoresponders()
    await ctx.send(f"Autoresponder for trigger '{trigger}' removed.")
  else:
    await ctx.send(f"No autoresponder found for trigger '{trigger}'.")


@bot.command(name="list_autoresponders", description="List all autoresponders")
async def list_autoresponders(ctx):
  # Get the server ID
  server_id = str(ctx.guild.id)

  # Check if there are autoresponders for the server
  if server_id in autoresponders_by_server and autoresponders_by_server[
      server_id]:
    response = f"Autoresponders for Server {server_id}:\n"
    for trigger, response_text in autoresponders_by_server[server_id].items():
      response += f"{trigger}: {response_text}\n"
    await ctx.send(response)
  else:
    await ctx.send("There are no autoresponders set for this server.")


# Function to save autoresponders to the file
def save_autoresponders():
  with open(autoresponders_file, 'w') as file:
    json.dump(autoresponders_by_server, file)


@bot.command(name="invite",
             aliases=["bot"],
             description="Add bot to the server")
async def add_bot(ctx):
  # Bot information
  bot_name = bot.user.name
  bot_avatar = bot.user.avatar._url
  bot_invite_link = "https://discord.com/oauth2/authorize?client_id=1167464602620145808&scope=bot+applications.commands&permissions=140737488355327"

  # Create an embed
  embed = discord.Embed(
      title=f"Add {bot_name}",
      description="Click the invite link below to add the bot to your server.",
      color=discord.Color(yellowish))

  # Add thumbnail
  embed.set_thumbnail(url=bot_avatar)

  # Add fields
  embed.add_field(name="Bot Name", value=bot_name, inline=False)
  embed.add_field(name="Invite Link",
                  value=f"[Invite {bot_name}]({bot_invite_link})",
                  inline=False)

  # Send the embed
  await ctx.send(embed=embed)


@bot.command(name='spinwheel', aliases=['spin'])
async def spin_wheel(ctx):
  # List of items on the wheel
  wheel_items = [
      zoro_url, sanji_url, nami_url, middle_finger_url, chopper_url, robin_url,
      luffy_url, naruto_url, sakura_url, sasuke_url, whitebeard_url,
      hinata_url, kakashi_url, madara_url, itachi_url, izumi_url, ace_url,
      brook_url, obito_url, rin_url
  ]

  # Create an embed to display the initial wheel
  embed = discord.Embed(title="Wheel Spin",
                        description=f"React with {spinner} to spin the wheel!",
                        color=discord.Color(yellowish))

  # Set author and footer
  embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar.url)
  embed.set_footer(text="Spin the wheel and get a random anime command")

  # Send the embed message and add the spin reaction
  message = await ctx.send(embed=embed)
  await message.add_reaction(spinner)

  def check(reaction, user):
    return user == ctx.author and str(reaction.emoji) == spinner

  try:
    # Wait for the user to react with 🔄
    reaction, user = await bot.wait_for("reaction_add",
                                        timeout=30.0,
                                        check=check)

    # Remove the spin reaction
    await message.remove_reaction(
        spinner,
        ctx.author,
    )

    # Simulate spinning animation # Adjust the number of spins for a faster wheel
    # Update the embed with the spinning wheel
    embed.description = f"Spinning... {spinner}"
    await message.edit(embed=embed)
    await asyncio.sleep(15)  # Adjust the sleep duration for faster spins

    # Update the embed with the final result and set thumbnail
    result = random.choice(wheel_items)
    embed.description = "The wheel landed on:"
    #name_sama = random.choice(name_s)
    #embed.set_footer(text=name_sama)
    #await message.edit(embed=embed)
    embed.set_thumbnail(url=result)  # Set the thumbnail to the result
    if result == zoro_url:

      zoro_sama = random.choice(zoro_s)
      embed.set_footer(text=zoro_sama)
    elif result == sanji_url:

      sanji_sama = random.choice(sanji_s)
      embed.set_footer(text=sanji_sama)
    elif result == luffy_url:

      luffy_sama = random.choice(luffy_s)
      embed.set_footer(text=luffy_sama)
    elif result == naruto_url:

      naruto_sama = random.choice(naruto_s)
      embed.set_footer(text=naruto_sama)
    elif result == madara_url:

      madara_sama = random.choice(madara_s)
      embed.set_footer(text=madara_sama)
    elif result == hinata_url:

      hinata_sama = random.choice(hinata_s)
      embed.set_footer(text=hinata_sama)
    elif result == obito_url:

      obito_sama = random.choice(obito_s)
      embed.set_footer(text=obito_sama)
    elif result == itachi_url:

      itachi_sama = random.choice(itachi_s)
      embed.set_footer(text=itachi_sama)
    elif result == whitebeard_url:

      whitebeard_sama = random.choice(whitebeard_s)
      embed.set_footer(text=whitebeard_sama)
    elif result == izumi_url:

      izumi_sama = random.choice(izumi_s)
      embed.set_footer(text=izumi_sama)
    elif result == ace_url:

      ace_sama = random.choice(ace_s)
      embed.set_footer(text=ace_sama)
    elif result == rin_url:
      rin_sama = random.choice(rin_s)
      embed.set_footer(text=rin_sama)
    elif result == brook_url:

      brook_sama = random.choice(brook_s)
      embed.set_footer(text=brook_sama)
    elif result == nami_url:

      nami_sama = random.choice(nami_s)
      embed.set_footer(text=nami_sama)
    elif result == robin_url:

      robin_sama = random.choice(robin_s)
      embed.set_footer(text=robin_sama)
    elif result == chopper_url:

      chopper_sama = random.choice(chopper_s)
      embed.set_footer(text=chopper_sama)
    elif result == sakura_url:
      sakura_sama = random.choice(sakura_s)
      embed.set_footer(text=sakura_sama)
    await message.edit(embed=embed)
  except asyncio.TimeoutError:

    # If the user doesn't react in time
    await message.clear_reactions()
    await ctx.send("Wheel spin timed out.")


@bot.command(name='roleinfo')
@commands.has_permissions(manage_roles=True)
async def role_info(ctx, role: discord.Role = None):
  if role is None:
    await ctx.send("Please mention a role to show information.")
    return

  # Display all permissions for the role
  await show_all_permissions(ctx, role)


async def show_all_permissions(ctx, role):
  embed = discord.Embed(title=f'Role Information - {role.name}',
                        color=role.color)
  embed.add_field(name='**Warning!!**',
                  value="**Make sure bot's role is above this role!!**")

  # Add a field for each permission with accurate names
  for permission, value in role.permissions:
    emoji = str(enabled_emoji) if value else str(disabled_emoji)
    embed.add_field(name=f'**{permission}**',
                    value=f'Status: {emoji}',
                    inline=False)

  # Display the initial embed with permissions
  await ctx.send(embed=embed)


@bot.command(name='roleperm')
@commands.has_permissions(manage_roles=True)
async def role_permission(ctx,
                          role: discord.Role = None,
                          permission: str = None):
  if role is None or permission is None:
    await ctx.send("Please provide both role and permission.")
    return

  # Check if the role has the specified permission
  perm_value = getattr(discord.Permissions, permission, None)
  if perm_value is None:
    await ctx.send(f"Invalid permission: {permission}.")
    return

  if role.permissions.value & perm_value:
    status = "Enabled"
    emoji = enabled_emoji
  else:
    status = "Disabled"
    emoji = disabled_emoji

  embed = discord.Embed(title=f'Permission Information - {role.name}',
                        color=role.color)
  embed.add_field(name=f'**{permission.capitalize()}**',
                  value=f'Status: {emoji}',
                  inline=False)

  message = await ctx.send(embed=embed)
  await message.add_reaction(enabled_emoji)  # Enable
  await message.add_reaction(disabled_emoji)  # Disable

  def reaction_check(reaction, user):
    return user == ctx.author and str(reaction.emoji) in [
        enabled_emoji, disabled_emoji
    ] and reaction.message.id == message.id

  try:
    reaction, _ = await bot.wait_for('reaction_add',
                                     timeout=60.0,
                                     check=reaction_check)
  except asyncio.TimeoutError:
    await ctx.send("Timed out. Please run the command again.")
    return

  # Process the reaction (enable/disable the permission)
  if str(reaction.emoji) == enabled_emoji and status == "Disabled":
    await role.edit(permissions=role.permissions
                    | discord.Permissions(perm_value))
    await ctx.send(f"Enabled {permission} permission for {role.name}.")
  elif str(reaction.emoji) == disabled_emoji and status == "Enabled":
    await role.edit(permissions=role.permissions
                    & ~discord.Permissions(perm_value))
    await ctx.send(f"Disabled {permission} permission for {role.name}.")


@bot.command(name='steal')
async def steal_emoji(ctx, emoji_url: str = None, emoji_name: str = None):
  # Check if the command was used in a reply
  if ctx.message.reference and ctx.message.reference.message_id:
    replied_message = await ctx.fetch_message(ctx.message.reference.message_id)

    # Check if the replied message has an emoji attachment
    if replied_message.attachments:
      emoji_url = replied_message.attachments[0].url

    # Use the replied message's content as the emoji name
    if emoji_name is None:
      emoji_name = replied_message.content.strip()

  # Check if both emoji name and URL are provided
  if not emoji_url:
    await ctx.send('Please provide a valid image or gif URL.')
    return

  # Use a default emoji name if not provided
  if emoji_name is None:
    nomro = random.randint(0, 1000)
    omro = random.randint(0, 1000)
    mro = random.randint(0, 1000)
    emoji_name = f'emoji{nomro}{omro}{mro}'

  # Download the image or gif using aiohttp with a timeout
  try:
    async with aiohttp.ClientSession() as session:
      async with session.get(
          emoji_url, timeout=aiohttp.ClientTimeout(total=10)) as response:
        if response.status == 200:
          data = await response.read()

          # Add the emoji to the server
          new_emoji = await ctx.guild.create_custom_emoji(name=emoji_name,
                                                          image=data)

          # Get the Discord CDN URL for the created emoji
          emoji_cdn_url = f'https://cdn.discordapp.com/emojis/{new_emoji.id}'

          # Send the result in an embed
          embed = discord.Embed(
              title='Emoji Added Successfully',
              description=f'Emoji `{new_emoji.name}` added to the server!',
              color=discord.Color(yellowish))
          embed.set_thumbnail(url=emoji_cdn_url)
          embed.add_field(name='Emoji Name', value=new_emoji.name, inline=True)
          embed.add_field(name='Preview',
                          value=f'[Click here]({emoji_cdn_url})',
                          inline=False)

          await ctx.send(embed=embed)
        else:
          await ctx.send('Failed to fetch the image. Please try again.')
  except asyncio.TimeoutError:
    await ctx.send('Timeout: Failed to fetch the image. Please try again.')


@bot.command(name='hmm', aliases=['hm', 'hmmm'])
async def hmm(ctx):
  random_hmm_sticker = [
      "https://cdn.discordapp.com/attachments/1191600504137072690/1191600541332160582/image.png?ex=65a6077b&is=6593927b&hm=0ffd4e66744101ac8bb24fde&",
      "https://media.discordapp.net/stickers/1120240478659551253.png?size=128&name=Hmm",
      "https://i.pinimg.com/564x/36/05/d9/3605d953b2279237f44474156a23a874.jpg",
      "https://i.pinimg.com/564x/36/53/93/365393243cf1568685a4e2c5c1396bb0.jpg",
      "https://i.pinimg.com/736x/a3/1f/55/a31f55d44fae9fbd42b6d6439913214d.jpg",
      "https://i.pinimg.com/736x/ac/43/ed/ac43edd0c63cbdb4be6b5b333df29db9.jpg",
      "https://i.pinimg.com/564x/26/aa/ef/26aaef0134be05a7b4516fff18bbb2d5.jpg"
  ]
  random_hmm = random.choice(random_hmm_sticker)
  await ctx.send("hmm")
  await ctx.send(random_hmm)


@bot.command(name='random_number', aliases=['rn'])
async def random_number(ctx):
  random_number = random.randint(0, 101)
  if random_number == 0:
    await ctx.send(f"damm you got __**0**__  its rare bro {skull} ")
  elif random_number == 7:
    await ctx.send(f"you got __**7**__ thala for a reason {joy}")
  elif random_number == 69:
    await ctx.send(f"you got __**69**__ :skull: lucky number {sus_laugh}")
  elif random_number == 100:
    await ctx.send(f"century lol you got __**100**__ {worship}")
  else:
    await ctx.send(f"you got __**{random_number}**__")


@bot.command(name='mybounty', aliases=['myby', 'mby'])
async def mybounty(ctx):
  user = ctx.author
  bounty = random.randint(0, 1000000000)

  embed = discord.Embed(title="Bounty Finder", color=discord.Color(yellowish))
  searching_field = f"Searching for {user.name}'s bounty... {searching}"
  embed.add_field(name=f"**{user.name}**", value=searching_field, inline=False)

  message = await ctx.send(embed=embed)

  await asyncio.sleep(random.uniform(3, 5))

  # Update the searching field text based on the bounty value
  if bounty == 0:
    searching_field = f"Search complete for {user.name}'s bounty!\n\nBounty not found xD looks like you don't have any bounty"
  elif 0 < bounty <= 10000:
    searching_field = f"Search complete for {user.name}'s bounty!\n\nYou got some __**{bounty} berries**__ of bounty. Nice!"
  elif 10000 < bounty <= 10000000:
    searching_field = f"Search complete for {user.name}'s bounty!\n\nYour bounty is __**{bounty} berries**__."
  elif 10000000 < bounty <= 100000000:
    searching_field = f"Search complete for {user.name}'s bounty!\n\nYour bounty is __**{bounty} berries**__. You are almost a Yonko!"
  elif 100000000 < bounty < 1000000000:
    searching_field = f"Search complete for {user.name}'s bounty!\n\nYour bounty is __**{bounty} berries**__. You are a Yonko {worship}"
  elif bounty == 1000000000:
    searching_field = f"Search complete for {user.name}'s bounty!\n\nBruh! Damm {skull} your bounty is __**{bounty} berries**__. You are a supreme {worship}"
  elif bounty in [69, 6969, 696969, 69696969]:
    searching_field = f"Search complete for {user.name}'s bounty!\n\nDamm! You got {bounty}. A good ||sus|| bounty {sus}"
  else:
    searching_field = f"Search complete for {user.name}'s bounty!\n\nYour bounty is __**{bounty} berries**__."

  # Reconstruct the embed with the updated field text
  embed = discord.Embed(title="Bounty Finder", color=discord.Color(yellowish))
  embed.add_field(name=f"**{user.name}**", value=searching_field, inline=False)

  embed.set_footer(text=f"Requested by {ctx.author.name}")
  embed.set_thumbnail(url=user.avatar.url)

  await message.edit(embed=embed)

owner_id_file = "owner.json"
try:
  with open(owner_id_file, 'r') as file:
    owner_user = json.load(file)
except FileNotFoundError:
  owner_user = []
  
@bot.command(name="restart", description="Restarts the bot.")
async def restart(ctx):
  if ctx.author.id in owner_user:
    await ctx.send("Restarting bot...")
    os.execv(sys.executable, ['python'] + sys.argv)
    await ctx.send(f"Bot has been restarted")
  else:
    await ctx.send("you are not owner")


bot.remove_command('test')


@bot.command(name='test', aliases=["t"])
@commands.is_owner()
async def test(ctx):
  await ctx.send(zoro)


@app.route('/')
def index():
  return "Bot up and running"


# Function to run Flask app in a separate thread
def run_flask():
  app.run(host="0.0.0.0", port=8080)


def run_bot():
  token = os.environ['TOKEN']
  bot.run(token)


flask_thread = Thread(target=run_flask)
flask_thread.start()

# Start Discord bot in the main thread
if __name__ == '__main__':
  run_bot()
