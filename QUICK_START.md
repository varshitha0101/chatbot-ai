# 🎯 QUICK START - Enable AI in 3 Steps

Your chatbot is running, but needs an API key to give ChatGPT-like responses!

## Step 1: Get FREE Google Gemini API Key (1 minute)

👉 **Go to: https://aistudio.google.com/app/apikey**

1. Sign in with your Google account  
2. Click **"Create API Key"**
3. Choose **"Create API key in new project"**
4. Copy the key (starts with `AIza...`)

✅ No credit card needed!
✅ 1,500 free requests per day

---

## Step 2: Add the Key to Your Project (30 seconds)

**Open PowerShell and run:**

```powershell
# Go to your project folder
cd C:\Users\Varsh\OneDrive\Apps\chatbot-ai

# Copy the example file
Copy-Item .env.example .env

# Open the file in notepad
notepad .env
```

**In the .env file, paste your API key:**
```
GEMINI_API_KEY=AIzaYourActualKeyGoesHere
```

Save and close.

---

## Step 3: Restart the Backend (30 seconds)

In VS Code terminal:
1. Press **Ctrl+C** to stop the Flask server
2. Run this command:

```powershell
c:/Users/Varsh/OneDrive/Apps/chatbot-ai/.venv/Scripts/python.exe backend/app.py
```

---

## ✅ Done! 

Open: **http://localhost:8000**

Your chatbot now responds with natural, empathetic AI-powered conversations! 🎉

---

## 🔍 Verify It's Working

Visit: http://localhost:5000/

You should see:
```json
{
  "ai_powered": true,
  "ai_status": "enabled"
}
```

If you see `"ai_powered": false`, double-check:
- ✓ The API key is in the `.env` file
- ✓ The key starts with `AIza`
- ✓ You restarted the Flask server

---

## 💬 The Difference

**Before (Template Mode - Current):**
> "I hear that you're feeling anxious. What thoughts are running through your mind?"

**After (AI Mode - With API Key):**
> "I can really feel how overwhelming this anxiety is for you. It sounds like your mind might be racing with worries. I'm wondering - when these anxious thoughts come up, do they tend to focus on something specific, or jump around? Sometimes just naming what we're anxious about can help us examine if those fears match reality."

---

## 📖 Full Documentation

See [AI_SETUP_GUIDE.md](AI_SETUP_GUIDE.md) for detailed instructions and troubleshooting.

---

**Need help?** The chatbot works right now with enhanced templates, but with AI it becomes 10x better! 🚀
