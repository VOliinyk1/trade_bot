#!/usr/bin/env python3
"""
Crypto Trading Bot без ChatGPT
Автоматичний бот для аналізу криптовалют та відправки торгових сигналів
"""

import asyncio
import signal
import sys
from datetime import datetime
import logging

from signal_processor_no_chatgpt import SignalProcessorNoChatGPT
from telegram_bot import TelegramBot
from config import TRADING_PAIRS, ANALYSIS_INTERVAL

# Налаштування логування
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('bot.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

class CryptoBotNoChatGPT:
    def __init__(self):
        self.signal_processor = SignalProcessorNoChatGPT()
        self.telegram_bot = TelegramBot()
        self.is_running = False
        
        # Налаштування обробки сигналів для graceful shutdown
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
    
    def _signal_handler(self, signum, frame):
        """Обробник сигналів для graceful shutdown"""
        logger.info(f"Отримано сигнал {signum}. Зупинка бота...")
        self.stop()
    
    async def start(self):
        """Запустити бота"""
        try:
            logger.info("🚀 Запуск Crypto Trading Bot (без ChatGPT)...")
            logger.info(f"📊 Торгові пари: {', '.join(TRADING_PAIRS)}")
            logger.info(f"⏰ Інтервал аналізу: {ANALYSIS_INTERVAL} секунд")
            
            self.is_running = True
            
            # Запускаємо основні задачі
            tasks = [
                asyncio.create_task(self.signal_processor.start_analysis_loop()),
                asyncio.create_task(self.telegram_bot.start_polling())
            ]
            
            # Відправляємо стартове повідомлення
            await self._send_startup_message()
            
            # Очікуємо завершення задач
            await asyncio.gather(*tasks, return_exceptions=True)
            
        except Exception as e:
            logger.error(f"❌ Критична помилка: {e}")
            await self.telegram_bot.send_error_notification(f"Критична помилка бота: {str(e)}")
        finally:
            await self.cleanup()
    
    async def _send_startup_message(self):
        """Відправити повідомлення про запуск"""
        try:
            startup_message = f"""
🤖 **Crypto Trading Bot запущено! (Режим без ChatGPT)**

📊 **Налаштування:**
• Торгові пари: {len(TRADING_PAIRS)}
• Інтервал аналізу: {ANALYSIS_INTERVAL} сек
• Поріг сигналу: 70%

🔧 **Модулі:**
• ✅ Binance API
• ✅ Технічний аналіз
• ✅ Збір новин
• ⚠️ ChatGPT аналіз (відключено)
• ✅ Telegram бот

⏰ **Час запуску:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

🚀 Бот готовий до роботи в режимі технічного аналізу!
            """
            
            await self.telegram_bot.send_news_update(startup_message)
            logger.info("✅ Стартове повідомлення відправлено")
            
        except Exception as e:
            logger.error(f"❌ Помилка відправки стартового повідомлення: {e}")
    
    def stop(self):
        """Зупинити бота"""
        logger.info("🛑 Зупинка бота...")
        self.is_running = False
        self.signal_processor.stop_analysis()
    
    async def cleanup(self):
        """Очистити ресурси"""
        try:
            logger.info("🧹 Очищення ресурсів...")
            await self.telegram_bot.stop_bot()
            logger.info("✅ Очищення завершено")
        except Exception as e:
            logger.error(f"❌ Помилка очищення: {e}")
    
    async def run_manual_analysis(self, symbol: str):
        """Запустити ручний аналіз"""
        try:
            logger.info(f"🔍 Ручний аналіз для {symbol}")
            await self.signal_processor.send_manual_analysis(symbol)
        except Exception as e:
            logger.error(f"❌ Помилка ручного аналізу: {e}")
    
    async def send_news_update(self):
        """Відправити оновлення новин"""
        try:
            logger.info("📰 Відправка оновлення новин")
            await self.signal_processor.send_news_update()
        except Exception as e:
            logger.error(f"❌ Помилка відправки новин: {e}")
    
    def get_status(self):
        """Отримати статус бота"""
        return {
            'is_running': self.is_running,
            'signal_processor': self.signal_processor.get_status(),
            'uptime': datetime.now().isoformat()
        }

async def main():
    """Головна функція"""
    bot = CryptoBotNoChatGPT()
    
    try:
        await bot.start()
    except KeyboardInterrupt:
        logger.info("⏹️ Отримано Ctrl+C. Зупинка...")
        bot.stop()
    except Exception as e:
        logger.error(f"❌ Неочікувана помилка: {e}")
    finally:
        await bot.cleanup()

if __name__ == "__main__":
    # Перевіряємо наявність необхідних змінних середовища
    from config import BINANCE_API_KEY, BINANCE_API_SECRET, TELEGRAM_BOT_TOKEN, TELEGRAM_CHANNEL_ID
    
    required_vars = {
        'BINANCE_API_KEY': BINANCE_API_KEY,
        'BINANCE_API_SECRET': BINANCE_API_SECRET,
        'TELEGRAM_BOT_TOKEN': TELEGRAM_BOT_TOKEN,
        'TELEGRAM_CHANNEL_ID': TELEGRAM_CHANNEL_ID
    }
    
    missing_vars = [var for var, value in required_vars.items() if not value]
    
    if missing_vars:
        logger.error(f"❌ Відсутні змінні середовища: {', '.join(missing_vars)}")
        logger.error("📝 Створіть файл .env на основі env.example")
        sys.exit(1)
    
    # Запускаємо бота
    asyncio.run(main())
