import asyncio
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import json

from binance_client import BinanceClient
from technical_analysis import TechnicalAnalyzer
from news_aggregator import NewsAggregator
from telegram_bot import TelegramBot
from config import TRADING_PAIRS, ANALYSIS_INTERVAL, SIGNAL_THRESHOLD

class SignalProcessorNoChatGPT:
    def __init__(self):
        self.binance_client = BinanceClient()
        self.technical_analyzer = TechnicalAnalyzer()
        self.news_aggregator = NewsAggregator()
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
        print("🚀 Запуск аналізу торгових сигналів (без ChatGPT)...")
        
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
                
                # Створюємо аналіз без ChatGPT
                analysis = self._create_analysis_without_chatgpt(
                    symbol, technical_analysis, market_sentiment
                )
                
                all_analyses.append(analysis)
                
                # Перевіряємо чи є сильний сигнал
                if self._is_strong_signal(analysis):
                    strong_signals.append(analysis)
                
                # Невелика затримка між аналізами
                await asyncio.sleep(0.5)
                
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
    
    def _create_analysis_without_chatgpt(self, symbol: str, technical_data: Dict, market_sentiment: Dict) -> Dict:
        """Створити аналіз без ChatGPT"""
        
        recommendation = technical_data.get('recommendation', 'HOLD')
        current_price = technical_data.get('current_price', 0)
        signal_strength = technical_data.get('signal_strength', 0)
        trend = technical_data.get('trend', 'NEUTRAL')
        
        # Аналізуємо сентимент ринку
        sentiment_score = market_sentiment.get('score', 0)
        sentiment = market_sentiment.get('sentiment', 'NEUTRAL')
        
        # Визначаємо рівень ризику
        if signal_strength >= 3 and sentiment == 'POSITIVE':
            risk_level = 'LOW'
            confidence = 0.8
            position_size = 0.15
        elif signal_strength >= 2:
            risk_level = 'MEDIUM'
            confidence = 0.6
            position_size = 0.1
        else:
            risk_level = 'HIGH'
            confidence = 0.4
            position_size = 0.05
        
        # Корегуємо рекомендацію на основі сентименту
        if sentiment == 'NEGATIVE' and recommendation == 'BUY':
            recommendation = 'HOLD'
            confidence *= 0.7
        elif sentiment == 'POSITIVE' and recommendation == 'SELL':
            recommendation = 'HOLD'
            confidence *= 0.7
        
        # Розраховуємо ціни
        if recommendation == 'BUY':
            stop_loss = current_price * 0.95  # -5%
            take_profit = current_price * 1.10  # +10%
        elif recommendation == 'SELL':
            stop_loss = current_price * 1.05  # +5%
            take_profit = current_price * 0.90  # -10%
        else:
            stop_loss = current_price
            take_profit = current_price
        
        # Формуємо обґрунтування
        reasoning_parts = []
        reasoning_parts.append(f"Технічний аналіз: {recommendation}")
        reasoning_parts.append(f"Тренд: {trend}")
        reasoning_parts.append(f"Сила сигналу: {signal_strength}")
        reasoning_parts.append(f"Сентимент ринку: {sentiment} ({sentiment_score:.2f})")
        
        if signal_strength >= 3:
            reasoning_parts.append("Сильні технічні сигнали")
        if sentiment == 'POSITIVE':
            reasoning_parts.append("Позитивний сентимент ринку")
        elif sentiment == 'NEGATIVE':
            reasoning_parts.append("Негативний сентимент ринку")
        
        reasoning = ". ".join(reasoning_parts) + "."
        
        analysis = {
            'symbol': symbol,
            'recommendation': recommendation,
            'risk_level': risk_level,
            'position_size': position_size,
            'entry_price': current_price,
            'stop_loss': stop_loss,
            'take_profit': take_profit,
            'reasoning': reasoning,
            'confidence': confidence
        }
        
        return analysis
    
    def _is_strong_signal(self, analysis: Dict) -> bool:
        """Перевірити чи є це сильний сигнал"""
        
        recommendation = analysis.get('recommendation', 'HOLD')
        confidence = analysis.get('confidence', 0)
        
        # Перевіряємо чи не відправляли цей сигнал нещодавно
        signal_key = f"{analysis['symbol']}_{recommendation}_{datetime.now().strftime('%Y%m%d%H')}"
        if signal_key in self.sent_signals:
            return False
        
        # Критерії сильного сигналу
        if recommendation in ['BUY', 'SELL']:
            if confidence >= self.signal_threshold:
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
            
            # Створюємо простий огляд без ChatGPT
            overview_text = self._create_simple_market_overview(all_analyses, statistics)
            
            # Відправляємо огляд
            await self.telegram_bot.send_market_overview(overview_text, statistics)
            
            # Оновлюємо час останнього огляду
            self.last_analysis_time['market_overview'] = datetime.now()
            
        except Exception as e:
            print(f"❌ Помилка відправки огляду ринку: {e}")
    
    def _create_simple_market_overview(self, all_analyses: List[Dict], statistics: Dict) -> str:
        """Створити простий огляд ринку без ChatGPT"""
        
        total_pairs = statistics['total_pairs']
        buy_signals = statistics['buy_signals']
        sell_signals = statistics['sell_signals']
        hold_signals = statistics['hold_signals']
        
        # Знаходимо найкращі можливості
        best_opportunities = sorted(
            [a for a in all_analyses if a.get('recommendation') in ['BUY', 'SELL']],
            key=lambda x: x.get('confidence', 0),
            reverse=True
        )[:3]
        
        overview = f"""
📊 **Огляд крипто ринку**

🔍 **Проаналізовано:** {total_pairs} торгових пар
📈 **BUY сигнали:** {buy_signals}
📉 **SELL сигнали:** {sell_signals}
⏸️ **HOLD сигнали:** {hold_signals}

🎯 **Найкращі можливості:**
"""
        
        for i, opp in enumerate(best_opportunities, 1):
            symbol = opp['symbol']
            recommendation = opp['recommendation']
            confidence = opp['confidence']
            price = opp['entry_price']
            
            emoji = "🟢" if recommendation == "BUY" else "🔴"
            overview += f"{i}. {emoji} **{symbol}** - {recommendation} ({confidence:.0%})\n"
            overview += f"   💰 Ціна: ${price:,.2f}\n"
        
        if not best_opportunities:
            overview += "   Наразі немає сильних сигналів\n"
        
        overview += f"\n⏰ **Час аналізу:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        
        return overview
    
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
            
            # Створюємо аналіз
            analysis = self._create_analysis_without_chatgpt(
                symbol, technical_analysis, market_sentiment
            )
            
            # Відправляємо сигнал
            await self.telegram_bot.send_trading_signal(analysis, news_summary, market_sentiment)
            
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
