#!/usr/bin/env python3
"""
Отримати ваш Telegram user ID
"""

import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from config import TELEGRAM_BOT_TOKEN

class MyTelegramIDGetter:
    def __init__(self):
        self.bot = Bot(token=TELEGRAM_BOT_TOKEN)
        self.dp = Dispatcher()
        self.user_id = None
        self.setup_handlers()
    
    def setup_handlers(self):
        """Налаштувати обробники команд"""
        
        @self.dp.message(Command("start"))
        async def start_handler(message: types.Message):
            user_id = message.from_user.id
            username = message.from_user.username or "Немає"
            first_name = message.from_user.first_name or "Немає"
            
            print(f"\n🎉 ЗНАЙДЕНО ВАШ TELEGRAM ID!")
            print(f"🆔 User ID: {user_id}")
            print(f"👤 Username: @{username}")
            print(f"📝 Ім'я: {first_name}")
            print(f"\n📋 Для виправлення помилки 'chat not found':")
            print(f"1. Відкрийте файл .env")
            print(f"2. Змініть TELEGRAM_CHANNEL_ID={user_id}")
            print(f"3. Збережіть файл")
            print(f"4. Запустіть бота знову")
            
            response_text = f"""
🎉 **Ваш Telegram ID знайдено!**

🆔 **User ID:** `{user_id}`
👤 **Username:** @{username}
📝 **Ім'я:** {first_name}

📋 **Для налаштування:**
1. Відкрийте файл .env
2. Змініть: TELEGRAM_CHANNEL_ID={user_id}
3. Збережіть файл
4. Запустіть бота знову

✅ Тепер бот зможе відправляти вам повідомлення!
            """
            
            await message.answer(response_text, parse_mode="Markdown")
            
            # Зберігаємо ID
            self.user_id = user_id
            
            # Зупиняємо бота
            await self.stop_bot()
    
    async def start_polling(self):
        """Запустити polling"""
        print("🤖 Запуск бота для отримання вашого Telegram ID...")
        print("📱 Знайдіть бота @techsig_843783248_bot в Telegram")
        print("📱 Надішліть команду /start")
        print("⏳ Очікування повідомлення...")
        
        try:
            await self.dp.start_polling(self.bot)
        except Exception as e:
            print(f"❌ Помилка polling: {e}")
    
    async def stop_bot(self):
        """Зупинити бота"""
        try:
            await self.bot.session.close()
        except Exception as e:
            print(f"❌ Помилка зупинки бота: {e}")
    
    def get_user_id(self):
        """Отримати user ID"""
        return self.user_id

async def main():
    """Головна функція"""
    print("🚀 Запуск отримання вашого Telegram ID...")
    print("📱 Цей скрипт допоможе виправити помилку 'chat not found'")
    
    id_getter = MyTelegramIDGetter()
    
    try:
        await id_getter.start_polling()
    except KeyboardInterrupt:
        print("\n⏹️ Зупинено користувачем")
    except Exception as e:
        print(f"❌ Помилка: {e}")
    finally:
        user_id = id_getter.get_user_id()
        if user_id:
            print(f"\n🎯 Ваш Telegram ID: {user_id}")
            print("📝 Використовуйте цей ID в .env файлі!")
        else:
            print("\n❌ ID не отримано.")
            print("💡 Переконайтеся, що надіслали /start боту @techsig_843783248_bot")

if __name__ == "__main__":
    asyncio.run(main())
