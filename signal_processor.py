import asyncio
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import json

from binance_client import BinanceClient
from technical_analysis import TechnicalAnalyzer
from news_aggregator import NewsAggregator
from chatgpt_analyzer import ChatGPTAnalyzer
from telegram_bot import TelegramBot
from config import TRADING_PAIRS, ANALYSIS_INTERVAL, SIGNAL_THRESHOLD

class SignalProcessor:
    def __init__(self):
        self.binance_client = BinanceClient()
        self.technical_analyzer = TechnicalAnalyzer()
        self.news_aggregator = NewsAggregator()
        self.chatgpt_analyzer = ChatGPTAnalyzer()
        self.telegram_bot = TelegramBot()
        
        self.trading_pairs = TRADING_PAIRS
        self.analysis_interval = ANALYSIS_INTERVAL
        self.signal_threshold = SIGNAL_THRESHOLD
        
        self.last_analysis_time = {}
        self.sent_signals = set()  # Для уникнення дублювання сигналів
        self.is_running = False
    
    async def start_analysis_loop(self):
        """Запустити основний цикл аналізу"""
        self.is_running = True
        print("🚀 Запуск аналізу торгових сигналів...")
        
        while self.is_running:
            try:
                await self._run_analysis_cycle()
                print(f"⏰ Наступний аналіз через {self.analysis_interval} секунд...")
                await asyncio.sleep(self.analysis_interval)
                
            except Exception as e:
                print(f"❌ Помилка в циклі аналізу: {e}")
                await self.telegram_bot.send_error_notification(f"Помилка в циклі аналізу: {str(e)}")
                await asyncio.sleep(60)  # Затримка при помилці
    
    async def _run_analysis_cycle(self):
        """Виконати один цикл аналізу"""
        print(f"📊 Початок аналізу {len(self.trading_pairs)} торгових пар...")
        
        # Отримуємо дані з Binance
        all_data = self.binance_client.get_all_pairs_data()
        if not all_data:
            print("❌ Не вдалося отримати дані з Binance")
            return
        
        # Отримуємо новини та сентимент
        print("📰 Отримання новин...")
        news_summary = self.news_aggregator.get_news_summary()
        market_sentiment = self.news_aggregator.get_sentiment_analysis()
        
        # Аналізуємо кожну пару
        all_analyses = []
        strong_signals = []
        
        for symbol, data in all_data.items():
            try:
                print(f"🔍 Аналіз {symbol}...")
                
                # Технічний аналіз
                technical_analysis = self.technical_analyzer.get_analysis_summary(
                    symbol, data['klines'], data['ticker_24h']
                )
                
                if not technical_analysis:
                    continue
                
                # ChatGPT аналіз
                chatgpt_analysis = self.chatgpt_analyzer.analyze_trading_opportunity(
                    symbol, technical_analysis, news_summary, market_sentiment
                )
                
                all_analyses.append(chatgpt_analysis)
                
                # Перевіряємо чи є сильний сигнал
                if self._is_strong_signal(chatgpt_analysis):
                    strong_signals.append(chatgpt_analysis)
                
                # Невелика затримка між аналізами
                await asyncio.sleep(1)
                
            except Exception as e:
                print(f"❌ Помилка аналізу {symbol}: {e}")
                continue
        
        # Відправляємо сильні сигнали
        if strong_signals:
            print(f"📈 Знайдено {len(strong_signals)} сильних сигналів!")
            await self._send_strong_signals(strong_signals, news_summary, market_sentiment)
        
        # Відправляємо огляд ринку кожні 30 хвилин
        if self._should_send_market_overview():
            await self._send_market_overview(all_analyses)
        
        print(f"✅ Аналіз завершено. Проаналізовано {len(all_analyses)} пар, знайдено {len(strong_signals)} сигналів")
    
    def _is_strong_signal(self, analysis: Dict) -> bool:
        """Перевірити чи є це сильний сигнал"""
        
        recommendation = analysis.get('recommendation', 'HOLD')
        confidence = analysis.get('confidence', 0)
        signal_strength = analysis.get('signal_strength', 0)
        
        # Перевіряємо чи не відправляли цей сигнал нещодавно
        signal_key = f"{analysis['symbol']}_{recommendation}_{datetime.now().strftime('%Y%m%d%H')}"
        if signal_key in self.sent_signals:
            return False
        
        # Критерії сильного сигналу
        if recommendation in ['BUY', 'SELL']:
            if confidence >= self.signal_threshold:
                if signal_strength >= 2:  # Мінімум 2 технічних сигнали
                    self.sent_signals.add(signal_key)
                    return True
        
        return False
    
    async def _send_strong_signals(self, signals: List[Dict], news_summary: str, market_sentiment: Dict):
        """Відправити сильні сигнали"""
        
        for signal in signals:
            try:
                await self.telegram_bot.send_trading_signal(signal, news_summary, market_sentiment)
                
                # Затримка між відправками
                await asyncio.sleep(2)
                
            except Exception as e:
                print(f"❌ Помилка відправки сигналу для {signal['symbol']}: {e}")
    
    async def _send_market_overview(self, all_analyses: List[Dict]):
        """Відправити огляд ринку"""
        
        try:
            # Підраховуємо статистику
            statistics = {
                'total_pairs': len(all_analyses),
                'buy_signals': len([a for a in all_analyses if a.get('recommendation') == 'BUY']),
                'sell_signals': len([a for a in all_analyses if a.get('recommendation') == 'SELL']),
                'hold_signals': len([a for a in all_analyses if a.get('recommendation') == 'HOLD'])
            }
            
            # Отримуємо огляд від ChatGPT
            overview_text = self.chatgpt_analyzer.get_market_overview(all_analyses)
            
            # Відправляємо огляд
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
    
    async def send_manual_analysis(self, symbol: str):
        """Відправити ручний аналіз для конкретного символу"""
        
        try:
            print(f"🔍 Ручний аналіз для {symbol}...")
            
            # Отримуємо дані
            data = self.binance_client.get_all_pairs_data()
            if symbol not in data:
                print(f"❌ Символ {symbol} не знайдено")
                return
            
            # Технічний аналіз
            technical_analysis = self.technical_analyzer.get_analysis_summary(
                symbol, data[symbol]['klines'], data[symbol]['ticker_24h']
            )
            
            if not technical_analysis:
                print(f"❌ Не вдалося проаналізувати {symbol}")
                return
            
            # Отримуємо новини
            news_summary = self.news_aggregator.get_news_summary()
            market_sentiment = self.news_aggregator.get_sentiment_analysis()
            
            # ChatGPT аналіз
            chatgpt_analysis = self.chatgpt_analyzer.analyze_trading_opportunity(
                symbol, technical_analysis, news_summary, market_sentiment
            )
            
            # Відправляємо сигнал
            await self.telegram_bot.send_trading_signal(chatgpt_analysis, news_summary, market_sentiment)
            
            print(f"✅ Ручний аналіз для {symbol} відправлено")
            
        except Exception as e:
            print(f"❌ Помилка ручного аналізу для {symbol}: {e}")
    
    async def send_news_update(self):
        """Відправити оновлення новин"""
        
        try:
            news_summary = self.news_aggregator.get_news_summary()
            await self.telegram_bot.send_news_update(news_summary)
            
        except Exception as e:
            print(f"❌ Помилка відправки новин: {e}")
    
    def stop_analysis(self):
        """Зупинити аналіз"""
        self.is_running = False
        print("🛑 Аналіз зупинено")
    
    def get_status(self) -> Dict:
        """Отримати статус процесора"""
        
        return {
            'is_running': self.is_running,
            'trading_pairs': len(self.trading_pairs),
            'analysis_interval': self.analysis_interval,
            'signal_threshold': self.signal_threshold,
            'last_analysis_time': self.last_analysis_time,
            'sent_signals_count': len(self.sent_signals)
        }
