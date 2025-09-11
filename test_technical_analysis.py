#!/usr/bin/env python3
"""
Тест технічного аналізу
"""

import sys
import os
from datetime import datetime
import pandas as pd
import numpy as np

# Додаємо поточну директорію в шлях
sys.path.append('.')

def test_technical_analysis_import():
    """Тест імпорту модулів технічного аналізу"""
    print("🔍 Тестування імпорту модулів технічного аналізу...")
    
    try:
        import ta
        import pandas as pd
        import numpy as np
        print("✅ Модулі технічного аналізу імпортовано успішно")
        return True
    except ImportError as e:
        print(f"❌ Помилка імпорту модулів: {e}")
        return False

def test_our_technical_analyzer():
    """Тест нашого технічного аналізатора"""
    print("🔍 Тестування нашого технічного аналізатора...")
    
    try:
        from technical_analysis import TechnicalAnalyzer
        
        analyzer = TechnicalAnalyzer()
        print("✅ Технічний аналізатор створено успішно")
        
        return analyzer
        
    except Exception as e:
        print(f"❌ Помилка створення аналізатора: {e}")
        return None

def create_test_data():
    """Створити тестові дані"""
    print("🔍 Створення тестових даних...")
    
    try:
        # Створюємо тестові дані
        dates = pd.date_range(start='2024-01-01', periods=100, freq='1H')
        
        # Генеруємо випадкові ціни
        np.random.seed(42)
        base_price = 50000
        prices = []
        current_price = base_price
        
        for i in range(100):
            change = np.random.normal(0, 0.02)  # 2% волатильність
            current_price *= (1 + change)
            prices.append(current_price)
        
        # Створюємо OHLCV дані
        data = []
        for i, price in enumerate(prices):
            high = price * (1 + abs(np.random.normal(0, 0.01)))
            low = price * (1 - abs(np.random.normal(0, 0.01)))
            open_price = prices[i-1] if i > 0 else price
            close = price
            volume = np.random.uniform(100, 1000)
            
            data.append({
                'timestamp': dates[i],
                'open': open_price,
                'high': high,
                'low': low,
                'close': close,
                'volume': volume
            })
        
        df = pd.DataFrame(data)
        print(f"✅ Створено тестові дані: {len(df)} записів")
        print(f"   Ціна від {df['close'].min():.2f} до {df['close'].max():.2f}")
        
        return df
        
    except Exception as e:
        print(f"❌ Помилка створення тестових даних: {e}")
        return None

def test_rsi_calculation(analyzer, df):
    """Тест розрахунку RSI"""
    print("🔍 Тестування розрахунку RSI...")
    
    try:
        rsi = analyzer.calculate_rsi(df)
        
        if rsi is not None and not rsi.empty:
            latest_rsi = rsi.iloc[-1]
            print(f"✅ RSI розраховано: {latest_rsi:.2f}")
            
            if 0 <= latest_rsi <= 100:
                print("✅ RSI в допустимому діапазоні (0-100)")
                return True
            else:
                print("❌ RSI поза допустимим діапазоном")
                return False
        else:
            print("❌ RSI не розраховано")
            return False
            
    except Exception as e:
        print(f"❌ Помилка розрахунку RSI: {e}")
        return False

def test_macd_calculation(analyzer, df):
    """Тест розрахунку MACD"""
    print("🔍 Тестування розрахунку MACD...")
    
    try:
        macd_data = analyzer.calculate_macd(df)
        
        if macd_data and 'macd' in macd_data:
            macd = macd_data['macd'].iloc[-1]
            macd_signal = macd_data['macd_signal'].iloc[-1]
            macd_histogram = macd_data['macd_histogram'].iloc[-1]
            
            print(f"✅ MACD розраховано:")
            print(f"   MACD: {macd:.6f}")
            print(f"   Signal: {macd_signal:.6f}")
            print(f"   Histogram: {macd_histogram:.6f}")
            
            return True
        else:
            print("❌ MACD не розраховано")
            return False
            
    except Exception as e:
        print(f"❌ Помилка розрахунку MACD: {e}")
        return False

def test_ema_calculation(analyzer, df):
    """Тест розрахунку EMA"""
    print("🔍 Тестування розрахунку EMA...")
    
    try:
        ema = analyzer.calculate_ema(df)
        
        if ema is not None and not ema.empty:
            latest_ema = ema.iloc[-1]
            latest_price = df['close'].iloc[-1]
            
            print(f"✅ EMA розраховано: {latest_ema:.2f}")
            print(f"   Поточна ціна: {latest_price:.2f}")
            print(f"   Різниця: {((latest_price - latest_ema) / latest_ema * 100):.2f}%")
            
            return True
        else:
            print("❌ EMA не розраховано")
            return False
            
    except Exception as e:
        print(f"❌ Помилка розрахунку EMA: {e}")
        return False

def test_bollinger_bands(analyzer, df):
    """Тест розрахунку Bollinger Bands"""
    print("🔍 Тестування розрахунку Bollinger Bands...")
    
    try:
        bb_data = analyzer.calculate_bollinger_bands(df)
        
        if bb_data and 'bb_upper' in bb_data:
            bb_upper = bb_data['bb_upper'].iloc[-1]
            bb_middle = bb_data['bb_middle'].iloc[-1]
            bb_lower = bb_data['bb_lower'].iloc[-1]
            current_price = df['close'].iloc[-1]
            
            print(f"✅ Bollinger Bands розраховано:")
            print(f"   Upper: {bb_upper:.2f}")
            print(f"   Middle: {bb_middle:.2f}")
            print(f"   Lower: {bb_lower:.2f}")
            print(f"   Current Price: {current_price:.2f}")
            
            # Перевіряємо логіку
            if bb_upper > bb_middle > bb_lower:
                print("✅ Bollinger Bands мають правильну структуру")
                return True
            else:
                print("❌ Bollinger Bands мають неправильну структуру")
                return False
        else:
            print("❌ Bollinger Bands не розраховано")
            return False
            
    except Exception as e:
        print(f"❌ Помилка розрахунку Bollinger Bands: {e}")
        return False

def test_signal_generation(analyzer, df):
    """Тест генерації сигналів"""
    print("🔍 Тестування генерації сигналів...")
    
    try:
        signals = analyzer.generate_signals(df)
        
        if signals:
            print(f"✅ Сигнали згенеровано:")
            print(f"   RSI: {signals['rsi']}")
            print(f"   MACD: {signals['macd']}")
            print(f"   EMA: {signals['ema']}")
            print(f"   Bollinger: {signals['bollinger']}")
            print(f"   Volume: {signals['volume']}")
            print(f"   Overall: {signals['overall']}")
            
            return True
        else:
            print("❌ Сигнали не згенеровано")
            return False
            
    except Exception as e:
        print(f"❌ Помилка генерації сигналів: {e}")
        return False

def test_full_analysis(analyzer, df):
    """Тест повного аналізу"""
    print("🔍 Тестування повного аналізу...")
    
    try:
        # Створюємо тестові дані для ticker_24h
        ticker_24h = {
            'change_percent': 2.5,
            'volume': 1000.0
        }
        
        analysis = analyzer.get_analysis_summary('BTCUSDT', df, ticker_24h)
        
        if analysis:
            print(f"✅ Повний аналіз завершено:")
            print(f"   Символ: {analysis['symbol']}")
            print(f"   Поточна ціна: ${analysis['current_price']:.2f}")
            print(f"   Тренд: {analysis['trend']}")
            print(f"   Рекомендація: {analysis['recommendation']}")
            print(f"   Сила сигналу: {analysis['signal_strength']}")
            print(f"   RSI: {analysis['indicators']['rsi']:.2f}")
            
            return True
        else:
            print("❌ Повний аналіз не вдався")
            return False
            
    except Exception as e:
        print(f"❌ Помилка повного аналізу: {e}")
        return False

def main():
    """Головна функція"""
    print("🚀 Тест технічного аналізу")
    print("=" * 50)
    
    # Тести
    tests = [
        ("Імпорт модулів", test_technical_analysis_import),
        ("Створення аналізатора", test_our_technical_analyzer),
        ("Створення тестових даних", create_test_data)
    ]
    
    passed = 0
    analyzer = None
    df = None
    
    for test_name, test_func in tests:
        print(f"\n📋 {test_name}...")
        try:
            result = test_func()
            if result is not None:
                passed += 1
                if test_name == "Створення аналізатора":
                    analyzer = result
                elif test_name == "Створення тестових даних":
                    df = result
            else:
                print(f"❌ Тест {test_name} провалено")
        except Exception as e:
            print(f"❌ Критична помилка в тесті {test_name}: {e}")
    
    # Додаткові тести якщо аналізатор та дані створені
    if analyzer and df is not None:
        additional_tests = [
            ("Розрахунок RSI", lambda: test_rsi_calculation(analyzer, df)),
            ("Розрахунок MACD", lambda: test_macd_calculation(analyzer, df)),
            ("Розрахунок EMA", lambda: test_ema_calculation(analyzer, df)),
            ("Bollinger Bands", lambda: test_bollinger_bands(analyzer, df)),
            ("Генерація сигналів", lambda: test_signal_generation(analyzer, df)),
            ("Повний аналіз", lambda: test_full_analysis(analyzer, df))
        ]
        
        for test_name, test_func in additional_tests:
            print(f"\n📋 {test_name}...")
            try:
                if test_func():
                    passed += 1
                else:
                    print(f"❌ Тест {test_name} провалено")
            except Exception as e:
                print(f"❌ Критична помилка в тесті {test_name}: {e}")
    
    print("\n" + "=" * 50)
    print("📊 ПІДСУМОК ТЕСТУВАННЯ:")
    
    total_tests = len(tests) + (6 if analyzer and df is not None else 0)
    
    if passed == total_tests:
        print("🎉 Всі тести пройдено! Технічний аналіз працює правильно!")
        print("\n✅ Готово до роботи з ботом!")
    else:
        print(f"⚠️ {passed}/{total_tests} тестів пройдено")
        print("\n🔧 Рекомендації:")
        print("1. Перевірте встановлення модуля ta")
        print("2. Перевірте встановлення pandas та numpy")
    
    print(f"\n⏰ Час тестування: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    main()
