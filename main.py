import bot
import discord
from discord.ext import commands
from config import TOKEN

if __name__ == '__main__':
    # Create bot instance
    bot_client = commands.Bot(command_prefix="!")

    # Initialize bot
    bot.initialize(bot_client)

    # Run the bot
    bot_client.run(TOKEN)
