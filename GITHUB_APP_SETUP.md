# 🚀 GitHub App Setup Guide for Smart Repository Assistant

This guide will help you create a GitHub App for professional integration with your Smart Repository Assistant.

## 🎯 Why Use a GitHub App?

✅ **Higher Rate Limits** (5,000 requests/hour per installation)  
✅ **Fine-grained Permissions** (only what you need)  
✅ **Professional Integration** (appears as an app, not a user)  
✅ **Webhook Integration** (real-time updates)  
✅ **Multi-repository Support** (install once, use everywhere)  
✅ **Better Security** (scoped access, rotating tokens)

## 📋 Step-by-Step Setup

### Step 1: Create Your GitHub App

1. **Go to GitHub App Settings**:
   ```
   https://github.com/settings/apps
   ```

2. **Click "New GitHub App"**

3. **Fill in Basic Information**:
   ```
   GitHub App name: Smart Repository Assistant
   Description: Intelligent repository management with auto-labeling and analytics
   Homepage URL: https://github.com/devesh950/Smart-Repository-Assistant
   User authorization callback URL: (leave blank)
   Setup URL: (leave blank)
   Webhook URL: https://your-domain.herokuapp.com/webhook
   Webhook secret: your_secure_random_string_here
   ```

### Step 2: Set Repository Permissions

**Required Permissions:**
- ✅ **Contents**: Read (repository analysis)
- ✅ **Issues**: Read & Write (auto-labeling, analytics)
- ✅ **Metadata**: Read (basic repository info)
- ✅ **Pull requests**: Read & Write (PR analysis, labeling)
- ✅ **Commit statuses**: Read (health analysis)

**Subscribe to Events:**
- ✅ **Issues** (opened, closed, edited, labeled)
- ✅ **Pull request** (opened, closed, edited, labeled)
- ✅ **Push** (commit analysis)

### Step 3: Generate and Download Keys

1. **After creating the app, scroll down to "Private keys"**
2. **Click "Generate a private key"**
3. **Download the `.pem` file** 
4. **Save it as `private-key.pem` in your project root**

### Step 4: Get Your App Credentials

After creating the app, note these values:

```bash
# From the app page URL: https://github.com/settings/apps/YOUR_APP_NAME
App ID: 123456

# After installing the app on repositories
Installation ID: 789012
```

### Step 5: Install Your App

1. **Go to your app page**: `https://github.com/settings/apps/smart-repository-assistant`
2. **Click "Install App"** in the left sidebar
3. **Choose repositories** to install on:
   - All repositories (recommended for full access)
   - Selected repositories (choose specific ones)
4. **Click "Install"**

### Step 6: Get Installation ID

After installation:
1. **Go to**: `https://github.com/settings/installations`
2. **Click "Configure"** next to your app
3. **Note the Installation ID** from the URL: `https://github.com/settings/installations/INSTALLATION_ID`

### Step 7: Configure Your Environment

Create/update your `.env` file:

```bash
# GitHub App Configuration
GITHUB_APP_ID=123456
GITHUB_APP_PRIVATE_KEY_PATH=private-key.pem
GITHUB_APP_INSTALLATION_ID=789012

# Webhook Configuration
GITHUB_WEBHOOK_SECRET=your_secure_random_string_here

# Repository Settings
DEFAULT_REPO=devesh950/Smart-Repository-Assistant

# Server Settings
FLASK_HOST=0.0.0.0
FLASK_PORT=5000
FLASK_DEBUG=True
ENVIRONMENT=production
```

## 🚀 Deployment Options with Webhook URLs

### Option 1: Heroku
```bash
# Deploy to Heroku
git push heroku main

# Your webhook URL will be:
https://your-app-name.herokuapp.com/webhook
```

### Option 2: Railway
```bash
# Deploy to Railway
railway deploy

# Your webhook URL will be:
https://your-app-name.railway.app/webhook
```

### Option 3: Vercel
```bash
# Deploy to Vercel
vercel deploy

# Your webhook URL will be:
https://your-app-name.vercel.app/webhook
```

### Option 4: ngrok (For Local Testing)
```bash
# Install ngrok and run locally
ngrok http 5000

# Your webhook URL will be:
https://abc123.ngrok.io/webhook
```

## 🔧 Update Webhook URL After Deployment

1. **Go back to your GitHub App settings**
2. **Update the Webhook URL** with your deployed app URL
3. **Save changes**

## ✅ Test Your Setup

Run the test script to verify everything works:

```bash
python test_github_app.py
```

## 🎯 Benefits After Setup

Once configured, your Smart Repository Assistant will:

✅ **Automatically label** new issues and PRs  
✅ **Provide real-time analytics** via webhooks  
✅ **Monitor repository health** continuously  
✅ **Track contributor activity** in real-time  
✅ **Generate comprehensive reports**  
✅ **Scale to multiple repositories** easily

## 🆘 Troubleshooting

### Common Issues:

**1. "Authentication failed"**
- Check your App ID and Installation ID are correct
- Ensure the private key file exists and is readable
- Verify the app is installed on the target repository

**2. "Webhook not receiving events"**
- Check the webhook URL is accessible from the internet
- Verify the webhook secret matches your configuration
- Ensure the app is subscribed to the right events

**3. "Permission denied"**
- Verify the app has the required permissions
- Check the app is installed on the repository
- Ensure you're using the correct Installation ID

### Getting Help:

- 📖 GitHub Apps Documentation: https://docs.github.com/en/developers/apps
- 🐛 Report issues: https://github.com/devesh950/Smart-Repository-Assistant/issues
- 💬 Discussions: https://github.com/devesh950/Smart-Repository-Assistant/discussions

## 🎉 You're All Set!

Your Smart Repository Assistant is now configured as a professional GitHub App with webhook integration. Deploy it and start experiencing intelligent repository management! 🚀