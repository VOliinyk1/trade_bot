#!/usr/bin/env python3
"""
Тест підключення до Binance API
"""

import sys
import os
from datetime import datetime
import time

# Додаємо поточну директорію в шлях
sys.path.append('.')

def test_binance_import():
    """Тест імпорту Binance клієнта"""
    print("🔍 Тестування імпорту Binance клієнта...")
    
    try:
        from binance.client import Client
        print("✅ Binance клієнт імпортовано успішно")
        return True
    except ImportError as e:
        print(f"❌ Помилка імпорту Binance клієнта: {e}")
        return False

def test_config_import():
    """Тест імпорту конфігурації"""
    print("🔍 Тестування імпорту конфігурації...")
    
    try:
        import config
        print("✅ Конфігурація імпортована успішно")
        return True
    except ImportError as e:
        print(f"❌ Помилка імпорту конфігурації: {e}")
        return False

def test_api_keys():
    """Тест наявності API ключів"""
    print("🔍 Тестування API ключів...")
    
    try:
        import config
        
        if not config.BINANCE_API_KEY or config.BINANCE_API_KEY == "your_binance_api_key_here":
            print("❌ BINANCE_API_KEY не налаштовано")
            return False
        
        if not config.BINANCE_API_SECRET or config.BINANCE_API_SECRET == "your_binance_api_secret_here":
            print("❌ BINANCE_API_SECRET не налаштовано")
            return False
        
        print("✅ API ключі налаштовані")
        return True
        
    except Exception as e:
        print(f"❌ Помилка перевірки API ключів: {e}")
        return False

def test_binance_connection():
    """Тест підключення до Binance"""
    print("🔍 Тестування підключення до Binance...")
    
    try:
        import config
        from binance.client import Client
        
        # Створюємо клієнта
        client = Client(config.BINANCE_API_KEY, config.BINANCE_API_SECRET)
        
        # Тестуємо підключення
        print("📡 Тестування підключення...")
        server_time = client.get_server_time()
        print(f"✅ Підключення успішне! Час сервера: {datetime.fromtimestamp(server_time['serverTime']/1000)}")
        
        return True
        
    except Exception as e:
        print(f"❌ Помилка підключення до Binance: {e}")
        return False

def test_binance_permissions():
    """Тест дозволів API"""
    print("🔍 Тестування дозволів API...")
    
    try:
        import config
        from binance.client import Client
        
        client = Client(config.BINANCE_API_KEY, config.BINANCE_API_SECRET)
        
        # Тестуємо отримання інформації про акаунт
        print("📊 Тестування доступу до акаунту...")
        account_info = client.get_account()
        print(f"✅ Доступ до акаунту успішний! Тип акаунту: {account_info.get('accountType', 'Unknown')}")
        
        # Перевіряємо дозволи
        permissions = account_info.get('permissions', [])
        print(f"📋 Дозволи: {', '.join(permissions)}")
        
        if 'SPOT' in permissions:
            print("✅ Spot Trading дозволено")
        else:
            print("⚠️ Spot Trading не дозволено")
        
        return True
        
    except Exception as e:
        print(f"❌ Помилка перевірки дозволів: {e}")
        return False

def test_binance_data():
    """Тест отримання даних"""
    print("🔍 Тестування отримання даних...")
    
    try:
        import config
        from binance.client import Client
        
        client = Client(config.BINANCE_API_KEY, config.BINANCE_API_SECRET)
        
        # Тестуємо отримання ціни
        print("💰 Тестування отримання ціни BTCUSDT...")
        ticker = client.get_symbol_ticker(symbol="BTCUSDT")
        price = float(ticker['price'])
        print(f"✅ Ціна BTCUSDT: ${price:,.2f}")
        
        # Тестуємо отримання 24h статистики
        print("📈 Тестування отримання 24h статистики...")
        ticker_24h = client.get_ticker(symbol="BTCUSDT")
        change_percent = float(ticker_24h['priceChangePercent'])
        volume = float(ticker_24h['volume'])
        print(f"✅ Зміна за 24г: {change_percent:+.2f}%")
        print(f"✅ Об'єм за 24г: {volume:,.2f} BTC")
        
        # Тестуємо отримання історичних даних
        print("📊 Тестування отримання історичних даних...")
        klines = client.get_klines(symbol="BTCUSDT", interval="1h", limit=5)
        print(f"✅ Отримано {len(klines)} записів історичних даних")
        
        if klines:
            latest_close = float(klines[-1][4])  # Close price
            print(f"✅ Остання ціна закриття: ${latest_close:,.2f}")
        
        return True
        
    except Exception as e:
        print(f"❌ Помилка отримання даних: {e}")
        return False

def test_binance_limits():
    """Тест лімітів API"""
    print("🔍 Тестування лімітів API...")
    
    try:
        import config
        from binance.client import Client
        
        client = Client(config.BINANCE_API_KEY, config.BINANCE_API_SECRET)
        
        # Тестуємо кілька запитів підряд
        print("⚡ Тестування швидкості запитів...")
        
        symbols = ["BTCUSDT", "ETHUSDT", "BNBUSDT"]
        start_time = time.time()
        
        for symbol in symbols:
            ticker = client.get_symbol_ticker(symbol=symbol)
            price = float(ticker['price'])
            print(f"   {symbol}: ${price:,.2f}")
        
        end_time = time.time()
        duration = end_time - start_time
        
        print(f"✅ {len(symbols)} запитів виконано за {duration:.2f} секунд")
        
        if duration < 2.0:
            print("✅ Швидкість запитів нормальна")
        else:
            print("⚠️ Запити виконуються повільно")
        
        return True
        
    except Exception as e:
        print(f"❌ Помилка тестування лімітів: {e}")
        return False

def test_binance_errors():
    """Тест обробки помилок"""
    print("🔍 Тестування обробки помилок...")
    
    try:
        import config
        from binance.client import Client
        from binance.exceptions import BinanceAPIException
        
        client = Client(config.BINANCE_API_KEY, config.BINANCE_API_SECRET)
        
        # Тестуємо запит з неіснуючим символом
        print("🚫 Тестування запиту з неіснуючим символом...")
        try:
            client.get_symbol_ticker(symbol="INVALIDPAIR")
            print("❌ Очікувалася помилка, але запит пройшов успішно")
            return False
        except BinanceAPIException as e:
            print(f"✅ Помилка оброблена правильно: {e.message}")
        
        # Тестуємо запит з невалідним інтервалом
        print("🚫 Тестування запиту з невалідним інтервалом...")
        try:
            client.get_klines(symbol="BTCUSDT", interval="invalid", limit=1)
            print("❌ Очікувалася помилка, але запит пройшов успішно")
            return False
        except BinanceAPIException as e:
            print(f"✅ Помилка оброблена правильно: {e.message}")
        
        return True
        
    except Exception as e:
        print(f"❌ Помилка тестування обробки помилок: {e}")
        return False

def main():
    """Головна функція тестування"""
    print("🚀 Тест підключення до Binance API")
    print("=" * 50)
    
    tests = [
        ("Імпорт Binance клієнта", test_binance_import),
        ("Імпорт конфігурації", test_config_import),
        ("API ключі", test_api_keys),
        ("Підключення до Binance", test_binance_connection),
        ("Дозволи API", test_binance_permissions),
        ("Отримання даних", test_binance_data),
        ("Ліміти API", test_binance_limits),
        ("Обробка помилок", test_binance_errors)
    ]
    
    passed = 0
    failed_tests = []
    
    for test_name, test_func in tests:
        print(f"\n📋 {test_name}...")
        try:
            if test_func():
                passed += 1
            else:
                failed_tests.append(test_name)
        except Exception as e:
            print(f"❌ Критична помилка в тесті {test_name}: {e}")
            failed_tests.append(test_name)
    
    print("\n" + "=" * 50)
    print("📊 ПІДСУМОК ТЕСТУВАННЯ:")
    
    if passed == len(tests):
        print("🎉 Всі тести пройдено! Binance API працює правильно.")
        print("\n✅ Готово до роботи з ботом!")
    else:
        print(f"⚠️ {passed}/{len(tests)} тестів пройдено")
        if failed_tests:
            print("❌ Провалені тести:")
            for test in failed_tests:
                print(f"   - {test}")
        
        print("\n🔧 Рекомендації:")
        if "API ключі" in failed_tests:
            print("   - Налаштуйте API ключі в .env файлі")
        if "Підключення до Binance" in failed_tests:
            print("   - Перевірте підключення до інтернету")
            print("   - Перевірте правильність API ключів")
        if "Дозволи API" in failed_tests:
            print("   - Дозвольте Spot Trading в налаштуваннях API")
        if "Ліміти API" in failed_tests:
            print("   - Можливо, перевищено ліміти API")
    
    print(f"\n⏰ Час тестування: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    main()
