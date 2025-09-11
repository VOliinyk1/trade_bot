import pandas as pd
import numpy as np
import ta
from config import RSI_PERIOD, MACD_FAST, MACD_SLOW, MACD_SIGNAL, EMA_PERIOD, BB_PERIOD, BB_STD

class TechnicalAnalyzer:
    def __init__(self):
        self.rsi_period = RSI_PERIOD
        self.macd_fast = MACD_FAST
        self.macd_slow = MACD_SLOW
        self.macd_signal = MACD_SIGNAL
        self.ema_period = EMA_PERIOD
        self.bb_period = BB_PERIOD
        self.bb_std = BB_STD
    
    def calculate_rsi(self, df):
        """Розрахувати RSI"""
        return ta.momentum.RSIIndicator(df['close'], window=self.rsi_period).rsi()
    
    def calculate_macd(self, df):
        """Розрахувати MACD"""
        macd_indicator = ta.trend.MACD(
            df['close'], 
            window_fast=self.macd_fast, 
            window_slow=self.macd_slow, 
            window_sign=self.macd_signal
        )
        return {
            'macd': macd_indicator.macd(),
            'macd_signal': macd_indicator.macd_signal(),
            'macd_histogram': macd_indicator.macd_diff()
        }
    
    def calculate_ema(self, df):
        """Розрахувати EMA"""
        return ta.trend.EMAIndicator(df['close'], window=self.ema_period).ema_indicator()
    
    def calculate_bollinger_bands(self, df):
        """Розрахувати Bollinger Bands"""
        bb_indicator = ta.volatility.BollingerBands(
            df['close'], 
            window=self.bb_period, 
            window_dev=self.bb_std
        )
        return {
            'bb_upper': bb_indicator.bollinger_hband(),
            'bb_middle': bb_indicator.bollinger_mavg(),
            'bb_lower': bb_indicator.bollinger_lband()
        }
    
    def calculate_volume_indicators(self, df):
        """Розрахувати об'ємні індикатори"""
        try:
            # Використовуємо простіші об'ємні індикатори
            volume_sma = df['volume'].rolling(window=20).mean()
            volume_ema = df['volume'].ewm(span=20).mean()
            
            return {
                'volume_sma': volume_sma,
                'volume_ema': volume_ema
            }
        except Exception as e:
            print(f"Помилка розрахунку об'ємних індикаторів: {e}")
            return {
                'volume_sma': df['volume'],
                'volume_ema': df['volume']
            }
    
    def calculate_support_resistance(self, df):
        """Знайти рівні підтримки та опору"""
        highs = df['high'].rolling(window=20).max()
        lows = df['low'].rolling(window=20).min()
        
        resistance = highs.iloc[-1] if not pd.isna(highs.iloc[-1]) else None
        support = lows.iloc[-1] if not pd.isna(lows.iloc[-1]) else None
        
        return {
            'resistance': resistance,
            'support': support
        }
    
    def analyze_trend(self, df):
        """Аналіз тренду"""
        # EMA тренд
        ema = self.calculate_ema(df)
        current_price = df['close'].iloc[-1]
        ema_current = ema.iloc[-1]
        
        # MACD тренд
        macd_data = self.calculate_macd(df)
        macd_current = macd_data['macd'].iloc[-1]
        macd_signal_current = macd_data['macd_signal'].iloc[-1]
        
        trend_strength = 0
        
        # EMA аналіз
        if current_price > ema_current:
            trend_strength += 1
        else:
            trend_strength -= 1
        
        # MACD аналіз
        if macd_current > macd_signal_current:
            trend_strength += 1
        else:
            trend_strength -= 1
        
        if trend_strength > 0:
            return "BULLISH"
        elif trend_strength < 0:
            return "BEARISH"
        else:
            return "NEUTRAL"
    
    def generate_signals(self, df):
        """Генерувати торгові сигнали"""
        signals = {
            'rsi': 0,
            'macd': 0,
            'ema': 0,
            'bollinger': 0,
            'volume': 0,
            'overall': 0
        }
        
        # RSI сигнали
        rsi = self.calculate_rsi(df)
        rsi_current = rsi.iloc[-1]
        
        if rsi_current < 30:  # Oversold
            signals['rsi'] = 1
        elif rsi_current > 70:  # Overbought
            signals['rsi'] = -1
        else:
            signals['rsi'] = 0
        
        # MACD сигнали
        macd_data = self.calculate_macd(df)
        macd_current = macd_data['macd'].iloc[-1]
        macd_signal_current = macd_data['macd_signal'].iloc[-1]
        macd_prev = macd_data['macd'].iloc[-2]
        macd_signal_prev = macd_data['macd_signal'].iloc[-2]
        
        # Перетин MACD лінії з сигнальною
        if macd_prev <= macd_signal_prev and macd_current > macd_signal_current:
            signals['macd'] = 1  # Bullish crossover
        elif macd_prev >= macd_signal_prev and macd_current < macd_signal_current:
            signals['macd'] = -1  # Bearish crossover
        else:
            signals['macd'] = 0
        
        # EMA сигнали
        ema = self.calculate_ema(df)
        current_price = df['close'].iloc[-1]
        ema_current = ema.iloc[-1]
        
        if current_price > ema_current:
            signals['ema'] = 1
        elif current_price < ema_current:
            signals['ema'] = -1
        else:
            signals['ema'] = 0
        
        # Bollinger Bands сигнали
        bb_data = self.calculate_bollinger_bands(df)
        bb_upper = bb_data['bb_upper'].iloc[-1]
        bb_lower = bb_data['bb_lower'].iloc[-1]
        
        if current_price <= bb_lower:
            signals['bollinger'] = 1  # Oversold
        elif current_price >= bb_upper:
            signals['bollinger'] = -1  # Overbought
        else:
            signals['bollinger'] = 0
        
        # Об'ємні сигнали
        volume_indicators = self.calculate_volume_indicators(df)
        current_volume = df['volume'].iloc[-1]
        volume_sma = volume_indicators['volume_sma'].iloc[-1]
        
        if current_volume > volume_sma * 1.5:  # Високий об'єм
            signals['volume'] = 1
        elif current_volume < volume_sma * 0.5:  # Низький об'єм
            signals['volume'] = -1
        else:
            signals['volume'] = 0
        
        # Загальний сигнал
        total_signals = sum(signals.values()) - signals['overall']  # Виключаємо overall з підрахунку
        signals['overall'] = total_signals
        
        return signals
    
    def get_analysis_summary(self, symbol, df, ticker_24h):
        """Отримати повний аналіз для символу"""
        try:
            # Розраховуємо всі індикатори
            rsi = self.calculate_rsi(df)
            macd_data = self.calculate_macd(df)
            ema = self.calculate_ema(df)
            bb_data = self.calculate_bollinger_bands(df)
            volume_indicators = self.calculate_volume_indicators(df)
            support_resistance = self.calculate_support_resistance(df)
            
            # Генеруємо сигнали
            signals = self.generate_signals(df)
            trend = self.analyze_trend(df)
            
            # Поточні значення
            current_price = df['close'].iloc[-1]
            current_volume = df['volume'].iloc[-1]
            
            analysis = {
                'symbol': symbol,
                'current_price': current_price,
                'price_change_24h': ticker_24h.get('change_percent', 0) if ticker_24h else 0,
                'volume_24h': ticker_24h.get('volume', 0) if ticker_24h else 0,
                'trend': trend,
                'signals': signals,
                'indicators': {
                    'rsi': rsi.iloc[-1] if not pd.isna(rsi.iloc[-1]) else None,
                    'macd': macd_data['macd'].iloc[-1] if not pd.isna(macd_data['macd'].iloc[-1]) else None,
                    'macd_signal': macd_data['macd_signal'].iloc[-1] if not pd.isna(macd_data['macd_signal'].iloc[-1]) else None,
                    'ema': ema.iloc[-1] if not pd.isna(ema.iloc[-1]) else None,
                    'bb_upper': bb_data['bb_upper'].iloc[-1] if not pd.isna(bb_data['bb_upper'].iloc[-1]) else None,
                    'bb_lower': bb_data['bb_lower'].iloc[-1] if not pd.isna(bb_data['bb_lower'].iloc[-1]) else None,
                    'volume_sma': volume_indicators['volume_sma'].iloc[-1] if not pd.isna(volume_indicators['volume_sma'].iloc[-1]) else None
                },
                'support_resistance': support_resistance,
                'signal_strength': abs(signals['overall']),
                'recommendation': self._get_recommendation(signals, trend)
            }
            
            return analysis
            
        except Exception as e:
            print(f"Помилка аналізу для {symbol}: {e}")
            return None
    
    def _get_recommendation(self, signals, trend):
        """Отримати рекомендацію на основі сигналів"""
        overall_signal = signals['overall']
        
        if overall_signal >= 3:
            return "STRONG_BUY"
        elif overall_signal >= 1:
            return "BUY"
        elif overall_signal <= -3:
            return "STRONG_SELL"
        elif overall_signal <= -1:
            return "SELL"
        else:
            return "HOLD"
