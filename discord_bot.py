import discord
import os
from main import run
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")
GUILD = os.getenv("DISCORD_GUILD")

intents = discord.Intents.default()
intents.messages = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    if message.content.startwith("!run"):
        parts = message.content.split()
        if len(parts) < 2:
            await message.channel.send("Usage: '!run (SYMBOL)'")
            return
        symbol = parts[1].upper()
        await message.channel.send(f"Running MarketBot for '{symbol}'...")
        try:
            result = run(symbol)
            await message.channel.send(f"{symbol} -> Trend: {result['trend']} -> Signal: {result['signal']}")
        except Exception as e:
            await message.channel.send(f"Error: {e}")

client.run(TOKEN)