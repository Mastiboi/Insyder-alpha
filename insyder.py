import asyncio
import discord
from dotenv import load_dotenv
from discord.ext import commands
from telethon import TelegramClient, events
import re
import os

load_dotenv()

API_ID = int(os.getenv("API_ID"))  # Your API ID from my.telegram.org
API_HASH = os.getenv('API_HASH')   # Your API Hash from my.telegram.org
SOURCE_CHANNEL = "earlypumpdetector"  # Example: "mynewschannel" or chat ID (e.g., -1001234567890)
DESTINATION_CHANNEL = "Insyderalphasol"  # Example: "mycopiedchannel" or chat ID

# Discord Credentials
DISCORD_TOKEN = os.getenv('DISCORD')  # Replace with your actual Discord token
DISCORD_CHANNEL_ID = 1337145725280325752


intents = discord.Intents.default()
discord_client = commands.Bot(command_prefix="!", intents=intents)

client_t = TelegramClient("forwarder_session", API_ID, API_HASH)

@client_t.on(events.NewMessage(chats=SOURCE_CHANNEL))

async def forward_message(event):
    """Forwards messages from source to destination"""
    message_text = event.raw_text
    
    # Split message into lines
    lines = message_text.split("\n")

    client_t.parse_mode = 'markdown'
    
    if "Profit" in message_text:
        first_line = lines[0]  # Get the first line

        # Extract the coin name (assumes it's the second word in the first line)
        words = first_line.split()
        coin_name = words[1]
        profit_done = words[5] 
        print() if len(words) > 1 else ""
      
        extracted_text = f"🤑 {coin_name} Profit Done {profit_done}✅"
        
        await client_t.send_message(DESTINATION_CHANNEL, extracted_text)

        discord_channel = discord_client.get_channel(DISCORD_CHANNEL_ID)
        if discord_channel:
            await discord_channel.send(extracted_text)
        

    elif "Token:" in message_text and "CA:" in message_text and "Current Mcap: " in message_text:
        token_match = re.search(r'Token:\s*([\w\d]+)', message_text)  # Extract token name
        ca_match = re.search(r'CA:\s*([\w\d]+)', message_text)  # Extract contract address
        mcap_match = re.search(r'Current Mcap:\s*([\$0-9.,K]+)', message_text)  # Extract market cap

        if token_match and ca_match and mcap_match:
            token_name = token_match.group(1)
            contract_address = ca_match.group(1)
            mcap_value = mcap_match.group(1)
            extracted_text = ("🚀 *Pump Detected* 🤖\n\n"
                              f"Token : {token_name}\n\n"
                              f"CA : `{contract_address}`\n\n"
                              f"Current Mcap : {mcap_value}\n\n"

                              "🔥 TOKENS ARE SENT AFTER PREMIUM GROUP MEMBERS GAIN 75% PROFIT 🔥\n\n"
                              "👉 For PREMIUM GROUP, text [@realInsyderalpha](https://t.me/realInsyderalpha)\n"
                              "💰 Trade with [AXIOM](https://axiom.trade/@mastiboi) or"
                              " [BullX](https://t.me/BullxBetaBot?start=access_PF4IF8I41A) or "
                              "[Photon](https://photon-sol.tinyastro.io/@Mastiboi)"
                              )
            
            
            await client_t.send_message(DESTINATION_CHANNEL, extracted_text)

            # Send to Discord
            discord_channel = discord_client.get_channel(DISCORD_CHANNEL_ID)
            if discord_channel:
                embed = discord.Embed(
                    title="🚀 Pump Detected 🤖",
                    description=f"**Token:** {token_name}\n**CA:** `{contract_address}`\n**Current Mcap:** {mcap_value}\n"
                                "🔥 **Tokens are sent after premium group members gain 75% profit!** 🔥\n\n"
                                            "👉 For **Premium Group**, Text [@Mastiboi](https://discord.com/users/784472320675807309)\n"
                                            "💰 Trade with [AXIOM](https://axiom.trade/@mastiboi) or "
                                            "[BullX](https://t.me/BullxBetaBot?start=access_PF4IF8I41A) or "
                                            "[Photon](https://photon-sol.tinyastro.io/@Mastiboi)",
                    color=discord.Color.blue()
                    )
                await discord_channel.send(embed=embed)                                            




@discord_client.event
async def on_ready():
    print(f"✅ Discord Bot Logged in as {discord_client.user}")

async def start_telegram():
    """Runs the Telegram client inside Discord's event loop"""
    await client_t.start()
    print("✅ Telegram Bot Started")
    await client_t.run_until_disconnected()

async def start_bots():
    """Start both bots, ensuring Telegram runs inside Discord's loop"""
    asyncio.create_task(start_telegram())  # Start Telegram without blocking Discord
    await discord_client.start(DISCORD_TOKEN)  # Start Discord bot

# Start the script
if __name__ == "__main__":
    asyncio.run(start_bots())



