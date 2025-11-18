# 🚀 Quick Start Guide

## Deploy in 3 Steps

### Option 1: Streamlit Cloud (Easiest - FREE) ⭐

1. **Push to GitHub**
   ```bash
   # Windows
   deploy.bat
   
   # Linux/Mac
   chmod +x deploy.sh
   ./deploy.sh
   ```

2. **Go to Streamlit Cloud**
   - Visit: https://share.streamlit.io
   - Sign in with GitHub
   - Click "New app"

3. **Configure & Deploy**
   - Repository: `YOUR_USERNAME/marathi-nlp-analysis`
   - Branch: `main`
   - Main file path: `app.py`
   - Click "Deploy!"
   
   **Done!** Your app will be live in 2-3 minutes at:
   `https://YOUR_USERNAME-marathi-nlp-analysis.streamlit.app`

---

### Option 2: Docker (Local/Server)

```bash
# Build and run
docker-compose up

# Access at: http://localhost:8501
```

---

### Option 3: Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Run app
streamlit run app.py

# Access at: http://localhost:8501
```

---

## ✅ Pre-Deployment Checklist

Before deploying, ensure:

- [ ] All CSV files present (sentiment_lexicon.csv, emotion_lexicon.csv, etc.)
- [ ] Model files present (lda_model.joblib, count_vocab.json, tfidf_vocab.json)
- [ ] requirements.txt complete
- [ ] .gitignore configured (excludes .venv/, __pycache__/)
- [ ] Git repository initialized
- [ ] GitHub repository created

---

## 🎯 What Gets Deployed

### Essential Files
```
app.py                      # Main Streamlit app
marathi_nlp_core.py        # Core NLP functions
semantic_analysis.py        # Semantic analysis module
requirements.txt           # Python dependencies
.streamlit/config.toml     # Streamlit configuration

Models & Vocabularies:
├── lda_model.joblib       # ~50MB
├── count_vocab.json       # ~200KB
└── tfidf_vocab.json       # ~300KB

Lexicons (all CSV files):
├── sentiment_lexicon.csv  # 215 words
├── emotion_lexicon.csv    # 300+ words
├── marathi_stopwords.csv  # 1000+ stopwords
├── marathi_entities.csv   # 1000+ entities
└── marathi_symbols.csv    # Symbols
```

### Excluded from Git (via .gitignore)
- `.venv/` - Virtual environment (too large)
- `__pycache__/` - Python cache files
- `marathi_dataset_real_12000.csv` - Training data (not needed in production)
- `.ipynb_checkpoints/` - Jupyter temp files

---

## 🔧 Configuration

### Streamlit Cloud Settings
- **Python version**: 3.11 (auto-detected)
- **Resources**: 1GB RAM, 2 CPU cores (free tier)
- **Auto-deploy**: Enabled (pushes to `main` auto-deploy)
- **Secrets**: None needed for this app

### Custom Domain (Optional)
1. Go to App Settings → General
2. Add custom domain
3. Update DNS CNAME record

---

## 📊 Expected Performance

| Metric | Value |
|--------|-------|
| Cold start | 15-20 seconds |
| Warm start | 2-3 seconds |
| Analysis time | <1 second |
| Memory usage | ~300MB |
| Concurrent users | 10-20 (free tier) |

---

## 🐛 Troubleshooting

### Deployment fails
**Check logs** in Streamlit Cloud → Manage app → Logs

Common issues:
- Missing CSV files → Ensure all lexicons committed
- Import errors → Check requirements.txt
- Model not loading → Verify .joblib file < 100MB

### App is slow
- Use `@st.cache_resource` for model loading (already implemented)
- Reduce demo sentences if needed
- Upgrade to paid tier for more resources

### Fonts not rendering
- Devanagari should work out-of-box
- If issues persist, install Noto Sans Devanagari font

---

## 📈 Monitoring

### Streamlit Cloud Dashboard
- View analytics: Daily active users, page views
- Check logs: Real-time error monitoring
- Usage limits: Track towards free tier limits

### Custom Analytics (Optional)
Add Google Analytics or Plausible:
```python
# In app.py
st.components.v1.html("""
<script async src="https://www.googletagmanager.com/gtag/js?id=YOUR_GA_ID"></script>
""")
```

---

## 🎉 Post-Deployment

### Share Your App
1. Test all features work
2. Get feedback from users
3. Share URL on:
   - Social media
   - GitHub README
   - Academic papers/presentations

### Iterate
1. Monitor usage patterns
2. Add requested features
3. Fix bugs reported by users
4. Push updates to `main` branch (auto-deploys)

---

## 💰 Upgrade Options

| Need | Solution | Cost |
|------|----------|------|
| More users | Streamlit Cloud Teams | $250/month |
| Custom branding | Remove Streamlit footer | Teams plan |
| Faster performance | Dedicated resources | Teams plan |
| Private apps | Private deployment | Teams/Enterprise |

**Recommendation**: Start with free tier, upgrade when you hit limits.

---

## 📞 Support

- **Streamlit Docs**: https://docs.streamlit.io
- **Community Forum**: https://discuss.streamlit.io
- **This Project**: See DEPLOY.md for detailed guide

---

**Ready to deploy? Run `deploy.bat` (Windows) or `./deploy.sh` (Linux/Mac)!** 🚀
