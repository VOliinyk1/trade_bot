#!/usr/bin/env python3
"""
Перевірити конфігурацію
"""

try:
    from config import (
        BINANCE_API_KEY, BINANCE_API_SECRET, 
        OPENAI_API_KEY, TELEGRAM_BOT_TOKEN, 
        TELEGRAM_CHANNEL_ID, TRADING_PAIRS
    )
    
    print("📋 Поточна конфігурація:")
    print(f"🔑 Binance API Key: {'✅ Встановлено' if BINANCE_API_KEY else '❌ Не встановлено'}")
    print(f"🔑 Binance API Secret: {'✅ Встановлено' if BINANCE_API_SECRET else '❌ Не встановлено'}")
    print(f"🤖 OpenAI API Key: {'✅ Встановлено' if OPENAI_API_KEY else '❌ Не встановлено'}")
    print(f"📱 Telegram Bot Token: {'✅ Встановлено' if TELEGRAM_BOT_TOKEN else '❌ Не встановлено'}")
    print(f"📱 Telegram Channel ID: {TELEGRAM_CHANNEL_ID}")
    print(f"📊 Trading Pairs: {TRADING_PAIRS}")
    
    if TELEGRAM_BOT_TOKEN:
        print(f"🔍 Token початок: {TELEGRAM_BOT_TOKEN[:15]}...")
    
except Exception as e:
    print(f"❌ Помилка завантаження конфігурації: {e}")
