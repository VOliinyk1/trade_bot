# 🤖 Crypto Trading Bot

Автоматичний бот для аналізу криптовалют на біржі Binance з інтеграцією ChatGPT та відправкою сигналів в Telegram.

## 🚀 Можливості

- **Технічний аналіз** багатьох торгових пар одночасно
- **AI аналіз** від ChatGPT для прийняття рішень
- **Збір новин** з різних джерел про крипто ринок
- **Автоматичні сигнали** в Telegram канал
- **Ризик-менеджмент** та рекомендації по розміру позицій

## 📊 Технічні індикатори

- **RSI** (Relative Strength Index)
- **MACD** (Moving Average Convergence Divergence)
- **EMA** (Exponential Moving Average)
- **Bollinger Bands**
- **Об'ємні індикатори**
- **Підтримка та опір**

## 🔧 Встановлення

### 1. Клонування репозиторію
```bash
git clone <repository-url>
cd crypto-trading-bot
```

### 2. Встановлення залежностей
```bash
pip install -r requirements.txt
```

### 3. Налаштування змінних середовища
Створіть файл `.env` на основі `env.example`:

```env
# Binance API
BINANCE_API_KEY=your_binance_api_key_here
BINANCE_API_SECRET=your_binance_api_secret_here

# OpenAI API
OPENAI_API_KEY=your_openai_api_key_here

# Telegram Bot
TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here
TELEGRAM_CHANNEL_ID=your_telegram_channel_id_here

# Trading Configuration
TRADING_PAIRS=BTCUSDT,ETHUSDT,BNBUSDT,ADAUSDT,SOLUSDT,MATICUSDT,AVAXUSDT,DOTUSDT,LINKUSDT,UNIUSDT
ANALYSIS_INTERVAL=300
SIGNAL_THRESHOLD=0.7
```

### 4. Отримання API ключів

#### Binance API
1. Зайдіть на [Binance](https://www.binance.com)
2. Перейдіть в API Management
3. Створіть новий API ключ
4. Дозвольте тільки Spot Trading

#### OpenAI API
1. Зайдіть на [OpenAI](https://platform.openai.com)
2. Створіть API ключ
3. Додайте кошти на акаунт

#### Telegram Bot
1. Напишіть [@BotFather](https://t.me/botfather)
2. Створіть нового бота командою `/newbot`
3. Отримайте токен бота
4. Додайте бота в канал як адміністратора
5. Отримайте ID каналу (наприклад: `@your_channel` або `-1001234567890`)

## 🚀 Запуск

```bash
python main.py
```

## 📱 Використання

### Автоматичні сигнали
Бот автоматично:
- Аналізує ринок кожні 5 хвилин
- Збирає новини з різних джерел
- Консультується з ChatGPT
- Відправляє сигнали в Telegram канал

### Команди Telegram бота
- `/start` - Почати роботу з ботом
- `/status` - Статус бота
- `/analysis` - Поточний аналіз ринку
- `/news` - Останні новини
- `/help` - Допомога

## 📊 Структура сигналу

Кожен сигнал містить:
- **Рекомендацію** (BUY/SELL/HOLD)
- **Впевненість** (0-100%)
- **Рівень ризику** (LOW/MEDIUM/HIGH)
- **Розмір позиції** (відсоток від капіталу)
- **Ціни входу, Stop Loss, Take Profit**
- **Обґрунтування від ChatGPT**
- **Сентимент ринку**

## ⚙️ Налаштування

### Торгові пари
Змініть `TRADING_PAIRS` в `.env`:
```env
TRADING_PAIRS=BTCUSDT,ETHUSDT,BNBUSDT,ADAUSDT,SOLUSDT
```

### Інтервал аналізу
```env
ANALYSIS_INTERVAL=300  # секунди (5 хвилин)
```

### Поріг сигналу
```env
SIGNAL_THRESHOLD=0.7  # 70% впевненості
```

## 📈 Приклад сигналу

```
🟢 ТОРГОВИЙ СИГНАЛ: BTCUSDT

📊 РЕКОМЕНДАЦІЯ: BUY
🎯 ВПЕВНЕНІСТЬ: 85%
⚠️ РИЗИК: MEDIUM 🟡
💰 РОЗМІР ПОЗИЦІЇ: 15%

💵 ЦІНИ:
• Вхід: $43,250.00
• Stop Loss: $41,087.50
• Take Profit: $47,575.00

📈 ПОТЕНЦІАЛ:
• Ризик: 5.0%
• Прибуток: 10.0%

🧠 АНАЛІЗ ChatGPT:
Технічні індикатори показують сильний bullish сигнал...
```

## 🛡️ Безпека

- **Не торгуйте на реальні кошти** без тестування
- **Використовуйте демо-рахунки** для перевірки
- **Встановіть розумні ліміти** ризику
- **Моніторте роботу бота** регулярно

## 📝 Логи

Логи зберігаються в файлі `bot.log`:
```bash
tail -f bot.log
```

## 🔧 Розробка

### Структура проекту
```
├── main.py                 # Головний файл
├── config.py              # Конфігурація
├── binance_client.py      # Binance API
├── technical_analysis.py  # Технічний аналіз
├── news_aggregator.py     # Збір новин
├── chatgpt_analyzer.py    # ChatGPT інтеграція
├── telegram_bot.py        # Telegram бот
├── signal_processor.py    # Обробка сигналів
├── requirements.txt       # Залежності
└── README.md             # Документація
```

### Додавання нових індикаторів
Додайте нові індикатори в `technical_analysis.py`:

```python
def calculate_new_indicator(self, df):
    # Ваша логіка
    return indicator_values
```

### Додавання нових джерел новин
Додайте нові джерела в `news_aggregator.py`:

```python
self.news_sources['new_source'] = {
    'rss': 'https://example.com/rss',
    'base_url': 'https://example.com'
}
```

## ⚠️ Відмова від відповідальності

Цей бот призначений тільки для освітніх цілей. Торгівля криптовалютами пов'язана з високими ризиками. Автори не несуть відповідальності за втрати коштів.

## 📞 Підтримка

При виникненні проблем:
1. Перевірте логи в `bot.log`
2. Переконайтеся що всі API ключі налаштовані
3. Перевірте підключення до інтернету
4. Створіть issue в репозиторії

## 📄 Ліцензія

MIT License - дивіться файл LICENSE для деталей.
