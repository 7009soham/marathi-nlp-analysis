# 🚀 Deployment Guide - Marathi NLP Analysis Tool

## Quick Deploy to Streamlit Cloud (Recommended)

### Step 1: Prepare Repository

1. **Initialize Git** (if not done)
```bash
git init
git add .
git commit -m "Initial commit - Marathi NLP Analysis Tool"
```

2. **Create GitHub Repository**
   - Go to [github.com](https://github.com) and create a new repository
   - Name it: `marathi-nlp-analysis` (or your preferred name)
   - Keep it public for free Streamlit Cloud hosting

3. **Push to GitHub**
```bash
git remote add origin https://github.com/YOUR_USERNAME/marathi-nlp-analysis.git
git branch -M main
git push -u origin main
```

### Step 2: Deploy on Streamlit Cloud

1. **Sign up** at [share.streamlit.io](https://share.streamlit.io)
   - Use your GitHub account (recommended)
   - Free tier: Unlimited public apps

2. **Create New App**
   - Click "New app" button
   - Select your repository: `YOUR_USERNAME/marathi-nlp-analysis`
   - Main file path: `app.py`
   - Branch: `main`
   - Advanced settings (optional):
     - Python version: 3.11
     - Keep defaults for everything else

3. **Deploy**
   - Click "Deploy!" button
   - Wait 2-4 minutes for initial deployment
   - Your app will be live at: `https://YOUR_USERNAME-marathi-nlp-analysis.streamlit.app`

### Step 3: Verify Deployment

✅ Check that all features work:
- Tokenization with Marathi-only filtering
- Sentiment analysis with modifiers
- Emotion detection (including complex emotions like grief)
- All visualizations render correctly
- User/Learner mode toggle
- 105 demo sentences load properly

---

## Alternative: Deploy to Heroku

### Prerequisites
- Heroku account ([signup.heroku.com](https://signup.heroku.com))
- Heroku CLI installed

### Files Needed

Create `Procfile`:
```
web: streamlit run app.py --server.port=$PORT --server.address=0.0.0.0
```

Create `setup.sh`:
```bash
mkdir -p ~/.streamlit/
echo "\
[server]\n\
headless = true\n\
port = $PORT\n\
enableCORS = false\n\
\n\
" > ~/.streamlit/config.toml
```

### Deploy Commands

```bash
# Login to Heroku
heroku login

# Create app
heroku create marathi-nlp-analysis

# Set buildpack
heroku buildpacks:set heroku/python

# Deploy
git push heroku main

# Open app
heroku open
```

---

## Alternative: Deploy to AWS EC2

### 1. Launch EC2 Instance
- Ubuntu 22.04 LTS
- t2.medium (2 vCPU, 4GB RAM recommended)
- Security group: Allow inbound on port 8501

### 2. SSH and Setup

```bash
# Connect to instance
ssh -i your-key.pem ubuntu@your-ec2-ip

# Update system
sudo apt update && sudo apt upgrade -y

# Install Python
sudo apt install python3.11 python3.11-venv python3-pip -y

# Clone repository
git clone https://github.com/YOUR_USERNAME/marathi-nlp-analysis.git
cd marathi-nlp-analysis

# Create virtual environment
python3.11 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run app
streamlit run app.py --server.port=8501 --server.address=0.0.0.0
```

### 3. Keep Running (use PM2 or systemd)

```bash
# Install PM2
sudo npm install -g pm2

# Start app with PM2
pm2 start "streamlit run app.py --server.port=8501 --server.address=0.0.0.0" --name marathi-nlp

# Save PM2 config
pm2 save
pm2 startup
```

Access at: `http://your-ec2-ip:8501`

---

## Alternative: Docker Deployment

### Create Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Expose Streamlit port
EXPOSE 8501

# Run app
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

### Build and Run

```bash
# Build image
docker build -t marathi-nlp-analysis .

# Run container
docker run -p 8501:8501 marathi-nlp-analysis

# Or with Docker Compose
docker-compose up
```

### docker-compose.yml

```yaml
version: '3.8'
services:
  app:
    build: .
    ports:
      - "8501:8501"
    environment:
      - STREAMLIT_SERVER_PORT=8501
    restart: unless-stopped
```

---

## Post-Deployment Checklist

✅ **Functionality**
- [ ] All 105 demo sentences load
- [ ] Marathi-only tokenization works
- [ ] Sentiment analysis accurate
- [ ] Emotion detection includes grief/complex emotions
- [ ] User/Learner mode toggle works
- [ ] All visualizations render

✅ **Performance**
- [ ] Page loads in <5 seconds
- [ ] Analysis completes in <2 seconds
- [ ] No memory leaks after multiple analyses

✅ **UI/UX**
- [ ] Responsive on mobile
- [ ] Devanagari fonts render correctly
- [ ] Colors/theme look professional
- [ ] Code blocks formatted properly in Learner mode

✅ **Data**
- [ ] All CSV files committed to repo
- [ ] Model files (lda_model.joblib) under 100MB
- [ ] Vocabulary JSONs present

---

## Monitoring & Maintenance

### Streamlit Cloud
- View logs: App → Manage app → Logs
- Restart: App → Manage app → Reboot
- Update: Push to GitHub, auto-redeploys

### Custom Server
- Check logs: `tail -f /var/log/streamlit.log`
- Monitor: `htop` or `pm2 monit`
- Update: `git pull && pm2 restart marathi-nlp`

---

## Troubleshooting

### Issue: App crashes on startup
**Solution**: Check requirements.txt has all dependencies with correct versions

### Issue: Models not loading
**Solution**: Ensure all .joblib and .json files are committed to Git

### Issue: Out of memory
**Solution**: Use smaller instance or optimize model loading (lazy load)

### Issue: Slow performance
**Solution**: 
- Cache model loading with `@st.cache_resource`
- Use smaller LDA model
- Reduce demo sentence count

---

## Cost Estimates

| Platform | Tier | Cost | Performance |
|----------|------|------|-------------|
| **Streamlit Cloud** | Free | $0/month | ⭐⭐⭐ Good |
| Streamlit Cloud | Teams | $250/month | ⭐⭐⭐⭐ Better |
| Heroku | Hobby | $7/month | ⭐⭐⭐ Good |
| AWS EC2 | t2.medium | ~$30/month | ⭐⭐⭐⭐ Better |
| DigitalOcean | Basic Droplet | $12/month | ⭐⭐⭐ Good |

**Recommendation**: Start with **Streamlit Cloud Free** tier for MVPs and demos.

---

## 🎉 Your App is Live!

Share your URL:
- Streamlit Cloud: `https://YOUR_USERNAME-marathi-nlp-analysis.streamlit.app`
- Custom domain: Configure via Streamlit settings or DNS

**Next Steps:**
1. Share with users for feedback
2. Monitor usage analytics
3. Iterate based on user behavior
4. Consider paid tier if traffic grows
