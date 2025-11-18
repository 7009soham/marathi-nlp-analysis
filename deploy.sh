#!/bin/bash

# Marathi NLP Analysis - Quick Deployment Script
echo "🚀 Marathi NLP Analysis - Deployment Setup"
echo "=========================================="

# Check if Git is initialized
if [ ! -d ".git" ]; then
    echo "📦 Initializing Git repository..."
    git init
    git add .
    git commit -m "Initial commit - Marathi NLP Analysis Tool"
    echo "✅ Git repository initialized"
else
    echo "✅ Git repository already exists"
fi

# Check for remote
if ! git remote | grep -q 'origin'; then
    echo ""
    echo "⚠️  No Git remote found!"
    echo "Please add your GitHub repository:"
    echo ""
    echo "  git remote add origin https://github.com/YOUR_USERNAME/marathi-nlp-analysis.git"
    echo "  git push -u origin main"
    echo ""
else
    echo "✅ Git remote configured"
    
    # Ask if user wants to push
    read -p "📤 Push to GitHub? (y/n): " push_choice
    if [ "$push_choice" = "y" ]; then
        echo "Pushing to GitHub..."
        git push -u origin main
        echo "✅ Pushed to GitHub"
    fi
fi

echo ""
echo "📋 Deployment Options:"
echo ""
echo "1️⃣  Streamlit Cloud (Recommended - FREE)"
echo "   → Go to: https://share.streamlit.io"
echo "   → Click 'New app'"
echo "   → Select your GitHub repo"
echo "   → Main file: app.py"
echo "   → Deploy!"
echo ""
echo "2️⃣  Docker (Local/Server)"
echo "   → docker-compose up"
echo ""
echo "3️⃣  Heroku"
echo "   → heroku create marathi-nlp-analysis"
echo "   → git push heroku main"
echo ""
echo "✅ Setup complete!"
echo "📖 See DEPLOY.md for detailed instructions"
