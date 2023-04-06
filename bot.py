import discord
from discord.ext import commands
from config import TOKEN
from statue import statue


def run_discord_bot():
    # creating instances of client and the bot
    client = discord.Client()
    bot = commands.Bot(command_prefix="!")

    @client.event
    async def on_ready():
        """
        Function which log to console information about the bot is ready to use.

        :return: None
        """
        print(f'Logged as {client.user}')

    @client.event
    async def on_member_join(member):
        """
        This function is called when a new member joins a server where the bot is present.
        It sends a message of statue (regulamin) and wait for user to accept it by clicking
        the emoji sign.

        :param member: A Member object representing the newly joined member.
        :return: None
        """
        channel = discord.utils.get(member.guild.channels, name='『📋』regulamin')
        if channel:
            embed = discord.Embed(title='Regulamin', description=statue, color=0x00ff00, )
            await channel.send(embed=embed)
            message = await channel.history().get(author=client.user)
            await message.add_reaction('✅')

    @client.event
    async def on_raw_reaction_add(payload):
        """
        This function add role "zweryfikowany" when user add the reaction under the statue message"

        :param payload: A RawReactionActionEvent object containing information about the reaction.
                        It contains information about the user who reacted, the message to which
                        the reaction was added, the emoji that was used, and other metadata associated with the event.
        :return:
        """
        channel_id = '『📋』regulamin'
        if payload.channel_id == channel_id:
            return

        guild = client.get_guild(payload.guild_id)
        # member = guild.get_member(payload.user_id)

        if payload.emoji.name == '✅':
            role = discord.utils.get(guild.roles, name='Zweryfikowany')
            await payload.member.add_roles(role)

    @client.event
    async def on_message(message):
        """
        This function is called whenever a message is sent in a channel the bot has access to.
        It processes the message content and responds appropriately.

        :param message:
        :return:
        """
        username = str(message.author).split("#")[0]
        channel = str(message.channel.name)
        user_message = str(message.content)

        print(f'Message {user_message} by {username} on {channel}')

        if message.author == client.user:
            return

        if user_message.lower() == "hello" or user_message.lower() == "hi":
            await message.channel.send(f'Hello {username}')
            return

        # # Respond to commands
        # if message.content.startswith("!roles"):
        #     await on_member_join(message.author)

    client.run(TOKEN)
