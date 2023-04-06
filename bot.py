import discord
from discord.ext import commands
from config import TOKEN
from statue import statue


def run_discord_bot():
    client = discord.Client()
    bot = commands.Bot(command_prefix="!")

    @client.event
    async def on_ready():
        print(f'Logged as {client.user}')

    @bot.event
    async def on_member_join(member):
        channel = discord.utils.get(member.guild.channels, name='『📋』regulamin')
        if channel:
            embed = discord.Embed(title='Regulamin', description=statue, color=0x00ff00, )
            await channel.send(embed=embed)
            message = await channel.history().get(author=client.user)
            await message.add_reaction('✅')

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

    client.run(TOKEN)
