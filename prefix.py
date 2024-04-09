import discord
from discord.ext import commands
from discord.ext.commands import Context
import json



def getConfig(guildID):
    with open("config.json", "r") as config:
        data = json.load(config)
    if str(guildID) not in data["guilds"]:
        defaultConfig = {
          "prefix": "!!",
        } 
        updateConfig(guildID, defaultConfig)
        return defaultConfig
    return data["guilds"][str(guildID)]


def updateConfig(guildID, data):
    with open("config.json", "r") as config:
        config = json.load(config)
    config["guilds"][str(guildID)] = data
    newdata = json.dumps(config, indent=4, ensure_ascii=False)
    with open("config.json", "w") as config:
        config.write(newdata)

async def get_prefix(self, message: discord.Message):
  with open('noprefix.json', 'r') as f:
    p = json.load(f)
  if message.author.id in p["np"]:
    return commands.when_mentioned_or('!', '')(self, message)
  else:
    if message.guild:
      data = getConfig(message.guild.id)
      prefix = data["prefix"]
      return commands.when_mentioned_or(prefix)(self, message)
    else:
      return commands.when_mentioned_or('!')(self, message)