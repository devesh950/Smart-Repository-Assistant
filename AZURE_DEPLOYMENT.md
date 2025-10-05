# 🚀 Microsoft Azure Deployment Guide

Deploy your Smart Repository Assistant to Microsoft Azure with professional enterprise features.

## 🌟 Why Choose Azure?

✅ **Enterprise-Grade Security** - Built-in security and compliance  
✅ **GitHub Integration** - Native GitHub Actions deployment  
✅ **Auto-Scaling** - Handles traffic spikes automatically  
✅ **Global CDN** - Fast worldwide access  
✅ **Built-in Monitoring** - Application Insights included  
✅ **Free Tier Available** - F1 tier for development  

## 📋 Deployment Options

### Option 1: Azure App Service (Recommended)
### Option 2: Azure Container Instances
### Option 3: Azure Functions (Serverless)
### Option 4: Azure Kubernetes Service (AKS)

---

## 🚀 Option 1: Azure App Service (Web Apps)

### Prerequisites
- Azure account (free at https://azure.microsoft.com/free/)
- Azure CLI installed

### Step 1: Install Azure CLI
```bash
# Windows (using winget)
winget install Microsoft.AzureCLI

# Or download from: https://aka.ms/installazurecliwindows
```

### Step 2: Login to Azure
```bash
az login
az account list --output table
az account set --subscription "Your-Subscription-Name"
```

### Step 3: Create Resource Group
```bash
az group create --name smart-repo-assistant-rg --location "East US"
```

### Step 4: Create App Service Plan
```bash
# Free tier for development
az appservice plan create \
  --name smart-repo-assistant-plan \
  --resource-group smart-repo-assistant-rg \
  --sku F1 \
  --is-linux

# Production tier (optional)
az appservice plan create \
  --name smart-repo-assistant-plan-prod \
  --resource-group smart-repo-assistant-rg \
  --sku B1 \
  --is-linux
```

### Step 5: Create Web App
```bash
az webapp create \
  --name smart-repo-assistant-devesh \
  --resource-group smart-repo-assistant-rg \
  --plan smart-repo-assistant-plan \
  --runtime "PYTHON|3.9"
```

### Step 6: Configure Environment Variables
```bash
# GitHub App Configuration
az webapp config appsettings set \
  --name smart-repo-assistant-devesh \
  --resource-group smart-repo-assistant-rg \
  --settings \
  GITHUB_APP_ID="your_app_id" \
  GITHUB_APP_INSTALLATION_ID="your_installation_id" \
  GITHUB_WEBHOOK_SECRET="your_webhook_secret" \
  DEFAULT_REPO="devesh950/Smart-Repository-Assistant" \
  FLASK_HOST="0.0.0.0" \
  FLASK_PORT="8000" \
  FLASK_DEBUG="False" \
  ENVIRONMENT="production"
```

### Step 7: Deploy from GitHub
```bash
# Configure deployment from GitHub
az webapp deployment source config \
  --name smart-repo-assistant-devesh \
  --resource-group smart-repo-assistant-rg \
  --repo-url https://github.com/devesh950/Smart-Repository-Assistant \
  --branch main \
  --manual-integration
```

### Step 8: Your URLs
- **App URL**: `https://smart-repo-assistant-devesh.azurewebsites.net`
- **Webhook URL**: `https://smart-repo-assistant-devesh.azurewebsites.net/webhook`
- **Health Check**: `https://smart-repo-assistant-devesh.azurewebsites.net/health`

---

## 🐳 Option 2: Azure Container Instances

### Step 1: Build and Push Docker Image
```bash
# Build image
docker build -t smart-repo-assistant .

# Tag for Azure Container Registry
docker tag smart-repo-assistant smartrepoassistant.azurecr.io/smart-repo-assistant:latest
```

### Step 2: Create Container Registry
```bash
az acr create \
  --name smartrepoassistant \
  --resource-group smart-repo-assistant-rg \
  --sku Basic \
  --admin-enabled true

# Login to registry
az acr login --name smartrepoassistant
```

### Step 3: Push Image
```bash
docker push smartrepoassistant.azurecr.io/smart-repo-assistant:latest
```

### Step 4: Deploy Container
```bash
az container create \
  --name smart-repo-assistant \
  --resource-group smart-repo-assistant-rg \
  --image smartrepoassistant.azurecr.io/smart-repo-assistant:latest \
  --registry-login-server smartrepoassistant.azurecr.io \
  --registry-username smartrepoassistant \
  --registry-password $(az acr credential show --name smartrepoassistant --query passwords[0].value -o tsv) \
  --dns-name-label smart-repo-assistant-devesh \
  --ports 5000 8501 \
  --environment-variables \
    GITHUB_APP_ID=your_app_id \
    GITHUB_APP_INSTALLATION_ID=your_installation_id \
    GITHUB_WEBHOOK_SECRET=your_webhook_secret \
    DEFAULT_REPO=devesh950/Smart-Repository-Assistant
```

---

## ⚡ Option 3: Azure Functions (Serverless)

### Step 1: Create Function App
```bash
az functionapp create \
  --name smart-repo-assistant-func \
  --resource-group smart-repo-assistant-rg \
  --consumption-plan-location "East US" \
  --runtime python \
  --runtime-version 3.9 \
  --functions-version 4 \
  --storage-account smartrepoassistantsa
```

### Step 2: Configure Function Settings
```bash
az functionapp config appsettings set \
  --name smart-repo-assistant-func \
  --resource-group smart-repo-assistant-rg \
  --settings \
  GITHUB_APP_ID="your_app_id" \
  GITHUB_APP_INSTALLATION_ID="your_installation_id" \
  GITHUB_WEBHOOK_SECRET="your_webhook_secret" \
  DEFAULT_REPO="devesh950/Smart-Repository-Assistant"
```

---

## 🎛️ Option 4: Azure Kubernetes Service (AKS)

### Step 1: Create AKS Cluster
```bash
az aks create \
  --name smart-repo-assistant-aks \
  --resource-group smart-repo-assistant-rg \
  --node-count 1 \
  --node-vm-size Standard_B2s \
  --generate-ssh-keys \
  --attach-acr smartrepoassistant
```

### Step 2: Get Credentials
```bash
az aks get-credentials \
  --name smart-repo-assistant-aks \
  --resource-group smart-repo-assistant-rg
```

### Step 3: Deploy with Kubernetes
```yaml
# kubernetes-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: smart-repo-assistant
spec:
  replicas: 2
  selector:
    matchLabels:
      app: smart-repo-assistant
  template:
    metadata:
      labels:
        app: smart-repo-assistant
    spec:
      containers:
      - name: smart-repo-assistant
        image: smartrepoassistant.azurecr.io/smart-repo-assistant:latest
        ports:
        - containerPort: 5000
        - containerPort: 8501
        env:
        - name: GITHUB_APP_ID
          value: "your_app_id"
        - name: GITHUB_APP_INSTALLATION_ID
          value: "your_installation_id"
        - name: GITHUB_WEBHOOK_SECRET
          value: "your_webhook_secret"
```

```bash
kubectl apply -f kubernetes-deployment.yaml
```

---

## 📊 Azure-Specific Features

### Application Insights Integration
```bash
# Enable Application Insights
az monitor app-insights component create \
  --app smart-repo-assistant-insights \
  --location "East US" \
  --resource-group smart-repo-assistant-rg

# Get instrumentation key
INSTRUMENTATION_KEY=$(az monitor app-insights component show \
  --app smart-repo-assistant-insights \
  --resource-group smart-repo-assistant-rg \
  --query instrumentationKey -o tsv)

# Configure app to use it
az webapp config appsettings set \
  --name smart-repo-assistant-devesh \
  --resource-group smart-repo-assistant-rg \
  --settings APPINSIGHTS_INSTRUMENTATIONKEY=$INSTRUMENTATION_KEY
```

### Azure Key Vault Integration
```bash
# Create Key Vault
az keyvault create \
  --name smart-repo-assistant-kv \
  --resource-group smart-repo-assistant-rg \
  --location "East US"

# Store secrets
az keyvault secret set \
  --vault-name smart-repo-assistant-kv \
  --name "github-app-id" \
  --value "your_app_id"

az keyvault secret set \
  --vault-name smart-repo-assistant-kv \
  --name "github-webhook-secret" \
  --value "your_webhook_secret"
```

### Auto-Scaling Configuration
```bash
# Configure auto-scaling
az monitor autoscale create \
  --name smart-repo-assistant-autoscale \
  --resource-group smart-repo-assistant-rg \
  --resource /subscriptions/{subscription-id}/resourceGroups/smart-repo-assistant-rg/providers/Microsoft.Web/serverfarms/smart-repo-assistant-plan \
  --min-count 1 \
  --max-count 5 \
  --count 1

# Scale out rule
az monitor autoscale rule create \
  --autoscale-name smart-repo-assistant-autoscale \
  --resource-group smart-repo-assistant-rg \
  --condition "CpuPercentage > 70 avg 5m" \
  --scale out 1
```

---

## 🔄 GitHub Actions for Azure CI/CD

Create `.github/workflows/azure-deploy.yml`:

```yaml
name: Deploy to Azure

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v3
      with:
        python-version: 3.9
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
    
    - name: Test application
      run: |
        python test_system.py
    
    - name: Login to Azure
      uses: azure/login@v1
      with:
        creds: ${{ secrets.AZURE_CREDENTIALS }}
    
    - name: Deploy to Azure Web App
      uses: azure/webapps-deploy@v2
      with:
        app-name: smart-repo-assistant-devesh
        slot-name: production
        package: .
```

---

## 💰 Cost Optimization

### Free Tier Resources
- **App Service**: F1 (Free) - 1 GB RAM, 1 GB storage
- **Application Insights**: First 5 GB/month free
- **Key Vault**: First 10,000 operations free

### Production Recommendations
- **App Service**: B1 Basic ($13/month) - 1.75 GB RAM, auto-scaling
- **Container Instances**: Pay per second usage
- **Functions**: Consumption plan - pay per execution

---

## 🔍 Monitoring and Diagnostics

### View Logs
```bash
# Stream logs
az webapp log tail \
  --name smart-repo-assistant-devesh \
  --resource-group smart-repo-assistant-rg

# Download logs
az webapp log download \
  --name smart-repo-assistant-devesh \
  --resource-group smart-repo-assistant-rg
```

### Performance Monitoring
- **Application Insights**: Real-time performance metrics
- **Log Analytics**: Advanced log querying
- **Azure Monitor**: Custom alerts and dashboards

---

## 🛡️ Security Best Practices

### Network Security
```bash
# Restrict access to webhook endpoint
az webapp config access-restriction add \
  --name smart-repo-assistant-devesh \
  --resource-group smart-repo-assistant-rg \
  --rule-name "GitHub-Webhooks" \
  --action Allow \
  --ip-address 140.82.112.0/20 \
  --priority 100
```

### SSL/TLS Configuration
```bash
# Force HTTPS
az webapp update \
  --name smart-repo-assistant-devesh \
  --resource-group smart-repo-assistant-rg \
  --https-only true
```

---

## 🎯 Final Setup Checklist

✅ **Azure resources created**  
✅ **Environment variables configured**  
✅ **Application deployed**  
✅ **Webhook URL updated in GitHub App**: `https://smart-repo-assistant-devesh.azurewebsites.net/webhook`  
✅ **SSL certificate configured**  
✅ **Monitoring enabled**  
✅ **Auto-scaling configured**  

## 📞 Support and Resources

- 📖 **Azure Documentation**: https://docs.microsoft.com/azure/
- 💬 **Azure Support**: https://azure.microsoft.com/support/
- 🎓 **Azure Learning**: https://docs.microsoft.com/learn/azure/
- 🛠️ **Azure CLI Reference**: https://docs.microsoft.com/cli/azure/

Your Smart Repository Assistant is now running on Microsoft Azure with enterprise-grade features! 🚀☁️