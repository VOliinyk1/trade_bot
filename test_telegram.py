#!/usr/bin/env python3
"""
Тест Telegram бота
"""

import sys
import os
from datetime import datetime

# Додаємо поточну директорію в шлях
sys.path.append('.')

def test_telegram_import():
    """Тест імпорту Telegram модулів"""
    print("🔍 Тестування імпорту Telegram модулів...")
    
    try:
        import aiogram
        from aiogram import Bot, Dispatcher
        print("✅ Telegram модулі імпортовано успішно")
        return True
    except ImportError as e:
        print(f"❌ Помилка імпорту Telegram модулів: {e}")
        return False

def test_telegram_config():
    """Тест конфігурації Telegram"""
    print("🔍 Тестування конфігурації Telegram...")
    
    try:
        import config
        
        if not config.TELEGRAM_BOT_TOKEN or config.TELEGRAM_BOT_TOKEN == "your_telegram_bot_token_here":
            print("❌ TELEGRAM_BOT_TOKEN не налаштовано")
            return False
        
        if not config.TELEGRAM_CHANNEL_ID or config.TELEGRAM_CHANNEL_ID == "your_telegram_channel_id_here":
            print("❌ TELEGRAM_CHANNEL_ID не налаштовано")
            return False
        
        print("✅ Telegram конфігурація налаштована")
        print(f"   Bot Token: {config.TELEGRAM_BOT_TOKEN[:10]}...")
        print(f"   Channel ID: {config.TELEGRAM_CHANNEL_ID}")
        
        return True
        
    except Exception as e:
        print(f"❌ Помилка перевірки конфігурації: {e}")
        return False

def test_telegram_bot_creation():
    """Тест створення Telegram бота"""
    print("🔍 Тестування створення Telegram бота...")
    
    try:
        import config
        from aiogram import Bot
        
        bot = Bot(token=config.TELEGRAM_BOT_TOKEN)
        print("✅ Telegram бот створено успішно")
        
        return bot
        
    except Exception as e:
        print(f"❌ Помилка створення бота: {e}")
        return None

def test_telegram_bot_info(bot):
    """Тест отримання інформації про бота"""
    print("🔍 Тестування отримання інформації про бота...")
    
    try:
        import asyncio
        
        async def get_bot_info():
            try:
                bot_info = await bot.get_me()
                print(f"✅ Інформація про бота:")
                print(f"   ID: {bot_info.id}")
                print(f"   Username: @{bot_info.username}")
                print(f"   First Name: {bot_info.first_name}")
                return True
            except Exception as e:
                print(f"❌ Помилка отримання інформації: {e}")
                return False
        
        return asyncio.run(get_bot_info())
        
    except Exception as e:
        print(f"❌ Помилка тестування інформації: {e}")
        return False

def test_telegram_channel_access(bot):
    """Тест доступу до каналу"""
    print("🔍 Тестування доступу до каналу...")
    
    try:
        import config
        import asyncio
        
        async def test_channel():
            try:
                # Спробуємо отримати інформацію про канал
                chat = await bot.get_chat(config.TELEGRAM_CHANNEL_ID)
                print(f"✅ Доступ до каналу успішний:")
                print(f"   Назва: {chat.title}")
                print(f"   Тип: {chat.type}")
                print(f"   ID: {chat.id}")
                return True
            except Exception as e:
                print(f"❌ Помилка доступу до каналу: {e}")
                print("🔧 Рекомендації:")
                print("   - Перевірте що бот доданий в канал як адміністратор")
                print("   - Перевірте правильність ID каналу")
                print("   - Для приватних каналів використовуйте числовий ID")
                return False
        
        return asyncio.run(test_channel())
        
    except Exception as e:
        print(f"❌ Помилка тестування каналу: {e}")
        return False

def test_telegram_message_sending(bot):
    """Тест відправки повідомлення"""
    print("🔍 Тестування відправки повідомлення...")
    
    try:
        import config
        import asyncio
        
        async def send_test_message():
            try:
                test_message = f"""
🧪 **Тест Telegram бота**

✅ Бот працює правильно!
⏰ Час: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

🔧 Якщо ви бачите це повідомлення, то Telegram інтеграція працює!
                """
                
                await bot.send_message(
                    chat_id=config.TELEGRAM_CHANNEL_ID,
                    text=test_message,
                    parse_mode="Markdown"
                )
                
                print("✅ Тестове повідомлення відправлено успішно!")
                return True
                
            except Exception as e:
                print(f"❌ Помилка відправки повідомлення: {e}")
                return False
        
        return asyncio.run(send_test_message())
        
    except Exception as e:
        print(f"❌ Помилка тестування відправки: {e}")
        return False

def main():
    """Головна функція"""
    print("🚀 Тест Telegram бота")
    print("=" * 50)
    
    tests = [
        ("Імпорт модулів", test_telegram_import),
        ("Конфігурація", test_telegram_config),
        ("Створення бота", test_telegram_bot_creation),
    ]
    
    passed = 0
    bot = None
    
    for test_name, test_func in tests:
        print(f"\n📋 {test_name}...")
        try:
            result = test_func()
            if result:
                passed += 1
                if test_name == "Створення бота":
                    bot = result
            else:
                print(f"❌ Тест {test_name} провалено")
        except Exception as e:
            print(f"❌ Критична помилка в тесті {test_name}: {e}")
    
    # Додаткові тести якщо бот створено
    if bot:
        additional_tests = [
            ("Інформація про бота", lambda: test_telegram_bot_info(bot)),
            ("Доступ до каналу", lambda: test_telegram_channel_access(bot)),
            ("Відправка повідомлення", lambda: test_telegram_message_sending(bot))
        ]
        
        for test_name, test_func in additional_tests:
            print(f"\n📋 {test_name}...")
            try:
                if test_func():
                    passed += 1
                else:
                    print(f"❌ Тест {test_name} провалено")
            except Exception as e:
                print(f"❌ Критична помилка в тесті {test_name}: {e}")
    
    print("\n" + "=" * 50)
    print("📊 ПІДСУМОК ТЕСТУВАННЯ:")
    
    total_tests = len(tests) + (3 if bot else 0)
    
    if passed == total_tests:
        print("🎉 Всі тести пройдено! Telegram бот працює правильно!")
        print("\n✅ Готово до роботи з ботом!")
    else:
        print(f"⚠️ {passed}/{total_tests} тестів пройдено")
        print("\n🔧 Рекомендації:")
        print("1. Перевірте налаштування в .env файлі")
        print("2. Переконайтеся що бот доданий в канал як адміністратор")
        print("3. Перевірте правильність ID каналу")
    
    print(f"\n⏰ Час тестування: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    main()
