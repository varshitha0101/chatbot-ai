# Railway.app Deployment Guide - CBT Chatbot

Complete step-by-step guide to deploy your chatbot on Railway.app for free.

## 📋 Prerequisites

- GitHub account (with your chatbot code pushed)
- Google Gemini API key (from https://aistudio.google.com/app/apikey)
- 10 minutes of setup time

## 🚀 Step 1: Create Railway Account

1. Go to https://railway.app
2. Click **"Start Project"**
3. Choose **"Deploy from GitHub"**
4. Authorize Railway to access your GitHub
5. Select your `chatbot-ai` repository

## 📦 Step 2: Configure Environment Variables

Once your repo is connected:

1. Click **"Add Variable"** in Railway dashboard
2. Add these variables:

```
SECRET_KEY = [generate random: python -c "import secrets; print(secrets.token_urlsafe(32))"]
JWT_SECRET_KEY = [generate random: python -c "import secrets; print(secrets.token_urlsafe(32))"]
GEMINI_API_KEY = [your key from https://aistudio.google.com/app/apikey]
FLASK_ENV = production
FLASK_DEBUG = false
API_BASE_URL = https://YOUR_RAILWAY_URL.railway.app
FRONTEND_URL = https://YOUR_RAILWAY_URL.railway.app
CORS_ORIGINS = https://YOUR_RAILWAY_URL.railway.app
DATABASE_TYPE = sqlite
LOG_LEVEL = INFO
```

**Note:** You'll get the Railway URL after first deployment (see Step 3)

## 🔧 Step 3: Add railway.json (Optional but Recommended)

Create a `railway.json` file in your project root:

```json
{
  "build": {
    "builder": "dockerfile"
  },
  "deploy": {
    "startCommand": "gunicorn -c gunicorn_config.py wsgi:app",
    "restartPolicyMaxRetries": 5,
    "restartPolicyWindow": 600
  }
}
```

OR update in Railway UI:
- **Build Command:** `pip install -r requirements.txt`
- **Start Command:** `gunicorn -c gunicorn_config.py wsgi:app`

## 🚀 Step 4: Deploy

1. Go back to Railway dashboard
2. Click **"Deploy"** button
3. Watch the logs - should see:
   ```
   Building Docker image...
   Deploying...
   Application is running!
   ```

**Deployment time:** 2-5 minutes

## 🔍 Step 5: Get Your Public URL

After deployment completes:

1. In Railway dashboard, click **"Domains"**
2. Copy the generated URL (looks like: `https://chatbot-xxx.railway.app`)
3. Update your environment variables:
   - `API_BASE_URL = https://chatbot-xxx.railway.app`
   - `FRONTEND_URL = https://chatbot-xxx.railway.app`
   - `CORS_ORIGINS = https://chatbot-xxx.railway.app`

4. Redeploy by pushing a small change to GitHub or clicking **"Redeploy"**

## ✅ Step 6: Verify It's Working

```bash
# Check health endpoint
curl https://YOUR_RAILWAY_URL.railway.app/health

# Should return:
# {
#   "message": "CBT Chatbot API is running",
#   "ai_powered": true,
#   "ai_status": "enabled"
# }
```

Or visit in browser: `https://YOUR_RAILWAY_URL.railway.app`

## 🔄 Step 7: Connect Database (Optional)

Railway includes PostgreSQL. To enable:

1. In Railway dashboard, click **"New Service"**
2. Select **"Database"** → **"PostgreSQL"**
3. Add these to your environment variables:
   ```
   DATABASE_TYPE = postgresql
   DATABASE_URL = ${{Postgres.DATABASE_URL}}
   ```
4. Redeploy

## 📝 Database Connection String Format

If using PostgreSQL:
```
postgresql://username:password@host:port/dbname
```

Railway provides this automatically as `${{Postgres.DATABASE_URL}}`

## 🔐 Security Notes

- ✅ All secrets are in environment variables (not in code)
- ✅ HTTPS automatic (Railway provides SSL)
- ✅ Firewall protection included
- ✅ Free tier includes DDoS protection

## 📊 Monitor Your App

In Railway dashboard:
- **Logs:** View real-time application logs
- **Metrics:** CPU, memory, requests
- **Deployments:** History of all deployments

To view logs:
```bash
# Show last 100 lines
railway logs -n 100

# Follow in real-time
railway logs -f
```

## 🐛 Troubleshooting

### App won't start - "Port already in use"
Railway automatically assigns PORT environment variable. Update `gunicorn_config.py`:
```python
bind = os.environ.get('PORT', '5000')
```

### Database permission denied
Solution: Use Railway's PostgreSQL database (see Step 7)

### API returning 404
- Check your `API_BASE_URL` is correct
- Verify `CORS_ORIGINS` includes your domain
- Redeploy after changing variables

### "No module named 'backend'"
Fix: Update `wsgi.py` to use correct import paths for Railway

### CORS errors in frontend
Update CORS_ORIGINS to include your Railway URL:
```
CORS_ORIGINS=https://your-chatbot-xxx.railway.app
```

## 💰 Free Tier Limits

- **Monthly credit:** $5 (usually 2-3 months of usage)
- **CPU:** Shared
- **Memory:** 512MB - 1GB
- **Storage:** 1GB
- **Bandwidth:** Limited

After free tier: ~$7-15/month depending on usage

## 🔄 Update Your App

To update:
1. Push changes to GitHub
2. Railway auto-deploys (or click "Redeploy")
3. Check logs to verify deployment

## 📱 Frontend Access

Your chatbot is live at:
```
https://YOUR_RAILWAY_URL.railway.app
```

Share this URL with users!

## 🔗 SSL Certificate

Railroad automatically provides:
- ✅ Free SSL certificate
- ✅ Auto-renewal
- ✅ HTTPS everywhere

## 📞 Need Help?

If deployment fails:
1. Check **Logs** in Railway dashboard
2. Look for error messages
3. Common issues:
   - Missing environment variables
   - Incorrect Dockerfile
   - Port conflicts

## 🎯 Next Steps

1. ✅ Deploy chatbot
2. ✅ Test health endpoint
3. ✅ Share URL with users
4. ✅ Monitor logs and performance
5. ✅ Set up monitoring alerts (Railway Pro)

---

## 📋 Quick Checklist

- [ ] GitHub account with chatbot code pushed
- [ ] Gemini API key obtained
- [ ] Railway account created
- [ ] Repository connected to Railway
- [ ] Environment variables added
- [ ] Deployment completed
- [ ] URL obtained
- [ ] Health check passing
- [ ] Frontend accessible
- [ ] API endpoints working

---

## 🎉 You're Live!

Your CBT Chatbot is now deployed on Railway.app and accessible online.

**Demo URL:** https://YOUR_RAILWAY_URL.railway.app

Share this with friends, users, or for your portfolio!

---

**Questions?** See the official Railway docs: https://docs.railway.app/

**Last Updated:** 2026-03-27
