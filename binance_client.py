import pandas as pd
import numpy as np
from binance.client import Client
from binance.exceptions import BinanceAPIException
import time
from config import BINANCE_API_KEY, BINANCE_API_SECRET, TRADING_PAIRS

class BinanceClient:
    def __init__(self):
        self.client = Client(BINANCE_API_KEY, BINANCE_API_SECRET)
        self.trading_pairs = TRADING_PAIRS
        
    def get_klines(self, symbol, interval='1h', limit=100):
        """Отримати історичні дані для символу"""
        try:
            klines = self.client.get_klines(
                symbol=symbol,
                interval=interval,
                limit=limit
            )
            
            df = pd.DataFrame(klines, columns=[
                'timestamp', 'open', 'high', 'low', 'close', 'volume',
                'close_time', 'quote_asset_volume', 'number_of_trades',
                'taker_buy_base_volume', 'taker_buy_quote_volume', 'ignore'
            ])
            
            # Конвертуємо в числові типи
            for col in ['open', 'high', 'low', 'close', 'volume']:
                df[col] = pd.to_numeric(df[col])
            
            df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
            return df[['timestamp', 'open', 'high', 'low', 'close', 'volume']]
            
        except BinanceAPIException as e:
            print(f"Помилка отримання даних для {symbol}: {e}")
            return None
    
    def get_current_price(self, symbol):
        """Отримати поточну ціну символу"""
        try:
            ticker = self.client.get_symbol_ticker(symbol=symbol)
            return float(ticker['price'])
        except BinanceAPIException as e:
            print(f"Помилка отримання ціни для {symbol}: {e}")
            return None
    
    def get_24h_ticker(self, symbol):
        """Отримати 24h статистику для символу"""
        try:
            ticker = self.client.get_ticker(symbol=symbol)
            return {
                'symbol': ticker['symbol'],
                'price': float(ticker['lastPrice']),
                'change': float(ticker['priceChange']),
                'change_percent': float(ticker['priceChangePercent']),
                'volume': float(ticker['volume']),
                'high': float(ticker['highPrice']),
                'low': float(ticker['lowPrice'])
            }
        except BinanceAPIException as e:
            print(f"Помилка отримання 24h статистики для {symbol}: {e}")
            return None
    
    def get_all_pairs_data(self):
        """Отримати дані для всіх торгових пар"""
        all_data = {}
        
        for symbol in self.trading_pairs:
            try:
                # Отримуємо історичні дані
                klines = self.get_klines(symbol, '1h', 100)
                if klines is not None:
                    all_data[symbol] = {
                        'klines': klines,
                        'current_price': self.get_current_price(symbol),
                        'ticker_24h': self.get_24h_ticker(symbol)
                    }
                
                # Невелика затримка щоб не перевищити ліміти API
                time.sleep(0.1)
                
            except Exception as e:
                print(f"Помилка обробки {symbol}: {e}")
                continue
        
        return all_data
    
    def get_order_book(self, symbol, limit=10):
        """Отримати ордербук для символу"""
        try:
            depth = self.client.get_order_book(symbol=symbol, limit=limit)
            return {
                'bids': [[float(bid[0]), float(bid[1])] for bid in depth['bids']],
                'asks': [[float(ask[0]), float(ask[1])] for ask in depth['asks']]
            }
        except BinanceAPIException as e:
            print(f"Помилка отримання ордербука для {symbol}: {e}")
            return None
