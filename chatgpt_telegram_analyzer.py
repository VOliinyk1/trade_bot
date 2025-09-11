import openai
from typing import Dict, List
import json
from datetime import datetime
from config import OPENAI_API_KEY

class ChatGPTTelegramAnalyzer:
    def __init__(self):
        openai.api_key = OPENAI_API_KEY
        self.client = openai.OpenAI(api_key=OPENAI_API_KEY)
    
    async def analyze_trading_opportunity(self, symbol: str, technical_data: Dict, news_data: str, market_sentiment: Dict, telegram_bot=None) -> Dict:
        """Аналізувати торгову можливість з ChatGPT та надсилати повідомлення в Telegram"""
        
        try:
            # Формуємо детальний промпт для ChatGPT
            prompt = self._create_detailed_analysis_prompt(symbol, technical_data, news_data, market_sentiment)
            
            print(f"🤖 ChatGPT аналіз {symbol}...")
            
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": """Ти професійний криптоаналітик з 10+ років досвіду. 
                        Твоя задача - проаналізувати торгову можливість та дати детальні рекомендації.
                        Відповідай структуровано, обґрунтовано та зрозуміло для трейдера."""
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                max_tokens=1500,
                temperature=0.3
            )
            
            analysis_text = response.choices[0].message.content
            
            # Парсимо відповідь для отримання структурованих даних
            structured_analysis = self._parse_analysis_response(analysis_text, symbol, technical_data)
            
            # Надсилаємо детальний аналіз в Telegram
            if telegram_bot:
                await self._send_chatgpt_analysis_to_telegram(telegram_bot, symbol, analysis_text, structured_analysis)
            
            return structured_analysis
            
        except Exception as e:
            print(f"Помилка аналізу ChatGPT для {symbol}: {e}")
            # Використовуємо fallback аналіз
            fallback_analysis = self._get_enhanced_fallback_analysis(symbol, technical_data, market_sentiment)
            
            # Надсилаємо fallback повідомлення
            if telegram_bot:
                await self._send_fallback_analysis_to_telegram(telegram_bot, symbol, fallback_analysis, str(e))
            
            return fallback_analysis
    
    def _create_detailed_analysis_prompt(self, symbol: str, technical_data: Dict, news_data: str, market_sentiment: Dict) -> str:
        """Створити детальний промпт для аналізу"""
        
        prompt = f"""
        Проаналізуй торгову можливість для {symbol} на основі наступних даних:

        📊 **ТЕХНІЧНИЙ АНАЛІЗ:**
        - Поточна ціна: ${technical_data.get('current_price', 0):.4f}
        - Зміна за 24г: {technical_data.get('price_change_24h', 0):.2f}%
        - Тренд: {technical_data.get('trend', 'NEUTRAL')}
        - RSI: {technical_data.get('indicators', {}).get('rsi', 0):.2f}
        - MACD: {technical_data.get('indicators', {}).get('macd', 0):.6f}
        - EMA: {technical_data.get('indicators', {}).get('ema', 0):.4f}
        - Сигнали: {technical_data.get('signals', {})}
        - Рекомендація: {technical_data.get('recommendation', 'HOLD')}
        - Сила сигналу: {technical_data.get('signal_strength', 0)}

        📰 **НОВИНИ ТА СЕНТИМЕНТ:**
        {news_data}

        🎯 **СЕНТИМЕНТ РИНКУ:**
        - Загальний сентимент: {market_sentiment.get('sentiment', 'NEUTRAL')}
        - Оцінка: {market_sentiment.get('score', 0):.2f}
        - Позитивні новини: {market_sentiment.get('positive_count', 0)}
        - Негативні новини: {market_sentiment.get('negative_count', 0)}

        **ЗАВДАННЯ:**
        1. Дай детальний аналіз поточного стану {symbol}
        2. Оціни ризики та можливості для BUY позиції
        3. Визнач рівень ризику (LOW/MEDIUM/HIGH)
        4. Рекомендуй розмір позиції (від 1% до 5% від доступного капіталу)
        5. Встанови цілі входу, Stop Loss та Take Profit з урахуванням волатільності
        6. Stop Loss має бути 2-5% від ціни входу
        7. Take Profit має бути 3-10% від ціни входу (співвідношення ризик/прибуток 1:1.5 або краще)
        8. Обґрунтуй своє рішення детально
        9. Врахуй сентимент ринку в аналізі

        **ФОРМАТ ВІДПОВІДІ:**
        РЕКОМЕНДАЦІЯ: [BUY/SELL/HOLD]
        РІВЕНЬ РИЗИКУ: [LOW/MEDIUM/HIGH]
        РОЗМІР ПОЗИЦІЇ: [X%]
        ЦІНА ВХОДУ: $[ціна]
        STOP LOSS: $[ціна]
        TAKE PROFIT: $[ціна]
        СЕНТИМЕНТ: [POSITIVE/NEGATIVE/NEUTRAL]
        ОЦІНКА СЕНТИМЕНТУ: [X.XX]
        ОБҐРУНТУВАННЯ: [детальне пояснення з урахуванням сентименту]
        """
        
        return prompt
    
    async def _send_chatgpt_analysis_to_telegram(self, telegram_bot, symbol: str, analysis_text: str, structured_analysis: Dict):
        """Надіслати ChatGPT аналіз в Telegram"""
        
        try:
            # Використовуємо існуючий метод send_trading_signal
            await telegram_bot.send_trading_signal(
                analysis=structured_analysis,
                news_summary=analysis_text[:500] + "..." if len(analysis_text) > 500 else analysis_text,
                market_sentiment={'sentiment': structured_analysis.get('sentiment', 'NEUTRAL'), 'score': structured_analysis.get('sentiment_score', 0.0)}
            )
            
            print(f"✅ ChatGPT аналіз для {symbol} відправлено в Telegram")
            
        except Exception as e:
            print(f"❌ Помилка відправки ChatGPT аналізу: {e}")
    
    async def _send_fallback_analysis_to_telegram(self, telegram_bot, symbol: str, fallback_analysis: Dict, error_message: str):
        """Надіслати fallback аналіз в Telegram"""
        
        try:
            # Використовуємо існуючий метод send_trading_signal
            await telegram_bot.send_trading_signal(
                analysis=fallback_analysis,
                news_summary=f"⚠️ Fallback аналіз (ChatGPT недоступний: {error_message})",
                market_sentiment={'sentiment': fallback_analysis.get('sentiment', 'NEUTRAL'), 'score': fallback_analysis.get('sentiment_score', 0.0)}
            )
            
            print(f"✅ Fallback аналіз для {symbol} відправлено в Telegram")
            
        except Exception as e:
            print(f"❌ Помилка відправки fallback аналізу: {e}")
    
    def _parse_analysis_response(self, response_text: str, symbol: str, technical_data: Dict) -> Dict:
        """Парсити відповідь ChatGPT"""
        
        try:
            lines = response_text.split('\n')
            
            analysis = {
                'symbol': symbol,
                'recommendation': 'HOLD',
                'risk_level': 'MEDIUM',
                'position_size': 0,
                'entry_price': technical_data.get('current_price', 0),
                'stop_loss': 0,
                'take_profit': 0,
                'reasoning': response_text,
                'confidence': 0.5,
                'sentiment': 'NEUTRAL',
                'sentiment_score': 0.0
            }
            
            for line in lines:
                line = line.strip()
                
                if line.startswith('РЕКОМЕНДАЦІЯ:'):
                    rec = line.split(':', 1)[1].strip().upper()
                    if rec in ['BUY', 'SELL', 'HOLD']:
                        analysis['recommendation'] = rec
                
                elif line.startswith('РІВЕНЬ РИЗИКУ:'):
                    risk = line.split(':', 1)[1].strip().upper()
                    if risk in ['LOW', 'MEDIUM', 'HIGH']:
                        analysis['risk_level'] = risk
                
                elif line.startswith('РОЗМІР ПОЗИЦІЇ:'):
                    try:
                        size_str = line.split(':', 1)[1].strip().replace('%', '')
                        analysis['position_size'] = float(size_str) / 100
                    except:
                        pass
                
                elif line.startswith('ЦІНА ВХОДУ:'):
                    try:
                        price_str = line.split(':', 1)[1].strip().replace('$', '').replace(',', '')
                        analysis['entry_price'] = float(price_str)
                    except:
                        pass
                
                elif line.startswith('STOP LOSS:'):
                    try:
                        sl_str = line.split(':', 1)[1].strip().replace('$', '').replace(',', '')
                        analysis['stop_loss'] = float(sl_str)
                    except:
                        pass
                
                elif line.startswith('TAKE PROFIT:'):
                    try:
                        tp_str = line.split(':', 1)[1].strip().replace('$', '').replace(',', '')
                        analysis['take_profit'] = float(tp_str)
                    except:
                        pass
                
                elif line.startswith('СЕНТИМЕНТ:'):
                    sentiment = line.split(':', 1)[1].strip().upper()
                    if sentiment in ['POSITIVE', 'NEGATIVE', 'NEUTRAL']:
                        analysis['sentiment'] = sentiment
                
                elif line.startswith('ОЦІНКА СЕНТИМЕНТУ:'):
                    try:
                        score_str = line.split(':', 1)[1].strip()
                        analysis['sentiment_score'] = float(score_str)
                    except:
                        pass
            
            # Розраховуємо впевненість
            signal_strength = technical_data.get('signal_strength', 0)
            analysis['confidence'] = min(0.9, 0.5 + (signal_strength * 0.1))
            
            # Якщо не вдалося розпарсити ціни, використовуємо покращені розрахунки
            if analysis['stop_loss'] == 0:
                current_price = analysis['entry_price']
                if analysis['recommendation'] == 'BUY':
                    # Покращені розрахунки для BUY позицій
                    signal_strength = technical_data.get('signal_strength', 0)
                    
                    # Stop Loss: 2-5% залежно від сили сигналу
                    if signal_strength >= 3:
                        stop_loss_percent = 0.02  # 2% для сильних сигналів
                    elif signal_strength >= 2:
                        stop_loss_percent = 0.03  # 3% для середніх сигналів
                    else:
                        stop_loss_percent = 0.05  # 5% для слабких сигналів
                    
                    # Take Profit: 1.5-2x від ризику
                    take_profit_multiplier = 1.8  # Співвідношення ризик/прибуток 1:1.8
                    
                    analysis['stop_loss'] = current_price * (1 - stop_loss_percent)
                    analysis['take_profit'] = current_price * (1 + (stop_loss_percent * take_profit_multiplier))
                    
                    # Оновлюємо розмір позиції на основі ризику
                    if analysis['risk_level'] == 'LOW':
                        analysis['position_size'] = min(0.05, analysis['position_size'])  # Макс 5%
                    elif analysis['risk_level'] == 'MEDIUM':
                        analysis['position_size'] = min(0.03, analysis['position_size'])  # Макс 3%
                    else:  # HIGH
                        analysis['position_size'] = min(0.02, analysis['position_size'])  # Макс 2%
                        
                elif analysis['recommendation'] == 'SELL':
                    # Для SELL позицій (хоча ми їх не використовуємо)
                    analysis['stop_loss'] = current_price * 1.05  # +5%
                    analysis['take_profit'] = current_price * 0.90  # -10%
            
            return analysis
            
        except Exception as e:
            print(f"Помилка парсингу відповіді ChatGPT: {e}")
            return self._get_fallback_analysis(symbol, technical_data)
    
    def _get_fallback_analysis(self, symbol: str, technical_data: Dict) -> Dict:
        """Fallback аналіз"""
        
        recommendation = technical_data.get('recommendation', 'HOLD')
        current_price = technical_data.get('current_price', 0)
        
        return {
            'symbol': symbol,
            'recommendation': recommendation,
            'risk_level': 'MEDIUM',
            'position_size': 0.1 if recommendation in ['BUY', 'SELL'] else 0,
            'entry_price': current_price,
            'stop_loss': current_price * 0.95 if recommendation == 'BUY' else current_price * 1.05,
            'take_profit': current_price * 1.10 if recommendation == 'BUY' else current_price * 0.90,
            'reasoning': f"Автоматичний аналіз на основі технічних індикаторів. Рекомендація: {recommendation}",
            'confidence': 0.3,
            'sentiment': 'NEUTRAL',
            'sentiment_score': 0.0
        }
    
    def _get_enhanced_fallback_analysis(self, symbol: str, technical_data: Dict, market_sentiment: Dict) -> Dict:
        """Розширений fallback аналіз з урахуванням сентименту"""
        
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
            confidence = 0.7
            position_size = 0.15
        elif signal_strength >= 2:
            risk_level = 'MEDIUM'
            confidence = 0.5
            position_size = 0.1
        else:
            risk_level = 'HIGH'
            confidence = 0.3
            position_size = 0.05
        
        # Корегуємо рекомендацію на основі сентименту
        if sentiment == 'NEGATIVE' and recommendation == 'BUY':
            recommendation = 'HOLD'
            confidence *= 0.7
        elif sentiment == 'POSITIVE' and recommendation == 'SELL':
            recommendation = 'HOLD'
            confidence *= 0.7
        
        # Розраховуємо ціни з покращеними розрахунками
        if recommendation == 'BUY':
            # Покращені розрахунки для BUY позицій
            if signal_strength >= 3:
                stop_loss_percent = 0.02  # 2% для сильних сигналів
            elif signal_strength >= 2:
                stop_loss_percent = 0.03  # 3% для середніх сигналів
            else:
                stop_loss_percent = 0.05  # 5% для слабких сигналів
            
            # Take Profit: 1.8x від ризику
            take_profit_multiplier = 1.8
            
            stop_loss = current_price * (1 - stop_loss_percent)
            take_profit = current_price * (1 + (stop_loss_percent * take_profit_multiplier))
            
            # Обмежуємо розмір позиції
            if risk_level == 'LOW':
                position_size = min(0.05, position_size)  # Макс 5%
            elif risk_level == 'MEDIUM':
                position_size = min(0.03, position_size)  # Макс 3%
            else:  # HIGH
                position_size = min(0.02, position_size)  # Макс 2%
                
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
        reasoning_parts.append("(Fallback аналіз - ChatGPT недоступний)")
        
        reasoning = ". ".join(reasoning_parts) + "."
        
        return {
            'symbol': symbol,
            'recommendation': recommendation,
            'risk_level': risk_level,
            'position_size': position_size,
            'entry_price': current_price,
            'stop_loss': stop_loss,
            'take_profit': take_profit,
            'reasoning': reasoning,
            'confidence': confidence,
            'sentiment': sentiment,
            'sentiment_score': sentiment_score
        }
