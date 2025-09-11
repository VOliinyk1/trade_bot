# PowerShell скрипт для встановлення Crypto Trading Bot на Windows

Write-Host "🚀 Встановлення Crypto Trading Bot на Windows" -ForegroundColor Green
Write-Host "================================================" -ForegroundColor Green

Write-Host ""
Write-Host "🔧 Встановлення основних залежностей..." -ForegroundColor Yellow

$packages = @(
    "fastapi==0.104.1",
    "uvicorn==0.24.0",
    "python-binance==1.0.19",
    "aiogram==3.2.0",
    "openai==1.3.7",
    "requests==2.31.0",
    "python-dotenv==1.0.0",
    "schedule==1.2.0",
    "beautifulsoup4==4.12.2",
    "feedparser==6.0.10",
    "aiohttp==3.9.1"
)

foreach ($package in $packages) {
    Write-Host "📦 Встановлення $package..." -ForegroundColor Cyan
    pip install $package
    if ($LASTEXITCODE -ne 0) {
        Write-Host "⚠️ Помилка встановлення $package" -ForegroundColor Red
    }
}

Write-Host ""
Write-Host "🔧 Встановлення numpy та pandas..." -ForegroundColor Yellow

$mathPackages = @(
    "numpy==1.24.4",
    "pandas==2.1.4",
    "ta==0.10.2"
)

foreach ($package in $mathPackages) {
    Write-Host "📦 Встановлення $package..." -ForegroundColor Cyan
    pip install $package
    if ($LASTEXITCODE -ne 0) {
        Write-Host "⚠️ Помилка встановлення $package" -ForegroundColor Red
    }
}

Write-Host ""
Write-Host "✅ Встановлення завершено!" -ForegroundColor Green
Write-Host ""
Write-Host "📝 Наступні кроки:" -ForegroundColor Yellow
Write-Host "1. Налаштуйте .env файл з API ключами" -ForegroundColor White
Write-Host "2. Запустіть тест: python test_bot.py" -ForegroundColor White
Write-Host "3. Запустіть бота: python main.py" -ForegroundColor White
Write-Host ""
Write-Host "Натисніть будь-яку клавішу для продовження..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
