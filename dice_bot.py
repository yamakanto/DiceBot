import os

import discord
from dotenv import load_dotenv
import random

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

# client = discord.Client()

class CustomClient(discord.Client):
    async def on_ready(self):
        guild = discord.utils.find(lambda g: g.name == GUILD, client.guilds)
        print(
            f'{client.user} is connected to the following guild:\n'
            f'{guild.name}(id: {guild.id})'
        )

    async def on_message(self, message):
        if message.author == client.user:
            return

        if len(message.content) < 5:
            return
        if message.content[:5] != "!roll":
            return

        if message.content[6:].isdecimal():
            dec = int(message.content[6:])
            rand_response = random.randint(1, dec)
            response = f"random placeholder response to: {rand_response}"
            await message.channel.send(response)
            return
        message_parts = message.content[6:].split("d")
        if len(message_parts) != 2:
            return
        response = f"rolled {message_parts[0]} times d{message_parts[1]}:\nresults:"
        total = 0
        for i in range(int(message_parts[0])):
            rand_res = random.randint(1, int(message_parts[1]))
            response += " " + str(rand_res)
            total += rand_res
        response += f"\nTotal: {total}"
        await message.channel.send(response)


client = CustomClient()
client.run(TOKEN)