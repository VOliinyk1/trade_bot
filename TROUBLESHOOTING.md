# 🔧 Вирішення проблем Crypto Trading Bot

## 🚨 Проблеми з встановленням залежностей

### Проблема: "Unknown compiler" або "Failed to activate VS environment"

**Причина:** Відсутність компілятора C++ на Windows

**Рішення 1 (Рекомендоване):**
```cmd
# Використовуйте готові скрипти
install_windows.bat

# АБО PowerShell
powershell -ExecutionPolicy Bypass -File install_windows.ps1
```

**Рішення 2:**
```cmd
# Встановлення по одній залежності
pip install fastapi uvicorn python-binance aiogram openai requests python-dotenv beautifulsoup4 feedparser aiohttp
pip install numpy pandas ta
```

**Рішення 3:**
```cmd
# Встановлення Visual Studio Build Tools
# Завантажте з: https://visualstudio.microsoft.com/visual-cpp-build-tools/
# Встановіть "C++ build tools"
# Перезапустіть командний рядок
pip install -r requirements.txt
```

### Проблема: "No module named 'pandas'"

**Рішення:**
```cmd
# Встановіть pandas окремо
pip install pandas==2.1.4
pip install numpy==1.24.4
```

### Проблема: "Permission denied" на Windows

**Рішення:**
```cmd
# Запустіть командний рядок як адміністратор
# АБО використовуйте --user
pip install --user -r requirements.txt
```

## 🔑 Проблеми з API ключами

### Проблема: "API key not found"

**Перевірте .env файл:**
```env
BINANCE_API_KEY=your_actual_api_key_here
BINANCE_API_SECRET=your_actual_secret_here
OPENAI_API_KEY=your_actual_openai_key_here
TELEGRAM_BOT_TOKEN=your_actual_bot_token_here
TELEGRAM_CHANNEL_ID=your_actual_channel_id_here
```

**Важливо:**
- Не використовуйте `your_*_here` - це заглушки
- Не додавайте пробіли навколо `=`
- Не додавайте лапки навколо значень

### Проблема: "Invalid API key"

**Для Binance:**
1. Перевірте що API ключ активний
2. Переконайтеся що дозволено Spot Trading
3. Перевірте IP обмеження

**Для OpenAI:**
1. Перевірте баланс акаунту
2. Переконайтеся що API ключ не застарів
3. Перевірте ліміти використання

**Для Telegram:**
1. Перевірте що бот створений через @BotFather
2. Переконайтеся що бот доданий в канал як адміністратор
3. Перевірте ID каналу (має починатися з @ або -)

## 🤖 Проблеми з Telegram ботом

### Проблема: "Bot was blocked by the user"

**Рішення:**
1. Розблокуйте бота в Telegram
2. Перезапустіть бота
3. Перевірте токен бота

### Проблема: "Chat not found"

**Рішення:**
1. Перевірте ID каналу в .env
2. Переконайтеся що бот доданий в канал
3. Перевірте права бота в каналі

## 📊 Проблеми з аналізом

### Проблема: "No data received from Binance"

**Рішення:**
1. Перевірте підключення до інтернету
2. Перевірте API ключі Binance
3. Перевірте що символ існує на Binance

### Проблема: "ChatGPT timeout"

**Рішення:**
1. Перевірте баланс OpenAI акаунту
2. Перевірте API ключ
3. Спробуйте пізніше (може бути перевантаження)

## 🐍 Проблеми з Python

### Проблема: "Python not found"

**Рішення:**
1. Встановіть Python 3.8+ з python.org
2. Переконайтеся що Python додано в PATH
3. Перезапустіть командний рядок

### Проблема: "pip not found"

**Рішення:**
```cmd
# Встановіть pip
python -m ensurepip --upgrade

# АБО завантажте get-pip.py
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python get-pip.py
```

## 🔍 Діагностика

### Запустіть простий тест:
```cmd
python test_simple.py
```

### Перевірте версії:
```cmd
python --version
pip --version
```

### Перевірте встановлені пакети:
```cmd
pip list
```

## 📞 Отримання допомоги

### Логи:
- Перевірте файл `bot.log`
- Запустіть з `python main.py` для детальних логів

### Тестування:
```cmd
# Простий тест
python test_simple.py

# Повний тест (після встановлення залежностей)
python test_bot.py
```

### Створення issue:
1. Опишіть проблему
2. Додайте логи
3. Вкажіть версію Python та ОС
4. Додайте кроки для відтворення

## 🎯 Швидкі рішення

### Повне перевстановлення:
```cmd
# Видаліть віртуальне середовище
rmdir /s venv

# Створіть нове
python -m venv venv
venv\Scripts\activate

# Встановіть залежності
pip install -r requirements.txt
```

### Альтернативне встановлення:
```cmd
# Використовуйте conda замість pip
conda install pandas numpy
pip install -r requirements.txt
```

### Docker (якщо все інше не працює):
```cmd
docker build -t crypto-bot .
docker run -d --env-file .env crypto-bot
```
