import discord
from discord.ext import commands
from config import TOKEN
from statue import statue
import re
import autorespond_quest


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

    async def auto_responder(message):
        """
        Checks if a message matches a specific pattern and sends a response to the channel if there is a match.
        :param message: A message object that contains information about the message sent in the channel.
        :return: None
        """
        admins_names_match = re.search(autorespond_quest.admins_names, message.content, re.IGNORECASE)
        admins_match = re.search(autorespond_quest.admins, message.content, re.IGNORECASE)
        converter_match = re.search(autorespond_quest.converter, message.content, re.IGNORECASE)
        sell_won_match = re.search(autorespond_quest.sell_won, message.content, re.IGNORECASE)
        issue_match = re.search(autorespond_quest.issue, message.content, re.IGNORECASE)
        new_server_match = re.search(autorespond_quest.new_server, message.content, re.IGNORECASE)

        if admins_names_match or admins_match:
            await message.channel.send(autorespond_quest.admins_ans)
        elif converter_match:
            await message.channel.send(autorespond_quest.converter_ans)
        elif sell_won_match:
            await message.delete()
        elif issue_match:
            await message.channel.send(autorespond_quest.issue_ans)
        if new_server_match:
            await message.channel.send(autorespond_quest.new_server_ans)

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

        # Log to console
        print(f'Message {user_message} by {username} on {channel}')

        # Ignore messages from the bot itself
        if message.author == client.user:
            return

        if user_message.lower() == "hello" or user_message.lower() == "hi":
            await message.channel.send(f'Hello {username}')
            return

        # Call the auto_responder function
        await auto_responder(message)

        # # Respond to commands
        # if message.content.startswith("!roles"):
        #     await on_member_join(message.author)

    client.run(TOKEN)
