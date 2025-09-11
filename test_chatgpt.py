#!/usr/bin/env python3
"""
Тест ChatGPT інтеграції
"""

import sys
import os
from datetime import datetime

# Додаємо поточну директорію в шлях
sys.path.append('.')

def test_openai_import():
    """Тест імпорту OpenAI"""
    print("🔍 Тестування імпорту OpenAI...")
    
    try:
        import openai
        print("✅ OpenAI модуль імпортовано успішно")
        return True
    except ImportError as e:
        print(f"❌ Помилка імпорту OpenAI: {e}")
        return False

def test_openai_config():
    """Тест конфігурації OpenAI"""
    print("🔍 Тестування конфігурації OpenAI...")
    
    try:
        import config
        
        if not config.OPENAI_API_KEY or config.OPENAI_API_KEY == "your_openai_api_key_here":
            print("❌ OPENAI_API_KEY не налаштовано")
            return False
        
        print("✅ OpenAI конфігурація налаштована")
        print(f"   API Key: {config.OPENAI_API_KEY[:10]}...")
        
        return True
        
    except Exception as e:
        print(f"❌ Помилка перевірки конфігурації: {e}")
        return False

def test_openai_client():
    """Тест створення OpenAI клієнта"""
    print("🔍 Тестування створення OpenAI клієнта...")
    
    try:
        import config
        import openai
        
        client = openai.OpenAI(api_key=config.OPENAI_API_KEY)
        print("✅ OpenAI клієнт створено успішно")
        
        return client
        
    except Exception as e:
        print(f"❌ Помилка створення клієнта: {e}")
        return None

def test_openai_models(client):
    """Тест доступних моделей"""
    print("🔍 Тестування доступних моделей...")
    
    try:
        import asyncio
        
        async def get_models():
            try:
                models = client.models.list()
                available_models = []
                
                for model in models.data:
                    if 'gpt' in model.id.lower():
                        available_models.append(model.id)
                
                print(f"✅ Доступні GPT моделі:")
                for model in available_models[:5]:  # Показуємо перші 5
                    print(f"   - {model}")
                
                # Перевіряємо чи доступна gpt-3.5-turbo
                if any('gpt-3.5-turbo' in model for model in available_models):
                    print("✅ gpt-3.5-turbo доступна")
                    return True
                else:
                    print("⚠️ gpt-3.5-turbo не знайдена")
                    return False
                    
            except Exception as e:
                print(f"❌ Помилка отримання моделей: {e}")
                return False
        
        return asyncio.run(get_models())
        
    except Exception as e:
        print(f"❌ Помилка тестування моделей: {e}")
        return False

def test_openai_simple_request(client):
    """Тест простого запиту"""
    print("🔍 Тестування простого запиту...")
    
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": "Привіт! Скажи 'Тест пройшов успішно!' українською мовою."}
            ],
            max_tokens=50,
            temperature=0.3
        )
        
        message = response.choices[0].message.content
        print(f"✅ Відповідь ChatGPT: {message}")
        
        return True
        
    except Exception as e:
        print(f"❌ Помилка простого запиту: {e}")
        return False

def test_our_chatgpt_analyzer():
    """Тест нашого ChatGPT аналізатора"""
    print("🔍 Тестування нашого ChatGPT аналізатора...")
    
    try:
        from chatgpt_analyzer import ChatGPTAnalyzer
        
        analyzer = ChatGPTAnalyzer()
        print("✅ ChatGPT аналізатор створено успішно")
        
        # Тестові дані
        test_technical_data = {
            'symbol': 'BTCUSDT',
            'current_price': 50000.0,
            'price_change_24h': 2.5,
            'trend': 'BULLISH',
            'indicators': {
                'rsi': 65.0,
                'macd': 0.001,
                'ema': 49500.0
            },
            'signals': {
                'rsi': 1,
                'macd': 1,
                'ema': 1,
                'overall': 3
            },
            'recommendation': 'BUY',
            'signal_strength': 3
        }
        
        test_news_summary = "Позитивні новини про Bitcoin"
        test_market_sentiment = {
            'sentiment': 'POSITIVE',
            'score': 0.7
        }
        
        # Тестуємо аналіз
        analysis = analyzer.analyze_trading_opportunity(
            'BTCUSDT',
            test_technical_data,
            test_news_summary,
            test_market_sentiment
        )
        
        if analysis:
            print(f"✅ Аналіз завершено:")
            print(f"   Рекомендація: {analysis.get('recommendation', 'N/A')}")
            print(f"   Впевненість: {analysis.get('confidence', 0):.1%}")
            print(f"   Рівень ризику: {analysis.get('risk_level', 'N/A')}")
            return True
        else:
            print("❌ Аналіз не вдався")
            return False
        
    except Exception as e:
        print(f"❌ Помилка тестування аналізатора: {e}")
        return False

def main():
    """Головна функція"""
    print("🚀 Тест ChatGPT інтеграції")
    print("=" * 50)
    
    tests = [
        ("Імпорт OpenAI", test_openai_import),
        ("Конфігурація", test_openai_config),
        ("Створення клієнта", test_openai_client),
    ]
    
    passed = 0
    client = None
    
    for test_name, test_func in tests:
        print(f"\n📋 {test_name}...")
        try:
            result = test_func()
            if result:
                passed += 1
                if test_name == "Створення клієнта":
                    client = result
            else:
                print(f"❌ Тест {test_name} провалено")
        except Exception as e:
            print(f"❌ Критична помилка в тесті {test_name}: {e}")
    
    # Додаткові тести якщо клієнт створено
    if client:
        additional_tests = [
            ("Доступні моделі", lambda: test_openai_models(client)),
            ("Простий запит", lambda: test_openai_simple_request(client)),
            ("Наш аналізатор", test_our_chatgpt_analyzer)
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
    
    total_tests = len(tests) + (3 if client else 0)
    
    if passed == total_tests:
        print("🎉 Всі тести пройдено! ChatGPT інтеграція працює правильно!")
        print("\n✅ Готово до роботи з ботом!")
    else:
        print(f"⚠️ {passed}/{total_tests} тестів пройдено")
        print("\n🔧 Рекомендації:")
        print("1. Перевірте налаштування OPENAI_API_KEY в .env файлі")
        print("2. Переконайтеся що на акаунті є кошти")
        print("3. Перевірте доступ до моделі gpt-3.5-turbo")
    
    print(f"\n⏰ Час тестування: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    main()
