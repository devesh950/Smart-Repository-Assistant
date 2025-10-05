# 🚀 Quick Deployment & Webhook Setup

## 🌟 Deployment Options

### 🟦 Heroku (Easiest)
### 🟨 Railway (Modern) 
### 🟩 Vercel (Serverless)
### ☁️  Microsoft Azure (Enterprise)

---

## Option 1: Deploy to Heroku (Easiest)

1. **Create Heroku App**:
   ```bash
   heroku create your-smart-repo-assistant
   ```

2. **Set Environment Variables**:
   ```bash
   heroku config:set GITHUB_APP_ID=your_app_id
   heroku config:set GITHUB_APP_INSTALLATION_ID=your_installation_id
   heroku config:set GITHUB_WEBHOOK_SECRET=your_secret
   heroku config:set DEFAULT_REPO=devesh950/Smart-Repository-Assistant
   ```

3. **Upload Private Key**:
   - Add your `private-key.pem` to the repository
   - Or use Heroku config vars for the key content

4. **Deploy**:
   ```bash
   git push heroku main
   ```

5. **Your Webhook URL**: `https://your-smart-repo-assistant.herokuapp.com/webhook`

## Option 2: Deploy to Railway

1. **Connect Repository**: https://railway.app/new
2. **Add Environment Variables** in Railway dashboard
3. **Deploy automatically**
4. **Your Webhook URL**: `https://your-app-name.railway.app/webhook`

## Option 3: Deploy to Vercel

1. **Import Repository**: https://vercel.com/new
2. **Add Environment Variables** in Vercel dashboard  
3. **Deploy**
4. **Your Webhook URL**: `https://your-app-name.vercel.app/webhook`

## 🔧 GitHub App Configuration URLs

After deployment, update these in your GitHub App:

1. **Go to**: https://github.com/settings/apps/smart-repository-assistant
2. **Update Webhook URL**: `https://your-deployed-app.com/webhook`
3. **Save changes**

---

## Option 4: Deploy to Microsoft Azure ☁️

**Automated Deployment**:
```bash
# Windows PowerShell
.\deploy-azure.ps1

# Bash/WSL
chmod +x deploy-azure.sh
./deploy-azure.sh
```

**Manual Azure Setup**:
1. Install Azure CLI: `winget install Microsoft.AzureCLI`
2. Login: `az login`
3. Run deployment script
4. Update GitHub App webhook URL to: `https://smart-repo-assistant-devesh.azurewebsites.net/webhook`

**Azure Features**:
- ✅ Enterprise-grade security
- ✅ Built-in monitoring & logging
- ✅ Auto-scaling capabilities
- ✅ Free tier available
- ✅ GitHub Actions CI/CD

📖 **Full Guide**: See `AZURE_DEPLOYMENT.md` for comprehensive Azure deployment options including Container Instances, Kubernetes, and Functions.

---

## 🎯 Complete Integration Flow:

1. ✅ Create GitHub App
2. ✅ Get App ID, Installation ID, Private Key
3. ✅ Deploy Smart Repository Assistant  
4. ✅ Update webhook URL in GitHub App
5. ✅ Install app on repositories
6. ✅ Start receiving real-time events!

## 📊 Access Your Analytics:

- **API Health**: `https://your-app.com/health`
- **Analytics**: `https://your-app.com/analytics`  
- **Dashboard**: Deploy Streamlit separately or use the API endpoints

Your Smart Repository Assistant will now automatically process issues and PRs in real-time! 🎉