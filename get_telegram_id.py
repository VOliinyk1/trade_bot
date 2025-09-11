#!/usr/bin/env python3
"""
Отримати Telegram user ID
"""

import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

# Тимчасовий токен для тестування
TELEGRAM_BOT_TOKEN = "8306907468:AAGjVQZvNQqH5kQ9kQ9kQ9kQ9kQ9kQ9kQ9k"

class TelegramIDGetter:
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
            username = message.from_user.username
            first_name = message.from_user.first_name
            
            print(f"\n✅ Знайдено користувача!")
            print(f"🆔 User ID: {user_id}")
            print(f"👤 Username: @{username}")
            print(f"📝 Ім'я: {first_name}")
            
            response_text = f"""
🎉 **Ваш Telegram ID знайдено!**

🆔 **User ID:** `{user_id}`
👤 **Username:** @{username}
📝 **Ім'я:** {first_name}

📋 **Для налаштування бота:**
1. Скопіюйте User ID: `{user_id}`
2. Вставте його в файл .env як TELEGRAM_CHANNEL_ID
3. Запустіть бота знову

💡 **Приклад .env файлу:**
```
TELEGRAM_CHANNEL_ID={user_id}
```
            """
            
            await message.answer(response_text, parse_mode="Markdown")
            
            # Зберігаємо ID для повернення
            self.user_id = user_id
            
            # Зупиняємо бота після отримання ID
            await self.stop_bot()
    
    async def start_polling(self):
        """Запустити polling"""
        print("🤖 Запуск бота для отримання вашого Telegram ID...")
        print("📱 Надішліть команду /start боту @techsig_843783248_bot")
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
    id_getter = TelegramIDGetter()
    
    try:
        await id_getter.start_polling()
    except Exception as e:
        print(f"❌ Помилка: {e}")
    finally:
        user_id = id_getter.get_user_id()
        if user_id:
            print(f"\n🎯 Ваш Telegram ID: {user_id}")
            print("📝 Використовуйте цей ID в .env файлі як TELEGRAM_CHANNEL_ID")
        else:
            print("\n❌ ID не отримано. Спробуйте ще раз.")

if __name__ == "__main__":
    asyncio.run(main())
