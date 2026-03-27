# Railway Deployment - Quick Start (5 Minutes)

## 🎯 Only 3 Steps to Go Live

### Step 1️⃣: Create Account & Connect GitHub (2 min)
```
1. Visit https://railway.app
2. Click "Start Project"
3. Select "Deploy from GitHub"
4. Authorize & select your chatbot-ai repo
✅ Done - Railway now has your code
```

### Step 2️⃣: Add Environment Variables (2 min)

In Railway dashboard, click **Variables** and add:

```
SECRET_KEY = abcd1234xyz... (random - generate with Python)
JWT_SECRET_KEY = efgh5678abc... (random - generate with Python)
GEMINI_API_KEY = YOUR_API_KEY_FROM_GOOGLE
FLASK_ENV = production
FLASK_DEBUG = false
```

**How to generate random keys:**
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

✅ Done - Variables saved

### Step 3️⃣: Deploy (1 min)

```
1. Click "Deploy" button
2. Wait ~2-3 minutes for build
3. Get your live URL from "Domains"
4. Update variables with your Railway URL:
   - API_BASE_URL = https://your-url.railway.app
   - CORS_ORIGINS = https://your-url.railway.app
5. Click "Redeploy"
✅ LIVE! Your chatbot is online
```

---

## ✅ Test It

```bash
# Your live URL will be:
https://chatbot-{random}.railway.app

# Test it:
curl https://chatbot-{random}.railway.app/health
```

---

## 📞 Still Need Help?

See: **RAILWAY_DEPLOYMENT_GUIDE.md** in this repository for detailed guide
