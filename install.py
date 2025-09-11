#!/usr/bin/env python3
"""
Скрипт встановлення Crypto Trading Bot
"""

import os
import sys
import subprocess
from pathlib import Path

def run_command(command, description):
    """Виконати команду з описом"""
    print(f"🔧 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} завершено")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Помилка {description}: {e}")
        print(f"   Вивід: {e.stderr}")
        return False

def check_python_version():
    """Перевірити версію Python"""
    print("🐍 Перевірка версії Python...")
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print(f"❌ Потрібен Python 3.8+, поточна версія: {version.major}.{version.minor}")
        return False
    print(f"✅ Python {version.major}.{version.minor}.{version.micro}")
    return True

def install_requirements():
    """Встановити залежності"""
    if not Path("requirements.txt").exists():
        print("❌ Файл requirements.txt не знайдено")
        return False
    
    # Спочатку пробуємо основні залежності
    print("🔧 Встановлення основних залежностей...")
    if run_command("pip install -r requirements.txt", "Встановлення залежностей"):
        return True
    
    # Якщо не вдалося, пробуємо Windows-оптимізовані
    print("⚠️ Основні залежності не встановилися, пробуємо Windows-версію...")
    if Path("requirements-windows.txt").exists():
        if run_command("pip install -r requirements-windows.txt", "Встановлення Windows-залежностей"):
            return True
    
    # Якщо і це не спрацювало, встановлюємо по одній
    print("⚠️ Пробуємо встановити залежності по одній...")
    basic_packages = [
        "fastapi==0.104.1",
        "uvicorn==0.24.0", 
        "python-binance==1.0.19",
        "aiogram==3.2.0",
        "openai==1.3.7",
        "requests==2.31.0",
        "python-dotenv==1.0.0",
        "beautifulsoup4==4.12.2",
        "feedparser==6.0.10",
        "aiohttp==3.9.1"
    ]
    
    for package in basic_packages:
        if not run_command(f"pip install {package}", f"Встановлення {package.split('==')[0]}"):
            print(f"⚠️ Не вдалося встановити {package}, продовжуємо...")
    
    # Спробуємо встановити numpy та pandas окремо
    print("🔧 Встановлення numpy та pandas...")
    run_command("pip install numpy==1.24.4", "Встановлення numpy")
    run_command("pip install pandas==2.1.4", "Встановлення pandas")
    run_command("pip install ta==0.10.2", "Встановлення ta")
    
    return True

def create_env_file():
    """Створити .env файл"""
    print("📝 Створення .env файлу...")
    
    if Path(".env").exists():
        print("✅ Файл .env вже існує")
        return True
    
    if not Path("env.example").exists():
        print("❌ Файл env.example не знайдено")
        return False
    
    try:
        # Копіюємо env.example в .env
        with open("env.example", "r", encoding="utf-8") as src:
            content = src.read()
        
        with open(".env", "w", encoding="utf-8") as dst:
            dst.write(content)
        
        print("✅ Файл .env створено")
        print("⚠️ Не забудьте налаштувати API ключі в .env файлі!")
        return True
        
    except Exception as e:
        print(f"❌ Помилка створення .env файлу: {e}")
        return False

def create_directories():
    """Створити необхідні директорії"""
    print("📁 Створення директорій...")
    
    directories = ["logs", "data", "cache"]
    
    for directory in directories:
        try:
            Path(directory).mkdir(exist_ok=True)
            print(f"✅ Директорія {directory} створена")
        except Exception as e:
            print(f"❌ Помилка створення директорії {directory}: {e}")
            return False
    
    return True

def test_installation():
    """Тестувати встановлення"""
    print("🧪 Тестування встановлення...")
    
    try:
        # Перевіряємо імпорт основних модулів
        import pandas
        import numpy
        import ta
        import openai
        import aiogram
        from binance.client import Client
        
        print("✅ Всі модулі успішно імпортовані")
        return True
        
    except ImportError as e:
        print(f"❌ Помилка імпорту модуля: {e}")
        return False

def main():
    """Головна функція встановлення"""
    print("🚀 Встановлення Crypto Trading Bot")
    print("=" * 40)
    
    steps = [
        ("Перевірка Python", check_python_version),
        ("Створення директорій", create_directories),
        ("Встановлення залежностей", install_requirements),
        ("Створення .env файлу", create_env_file),
        ("Тестування встановлення", test_installation)
    ]
    
    failed_steps = []
    
    for step_name, step_func in steps:
        print(f"\n📋 {step_name}...")
        if not step_func():
            failed_steps.append(step_name)
    
    print("\n" + "=" * 40)
    print("📊 ПІДСУМОК ВСТАНОВЛЕННЯ:")
    
    if not failed_steps:
        print("🎉 Встановлення завершено успішно!")
        print("\n📝 Наступні кроки:")
        print("1. Налаштуйте API ключі в .env файлі")
        print("2. Запустіть тест: python test_bot.py")
        print("3. Запустіть бота: python main.py")
    else:
        print("❌ Встановлення завершено з помилками:")
        for step in failed_steps:
            print(f"   - {step}")
        print("\n🔧 Виправте помилки та запустіть встановлення знову")
        sys.exit(1)

if __name__ == "__main__":
    main()
