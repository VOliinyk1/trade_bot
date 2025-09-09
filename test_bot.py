#!/usr/bin/env python3
"""
Тестовий скрипт для перевірки роботи бота
"""

import asyncio
import sys
from datetime import datetime

# Додаємо поточну директорію в шлях
sys.path.append('.')

from binance_client import BinanceClient
from technical_analysis import TechnicalAnalyzer
from news_aggregator import NewsAggregator
from chatgpt_analyzer import ChatGPTAnalyzer
from config import TRADING_PAIRS

async def test_binance_client():
    """Тест Binance клієнта"""
    print("🔍 Тестування Binance клієнта...")
    
    try:
        client = BinanceClient()
        
        # Тестуємо отримання даних для однієї пари
        symbol = TRADING_PAIRS[0]
        print(f"📊 Отримання даних для {symbol}...")
        
        data = client.get_all_pairs_data()
        if data and symbol in data:
            print(f"✅ Дані отримано для {symbol}")
            print(f"   Поточна ціна: ${data[symbol]['current_price']}")
            print(f"   Зміна 24г: {data[symbol]['ticker_24h']['change_percent']:.2f}%")
            return data[symbol]
        else:
            print(f"❌ Не вдалося отримати дані для {symbol}")
            return None
            
    except Exception as e:
        print(f"❌ Помилка тестування Binance: {e}")
        return None

def test_technical_analysis(symbol_data):
    """Тест технічного аналізу"""
    print("\n🔍 Тестування технічного аналізу...")
    
    try:
        analyzer = TechnicalAnalyzer()
        
        if not symbol_data or 'klines' not in symbol_data:
            print("❌ Немає даних для аналізу")
            return None
        
        symbol = TRADING_PAIRS[0]
        analysis = analyzer.get_analysis_summary(
            symbol, 
            symbol_data['klines'], 
            symbol_data['ticker_24h']
        )
        
        if analysis:
            print(f"✅ Аналіз завершено для {symbol}")
            print(f"   Рекомендація: {analysis['recommendation']}")
            print(f"   Тренд: {analysis['trend']}")
            print(f"   RSI: {analysis['indicators']['rsi']:.2f}")
            print(f"   Сила сигналу: {analysis['signal_strength']}")
            return analysis
        else:
            print("❌ Не вдалося проаналізувати дані")
            return None
            
    except Exception as e:
        print(f"❌ Помилка технічного аналізу: {e}")
        return None

def test_news_aggregator():
    """Тест збору новин"""
    print("\n🔍 Тестування збору новин...")
    
    try:
        aggregator = NewsAggregator()
        
        print("📰 Отримання новин...")
        news = aggregator.get_all_news()
        
        if news:
            print(f"✅ Отримано {len(news)} новин")
            print("📋 Перші 3 новини:")
            for i, item in enumerate(news[:3], 1):
                print(f"   {i}. {item['title'][:50]}...")
            
            # Тестуємо сентимент
            sentiment = aggregator.get_sentiment_analysis()
            print(f"📊 Сентимент: {sentiment['sentiment']} (оцінка: {sentiment['score']:.2f})")
            
            return news, sentiment
        else:
            print("❌ Новини не отримано")
            return None, None
            
    except Exception as e:
        print(f"❌ Помилка збору новин: {e}")
        return None, None

async def test_chatgpt_analyzer(technical_analysis, news_summary, market_sentiment):
    """Тест ChatGPT аналізу"""
    print("\n🔍 Тестування ChatGPT аналізу...")
    
    try:
        analyzer = ChatGPTAnalyzer()
        
        if not technical_analysis:
            print("❌ Немає технічного аналізу для ChatGPT")
            return None
        
        symbol = technical_analysis['symbol']
        print(f"🤖 Аналіз ChatGPT для {symbol}...")
        
        chatgpt_analysis = analyzer.analyze_trading_opportunity(
            symbol, 
            technical_analysis, 
            news_summary, 
            market_sentiment
        )
        
        if chatgpt_analysis:
            print(f"✅ ChatGPT аналіз завершено")
            print(f"   Рекомендація: {chatgpt_analysis['recommendation']}")
            print(f"   Впевненість: {chatgpt_analysis['confidence']:.1%}")
            print(f"   Рівень ризику: {chatgpt_analysis['risk_level']}")
            print(f"   Розмір позиції: {chatgpt_analysis['position_size']:.1%}")
            return chatgpt_analysis
        else:
            print("❌ ChatGPT аналіз не вдався")
            return None
            
    except Exception as e:
        print(f"❌ Помилка ChatGPT аналізу: {e}")
        return None

async def main():
    """Головна функція тестування"""
    print("🚀 Запуск тестування Crypto Trading Bot")
    print("=" * 50)
    
    # Тест 1: Binance клієнт
    symbol_data = await test_binance_client()
    
    # Тест 2: Технічний аналіз
    technical_analysis = test_technical_analysis(symbol_data)
    
    # Тест 3: Збір новин
    news, market_sentiment = test_news_aggregator()
    news_summary = "Тестові новини" if news else "Новини недоступні"
    
    # Тест 4: ChatGPT аналіз
    chatgpt_analysis = await test_chatgpt_analyzer(
        technical_analysis, 
        news_summary, 
        market_sentiment or {}
    )
    
    # Підсумок
    print("\n" + "=" * 50)
    print("📊 ПІДСУМОК ТЕСТУВАННЯ:")
    
    tests = [
        ("Binance API", symbol_data is not None),
        ("Технічний аналіз", technical_analysis is not None),
        ("Збір новин", news is not None),
        ("ChatGPT аналіз", chatgpt_analysis is not None)
    ]
    
    passed = 0
    for test_name, result in tests:
        status = "✅ ПРОЙДЕНО" if result else "❌ ПРОВАЛЕНО"
        print(f"   {test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\n🎯 Результат: {passed}/{len(tests)} тестів пройдено")
    
    if passed == len(tests):
        print("🎉 Всі тести пройдено! Бот готовий до роботи.")
    else:
        print("⚠️ Деякі тести провалено. Перевірте налаштування.")
    
    # Показуємо приклад сигналу
    if chatgpt_analysis:
        print("\n📈 ПРИКЛАД СИГНАЛУ:")
        print(f"   Символ: {chatgpt_analysis['symbol']}")
        print(f"   Рекомендація: {chatgpt_analysis['recommendation']}")
        print(f"   Вхід: ${chatgpt_analysis['entry_price']:.4f}")
        print(f"   Stop Loss: ${chatgpt_analysis['stop_loss']:.4f}")
        print(f"   Take Profit: ${chatgpt_analysis['take_profit']:.4f}")

if __name__ == "__main__":
    asyncio.run(main())
