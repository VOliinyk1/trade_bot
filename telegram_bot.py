import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHANNEL_ID
from typing import Dict, List
import json
from datetime import datetime

class TelegramBot:
    def __init__(self):
        self.bot = Bot(token=TELEGRAM_BOT_TOKEN)
        self.dp = Dispatcher()
        self.channel_id = TELEGRAM_CHANNEL_ID
        self.setup_handlers()
    
    def setup_handlers(self):
        """Налаштувати обробники команд"""
        
        @self.dp.message(Command("start"))
        async def start_handler(message: types.Message):
            welcome_text = """
🤖 **Crypto Trading Bot**

Привіт! Я автоматичний бот для аналізу криптовалют.

📊 **Мої можливості:**
• Технічний аналіз багатьох торгових пар
• Аналіз новин та сентименту ринку
• Рекомендації від ChatGPT
• Автоматичні торгові сигнали

🔧 **Команди:**
/status - Статус бота
/analysis - Поточний аналіз ринку
/news - Останні новини
/help - Допомога

📈 Сигнали надсилаються автоматично в канал!
            """
            await message.answer(welcome_text, parse_mode="Markdown")
        
        @self.dp.message(Command("help"))
        async def help_handler(message: types.Message):
            help_text = """
📚 **Допомога по командам:**

/start - Почати роботу з ботом
/status - Перевірити статус бота
/analysis - Отримати поточний аналіз ринку
/news - Показати останні новини
/help - Показати цю довідку

🔔 **Автоматичні сигнали:**
Бот автоматично аналізує ринок та надсилає сигнали в канал коли знаходить торгові можливості.

📊 **Що аналізує бот:**
• Технічні індикатори (RSI, MACD, EMA, Bollinger Bands)
• Новини та сентимент ринку
• Рекомендації від ChatGPT
• Ризик-менеджмент
            """
            await message.answer(help_text, parse_mode="Markdown")
        
        @self.dp.message(Command("status"))
        async def status_handler(message: types.Message):
            status_text = """
🟢 **Статус бота: АКТИВНИЙ**

📊 **Остання активність:**
• Аналіз ринку: ✅
• Збір новин: ✅
• ChatGPT аналіз: ✅
• Відправка сигналів: ✅

⏰ **Наступний аналіз:** Через 5 хвилин
            """
            await message.answer(status_text, parse_mode="Markdown")
    
    async def send_trading_signal(self, analysis: Dict, news_summary: str, market_sentiment: Dict):
        """Відправити торговий сигнал в канал"""
        
        try:
            symbol = analysis['symbol']
            recommendation = analysis['recommendation']
            confidence = analysis['confidence']
            
            # Формуємо повідомлення
            signal_text = self._format_trading_signal(analysis, news_summary, market_sentiment)
            
            # Створюємо кнопки
            keyboard = self._create_signal_keyboard(analysis)
            
            # Відправляємо повідомлення
            await self.bot.send_message(
                chat_id=self.channel_id,
                text=signal_text,
                parse_mode="Markdown",
                reply_markup=keyboard
            )
            
            print(f"✅ Сигнал відправлено для {symbol}")
            
        except Exception as e:
            print(f"❌ Помилка відправки сигналу: {e}")
    
    def _format_trading_signal(self, analysis: Dict, news_summary: str, market_sentiment: Dict) -> str:
        """Форматувати торговий сигнал"""
        
        symbol = analysis['symbol']
        recommendation = analysis['recommendation']
        confidence = analysis['confidence']
        risk_level = analysis['risk_level']
        position_size = analysis['position_size']
        entry_price = analysis['entry_price']
        stop_loss = analysis['stop_loss']
        take_profit = analysis['take_profit']
        reasoning = analysis['reasoning']
        
        # Емодзі для рекомендацій
        emoji_map = {
            'BUY': '🟢',
            'SELL': '🔴',
            'HOLD': '🟡'
        }
        
        # Емодзі для рівня ризику
        risk_emoji_map = {
            'LOW': '🟢',
            'MEDIUM': '🟡',
            'HIGH': '🔴'
        }
        
        signal_text = f"""
{emoji_map.get(recommendation, '🟡')} **ТОРГОВИЙ СИГНАЛ: {symbol}**

📊 **РЕКОМЕНДАЦІЯ:** {recommendation}
🎯 **ВПЕВНЕНІСТЬ:** {confidence:.1%}
⚠️ **РИЗИК:** {risk_level} {risk_emoji_map.get(risk_level, '🟡')}
💰 **РОЗМІР ПОЗИЦІЇ:** {position_size:.1%}

💵 **ЦІНИ:**
• Вхід: ${entry_price:.4f}
• Stop Loss: ${stop_loss:.4f}
• Take Profit: ${take_profit:.4f}

📈 **ПОТЕНЦІАЛ:**
• Ризик: {abs(entry_price - stop_loss) / entry_price * 100:.1f}%
• Прибуток: {abs(take_profit - entry_price) / entry_price * 100:.1f}%

🧠 **АНАЛІЗ ChatGPT:**
{reasoning[:300]}{'...' if len(reasoning) > 300 else ''}

📰 **СЕНТИМЕНТ РИНКУ:** {market_sentiment.get('sentiment', 'NEUTRAL')}
📊 **ОЦІНКА:** {market_sentiment.get('score', 0):.2f}

⏰ **ЧАС:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

⚠️ **ВАЖЛИВО:** Це не фінансова порада. Торгуйте на свій ризик!
        """
        
        return signal_text.strip()
    
    def _create_signal_keyboard(self, analysis: Dict) -> InlineKeyboardMarkup:
        """Створити клавіатуру для сигналу"""
        
        symbol = analysis['symbol']
        
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="📊 Детальний аналіз",
                    callback_data=f"analysis_{symbol}"
                ),
                InlineKeyboardButton(
                    text="📰 Новини",
                    callback_data="news"
                )
            ],
            [
                InlineKeyboardButton(
                    text="📈 Графік",
                    url=f"https://www.binance.com/en/trade/{symbol}"
                ),
                InlineKeyboardButton(
                    text="🔔 Налаштування",
                    callback_data="settings"
                )
            ]
        ])
        
        return keyboard
    
    async def send_market_overview(self, overview_text: str, statistics: Dict):
        """Відправити огляд ринку"""
        
        try:
            overview_message = f"""
📊 **ОГЛЯД РИНКУ**

{overview_text}

📈 **СТАТИСТИКА:**
• Проаналізовано пар: {statistics.get('total_pairs', 0)}
• BUY сигнали: {statistics.get('buy_signals', 0)}
• SELL сигнали: {statistics.get('sell_signals', 0)}
• HOLD сигнали: {statistics.get('hold_signals', 0)}

⏰ **ЧАС:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
            """
            
            await self.bot.send_message(
                chat_id=self.channel_id,
                text=overview_message,
                parse_mode="Markdown"
            )
            
            print("✅ Огляд ринку відправлено")
            
        except Exception as e:
            print(f"❌ Помилка відправки огляду ринку: {e}")
    
    async def send_news_update(self, news_text: str):
        """Відправити оновлення новин"""
        
        try:
            await self.bot.send_message(
                chat_id=self.channel_id,
                text=news_text,
                parse_mode="Markdown"
            )
            
            print("✅ Оновлення новин відправлено")
            
        except Exception as e:
            print(f"❌ Помилка відправки новин: {e}")
    
    async def send_error_notification(self, error_message: str):
        """Відправити сповіщення про помилку"""
        
        try:
            error_text = f"""
⚠️ **СПОВІЩЕННЯ ПРО ПОМИЛКУ**

{error_message}

⏰ **ЧАС:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
            """
            
            await self.bot.send_message(
                chat_id=self.channel_id,
                text=error_text,
                parse_mode="Markdown"
            )
            
            print("✅ Сповіщення про помилку відправлено")
            
        except Exception as e:
            print(f"❌ Помилка відправки сповіщення: {e}")
    
    async def start_polling(self):
        """Запустити бота"""
        try:
            await self.dp.start_polling(self.bot)
        except Exception as e:
            print(f"❌ Помилка запуску бота: {e}")
    
    async def stop_bot(self):
        """Зупинити бота"""
        await self.bot.session.close()
