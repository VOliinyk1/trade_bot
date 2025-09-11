#!/usr/bin/env python3
"""
Crypto Trading Bot - з ChatGPT повідомленнями в Telegram
Автоматичний бот для аналізу криптовалют та відправки детальних ChatGPT аналізів в Telegram
"""

import asyncio
import signal
import sys
from datetime import datetime
import logging

from signal_processor_telegram import SignalProcessorTelegram
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

class CryptoBotTelegramChatGPT:
    def __init__(self):
        self.signal_processor = SignalProcessorTelegram()
        self.telegram_bot = TelegramBot()
        self.is_running = False
        self.shutdown_event = asyncio.Event()
        
        # Налаштування обробки сигналів для graceful shutdown
        self._setup_signal_handlers()
    
    def _setup_signal_handlers(self):
        """Налаштувати обробники сигналів"""
        def signal_handler(signum, frame):
            logger.info(f"Отримано сигнал {signum}. Зупинка бота...")
            self.shutdown_event.set()
        
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)
    
    async def start(self):
        """Запустити бота"""
        try:
            logger.info("🚀 Запуск Crypto Trading Bot (з ChatGPT Telegram повідомленнями)...")
            logger.info(f"📊 Торгові пари: {', '.join(TRADING_PAIRS)}")
            logger.info(f"⏰ Інтервал аналізу: {ANALYSIS_INTERVAL} секунд")
            
            self.is_running = True
            
            # Відправляємо стартове повідомлення
            startup_message = f"""
🤖 **Crypto Trading Bot з ChatGPT запущено!**

📊 **Налаштування:**
• Торгові пари: {len(TRADING_PAIRS)}
• Інтервал аналізу: {ANALYSIS_INTERVAL} сек
• Поріг сигналу: 70%

🔧 **Модулі:**
• ✅ Binance API
• ✅ Технічний аналіз
• ✅ Збір новин
• ✅ ChatGPT аналіз (з відправкою в Telegram)
• ✅ Telegram бот

⏰ **Час запуску:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

🚀 Бот готовий до роботи!

💡 **Особливості:**
• ChatGPT аналіз надсилається напряму в Telegram
• Детальні рекомендації з обґрунтуванням
• Автоматичні торгові сигнали
• Fallback аналіз при недоступності ChatGPT
            """
            try:
                await self.telegram_bot.send_error_notification(startup_message)
            except:
                logger.info("✅ Стартове повідомлення не відправлено (проблема з Telegram)")
            
            # Запускаємо основний цикл аналізу з можливістю зупинки
            await self._run_with_shutdown()
            
        except Exception as e:
            logger.error(f"❌ Критична помилка: {e}")
        finally:
            await self.cleanup()
    
    async def _run_with_shutdown(self):
        """Запустити аналіз з можливістю graceful shutdown"""
        # Створюємо завдання для аналізу та Telegram бота
        analysis_task = asyncio.create_task(self.signal_processor.start_analysis_loop())
        telegram_task = asyncio.create_task(self.telegram_bot.start_polling())
        
        # Чекаємо на сигнал зупинки або завершення завдань
        try:
            # Створюємо завдання для очікування сигналу зупинки
            shutdown_task = asyncio.create_task(self.shutdown_event.wait())
            
            # Очікуємо на будь-яке з завдань
            done, pending = await asyncio.wait(
                [analysis_task, telegram_task, shutdown_task],
                return_when=asyncio.FIRST_COMPLETED
            )
            
            # Якщо отримали сигнал зупинки
            if shutdown_task in done:
                logger.info("🛑 Отримано сигнал зупинки...")
            else:
                logger.info("🛑 Одна з задач завершилася...")
            
        except asyncio.CancelledError:
            logger.info("🛑 Аналіз скасовано...")
        
        # Скасовуємо всі завдання
        for task in [analysis_task, telegram_task]:
            if not task.done():
                task.cancel()
                try:
                    await task
                except asyncio.CancelledError:
                    pass
    
    def stop(self):
        """Зупинити бота"""
        logger.info("🛑 Зупинка бота...")
        self.is_running = False
        self.signal_processor.stop_analysis()
        self.shutdown_event.set()
    
    async def cleanup(self):
        """Очистити ресурси"""
        try:
            logger.info("🧹 Очищення ресурсів...")
            self.stop()
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
    
    def get_status(self):
        """Отримати статус бота"""
        return {
            'is_running': self.is_running,
            'signal_processor': self.signal_processor.get_status(),
            'uptime': datetime.now().isoformat()
        }

async def main():
    """Головна функція"""
    bot = CryptoBotTelegramChatGPT()
    
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
    from config import BINANCE_API_KEY, BINANCE_API_SECRET, OPENAI_API_KEY, TELEGRAM_BOT_TOKEN
    
    required_vars = {
        'BINANCE_API_KEY': BINANCE_API_KEY,
        'BINANCE_API_SECRET': BINANCE_API_SECRET,
        'OPENAI_API_KEY': OPENAI_API_KEY,
        'TELEGRAM_BOT_TOKEN': TELEGRAM_BOT_TOKEN
    }
    
    missing_vars = [var for var, value in required_vars.items() if not value]
    
    if missing_vars:
        logger.error(f"❌ Відсутні змінні середовища: {', '.join(missing_vars)}")
        logger.error("📝 Створіть файл .env на основі env.example")
        sys.exit(1)
    
    # Запускаємо бота
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("⏹️ Програма зупинена користувачем")
    except Exception as e:
        logger.error(f"❌ Критична помилка: {e}")
        sys.exit(1)
