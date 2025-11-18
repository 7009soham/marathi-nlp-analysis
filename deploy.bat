@echo off
REM Marathi NLP Analysis - Quick Deployment Script for Windows

echo ========================================
echo 🚀 Marathi NLP Analysis - Deployment
echo ========================================
echo.

REM Check if Git is initialized
if not exist ".git" (
    echo 📦 Initializing Git repository...
    git init
    git add .
    git commit -m "Initial commit - Marathi NLP Analysis Tool"
    echo ✅ Git repository initialized
) else (
    echo ✅ Git repository already exists
)

echo.
echo Checking Git remote...
git remote | findstr "origin" > nul
if errorlevel 1 (
    echo.
    echo ⚠️  No Git remote found!
    echo Please add your GitHub repository:
    echo.
    echo   git remote add origin https://github.com/YOUR_USERNAME/marathi-nlp-analysis.git
    echo   git push -u origin main
    echo.
) else (
    echo ✅ Git remote configured
    echo.
    set /p push_choice="📤 Push to GitHub? (y/n): "
    if /i "%push_choice%"=="y" (
        echo Pushing to GitHub...
        git push -u origin main
        echo ✅ Pushed to GitHub
    )
)

echo.
echo ========================================
echo 📋 Deployment Options:
echo ========================================
echo.
echo 1️⃣  Streamlit Cloud (Recommended - FREE)
echo    → Go to: https://share.streamlit.io
echo    → Click 'New app'
echo    → Select your GitHub repo
echo    → Main file: app.py
echo    → Deploy!
echo.
echo 2️⃣  Docker (Local/Server)
echo    → docker-compose up
echo.
echo 3️⃣  Heroku
echo    → heroku create marathi-nlp-analysis
echo    → git push heroku main
echo.
echo ✅ Setup complete!
echo 📖 See DEPLOY.md for detailed instructions
echo.
pause
