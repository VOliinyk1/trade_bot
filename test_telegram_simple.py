#!/usr/bin/env python3
"""
Простий тест Telegram бота
"""

import asyncio
import sys
from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHANNEL_ID

async def test_telegram():
    """Тестувати Telegram бота"""
    
    try:
        from aiogram import Bot
        
        print("🤖 Тестування Telegram бота...")
        print(f"🔑 Token: {TELEGRAM_BOT_TOKEN[:10]}...")
        print(f"📱 Channel ID: {TELEGRAM_CHANNEL_ID}")
        
        bot = Bot(token=TELEGRAM_BOT_TOKEN)
        
        # Тест 1: Отримати інформацію про бота
        print("\n📊 Тест 1: Інформація про бота")
        try:
            bot_info = await bot.get_me()
            print(f"✅ Бот: @{bot_info.username} ({bot_info.first_name})")
        except Exception as e:
            print(f"❌ Помилка отримання інформації про бота: {e}")
            return False
        
        # Тест 2: Спробувати відправити повідомлення
        print("\n📤 Тест 2: Відправка повідомлення")
        try:
            test_message = "🤖 Тест повідомлення від Crypto Trading Bot!"
            await bot.send_message(
                chat_id=TELEGRAM_CHANNEL_ID,
                text=test_message
            )
            print(f"✅ Повідомлення відправлено до {TELEGRAM_CHANNEL_ID}")
        except Exception as e:
            print(f"❌ Помилка відправки: {e}")
            
            # Спробуємо зробити chat_id числом
            try:
                chat_id_int = int(TELEGRAM_CHANNEL_ID)
                await bot.send_message(
                    chat_id=chat_id_int,
                    text=test_message
                )
                print(f"✅ Повідомлення відправлено до {chat_id_int} (як число)")
            except Exception as e2:
                print(f"❌ Помилка з числовим ID: {e2}")
                return False
        
        # Тест 3: Отримати інформацію про чат
        print("\n📋 Тест 3: Інформація про чат")
        try:
            chat_info = await bot.get_chat(TELEGRAM_CHANNEL_ID)
            print(f"✅ Чат: {chat_info.title or chat_info.first_name}")
            print(f"   Тип: {chat_info.type}")
        except Exception as e:
            print(f"❌ Помилка отримання інформації про чат: {e}")
        
        await bot.session.close()
        return True
        
    except Exception as e:
        print(f"❌ Критична помилка: {e}")
        return False

async def main():
    """Головна функція"""
    print("🚀 Запуск тесту Telegram бота...")
    
    if not TELEGRAM_BOT_TOKEN:
        print("❌ TELEGRAM_BOT_TOKEN не встановлено")
        return
    
    if not TELEGRAM_CHANNEL_ID:
        print("❌ TELEGRAM_CHANNEL_ID не встановлено")
        return
    
    success = await test_telegram()
    
    if success:
        print("\n✅ Тест пройдено успішно!")
    else:
        print("\n❌ Тест провалено!")
        print("\n💡 Рекомендації:")
        print("1. Перевірте правильність TELEGRAM_BOT_TOKEN")
        print("2. Перевірте правильність TELEGRAM_CHANNEL_ID")
        print("3. Переконайтеся, що бот додано до каналу/групи")
        print("4. Для особистих повідомлень використовуйте ваш user_id")

if __name__ == "__main__":
    asyncio.run(main())
