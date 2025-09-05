# 🚀 Complete Backend Hosting Guide

## Your Flask Backend Needs to be Hosted Online

I've created everything you need for deployment. Here are your **best hosting options**:

## 🏆 Option 1: Render (RECOMMENDED - FREE)

### ✅ Why Render?
- **FREE tier** with always-on hosting
- **Easy deployment** from GitHub
- **Automatic HTTPS**
- **No credit card required**
- **Great for beginners**

### 📋 Step-by-Step Deployment:

#### 1. Push to GitHub (if not already done):
```bash
cd /Users/rahoolk/raw/survey
git add .
git commit -m "Add Flask backend for unlimited survey responses"
git push origin main
```

#### 2. Deploy on Render:
1. Go to [render.com](https://render.com)
2. Sign up with your GitHub account
3. Click "New" → "Web Service"
4. Connect your `survey` repository
5. Configure deployment:
   - **Name**: `wisdom-survey-backend` (or any name you like)
   - **Region**: Choose closest to your users
   - **Branch**: `main`
   - **Root Directory**: Leave blank
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`

#### 3. Set Environment Variables (Optional - for email):
In Render dashboard → Environment tab, add:
- `SENDER_EMAIL`: your-email@gmail.com
- `SENDER_PASSWORD`: your-gmail-app-password
- `RECIPIENT_EMAIL`: where-to-receive-notifications@gmail.com

#### 4. Deploy:
- Click "Create Web Service"
- Wait 2-3 minutes for deployment
- You'll get a URL like: `https://wisdom-survey-backend.onrender.com`

#### 5. Update Your HTML:
Replace this line in `wisdom_questionnaire.html`:
```javascript
const BACKEND_URL = 'https://your-app-name.onrender.com';
```
With your actual Render URL:
```javascript
const BACKEND_URL = 'https://wisdom-survey-backend.onrender.com';
```

## 💡 Option 2: Railway (SIMPLE & FAST)

### Cost: $5/month for unlimited usage

#### Deployment Steps:
1. Go to [railway.app](https://railway.app)
2. Sign up with GitHub
3. Click "Deploy from GitHub repo"
4. Select your `survey` repository
5. Railway auto-detects Python and deploys!
6. Get your URL and update HTML

## 🔧 Option 3: PythonAnywhere (PYTHON-FOCUSED)

### Cost: FREE tier (limited) or $5/month

#### Deployment Steps:
1. Go to [pythonanywhere.com](https://pythonanywhere.com)
2. Sign up for free account
3. Upload your files via dashboard
4. Configure web app in Web tab
5. Set WSGI file to point to your `app.py`

## 🔄 Option 4: Heroku (TRADITIONAL)

### Cost: $7/month (no free tier anymore)

#### Files Already Created:
- ✅ `Procfile` - Tells Heroku how to run your app
- ✅ `runtime.txt` - Specifies Python version
- ✅ `requirements.txt` - Lists dependencies

#### Deployment:
1. Install [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli)
2. Run commands:
```bash
heroku login
heroku create your-survey-app
git push heroku main
```

## 📁 Files I've Created for Deployment:

- ✅ **`app.py`** - Production-ready Flask backend
- ✅ **`requirements.txt`** - All dependencies
- ✅ **`Procfile`** - For Heroku deployment
- ✅ **`runtime.txt`** - Python version specification
- ✅ **Updated HTML** - Ready to connect to hosted backend

## 🎯 Recommended Workflow:

### For Research/Academic Use:
1. **Use Render (FREE)** - Perfect for academic research
2. **Deploy in 5 minutes** 
3. **Get unlimited responses**
4. **Share survey link** globally

### For Professional Use:
1. **Use Railway ($5/month)** - More reliable
2. **Better performance** 
3. **Professional support**

## 🚀 Quick Start (Render):
1. Push code to GitHub
2. Connect to Render
3. Deploy (takes 3 minutes)
4. Update HTML with your URL
5. Share survey and collect unlimited responses!

## 📊 After Deployment:
- **Survey URL**: Your HTML file (can host on GitHub Pages)
- **Backend URL**: Your Render/Railway URL
- **Data Dashboard**: `your-backend-url.com/stats`
- **Download Data**: `your-backend-url.com/download_csv`

## 🔧 Testing Your Deployment:
1. Visit `your-backend-url.com` - Should show API status
2. Visit `your-backend-url.com/stats` - Should show "0 responses"
3. Submit a test survey response
4. Check `/stats` again - Should show 1 response!

**Ready to deploy? I recommend starting with Render (free) - it's the easiest option!**
