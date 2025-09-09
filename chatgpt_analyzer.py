import openai
from typing import Dict, List
import json
from config import OPENAI_API_KEY

class ChatGPTAnalyzer:
    def __init__(self):
        openai.api_key = OPENAI_API_KEY
        self.client = openai.OpenAI(api_key=OPENAI_API_KEY)
    
    def analyze_trading_opportunity(self, symbol: str, technical_data: Dict, news_data: str, market_sentiment: Dict) -> Dict:
        """Аналізувати торгову можливість з ChatGPT"""
        
        # Формуємо промпт для ChatGPT
        prompt = self._create_analysis_prompt(symbol, technical_data, news_data, market_sentiment)
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {
                        "role": "system",
                        "content": """Ти професійний криптоаналітик з 10+ років досвіду. 
                        Твоя задача - проаналізувати торгову можливість та дати чіткі рекомендації.
                        Відповідай структуровано та обґрунтовано."""
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                max_tokens=1000,
                temperature=0.3
            )
            
            analysis_text = response.choices[0].message.content
            
            # Парсимо відповідь для отримання структурованих даних
            structured_analysis = self._parse_analysis_response(analysis_text, symbol, technical_data)
            
            return structured_analysis
            
        except Exception as e:
            print(f"Помилка аналізу ChatGPT для {symbol}: {e}")
            return self._get_fallback_analysis(symbol, technical_data)
    
    def _create_analysis_prompt(self, symbol: str, technical_data: Dict, news_data: str, market_sentiment: Dict) -> str:
        """Створити промпт для аналізу"""
        
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

        📰 **НОВИНИ ТА СЕНТИМЕНТ:**
        {news_data}

        🎯 **СЕНТИМЕНТ РИНКУ:**
        - Загальний сентимент: {market_sentiment.get('sentiment', 'NEUTRAL')}
        - Оцінка: {market_sentiment.get('score', 0):.2f}
        - Позитивні новини: {market_sentiment.get('positive_count', 0)}
        - Негативні новини: {market_sentiment.get('negative_count', 0)}

        **ЗАВДАННЯ:**
        1. Проаналізуй всі дані та дай оцінку торгової можливості
        2. Визнач рівень ризику (LOW/MEDIUM/HIGH)
        3. Рекомендуй розмір позиції (від 0% до 100% від доступного капіталу)
        4. Встанови цілі входу, Stop Loss та Take Profit
        5. Обґрунтуй своє рішення

        **ФОРМАТ ВІДПОВІДІ:**
        РЕКОМЕНДАЦІЯ: [BUY/SELL/HOLD]
        РІВЕНЬ РИЗИКУ: [LOW/MEDIUM/HIGH]
        РОЗМІР ПОЗИЦІЇ: [X%]
        ЦІНА ВХОДУ: $[ціна]
        STOP LOSS: $[ціна]
        TAKE PROFIT: $[ціна]
        ОБҐРУНТУВАННЯ: [детальне пояснення]
        """
        
        return prompt
    
    def _parse_analysis_response(self, response_text: str, symbol: str, technical_data: Dict) -> Dict:
        """Парсити відповідь ChatGPT"""
        
        try:
            # Базовий парсинг відповіді
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
                'confidence': 0.5
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
            
            # Розраховуємо впевненість на основі технічних сигналів
            signal_strength = technical_data.get('signal_strength', 0)
            analysis['confidence'] = min(0.9, 0.5 + (signal_strength * 0.1))
            
            # Якщо не вдалося розпарсити ціни, використовуємо технічні дані
            if analysis['stop_loss'] == 0:
                current_price = analysis['entry_price']
                if analysis['recommendation'] == 'BUY':
                    analysis['stop_loss'] = current_price * 0.95  # -5%
                    analysis['take_profit'] = current_price * 1.10  # +10%
                elif analysis['recommendation'] == 'SELL':
                    analysis['stop_loss'] = current_price * 1.05  # +5%
                    analysis['take_profit'] = current_price * 0.90  # -10%
            
            return analysis
            
        except Exception as e:
            print(f"Помилка парсингу відповіді ChatGPT: {e}")
            return self._get_fallback_analysis(symbol, technical_data)
    
    def _get_fallback_analysis(self, symbol: str, technical_data: Dict) -> Dict:
        """Fallback аналіз якщо ChatGPT недоступний"""
        
        recommendation = technical_data.get('recommendation', 'HOLD')
        current_price = technical_data.get('current_price', 0)
        
        analysis = {
            'symbol': symbol,
            'recommendation': recommendation,
            'risk_level': 'MEDIUM',
            'position_size': 0.1 if recommendation in ['BUY', 'SELL'] else 0,
            'entry_price': current_price,
            'stop_loss': current_price * 0.95 if recommendation == 'BUY' else current_price * 1.05,
            'take_profit': current_price * 1.10 if recommendation == 'BUY' else current_price * 0.90,
            'reasoning': f"Автоматичний аналіз на основі технічних індикаторів. Рекомендація: {recommendation}",
            'confidence': 0.3
        }
        
        return analysis
    
    def get_market_overview(self, all_analyses: List[Dict]) -> str:
        """Отримати загальний огляд ринку"""
        
        try:
            # Підраховуємо статистику
            total_pairs = len(all_analyses)
            buy_signals = len([a for a in all_analyses if a.get('recommendation') == 'BUY'])
            sell_signals = len([a for a in all_analyses if a.get('recommendation') == 'SELL'])
            hold_signals = len([a for a in all_analyses if a.get('recommendation') == 'HOLD'])
            
            # Знаходимо найкращі можливості
            best_opportunities = sorted(
                [a for a in all_analyses if a.get('recommendation') in ['BUY', 'SELL']],
                key=lambda x: x.get('confidence', 0),
                reverse=True
            )[:3]
            
            prompt = f"""
            Проаналізуй загальний стан крипто ринку на основі аналізу {total_pairs} торгових пар:

            📊 **СТАТИСТИКА СИГНАЛІВ:**
            - BUY сигнали: {buy_signals}
            - SELL сигнали: {sell_signals}
            - HOLD сигнали: {hold_signals}

            🎯 **НАЙКРАЩІ МОЖЛИВОСТІ:**
            {json.dumps(best_opportunities, indent=2, ensure_ascii=False)}

            Дай короткий огляд ринку та загальні рекомендації.
            """
            
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {
                        "role": "system",
                        "content": "Ти професійний криптоаналітик. Дай короткий та зрозумілий огляд ринку."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                max_tokens=500,
                temperature=0.3
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            print(f"Помилка отримання огляду ринку: {e}")
            return f"Загальний огляд ринку: {buy_signals} BUY, {sell_signals} SELL, {hold_signals} HOLD сигналів з {total_pairs} пар."
