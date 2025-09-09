#!/usr/bin/env python3
"""
Швидкий запуск Crypto Trading Bot
"""

import os
import sys
import asyncio
from pathlib import Path

def check_requirements():
    """Перевірити наявність необхідних файлів"""
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
    
    return True

def check_env_file():
    """Перевірити наявність .env файлу"""
    if not Path('.env').exists():
        print("❌ Файл .env не знайдено")
        print("📝 Створіть файл .env на основі env.example")
        return False
    return True

def main():
    """Головна функція"""
    print("🤖 Crypto Trading Bot - Швидкий запуск")
    print("=" * 40)
    
    # Перевіряємо файли
    if not check_requirements():
        print("\n❌ Не всі необхідні файли присутні")
        sys.exit(1)
    
    # Перевіряємо .env файл
    if not check_env_file():
        print("\n❌ Налаштуйте .env файл перед запуском")
        sys.exit(1)
    
    print("✅ Всі файли присутні")
    print("✅ .env файл знайдено")
    
    # Запускаємо бота
    print("\n🚀 Запуск бота...")
    try:
        from main import main as bot_main
        asyncio.run(bot_main())
    except KeyboardInterrupt:
        print("\n⏹️ Бот зупинено користувачем")
    except Exception as e:
        print(f"\n❌ Помилка запуску: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
