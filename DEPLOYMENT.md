# Deployment Guide for RootSource AI

This guide provides step-by-step instructions for deploying your RootSource AI application to various cloud platforms.

## 🚀 Quick Deploy Options

### 1. Streamlit Community Cloud (FREE) ⭐ **RECOMMENDED**

**Prerequisites:**
- GitHub account
- Groq API key

**Steps:**

1. **Push your code to GitHub:**
   ```bash
   git add .
   git commit -m "Initial commit with deployment configs"
   git push origin main
   ```

2. **Deploy to Streamlit Cloud:**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Click "New app"
   - Choose "From existing repo"
   - Select your GitHub repository: `Rafi-uzzaman/RootSourceBot`
   - Set main file path: `app.py`
   - Click "Advanced settings"
   - Add secrets:
     ```
     GROQ_API_KEY = "your_actual_groq_api_key_here"
     ```
   - Click "Deploy!"

3. **Your app will be live at:** `https://your-app-name.streamlit.app`

### 2. Railway (FREE tier available)

1. **Connect to Railway:**
   - Go to [railway.app](https://railway.app)
   - Sign in with GitHub
   - Click "New Project" → "Deploy from GitHub repo"
   - Select your repository

2. **Configure environment variables:**
   - In your Railway dashboard, go to Variables
   - Add: `GROQ_API_KEY = your_actual_groq_api_key_here`

3. **Deploy:**
   - Railway will automatically build and deploy
   - Your app will be available at the provided URL

### 3. Render (FREE tier available)

1. **Connect to Render:**
   - Go to [render.com](https://render.com)
   - Sign in with GitHub
   - Click "New" → "Web Service"
   - Connect your repository

2. **Configure deployment:**
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `streamlit run app.py --server.port $PORT --server.address 0.0.0.0`

3. **Add environment variables:**
   - Add: `GROQ_API_KEY = your_actual_groq_api_key_here`

4. **Deploy:**
   - Click "Create Web Service"

### 4. Heroku (Paid plans)

1. **Install Heroku CLI and login:**
   ```bash
   heroku login
   ```

2. **Create Heroku app:**
   ```bash
   heroku create your-app-name
   ```

3. **Set environment variables:**
   ```bash
   heroku config:set GROQ_API_KEY=your_actual_groq_api_key_here
   ```

4. **Deploy:**
   ```bash
   git push heroku main
   ```

## 🔧 Pre-deployment Checklist

- [ ] **API Key Ready:** Have your Groq API key available
- [ ] **Code Committed:** All changes are committed to Git
- [ ] **Requirements Updated:** `requirements.txt` contains all dependencies
- [ ] **Environment Variables:** Know where to set `GROQ_API_KEY`
- [ ] **Test Locally:** App runs successfully with `streamlit run app.py`

## 🛠️ Troubleshooting

### Common Issues:

1. **"Module not found" errors:**
   - Ensure all packages are in `requirements.txt`
   - Check package names and versions

2. **API key errors:**
   - Verify `GROQ_API_KEY` is set correctly in your deployment platform
   - Ensure no quotes around the key value

3. **Port binding issues:**
   - Make sure your `Procfile` is configured correctly
   - For Heroku: `web: streamlit run app.py --server.port=$PORT --server.address=0.0.0.0`

4. **Build timeouts:**
   - Some platforms have build time limits
   - Consider using lighter dependencies if needed

### Getting Help:

- **Streamlit Community:** [discuss.streamlit.io](https://discuss.streamlit.io)
- **Platform-specific docs:**
  - [Streamlit deployment docs](https://docs.streamlit.io/streamlit-community-cloud)
  - [Railway docs](https://docs.railway.app)
  - [Render docs](https://render.com/docs)

## 🌟 Post-Deployment

Once deployed:

1. **Test your live app** - Make sure all features work
2. **Share the URL** - Your app is now publicly accessible
3. **Monitor usage** - Check your platform's analytics
4. **Update as needed** - Push changes to automatically redeploy

## 💡 Cost Comparison

| Platform | Free Tier | Pros | Cons |
|----------|-----------|------|------|
| **Streamlit Cloud** | Yes (unlimited) | Easy setup, Streamlit-optimized | Limited to Streamlit apps |
| **Railway** | 500 hours/month | Good free tier, easy setup | Time limit on free tier |
| **Render** | 750 hours/month | Generous free tier | Sleeps after inactivity |
| **Heroku** | No (paid only) | Reliable, mature platform | No free tier |

**Recommendation:** Start with **Streamlit Community Cloud** for the easiest free deployment!