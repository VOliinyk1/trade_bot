#!/usr/bin/env python3
"""
Тест нашого власного Binance клієнта
"""

import sys
import os
from datetime import datetime

# Додаємо поточну директорію в шлях
sys.path.append('.')

def test_our_binance_client():
    """Тест нашого Binance клієнта"""
    print("🔍 Тестування нашого Binance клієнта...")
    
    try:
        from binance_client import BinanceClient
        
        # Створюємо клієнта
        client = BinanceClient()
        print("✅ Binance клієнт створено успішно")
        
        return client
        
    except Exception as e:
        print(f"❌ Помилка створення клієнта: {e}")
        return None

def test_get_klines(client):
    """Тест отримання історичних даних"""
    print("🔍 Тестування отримання історичних даних...")
    
    try:
        # Тестуємо отримання даних для BTCUSDT
        klines = client.get_klines("BTCUSDT", "1h", 10)
        
        if klines is not None and not klines.empty:
            print(f"✅ Отримано {len(klines)} записів для BTCUSDT")
            print(f"   Остання ціна: ${klines['close'].iloc[-1]:,.2f}")
            print(f"   Об'єм: {klines['volume'].iloc[-1]:,.2f}")
            return True
        else:
            print("❌ Не вдалося отримати історичні дані")
            return False
            
    except Exception as e:
        print(f"❌ Помилка отримання історичних даних: {e}")
        return False

def test_get_current_price(client):
    """Тест отримання поточної ціни"""
    print("🔍 Тестування отримання поточної ціни...")
    
    try:
        # Тестуємо отримання ціни для кількох символів
        symbols = ["BTCUSDT", "ETHUSDT", "BNBUSDT"]
        
        for symbol in symbols:
            price = client.get_current_price(symbol)
            if price is not None:
                print(f"   {symbol}: ${price:,.2f}")
            else:
                print(f"   {symbol}: ❌ Не вдалося отримати ціну")
        
        return True
        
    except Exception as e:
        print(f"❌ Помилка отримання поточної ціни: {e}")
        return False

def test_get_24h_ticker(client):
    """Тест отримання 24h статистики"""
    print("🔍 Тестування отримання 24h статистики...")
    
    try:
        # Тестуємо отримання статистики для BTCUSDT
        ticker = client.get_24h_ticker("BTCUSDT")
        
        if ticker is not None:
            print(f"✅ 24h статистика для {ticker['symbol']}:")
            print(f"   Ціна: ${ticker['price']:,.2f}")
            print(f"   Зміна: {ticker['change_percent']:+.2f}%")
            print(f"   Об'єм: {ticker['volume']:,.2f}")
            print(f"   Максимум: ${ticker['high']:,.2f}")
            print(f"   Мінімум: ${ticker['low']:,.2f}")
            return True
        else:
            print("❌ Не вдалося отримати 24h статистику")
            return False
            
    except Exception as e:
        print(f"❌ Помилка отримання 24h статистики: {e}")
        return False

def test_get_order_book(client):
    """Тест отримання ордербука"""
    print("🔍 Тестування отримання ордербука...")
    
    try:
        # Тестуємо отримання ордербука для BTCUSDT
        order_book = client.get_order_book("BTCUSDT", 5)
        
        if order_book is not None:
            print(f"✅ Ордербук BTCUSDT:")
            print("   Найкращі покупки:")
            for i, bid in enumerate(order_book['bids'][:3], 1):
                price, quantity = bid[0], bid[1]
                print(f"     {i}. ${price:,.2f} - {quantity:.6f} BTC")
            
            print("   Найкращі продажі:")
            for i, ask in enumerate(order_book['asks'][:3], 1):
                price, quantity = ask[0], ask[1]
                print(f"     {i}. ${price:,.2f} - {quantity:.6f} BTC")
            
            return True
        else:
            print("❌ Не вдалося отримати ордербук")
            return False
            
    except Exception as e:
        print(f"❌ Помилка отримання ордербука: {e}")
        return False

def test_get_all_pairs_data(client):
    """Тест отримання даних для всіх пар"""
    print("🔍 Тестування отримання даних для всіх пар...")
    
    try:
        # Тестуємо отримання даних для всіх пар
        all_data = client.get_all_pairs_data()
        
        if all_data:
            print(f"✅ Отримано дані для {len(all_data)} пар:")
            
            for symbol, data in all_data.items():
                if data and 'current_price' in data and data['current_price']:
                    price = data['current_price']
                    print(f"   {symbol}: ${price:,.2f}")
                else:
                    print(f"   {symbol}: ❌ Немає даних")
            
            return True
        else:
            print("❌ Не вдалося отримати дані для пар")
            return False
            
    except Exception as e:
        print(f"❌ Помилка отримання даних для всіх пар: {e}")
        return False

def main():
    """Головна функція"""
    print("🚀 Тест нашого Binance клієнта")
    print("=" * 50)
    
    # Створюємо клієнта
    client = test_our_binance_client()
    if not client:
        print("❌ Не вдалося створити клієнта. Завершення тестування.")
        return
    
    tests = [
        ("Історичні дані", lambda: test_get_klines(client)),
        ("Поточна ціна", lambda: test_get_current_price(client)),
        ("24h статистика", lambda: test_get_24h_ticker(client)),
        ("Ордербук", lambda: test_get_order_book(client)),
        ("Дані всіх пар", lambda: test_get_all_pairs_data(client))
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
        print("🎉 Всі тести пройдено! Наш Binance клієнт працює відмінно!")
        print("\n✅ Готово до роботи з ботом!")
    else:
        print(f"⚠️ {passed}/{len(tests)} тестів пройдено")
        print("🔧 Перевірте налаштування API ключів")
    
    print(f"\n⏰ Час тестування: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    main()
