# 🚀 Швидкий старт Crypto Trading Bot

## ⚡ Швидке встановлення (5 хвилин)

### 1. Встановлення

#### Windows (рекомендовано):
```cmd
# Клонуйте репозиторій
git clone <repository-url>
cd crypto-trading-bot

# Встановлення через batch файл
install_windows.bat

# АБО через PowerShell
powershell -ExecutionPolicy Bypass -File install_windows.ps1
```

#### Linux/Mac:
```bash
# Клонуйте репозиторій
git clone <repository-url>
cd crypto-trading-bot

# Автоматичне встановлення
python install.py
```

#### Якщо виникають проблеми з встановленням:
```cmd
# Встановлення по одній залежності
pip install fastapi uvicorn python-binance aiogram openai requests python-dotenv beautifulsoup4 feedparser aiohttp
pip install numpy pandas ta
```

### 2. Налаштування API ключів
Відредагуйте файл `.env`:

```env
# Binance API (обов'язково)
BINANCE_API_KEY=your_binance_api_key_here
BINANCE_API_SECRET=your_binance_api_secret_here

# OpenAI API (обов'язково)
OPENAI_API_KEY=your_openai_api_key_here

# Telegram Bot (обов'язково)
TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here
TELEGRAM_CHANNEL_ID=your_telegram_channel_id_here
```

### 3. Тестування
```bash
python test_bot.py
```

### 4. Запуск
```bash
python main.py
```

## 🔑 Отримання API ключів

### Binance API
1. Зайдіть на [binance.com](https://www.binance.com)
2. Account → API Management
3. Create API → Spot & Margin Trading
4. Скопіюйте API Key та Secret

### OpenAI API
1. Зайдіть на [platform.openai.com](https://platform.openai.com)
2. API Keys → Create new secret key
3. Додайте кошти на акаунт ($5-10)

### Telegram Bot
1. Напишіть [@BotFather](https://t.me/botfather)
2. `/newbot` → введіть назву бота
3. Скопіюйте токен
4. Створіть канал та додайте бота як адміністратора
5. Отримайте ID каналу (наприклад: `@your_channel`)

## 📊 Що робить бот

1. **Аналізує** 10+ торгових пар кожні 5 хвилин
2. **Збирає** новини з різних джерел
3. **Консультується** з ChatGPT для прийняття рішень
4. **Відправляє** сигнали в Telegram канал

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

🧠 АНАЛІЗ ChatGPT:
Технічні індикатори показують сильний bullish сигнал...
```

## ⚙️ Налаштування

### Зміна торгових пар
```env
TRADING_PAIRS=BTCUSDT,ETHUSDT,BNBUSDT,ADAUSDT,SOLUSDT
```

### Зміна інтервалу аналізу
```env
ANALYSIS_INTERVAL=300  # секунди (5 хвилин)
```

### Зміна порогу сигналу
```env
SIGNAL_THRESHOLD=0.7  # 70% впевненості
```

## 🐳 Docker (опціонально)

```bash
# Збірка
docker build -t crypto-bot .

# Запуск
docker run -d --env-file .env crypto-bot
```

## 📱 Команди Telegram бота

- `/start` - Почати роботу
- `/status` - Статус бота
- `/analysis` - Поточний аналіз
- `/news` - Останні новини
- `/help` - Допомога

## 🛡️ Безпека

- ⚠️ **НЕ торгуйте на реальні кошти** без тестування
- 🧪 Використовуйте демо-рахунки
- 📊 Встановіть розумні ліміти ризику
- 👀 Моніторте роботу бота

## 🔧 Вирішення проблем

### Помилка "API key not found"
- Перевірте файл `.env`
- Переконайтеся що API ключі правильні

### Помилка "ChatGPT timeout"
- Перевірте баланс OpenAI акаунту
- Переконайтеся що API ключ активний

### Помилка "Telegram bot not responding"
- Перевірте токен бота
- Переконайтеся що бот доданий в канал

## 📞 Підтримка

При проблемах:
1. Перевірте логи в `bot.log`
2. Запустіть `python test_bot.py`
3. Створіть issue в репозиторії

## 🎯 Готово!

Ваш бот готовий до роботи! 🚀

**Наступні кроки:**
1. Налаштуйте API ключі
2. Запустіть тест
3. Запустіть бота
4. Отримуйте сигнали в Telegram! 📱
