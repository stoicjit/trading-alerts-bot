import requests
import asyncio
import os
from telegram import Bot

# Set up Telegram bot with your bot token and chat ID
bot_token = os.getenv('BOT_TOKEN')  # Replace with your Telegram bot token
chat_id = os.getenv('CHAT_ID')  # Replace with your Telegram chat ID
bot = Bot(token=bot_token)

# Set up the target price level for Bitcoin (daily high example)
target_price_bitcoin = 25000  # You can adjust this value

# CoinGecko API endpoint for simple price data
url = 'https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum&vs_currencies=usd'

# Send request to the API
response = requests.get(url)
data = response.json()

# Fetch current price for Bitcoin
bitcoin_price = data['bitcoin']['usd']

# Check if price crosses the target level
if bitcoin_price >= target_price_bitcoin:
    message = f"🚨 ALERT: Bitcoin price is above the daily high of ${target_price_bitcoin}. Current price: ${bitcoin_price}"

    # Define an async function to send the message
    async def send_telegram_message():
        await bot.send_message(chat_id=chat_id, text=message)

    # Run the async function
    asyncio.run(send_telegram_message())

# Output to the console
print(f"Bitcoin price: ${bitcoin_price}")

