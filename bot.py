import discord
import responses


async def send_message(message, user_message, is_private):
    try:
        response = responses.handle_response(user_message)
        await message.author.send(response) if is_private else await message.channel.send(response)
    except Exception as e:
        print(e)


def run_discord_bot():
    TOKEN = 'MTA5MjgxOTM0ODgxODc3MjAwMA.GNTSvb.l1IzTGOHg0MXrirTGptmzp-h0_KclaXuuHUF1o'
    client = discord.Client()

    @client.event
    async def on_ready():
        print(f'{client.user} is no running!')

    client.run(TOKEN)


def handle_response(message) -> str:
    p_message = message.lower()

    if p_message == 'hello':
        return 'hello there!'

