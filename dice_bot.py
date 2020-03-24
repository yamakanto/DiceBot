import os

import discord
from dotenv import load_dotenv
import random

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')


class CustomClient(discord.Client):
    def __init__(self, command_start):
        super(CustomClient, self).__init__()
        self.command_start = command_start
        self.comm_length = len(command_start)
        self.max_message_length = 2000

    async def on_ready(self):
        guild = discord.utils.find(lambda g: g.name == GUILD, client.guilds)
        print(
            f'{client.user} is connected to the following guild:\n'
            f'{guild.name}(id: {guild.id})'
        )

    async def on_message(self, message):
        if message.author == client.user:
            return

        if len(message.content) < self.comm_length:
            return
        if message.content[:self.comm_length] != self.command_start:
            return

        if message.content[self.comm_length + 1:].isdecimal():
            dec = int(message.content[self.comm_length + 1:])
            rand_response = random.randint(1, dec)
            response = f"random from 1 to {dec}: {rand_response}"
            await message.channel.send(response)
            return

        message_parts = message.content[self.comm_length + 1:].split("d")
        if len(message_parts) != 2 or not message_parts[0].isdecimal() or not message_parts[1].isdecimal():
            print(f"skipped {message.content}")
            return

        response = f"rolled {message_parts[0]} times d{message_parts[1]}:\nresults:"
        total = 0
        for i in range(int(message_parts[0])):
            rand_res = random.randint(1, int(message_parts[1]))
            if len(response) + len(str(rand_res)) > self.max_message_length:
                await message.channel.send(response)
                response = ""
            response += f" {rand_res}"
            total += rand_res

        if len(response) + len(f"\nTotal: {total}") > self.max_message_length:
            await message.channel.send(response)
            response = ""
        response += f"\nTotal: {total}"
        await message.channel.send(response)


client = CustomClient("!roll")
client.run(TOKEN)
