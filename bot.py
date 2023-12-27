# bot.py

import os
import traceback

import discord
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
ASHADEDBLOBFISH = int(os.getenv("ASHADEDBLOBFISH_ID"))

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"{client.user} has connected to Discord!")

@client.event
async def on_message(message):

    if message.author == client.user:
        return
    

    if message.content.startswith('sven say '):
        await message.channel.send(message.content[8:])


    if message.content == 'sven stop':
        if message.author.id == ASHADEDBLOBFISH:
            await message.channel.send('Shutting down...\nBye for now!')
            exit(0)
        else:
            await message.channel.send("This action is restricted. Access Denied: You are not AShadedBlobfish")


    if message.content == 'sven whoami':
        await message.channel.send(message.author.id)


    if message.content.startswith('sven delete after '):
        
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

        


client.run(TOKEN)