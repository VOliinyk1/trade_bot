import asyncio
import signal
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import logging

from binance_client import BinanceClient
from technical_analysis import TechnicalAnalyzer
from news_aggregator import NewsAggregator
from chatgpt_telegram_analyzer import ChatGPTTelegramAnalyzer
from telegram_bot import TelegramBot
from config import TRADING_PAIRS, ANALYSIS_INTERVAL, SIGNAL_THRESHOLD

logger = logging.getLogger(__name__)

class SignalProcessorTelegram:
    def __init__(self):
        self.binance_client = BinanceClient()
        self.technical_analyzer = TechnicalAnalyzer()
        self.news_aggregator = NewsAggregator()
        self.chatgpt_analyzer = ChatGPTTelegramAnalyzer()
        self.telegram_bot = TelegramBot()
        
        self.trading_pairs = TRADING_PAIRS
        self.analysis_interval = ANALYSIS_INTERVAL
        self.signal_threshold = SIGNAL_THRESHOLD
        
        # Статистика аналізу
        self.analysis_stats = {
            'total_analyses': 0,
            'successful_analyses': 0,
            'failed_analyses': 0,
            'strong_signals_found': 0,
            'last_analysis_time': None
        }
        
        # Час останніх аналізів
        self.last_analysis_time = {}
        
        # Флаг для зупинки
        self.is_running = False
        
        # Налаштування обробки сигналів для graceful shutdown
        self.shutdown_event = asyncio.Event()
        self._setup_signal_handlers()
    
    def _setup_signal_handlers(self):
        """Налаштувати обробники сигналів"""
        def signal_handler(signum, frame):
            logger.info(f"Отримано сигнал {signum}. Зупинка аналізу...")
            self.shutdown_event.set()
        
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)
    
    async def start_analysis_loop(self):
        """Запустити основний цикл аналізу"""
        
        logger.info("🚀 Запуск аналізу торгових сигналів з Telegram ChatGPT...")
        self.is_running = True
        
        while self.is_running and not self.shutdown_event.is_set():
            try:
                await self._run_analysis_cycle()
                print(f"⏰ Наступний аналіз через {self.analysis_interval} секунд...")
                
                # Використовуємо asyncio.sleep з можливістю переривання
                try:
                    await asyncio.sleep(self.analysis_interval)
                except asyncio.CancelledError:
                    print("🛑 Аналіз перервано...")
                    break
                    
            except asyncio.CancelledError:
                print("🛑 Аналіз скасовано...")
                break
            except Exception as e:
                print(f"❌ Помилка в циклі аналізу: {e}")
                try:
                    await self.telegram_bot.send_error_notification(f"Помилка в циклі аналізу: {str(e)}")
                except Exception as telegram_error:
                    print(f"❌ Помилка Telegram: {telegram_error}")
                    pass  # Ігноруємо помилки відправки повідомлень
                
                # Затримка при помилці з можливістю переривання
                try:
                    await asyncio.sleep(60)
                except asyncio.CancelledError:
                    break
        
        logger.info("🛑 Аналіз зупинено")
    
    async def _run_analysis_cycle(self):
        """Виконати один цикл аналізу"""
        
        print(f"📊 Початок аналізу {len(self.trading_pairs)} торгових пар...")
        
        # Оновлюємо статистику
        self.analysis_stats['total_analyses'] += 1
        self.analysis_stats['last_analysis_time'] = datetime.now()
        
        # Отримуємо дані для всіх пар
        all_data = await self._fetch_all_data()
        
        # Отримуємо новини та сентимент
        print("📰 Отримання новин...")
        news_data = self.news_aggregator.get_all_news()
        news_summary = self.news_aggregator.get_news_summary()
        market_sentiment = self.news_aggregator.get_sentiment_analysis()
        
        # Аналізуємо всі пари
        all_technical_analyses = []
        potential_signals = []
        
        for symbol, data in all_data.items():
            try:
                print(f"🔍 Технічний аналіз {symbol}...")
                technical_analysis = self.technical_analyzer.get_analysis_summary(
                    symbol, data['klines'], data['ticker_24h']
                )
                
                # Додаємо символ до аналізу
                analysis_result = {
                    'symbol': symbol,
                    'technical': technical_analysis
                }
                all_technical_analyses.append(analysis_result)
                
                # Перевіряємо чи є потенційний BUY сигнал
                if self._is_potential_signal(technical_analysis):
                    potential_signals.append({'symbol': symbol, 'technical': technical_analysis})
                    print(f"🎯 {symbol}: знайдено потенційний BUY сигнал для ChatGPT аналізу")
                
            except Exception as e:
                print(f"❌ Помилка обробки {symbol}: {e}")
                self.analysis_stats['failed_analyses'] += 1
                continue
        
        # ChatGPT аналіз для потенційних BUY сигналів з відправкою в Telegram
        strong_signals = []
        if potential_signals:
            print(f"🤖 ChatGPT аналіз для {len(potential_signals)} потенційних BUY сигналів...")
            
            for signal_data in potential_signals:
                symbol = signal_data['symbol']
                technical_analysis = signal_data['technical']
                
                try:
                    print(f"🧠 ChatGPT аналіз {symbol} з відправкою в Telegram...")
                    
                    # ChatGPT аналіз з автоматичною відправкою в Telegram
                    chatgpt_analysis = await self.chatgpt_analyzer.analyze_trading_opportunity(
                        symbol=symbol,
                        technical_data=technical_analysis,
                        news_data=news_summary,
                        market_sentiment=market_sentiment,
                        telegram_bot=self.telegram_bot
                    )
                    
                    # Перевіряємо чи це сильний сигнал
                    if chatgpt_analysis['confidence'] >= self.signal_threshold:
                        strong_signals.append(chatgpt_analysis)
                        print(f"🚨 СИЛЬНИЙ СИГНАЛ: {symbol} - {chatgpt_analysis['recommendation']} ({chatgpt_analysis['confidence']:.1%})")
                        self.analysis_stats['strong_signals_found'] += 1
                    
                except Exception as e:
                    print(f"❌ Помилка ChatGPT аналізу для {symbol}: {e}")
                    
                    # Відправляємо повідомлення про помилку
                    try:
                        await self.telegram_bot.send_error_notification(f"Помилка ChatGPT аналізу для {symbol}: {str(e)}")
                    except:
                        pass
        else:
            print("ℹ️ Потенційних BUY сигналів для ChatGPT аналізу не знайдено")
        
        # Оновлюємо статистику
        self.analysis_stats['successful_analyses'] += len(all_technical_analyses)
        
        # Відправляємо огляд ринку кожні 30 хвилин
        if self._should_send_market_overview():
            await self._send_market_overview(all_technical_analyses)
        
        print(f"✅ Аналіз завершено. Проаналізовано {len(all_technical_analyses)} пар, ChatGPT BUY аналіз: {len(potential_signals)}, знайдено {len(strong_signals)} сильних BUY сигналів")
        
        # Відправляємо звіт про аналіз
        await self._send_analysis_report(all_technical_analyses, potential_signals, strong_signals)
    
    def _is_potential_signal(self, technical_analysis: Dict) -> bool:
        """Перевірити чи є це потенційний BUY сигнал для ChatGPT аналізу"""
        
        recommendation = technical_analysis.get('recommendation', 'HOLD')
        signal_strength = technical_analysis.get('signal_strength', 0)
        trend = technical_analysis.get('trend', 'NEUTRAL')
        
        # Тільки BUY сигнали для ChatGPT аналізу
        if recommendation == 'BUY':
            if signal_strength >= 1:
                return True
        
        # Також перевіряємо сильні восходячі тренди
        if trend == 'STRONG_UP' and signal_strength >= 2:
            return True
        
        return False
    
    async def _fetch_all_data(self) -> Dict:
        """Отримати дані для всіх торгових пар"""
        
        all_data = {}
        
        for symbol in self.trading_pairs:
            try:
                # Отримуємо дані з Binance
                klines = self.binance_client.get_klines(symbol)
                current_price = self.binance_client.get_current_price(symbol)
                ticker_24h = self.binance_client.get_24h_ticker(symbol)
                
                data = {
                    'klines': klines,
                    'current_price': current_price,
                    'ticker_24h': ticker_24h,
                    'symbol': symbol
                }
                all_data[symbol] = data
                
            except Exception as e:
                print(f"❌ Помилка отримання даних для {symbol}: {e}")
                continue
        
        return all_data
    
    async def _send_market_overview(self, all_analyses: List[Dict]):
        """Відправити огляд ринку"""
        
        try:
            # Підраховуємо статистику
            buy_count = sum(1 for analysis in all_analyses 
                          if analysis.get('technical', {}).get('recommendation') == 'BUY')
            sell_count = sum(1 for analysis in all_analyses 
                           if analysis.get('technical', {}).get('recommendation') == 'SELL')
            hold_count = len(all_analyses) - buy_count - sell_count
            
            # Формуємо текст огляду
            overview_text = f"Загальний огляд ринку: {buy_count} BUY, {sell_count} SELL, {hold_count} HOLD сигналів з {len(all_analyses)} пар."
            
            statistics = {
                'total_pairs': len(all_analyses),
                'buy_signals': buy_count,
                'sell_signals': sell_count,
                'hold_signals': hold_count
            }
            
            await self.telegram_bot.send_market_overview(overview_text, statistics)
            
            # Оновлюємо час останнього огляду
            self.last_analysis_time['market_overview'] = datetime.now()
            
        except Exception as e:
            print(f"❌ Помилка відправки огляду ринку: {e}")
    
    def _should_send_market_overview(self) -> bool:
        """Перевірити чи потрібно відправити огляд ринку"""
        
        last_overview = self.last_analysis_time.get('market_overview')
        if not last_overview:
            return True
        
        # Відправляємо огляд кожні 30 хвилин
        return datetime.now() - last_overview > timedelta(minutes=30)
    
    async def _send_analysis_report(self, all_technical_analyses: List[Dict], potential_signals: List[Dict], strong_signals: List[Dict]):
        """Відправити звіт про аналіз"""
        
        try:
            # Підраховуємо статистику (фокус на BUY сигналах)
            buy_signals = sum(1 for analysis in all_technical_analyses if analysis.get('technical', {}).get('recommendation', 'HOLD') == 'BUY')
            sell_signals = sum(1 for analysis in all_technical_analyses if analysis.get('technical', {}).get('recommendation', 'HOLD') == 'SELL')
            hold_signals = sum(1 for analysis in all_technical_analyses if analysis.get('technical', {}).get('recommendation', 'HOLD') == 'HOLD')
            
            # ChatGPT аналіз тільки для BUY сигналів
            chatgpt_buy_signals = len([signal for signal in potential_signals if signal.get('technical', {}).get('recommendation') == 'BUY'])
            
            # Формуємо статистику по парах
            pairs_stats = {}
            for analysis in all_technical_analyses:
                symbol = analysis.get('symbol', 'UNKNOWN')
                technical = analysis.get('technical', {})
                pairs_stats[symbol] = {
                    'recommendation': technical.get('recommendation', 'HOLD'),
                    'confidence': technical.get('confidence', 0),
                    'signal_strength': technical.get('signal_strength', 0)
                }
            
            # Формуємо дані для звіту
            report_data = {
                'total_pairs': len(self.trading_pairs),
                'analyzed_pairs': len(all_technical_analyses),
                'chatgpt_analyzed': len(potential_signals),
                'strong_signals': len(strong_signals),
                'buy_signals': buy_signals,
                'sell_signals': sell_signals,
                'hold_signals': hold_signals,
                'pairs_stats': pairs_stats
            }
            
            # Відправляємо звіт (спрощена версія)
            try:
                report_text = f"""
📊 **ЗВІТ ПРО АНАЛІЗ РИНКУ**

📈 **ЗАГАЛЬНА СТАТИСТИКА:**
• Всього пар: {report_data['total_pairs']}
• Проаналізовано: {report_data['analyzed_pairs']}
• ChatGPT аналіз (BUY): {chatgpt_buy_signals}
• Сильні BUY сигнали: {report_data['strong_signals']}

🎯 **СИГНАЛИ:**
• 🟢 BUY: {report_data['buy_signals']} (ChatGPT: {chatgpt_buy_signals})
• 🔴 SELL: {report_data['sell_signals']}
• 🟡 HOLD: {report_data['hold_signals']}

💡 **ФОКУС:** ChatGPT аналіз тільки для BUY сигналів з покращеними розрахунками Stop Loss та Take Profit

⏰ **ЧАС:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
                """
                await self.telegram_bot.bot.send_message(
                    chat_id=self.telegram_bot.channel_id,
                    text=report_text,
                    parse_mode="Markdown"
                )
                print("✅ Звіт про аналіз відправлено")
            except Exception as e:
                print(f"❌ Помилка відправки звіту: {e}")
            
        except Exception as e:
            print(f"❌ Помилка відправки звіту про аналіз: {e}")
    
    async def send_manual_analysis(self, symbol: str):
        """Відправити ручний аналіз для конкретного символу"""
        
        try:
            print(f"🔍 Ручний аналіз для {symbol}")
            
            # Отримуємо дані
            klines = self.binance_client.get_klines(symbol)
            current_price = self.binance_client.get_current_price(symbol)
            ticker_24h = self.binance_client.get_24h_ticker(symbol)
            
            data = {
                'klines': klines,
                'current_price': current_price,
                'ticker_24h': ticker_24h,
                'symbol': symbol
            }
            
            # Технічний аналіз
            technical_analysis = self.technical_analyzer.get_analysis_summary(
                symbol, data['klines'], data['ticker_24h']
            )
            
            # ChatGPT аналіз з відправкою в Telegram
            news_data = self.news_aggregator.get_all_news()
            news_summary = self.news_aggregator.get_news_summary()
            market_sentiment = self.news_aggregator.get_sentiment_analysis()
            
            chatgpt_analysis = await self.chatgpt_analyzer.analyze_trading_opportunity(
                symbol=symbol,
                technical_data=technical_analysis,
                news_data=news_summary,
                market_sentiment=market_sentiment,
                telegram_bot=self.telegram_bot
            )
            
            print(f"✅ Ручний аналіз для {symbol} відправлено")
            
        except Exception as e:
            print(f"❌ Помилка ручного аналізу: {e}")
    
    def stop_analysis(self):
        """Зупинити аналіз"""
        self.is_running = False
        self.shutdown_event.set()
    
    def get_status(self) -> Dict:
        """Отримати статус процесора"""
        return {
            'is_running': self.is_running,
            'analysis_stats': self.analysis_stats,
            'trading_pairs': len(self.trading_pairs),
            'signal_threshold': self.signal_threshold
        }
