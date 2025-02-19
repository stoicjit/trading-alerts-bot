import requests
import asyncio
import os
from telegram import Bot

# Set up Telegram bot with your bot token and chat ID
bot_token = os.getenv('BOT_TOKEN')  # Replace with your Telegram bot token
chat_id = os.getenv('CHAT_ID')  # Replace with your Telegram chat ID
bot = Bot(token=bot_token)

# Fetch BTC market data from CoinGecko
def get_btc_data():
    url = "https://api.coingecko.com/api/v3/coins/bitcoin/market_chart?vs_currency=usd&days=6&interval=daily"
    response = requests.get(url)

    if response.status_code != 200:
        print("Error fetching BTC data:", response.text)
        return [], []

    data = response.json()

    if 'prices' not in data:
        print("Invalid data format returned")
        return [], []

    # Extract daily highs and lows
    daily_prices = data['prices'][-6:-1]  # Last 5 full days
    daily_highs = [price[1] for price in daily_prices]  # Approximate using closing prices
    daily_lows = [price[1] for price in daily_prices]

    # Identify highest high and lowest low independently
    highest_high = max(daily_highs)
    lowest_low = min(daily_lows)

    # Keep only relevant highs and lows
    filtered_highs = [h for h in daily_highs if h >= highest_high]
    filtered_lows = [l for l in daily_lows if l <= lowest_low]

    return filtered_highs, filtered_lows


# Fetch the latest hourly BTC candle
def get_hourly_btc():
    url = "https://api.coingecko.com/api/v3/coins/bitcoin/market_chart?vs_currency=usd&days=2"
    response = requests.get(url)

    if response.status_code != 200:
        print("Error fetching hourly BTC data:", response.text)
        return None, None, None

    data = response.json()

    if 'prices' not in data:
        print("Invalid data format returned")
        return None, None, None

    # Extract last hourly candle
    hourly_prices = data['prices'][-24:]  # Get the last 24 hours of data
    last_candle = hourly_prices[-1]
    hourly_high = last_candle[1]  # Approximate using closing price
    hourly_low = last_candle[1]
    hourly_close = last_candle[1]  # Closing price

    return hourly_high, hourly_low, hourly_close


# Check if conditions are met and send alerts
def check_conditions():
    filtered_highs, filtered_lows = get_btc_data()
    hourly_high, hourly_low, hourly_close = get_hourly_btc()

    if hourly_high is None:
        return  # Skip if data couldn't be fetched

    alert_message = "test"

    for h in filtered_highs:
        if hourly_high > h and hourly_close < h:  # Fakeout: Breaks above but closes below
            alert_message += "BTC Hourly fakeout above a previous daily high! \n"

    for l in filtered_lows:
        if hourly_low < l and hourly_close > l:  # Fakeout: Breaks below but closes above
            alert_message += "BTC Hourly fakeout below a previous daily low! \n"

    if alert_message:
        bot.send_message(chat_id=CHAT_ID, text=alert_message)


# Run the check every hour
if __name__ == "__main__":
    check_conditions()
