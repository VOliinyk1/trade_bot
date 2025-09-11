#!/usr/bin/env python3
"""
Простий тест без залежностей
"""

import sys
import os
from pathlib import Path

def test_basic_imports():
    """Тест базових імпортів"""
    print("🔍 Тестування базових імпортів...")
    
    try:
        import json
        import time
        import datetime
        import asyncio
        print("✅ Базові модулі Python працюють")
        return True
    except Exception as e:
        print(f"❌ Помилка базових модулів: {e}")
        return False

def test_file_structure():
    """Тест структури файлів"""
    print("🔍 Тестування структури файлів...")
    
    required_files = [
        'config.py',
        'binance_client.py',
        'technical_analysis.py',
        'news_aggregator.py',
        'chatgpt_analyzer.py',
        'telegram_bot.py',
        'signal_processor.py',
        'main.py'
    ]
    
    missing_files = []
    for file in required_files:
        if not Path(file).exists():
            missing_files.append(file)
    
    if missing_files:
        print("❌ Відсутні файли:")
        for file in missing_files:
            print(f"   - {file}")
        return False
    
    print("✅ Всі необхідні файли присутні")
    return True

def test_config():
    """Тест конфігурації"""
    print("🔍 Тестування конфігурації...")
    
    try:
        # Перевіряємо чи можна імпортувати config
        sys.path.append('.')
        import config
        
        # Перевіряємо основні змінні
        if hasattr(config, 'TRADING_PAIRS'):
            print(f"✅ Торгові пари: {config.TRADING_PAIRS}")
        else:
            print("❌ TRADING_PAIRS не знайдено")
            return False
        
        if hasattr(config, 'ANALYSIS_INTERVAL'):
            print(f"✅ Інтервал аналізу: {config.ANALYSIS_INTERVAL}")
        else:
            print("❌ ANALYSIS_INTERVAL не знайдено")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Помилка конфігурації: {e}")
        return False

def test_env_file():
    """Тест .env файлу"""
    print("🔍 Тестування .env файлу...")
    
    if not Path('.env').exists():
        print("❌ Файл .env не знайдено")
        print("📝 Створіть файл .env на основі env.example")
        return False
    
    print("✅ Файл .env знайдено")
    
    # Перевіряємо основні змінні
    try:
        with open('.env', 'r', encoding='utf-8') as f:
            content = f.read()
        
        required_vars = [
            'BINANCE_API_KEY',
            'BINANCE_API_SECRET',
            'OPENAI_API_KEY',
            'TELEGRAM_BOT_TOKEN',
            'TELEGRAM_CHANNEL_ID'
        ]
        
        missing_vars = []
        for var in required_vars:
            if var not in content or f"{var}=your_" in content:
                missing_vars.append(var)
        
        if missing_vars:
            print("⚠️ Не налаштовані змінні:")
            for var in missing_vars:
                print(f"   - {var}")
            print("📝 Налаштуйте ці змінні в .env файлі")
        else:
            print("✅ Всі змінні налаштовані")
        
        return True
        
    except Exception as e:
        print(f"❌ Помилка читання .env: {e}")
        return False

def main():
    """Головна функція"""
    print("🧪 Простий тест Crypto Trading Bot")
    print("=" * 40)
    
    tests = [
        ("Базові імпорти", test_basic_imports),
        ("Структура файлів", test_file_structure),
        ("Конфігурація", test_config),
        (".env файл", test_env_file)
    ]
    
    passed = 0
    for test_name, test_func in tests:
        print(f"\n📋 {test_name}...")
        if test_func():
            passed += 1
    
    print("\n" + "=" * 40)
    print("📊 ПІДСУМОК ТЕСТУВАННЯ:")
    
    if passed == len(tests):
        print("🎉 Всі базові тести пройдено!")
        print("\n📝 Наступні кроки:")
        print("1. Встановіть залежності: pip install -r requirements.txt")
        print("2. Налаштуйте API ключі в .env файлі")
        print("3. Запустіть повний тест: python test_bot.py")
        print("4. Запустіть бота: python main.py")
    else:
        print(f"⚠️ {passed}/{len(tests)} тестів пройдено")
        print("🔧 Виправте помилки та запустіть тест знову")

if __name__ == "__main__":
    main()
