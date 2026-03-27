# AI Setup Guide - Google Gemini Integration

## 🚀 Quick Setup (3 minutes)

### Step 1: Get Your Free Google Gemini API Key

1. Go to: **https://aistudio.google.com/app/apikey**
2. Sign in with your Google account (Gmail)
3. Click **"Create API Key"** or **"Get API Key"**
4. Select **"Create API key in new project"** (or choose existing project)
5. Copy your key (starts with `AIza...`)

✅ **No credit card required!**
✅ **Free tier includes 1,500 requests/day**
✅ **Very fast and capable**

### Step 2: Set the API Key (Windows)

**Option A - Using .env file (Recommended):**
```powershell
# Copy the example file
Copy-Item .env.example .env

# Edit the file
notepad .env
```

Then paste your key:
```
GEMINI_API_KEY=AIzaYourActualKeyHere
```

**Option B - Environment Variable (Permanent):**
```powershell
# Set permanently for your user
[Environment]::SetEnvironmentVariable("GEMINI_API_KEY", "AIzaYourKeyHere", "User")

# Then restart VS Code/Terminal
```

**Option C - Temporary (Current Session Only):**
```powershell
$env:GEMINI_API_KEY="AIzaYourKeyHere"
```

### Step 3: Restart the Server

Stop the current server (Ctrl+C in the terminal where Flask is running) and restart:
```powershell
c:/Users/Varsh/OneDrive/Apps/chatbot-ai/.venv/Scripts/python.exe backend/app.py
```

## ✅ Verify It's Working

Visit http://localhost:5000/ in your browser. You should see:
```json
{
  "message": "CBT Chatbot API is running",
  "ai_powered": true,
  "ai_status": "enabled"
}
```

If `ai_powered` is `false`, the API key isn't loaded. Check the steps above.

## 🎭 What You Get with Gemini

- ✨ **Natural conversations** like ChatGPT
- 🧠 **Conversation memory** - remembers chat context
- 💬 **Empathetic responses** tailored to your emotions
- 🎯 **CBT-aware** - uses cognitive behavioral therapy techniques
- ⚡ **Fast** - typically responds in 1-2 seconds
- 🆓 **Free tier** - 1,500 requests/day (plenty for personal use!)

## 💬 Response Quality Comparison

**Without AI (Template Mode):**
> "I hear that you're feeling anxious. That must be really difficult. What thoughts are running through your mind right now?"

**With Gemini AI:**
> "I can sense how overwhelming this anxiety feels. It's like your mind is racing, isn't it? When you notice these anxious thoughts starting, what tends to trigger them? Sometimes understanding the 'why' can help us see if our mind is predicting something that's not actually likely to happen. Let's explore this together - what specific situation is making you anxious right now?"

## 🆓 Google Gemini Free Tier Limits

- **1,500 requests per day** (free)
- **60 requests per minute**
- **Gemini 1.5 Flash** - Fast and intelligent
- **No credit card needed**

For most personal mental health chatbot use, the free tier is more than enough!

## 🔒 Privacy Note

- Messages are sent to Google's API for processing
- Google uses data to improve services (see their [privacy policy](https://ai.google.dev/gemini-api/terms))
- Data is **not used for training Gemini** if you're using the API
- For 100% privacy, you could use local models (Ollama) instead

## 🐛 Troubleshooting

**"ai_powered: false" even with API key set?**
- Make sure the key is in the `.env` file in the root directory
- Check the key starts with `AIza`
- Restart the Flask server completely
- Try Option B (environment variable) and restart VS Code

**API Error 400 - "API key not valid"?**
- Double-check you copied the complete key
- Make sure there are no extra spaces
- Generate a new key if needed

**API Error 429 - Rate limit?**
- Free tier: 60 requests/minute
- Wait a minute and try again
- You're unlikely to hit daily limit (1,500/day) in normal use

**Responses seem slow?**
- First request may take 2-3 seconds
- Subsequent requests are faster (1-2 seconds)
- This is normal for cloud AI services

## 💡 Pro Tips

1. **Use the .env file** (Option A) - it's the easiest and most reliable
2. **Keep your API key secret** - don't commit it to Git
3. **The free tier is generous** - you probably won't need to upgrade
4. **Gemini remembers context** - have natural flowing conversations!

## 🎯 Next Steps

1. Get your API key from https://aistudio.google.com/app/apikey
2. Add it to `.env` file
3. Restart the server
4. Chat with your AI therapist at http://localhost:8000

Enjoy your AI-powered mental wellness companion! 🌟