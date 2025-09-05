# Deploy to Vercel (Free Tier)
# Quick deployment for Flask apps

## Why Vercel?
- ✅ **FREE hobby tier** 
- ✅ **No credit card required**
- ✅ **Super fast deployment**
- ✅ **GitHub integration**

## Step-by-Step:

### 1. Create Vercel Configuration
Create `vercel.json` in your project:
```json
{
  "version": 2,
  "builds": [
    {
      "src": "./app.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "/"
    }
  ]
}
```

### 2. Update app.py for Vercel
Add this to the bottom of app.py:
```python
# For Vercel deployment
if __name__ != '__main__':
    # Production mode
    app.run(debug=False)
```

### 3. Deploy
1. Go to [vercel.com](https://vercel.com)
2. Sign up with GitHub
3. Click "New Project"
4. Import your `survey` repository
5. Vercel auto-deploys!

## Your URLs:
- Backend: `https://your-project-name.vercel.app`
- Stats: `https://your-project-name.vercel.app/stats`
