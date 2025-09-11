import asyncio
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import json

from binance_client import BinanceClient
from technical_analysis import TechnicalAnalyzer
from news_aggregator import NewsAggregator
from config import TRADING_PAIRS, ANALYSIS_INTERVAL, SIGNAL_THRESHOLD

class SignalProcessorConsole:
    def __init__(self):
        self.binance_client = BinanceClient()
        self.technical_analyzer = TechnicalAnalyzer()
        self.news_aggregator = NewsAggregator()
        
        self.trading_pairs = TRADING_PAIRS
        self.analysis_interval = ANALYSIS_INTERVAL
        self.signal_threshold = SIGNAL_THRESHOLD
        
        self.last_analysis_time = {}
        self.sent_signals = set()  # Для уникнення дублювання сигналів
        self.is_running = False
    
    async def start_analysis_loop(self):
        """Запустити основний цикл аналізу"""
        self.is_running = True
        print("🚀 Запуск аналізу торгових сигналів (консольний режим)...")
        
        while self.is_running:
            try:
                await self._run_analysis_cycle()
                print(f"⏰ Наступний аналіз через {self.analysis_interval} секунд...")
                await asyncio.sleep(self.analysis_interval)
                
            except Exception as e:
                print(f"❌ Помилка в циклі аналізу: {e}")
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
        
        # Виводимо сильні сигнали в консоль
        if strong_signals:
            print(f"📈 Знайдено {len(strong_signals)} сильних сигналів!")
            self._print_strong_signals(strong_signals, news_summary, market_sentiment)
        
        # Виводимо огляд ринку кожні 30 хвилин
        if self._should_send_market_overview():
            self._print_market_overview(all_analyses)
        
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
    
    def _print_strong_signals(self, signals: List[Dict], news_summary: str, market_sentiment: Dict):
        """Вивести сильні сигнали в консоль"""
        
        print("\n" + "="*80)
        print("📈 СИЛЬНІ ТОРГОВІ СИГНАЛИ")
        print("="*80)
        
        for signal in signals:
            symbol = signal['symbol']
            recommendation = signal['recommendation']
            confidence = signal['confidence']
            risk_level = signal['risk_level']
            position_size = signal['position_size']
            entry_price = signal['entry_price']
            stop_loss = signal['stop_loss']
            take_profit = signal['take_profit']
            reasoning = signal['reasoning']
            
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
            
            print(f"\n{emoji_map.get(recommendation, '🟡')} **ТОРГОВИЙ СИГНАЛ: {symbol}**")
            print(f"📊 РЕКОМЕНДАЦІЯ: {recommendation}")
            print(f"🎯 ВПЕВНЕНІСТЬ: {confidence:.1%}")
            print(f"⚠️ РИЗИК: {risk_level} {risk_emoji_map.get(risk_level, '🟡')}")
            print(f"💰 РОЗМІР ПОЗИЦІЇ: {position_size:.1%}")
            print(f"💵 ЦІНИ:")
            print(f"   • Вхід: ${entry_price:.4f}")
            print(f"   • Stop Loss: ${stop_loss:.4f}")
            print(f"   • Take Profit: ${take_profit:.4f}")
            print(f"📈 ПОТЕНЦІАЛ:")
            print(f"   • Ризик: {abs(entry_price - stop_loss) / entry_price * 100:.1f}%")
            print(f"   • Прибуток: {abs(take_profit - entry_price) / entry_price * 100:.1f}%")
            print(f"🧠 АНАЛІЗ: {reasoning}")
            print(f"⏰ ЧАС: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            print("-" * 80)
        
        print(f"\n📰 СЕНТИМЕНТ РИНКУ: {market_sentiment.get('sentiment', 'NEUTRAL')}")
        print(f"📊 ОЦІНКА: {market_sentiment.get('score', 0):.2f}")
        print("="*80)
    
    def _print_market_overview(self, all_analyses: List[Dict]):
        """Вивести огляд ринку в консоль"""
        
        try:
            # Підраховуємо статистику
            statistics = {
                'total_pairs': len(all_analyses),
                'buy_signals': len([a for a in all_analyses if a.get('recommendation') == 'BUY']),
                'sell_signals': len([a for a in all_analyses if a.get('recommendation') == 'SELL']),
                'hold_signals': len([a for a in all_analyses if a.get('recommendation') == 'HOLD'])
            }
            
            # Створюємо простий огляд
            overview_text = self._create_simple_market_overview(all_analyses, statistics)
            
            print("\n" + "="*80)
            print("📊 ОГЛЯД РИНКУ")
            print("="*80)
            print(overview_text)
            print("="*80)
            
            # Оновлюємо час останнього огляду
            self.last_analysis_time['market_overview'] = datetime.now()
            
        except Exception as e:
            print(f"❌ Помилка створення огляду ринку: {e}")
    
    def _create_simple_market_overview(self, all_analyses: List[Dict], statistics: Dict) -> str:
        """Створити простий огляд ринку"""
        
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
            
            # Виводимо сигнал в консоль
            self._print_strong_signals([analysis], news_summary, market_sentiment)
            
            print(f"✅ Ручний аналіз для {symbol} завершено")
            
        except Exception as e:
            print(f"❌ Помилка ручного аналізу для {symbol}: {e}")
    
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
