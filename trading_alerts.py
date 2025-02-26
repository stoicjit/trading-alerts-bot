import requests
import asyncio
import os
from tradingview_ta import TA_Handler, Interval, Exchange
from telegram import Bot

# Set up Telegram bot with your bot token and chat ID
bot_token = os.getenv('BOT_TOKEN')  # Replace with your Telegram bot token
CHAT_ID = os.getenv('CHAT_ID')  # Replace with your Telegram chat ID
bot = Bot(token=bot_token)

# Define the trading pair and exchange
symbols = ["BTCUSD", 'ETHUSD', "XRPUSD"]
exchange = "BINANCE"  # Use your preferred exchange
w_list=[]
h_list=[]
compare_list=[0,1,2]

def weekly_rsi():
    for symbol in symbols:
        ta = TA_Handler(
            symbol=symbol,
            exchange=exchange,
            screener="crypto",
            interval=Interval.INTERVAL_1_WEEK,  # Choose the timeframe (e.g., 1h, 1d)
        )

        # Get the latest rsi data
        analysis = ta.get_analysis()
        print(symbol)
        print('rsi:', analysis.indicators["RSI"])
        rsi=analysis.indicators['RSI']
        w_list.append(rsi)
    print(w_list)
    return None

def four_hour_rsi():# Fetch TradingView OHLC Data
    for symbol in symbols:
        ta = TA_Handler(
        symbol=symbol,
        exchange=exchange,
        screener="crypto",
        interval=Interval.INTERVAL_4_HOURS,  # Choose the timeframe (e.g., 1h, 1d)
        )

# Get the latest 4h rsi data
        analysis = ta.get_analysis()
        print(symbol)
        print('rsi:', analysis.indicators["RSI"])
        rsi = analysis.indicators["RSI"]
        h_list.append(rsi)


def compare_rsi():
    for x in compare_list:
        if h_list[x] < 20 and w_list[x] > 50:
            async def send_telegram_message():
                message=f'{symbols[x]} just flashed on the rsi'
                await bot.send_message(chat_id=CHAT_ID, text=message)
            asyncio.run(send_telegram_message())
        if h_list[x] > 80 and w_list[x] < 50:
            async def send_telegram_message():
                message=f'{symbols[x]} just flashed on the rsi'
                await bot.send_message(chat_id=CHAT_ID, text=message)
            asyncio.run(send_telegram_message())
        else:
            async def send_telegram_message():
                message='nothing here'
                await bot.send_message(chat_id=CHAT_ID, text=message)
            asyncio.run(send_telegram_message())


weekly_rsi()
four_hour_rsi()
compare_rsi()
