#!/usr/bin/env python3
"""
Запуск всіх тестів для Crypto Trading Bot
"""

import sys
import os
import subprocess
from datetime import datetime

def run_test(test_file, test_name):
    """Запустити тест"""
    print(f"\n{'='*60}")
    print(f"🧪 {test_name}")
    print(f"{'='*60}")
    
    try:
        result = subprocess.run([sys.executable, test_file], 
                              capture_output=True, text=True, timeout=60)
        
        if result.returncode == 0:
            print("✅ Тест пройдено успішно")
            return True
        else:
            print("❌ Тест провалено")
            if result.stderr:
                print(f"Помилка: {result.stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        print("⏰ Тест перевищив час очікування")
        return False
    except Exception as e:
        print(f"❌ Помилка запуску тесту: {e}")
        return False

def main():
    """Головна функція"""
    print("🚀 Запуск всіх тестів Crypto Trading Bot")
    print(f"⏰ Час початку: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Список тестів
    tests = [
        ("test_simple.py", "Простий тест (базові перевірки)"),
        ("test_binance_simple.py", "Простий тест Binance API"),
        ("test_our_binance_client.py", "Тест нашого Binance клієнта"),
        ("test_binance_connection.py", "Повний тест Binance API")
    ]
    
    passed = 0
    total = len(tests)
    
    for test_file, test_name in tests:
        if os.path.exists(test_file):
            if run_test(test_file, test_name):
                passed += 1
        else:
            print(f"\n{'='*60}")
            print(f"🧪 {test_name}")
            print(f"{'='*60}")
            print(f"❌ Файл {test_file} не знайдено")
    
    # Підсумок
    print(f"\n{'='*60}")
    print("📊 ПІДСУМОК ВСІХ ТЕСТІВ")
    print(f"{'='*60}")
    
    if passed == total:
        print("🎉 Всі тести пройдено! Бот готовий до роботи!")
        print("\n✅ Наступні кроки:")
        print("1. Налаштуйте API ключі в .env файлі")
        print("2. Запустіть бота: python main.py")
    else:
        print(f"⚠️ {passed}/{total} тестів пройдено")
        print("\n🔧 Рекомендації:")
        print("1. Перевірте налаштування API ключів")
        print("2. Переконайтеся що всі залежності встановлені")
        print("3. Прочитайте TROUBLESHOOTING.md для детальних рішень")
    
    print(f"\n⏰ Час завершення: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    main()
