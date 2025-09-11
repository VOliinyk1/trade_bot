#!/usr/bin/env python3
"""
Простий тест підключення до Binance API (без перевірки дозволів)
"""

import sys
import os
from datetime import datetime

# Додаємо поточну директорію в шлях
sys.path.append('.')

def test_basic_connection():
    """Базовий тест підключення"""
    print("🔍 Тестування базового підключення до Binance...")
    
    try:
        import config
        from binance.client import Client
        
        # Створюємо клієнта
        client = Client(config.BINANCE_API_KEY, config.BINANCE_API_SECRET)
        
        # Тестуємо підключення
        server_time = client.get_server_time()
        print(f"✅ Підключення успішне! Час сервера: {datetime.fromtimestamp(server_time['serverTime']/1000)}")
        
        return True
        
    except Exception as e:
        print(f"❌ Помилка підключення: {e}")
        return False

def test_price_data():
    """Тест отримання цін"""
    print("🔍 Тестування отримання цін...")
    
    try:
        import config
        from binance.client import Client
        
        client = Client(config.BINANCE_API_KEY, config.BINANCE_API_SECRET)
        
        # Тестуємо кілька популярних пар
        symbols = ["BTCUSDT", "ETHUSDT", "BNBUSDT", "ADAUSDT", "SOLUSDT"]
        
        for symbol in symbols:
            try:
                ticker = client.get_symbol_ticker(symbol=symbol)
                price = float(ticker['price'])
                print(f"   {symbol}: ${price:,.2f}")
            except Exception as e:
                print(f"   {symbol}: ❌ {e}")
        
        return True
        
    except Exception as e:
        print(f"❌ Помилка отримання цін: {e}")
        return False

def test_historical_data():
    """Тест отримання історичних даних"""
    print("🔍 Тестування отримання історичних даних...")
    
    try:
        import config
        from binance.client import Client
        
        client = Client(config.BINANCE_API_KEY, config.BINANCE_API_SECRET)
        
        # Тестуємо отримання історичних даних
        klines = client.get_klines(symbol="BTCUSDT", interval="1h", limit=10)
        
        if klines:
            print(f"✅ Отримано {len(klines)} записів для BTCUSDT")
            
            # Показуємо останні 3 записи
            for i, kline in enumerate(klines[-3:], 1):
                timestamp = datetime.fromtimestamp(kline[0]/1000)
                open_price = float(kline[1])
                high_price = float(kline[2])
                low_price = float(kline[3])
                close_price = float(kline[4])
                volume = float(kline[5])
                
                print(f"   {i}. {timestamp.strftime('%Y-%m-%d %H:%M')}: "
                      f"O=${open_price:,.2f} H=${high_price:,.2f} "
                      f"L=${low_price:,.2f} C=${close_price:,.2f} V={volume:,.2f}")
        else:
            print("❌ Не вдалося отримати історичні дані")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Помилка отримання історичних даних: {e}")
        return False

def test_24h_stats():
    """Тест отримання 24h статистики"""
    print("🔍 Тестування отримання 24h статистики...")
    
    try:
        import config
        from binance.client import Client
        
        client = Client(config.BINANCE_API_KEY, config.BINANCE_API_SECRET)
        
        # Тестуємо отримання 24h статистики
        ticker_24h = client.get_ticker(symbol="BTCUSDT")
        
        price = float(ticker_24h['lastPrice'])
        change = float(ticker_24h['priceChange'])
        change_percent = float(ticker_24h['priceChangePercent'])
        volume = float(ticker_24h['volume'])
        high = float(ticker_24h['highPrice'])
        low = float(ticker_24h['lowPrice'])
        
        print(f"✅ BTCUSDT 24h статистика:")
        print(f"   Поточна ціна: ${price:,.2f}")
        print(f"   Зміна: ${change:+,.2f} ({change_percent:+.2f}%)")
        print(f"   Об'єм: {volume:,.2f} BTC")
        print(f"   Максимум: ${high:,.2f}")
        print(f"   Мінімум: ${low:,.2f}")
        
        return True
        
    except Exception as e:
        print(f"❌ Помилка отримання 24h статистики: {e}")
        return False

def test_order_book():
    """Тест отримання ордербука"""
    print("🔍 Тестування отримання ордербука...")
    
    try:
        import config
        from binance.client import Client
        
        client = Client(config.BINANCE_API_KEY, config.BINANCE_API_SECRET)
        
        # Тестуємо отримання ордербука
        depth = client.get_order_book(symbol="BTCUSDT", limit=5)
        
        print(f"✅ Ордербук BTCUSDT:")
        print("   Найкращі покупки (Bids):")
        for i, bid in enumerate(depth['bids'][:3], 1):
            price, quantity = float(bid[0]), float(bid[1])
            print(f"     {i}. ${price:,.2f} - {quantity:.6f} BTC")
        
        print("   Найкращі продажі (Asks):")
        for i, ask in enumerate(depth['asks'][:3], 1):
            price, quantity = float(ask[0]), float(ask[1])
            print(f"     {i}. ${price:,.2f} - {quantity:.6f} BTC")
        
        return True
        
    except Exception as e:
        print(f"❌ Помилка отримання ордербука: {e}")
        return False

def main():
    """Головна функція"""
    print("🚀 Простий тест підключення до Binance API")
    print("=" * 50)
    
    tests = [
        ("Базове підключення", test_basic_connection),
        ("Отримання цін", test_price_data),
        ("Історичні дані", test_historical_data),
        ("24h статистика", test_24h_stats),
        ("Ордербук", test_order_book)
    ]
    
    passed = 0
    
    for test_name, test_func in tests:
        print(f"\n📋 {test_name}...")
        try:
            if test_func():
                passed += 1
        except Exception as e:
            print(f"❌ Критична помилка: {e}")
    
    print("\n" + "=" * 50)
    print("📊 ПІДСУМОК ТЕСТУВАННЯ:")
    
    if passed == len(tests):
        print("🎉 Всі тести пройдено! Binance API працює відмінно!")
        print("\n✅ Готово до роботи з ботом!")
    else:
        print(f"⚠️ {passed}/{len(tests)} тестів пройдено")
        print("🔧 Перевірте налаштування API ключів")
    
    print(f"\n⏰ Час тестування: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    main()
