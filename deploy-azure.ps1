# 🚀 PowerShell Azure Deployment Script for Smart Repository Assistant
# Run this script to deploy to Azure App Service from Windows

# Configuration
$ResourceGroup = "smart-repo-assistant-rg"
$AppName = "smart-repo-assistant-devesh"
$PlanName = "smart-repo-assistant-plan"
$Location = "East US"
$PythonVersion = "3.9"

Write-Host "🚀 Smart Repository Assistant - Azure Deployment" -ForegroundColor Blue
Write-Host "=================================================" -ForegroundColor Blue

# Check if Azure CLI is installed
try {
    az --version | Out-Null
    Write-Host "✅ Azure CLI found" -ForegroundColor Green
} catch {
    Write-Host "❌ Azure CLI is not installed. Please install it first:" -ForegroundColor Red
    Write-Host "   winget install Microsoft.AzureCLI" -ForegroundColor Yellow
    Write-Host "   Or download from: https://aka.ms/installazurecliwindows" -ForegroundColor Yellow
    exit 1
}

# Check if logged in to Azure
try {
    $account = az account show 2>$null | ConvertFrom-Json
    if (-not $account) {
        throw "Not logged in"
    }
    Write-Host "✅ Already logged in to Azure" -ForegroundColor Green
} catch {
    Write-Host "🔐 Please login to Azure..." -ForegroundColor Yellow
    az login
}

# Get subscription info
$subscription = az account show --query name -o tsv
Write-Host "📋 Using subscription: $subscription" -ForegroundColor Blue

# Create resource group
Write-Host "📦 Creating resource group..." -ForegroundColor Yellow
az group create `
    --name $ResourceGroup `
    --location $Location `
    --output table

# Create app service plan
Write-Host "🏗️  Creating app service plan..." -ForegroundColor Yellow
az appservice plan create `
    --name $PlanName `
    --resource-group $ResourceGroup `
    --sku F1 `
    --is-linux `
    --output table

# Create web app
Write-Host "🌐 Creating web app..." -ForegroundColor Yellow
az webapp create `
    --name $AppName `
    --resource-group $ResourceGroup `
    --plan $PlanName `
    --runtime "PYTHON|$PythonVersion" `
    --output table

# Configure startup command
Write-Host "⚙️  Configuring startup command..." -ForegroundColor Yellow
az webapp config set `
    --name $AppName `
    --resource-group $ResourceGroup `
    --startup-file "startup.sh"

# Set app settings
Write-Host "🔧 Configuring environment variables..." -ForegroundColor Yellow
Write-Host "⚠️  IMPORTANT: Update these with your actual GitHub App credentials!" -ForegroundColor Red

az webapp config appsettings set `
    --name $AppName `
    --resource-group $ResourceGroup `
    --settings `
    GITHUB_APP_ID="your_app_id_here" `
    GITHUB_APP_INSTALLATION_ID="your_installation_id_here" `
    GITHUB_WEBHOOK_SECRET="your_webhook_secret_here" `
    GITHUB_PRIVATE_KEY_PATH="/home/site/wwwroot/github-private-key.pem" `
    DEFAULT_REPO="devesh950/Smart-Repository-Assistant" `
    FLASK_HOST="0.0.0.0" `
    FLASK_PORT="8000" `
    FLASK_DEBUG="False" `
    ENVIRONMENT="production" `
    SCM_DO_BUILD_DURING_DEPLOYMENT="true" `
    --output table

# Enable logging
Write-Host "📊 Enabling application logging..." -ForegroundColor Yellow
az webapp log config `
    --name $AppName `
    --resource-group $ResourceGroup `
    --application-logging filesystem `
    --level information

# Deploy from GitHub
Write-Host "🚀 Configuring deployment from GitHub..." -ForegroundColor Yellow
az webapp deployment source config `
    --name $AppName `
    --resource-group $ResourceGroup `
    --repo-url https://github.com/devesh950/Smart-Repository-Assistant `
    --branch main `
    --manual-integration

# Get URLs
$AppUrl = "https://$AppName.azurewebsites.net"
$WebhookUrl = "$AppUrl/webhook"

Write-Host ""
Write-Host "🎉 Deployment completed successfully!" -ForegroundColor Green
Write-Host "=================================" -ForegroundColor Green
Write-Host "📱 App URL:        $AppUrl" -ForegroundColor Blue
Write-Host "🔗 Webhook URL:    $WebhookUrl" -ForegroundColor Blue
Write-Host "💚 Health Check:   $AppUrl/health" -ForegroundColor Blue
Write-Host "📊 Dashboard:      $AppUrl`:8501" -ForegroundColor Blue
Write-Host ""

Write-Host "📋 Next Steps:" -ForegroundColor Yellow
Write-Host "1. 🔐 Update GitHub App credentials in Azure portal or run:"
Write-Host "   az webapp config appsettings set --name $AppName --resource-group $ResourceGroup --settings GITHUB_APP_ID=your_real_app_id"
Write-Host ""
Write-Host "2. 🔗 Update GitHub App webhook URL to:"
Write-Host "   $WebhookUrl"
Write-Host ""
Write-Host "3. 📄 Upload your GitHub App private key:"
Write-Host "   - Go to Azure Portal > App Services > $AppName > Advanced Tools > Go > Debug Console"
Write-Host "   - Upload github-private-key.pem to /home/site/wwwroot/"
Write-Host ""
Write-Host "4. 🧪 Test the deployment:"
Write-Host "   Invoke-RestMethod -Uri '$AppUrl/health'"
Write-Host ""

Write-Host "✨ Your Smart Repository Assistant is now running on Azure! ✨" -ForegroundColor Green

# Open browser
try {
    Start-Process $AppUrl
    Write-Host "🌐 Opening app in browser..." -ForegroundColor Blue
} catch {
    Write-Host "🌐 Please open: $AppUrl" -ForegroundColor Blue
}

# Show logs command
Write-Host ""
Write-Host "📊 You can view logs with:" -ForegroundColor Yellow
Write-Host "az webapp log tail --name $AppName --resource-group $ResourceGroup"