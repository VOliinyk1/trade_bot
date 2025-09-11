@echo off
echo 🚀 Встановлення Crypto Trading Bot на Windows
echo ================================================

echo.
echo 🔧 Встановлення основних залежностей...
pip install fastapi==0.104.1
pip install uvicorn==0.24.0
pip install python-binance==1.0.19
pip install aiogram==3.2.0
pip install openai==1.3.7
pip install requests==2.31.0
pip install python-dotenv==1.0.0
pip install schedule==1.2.0
pip install beautifulsoup4==4.12.2
pip install feedparser==6.0.10
pip install aiohttp==3.9.1

echo.
echo 🔧 Встановлення numpy та pandas...
pip install numpy==1.24.4
pip install pandas==2.1.4
pip install ta==0.10.2

echo.
echo ✅ Встановлення завершено!
echo.
echo 📝 Наступні кроки:
echo 1. Налаштуйте .env файл з API ключами
echo 2. Запустіть тест: python test_bot.py
echo 3. Запустіть бота: python main.py
echo.
pause
