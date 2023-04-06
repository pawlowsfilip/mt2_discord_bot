import random
import os
import discord
import re
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
client = discord.Client()
token = os.getenv('TOKEN')
bot = commands.Bot(command_prefix="!")

statue = f'''§1. Każdy użytkownik przebywający na naszym discordzie akceptuje jego regulamin.

§2. Nieznajomość regulaminu nie zwalnia z obowiązku przestrzegania go.

§3. Należy również przestrzegać Warunków korzystania z usługi Discord.
                                
§4. Odnosimy się do siebie z szacunkiem oraz kulturą.

§5. Do czynności zabronionych należy m.in:
- upublicznianie informacji pofunych, danych osobowych (imion,nazwisk,adresów,numerów) 
  innych użytkowników
- podszywanie sie pod inne osoby, w szczególności administracje
- nagrywanie rozmów, bez zgody rozmówców
- trollowanie
- obraza innych uzytkowników, celowa prowokacja, groźby

§6. Administracja ma prawo ukarać użytkownika bez podania powodu, gdy uzna że użytkownik
    działa na szkodę serwera.'''


@client.event
async def on_ready():
    print(f"Logged in as a bot {client.user}")


@client.event
async def on_raw_reaction_add(payload):
    channel_id = '『📋』regulamin'
    if payload.channel_id == channel_id:
        return

    guild = client.get_guild(payload.guild_id)
    member = guild.get_member(payload.user_id)

    if payload.emoji.name == '✅':
        role = discord.utils.get(guild.roles, name='Zweryfikowany')
        await payload.member.add_roles(role)


@bot.event
async def on_member_join(member):
    channel = discord.utils.get(member.guild.channels, name='『📋』regulamin')
    if channel:
        embed = discord.Embed(title='Regulamin', description=statue, color=0x00ff00, )
        await channel.send(embed=embed)
        message = await channel.history().get(author=client.user)
        await message.add_reaction('✅')


@client.event
async def on_message(message):
    username = str(message.author).split("#")[0]
    channel = str(message.channel.name)
    user_message = str(message.content)

    print(f'Message {user_message} by {username} on {channel}')

    if message.author == client.user:
        return

    if user_message.lower() == "hello" or user_message.lower() == "hi":
        await message.channel.send(f'Hello {username}')
        return

    # Respond to commands
    if message.content.startswith("!roles"):
        await on_member_join(message.author)

client.run(token)
