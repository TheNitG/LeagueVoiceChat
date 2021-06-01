from riotwatcher import LolWatcher
from dotenv import load_dotenv
import discord
import os
import mysql.connector


load_dotenv()

mydb = mysql.connector.connect(
  host="localhost",
  user="yourusername",
  password="yourpassword"
)

watcher = LolWatcher(os.getenv('API_KEY'))

client = discord.Client()

@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.idle, activity=discord.Game("Waiting for your commands!"))
    print(f'{client.user.name} has connected to Discord!')


@client.event
async def on_message(message):
    content = message.content
    if content[:5] == '/team':
        user = content[6:]
        print(user)
        await message.channel.send(str(await team(user)))


# Need to check every time a new game is started ever (at least on accounts registered to the database)
# Probably just keep checking the accounts in the database to see if they are playing a game

# For the game, async method that finds the player names and gets their discord ids, then makes a voice channel
# Above code should ideally get the live game team players and make a server with the people or a hidden voice channel only the team can access in a general server for everone using the bot


async def team(user):
    region = 'NA1'
    try:
        encrypted_summoner_id = watcher.summoner.by_name(region, user)['id']
        results = watcher.spectator.by_summoner(region, encrypted_summoner_id)['participants']
        print([x['summonerName'] for x in results])
        return [x['summonerName'] for x in results]
    except Exception as err:
        print(err)
        return 'Player not in game'


client.run(os.getenv('DISCORD_BOT_TOKEN'))
