# bot.py #


import os
import traceback

import discord
from dotenv import load_dotenv

load_dotenv()
# The following two variables are fetched from a .env file
# If you are using this script to run your own discord bot, you will need a file named .env in the same directory as the running script.
# This file will need to contain the following lines:
# DISCORD_TOKEN="<your bot's token>"
# ASHADEDBLOBFISH_ID="<your discord user id>"
# Replace <your bot's token> with your bot's discord token, which can be found in the discord developer portal
# Replace <your discord user id> with the unique user id of your discord account. This can be found by enabling developer mode in discord, clicking on your profile, and clicking "Copy User ID"
# If you need help with any of these steps, try using this guide: https://realpython.com/how-to-make-a-discord-bot-python/
TOKEN = os.getenv("DISCORD_TOKEN")
ASHADEDBLOBFISH = int(os.getenv("ASHADEDBLOBFISH_ID"))

intents = discord.Intents.default() # The bot's intents must be passed to the discord.Client instance. discord.Intents.default() sets all 3 intents to False
intents.message_content = True  # The only intent required by this bot is the message content intent. These intents must match those selected in your discord developer portal

client = discord.Client(intents=intents)    # Creates an instance of discord.Client


# Async event definitions

# Outputs a message to say that the bot has connected to discord, when it recieves the on_ready() call from the Discord API, suggesting it has connected
@client.event
async def on_ready():
    print(f"{client.user} has connected to Discord!")

# on_message event. Reads each message sent in the server and acts accordingly
@client.event
async def on_message(message):
    # Ignores all messages sent by the bot itself
    if message.author == client.user:
        return
    
    # The "sven say" function. A user will type "sven say <something>" and the bot will send a message saying <something>
    if message.content.startswith('sven say '):
        await message.channel.send(message.content[8:])

    # An owner-restricted function. Stops the bot. Will only work if you have a .env file configured with your unique discord user id
    if message.content == 'sven stop':
        if message.author.id == ASHADEDBLOBFISH:
            await message.channel.send('Shutting down...\nBye for now!')
            exit(0)
        else:
            await message.channel.send("This action is restricted. Access Denied: You are not AShadedBlobfish")

    # sven whoami function. Useful to quickly check your user id if you don't have developer mode enabled, or to check that the bot is correctly identifying you
    if message.content == 'sven whoami':
        await message.channel.send(message.author.id)

    # Function that the bot was initially made for. I needed to clear out a channel where users had been spamming irrelevant content, but didn't want to delete hundreds of messages by hand
    if message.content.startswith('sven delete after '):
        
        # An owner-restriced function. You may want to change this to a role using message.author.get_role(id)
        # e.g if message.author.get_role(<id for admin role>) == <id for admin role>: <code>
        if message.author.id != ASHADEDBLOBFISH:
            await message.channel.send("This action is restricted. Access Denied: You are not AShadedBlobfish")
            return

        else:
            n = 0
            while True:
                try:
                    messages = []
                    msggg = await message.channel.fetch_message(int(message.content[17:]))
                    async for msg in message.channel.history(after=msggg):
                        messages.append(msg)
                        n += 1

                    if len(messages) == 0:
                        break

                except:
                    traceback.print_exc()
                    await message.channel.send("Please provide a valid message ID\nSyntax: 'sven delete after <message id> (Deletes all messages after the message who's ID was provided)")
                    return
        
                for msgg in messages:
                    await msgg.delete()

            await message.channel.send(f"{n} messages deleted")

        


client.run(TOKEN)   # Starts the bot by intialising the discord.Client() instance with your discord token (read from the .env file)