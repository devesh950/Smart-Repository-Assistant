#!/bin/bash

# 🚀 Quick Azure Deployment Script for Smart Repository Assistant
# Run this script to deploy to Azure App Service

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
RESOURCE_GROUP="smart-repo-assistant-rg"
APP_NAME="smart-repo-assistant-devesh"
PLAN_NAME="smart-repo-assistant-plan"
LOCATION="East US"
PYTHON_VERSION="3.9"

echo -e "${BLUE}🚀 Smart Repository Assistant - Azure Deployment${NC}"
echo -e "${BLUE}=================================================${NC}"

# Check if Azure CLI is installed
if ! command -v az &> /dev/null; then
    echo -e "${RED}❌ Azure CLI is not installed. Please install it first:${NC}"
    echo "   Windows: winget install Microsoft.AzureCLI"
    echo "   Or download from: https://aka.ms/installazurecliwindows"
    exit 1
fi

# Check if logged in to Azure
if ! az account show &> /dev/null; then
    echo -e "${YELLOW}🔐 Please login to Azure...${NC}"
    az login
fi

echo -e "${GREEN}✅ Azure CLI configured${NC}"

# Get subscription info
SUBSCRIPTION=$(az account show --query name -o tsv)
echo -e "${BLUE}📋 Using subscription: ${SUBSCRIPTION}${NC}"

# Create resource group
echo -e "${YELLOW}📦 Creating resource group...${NC}"
az group create \
    --name "$RESOURCE_GROUP" \
    --location "$LOCATION" \
    --output table

# Create app service plan
echo -e "${YELLOW}🏗️  Creating app service plan...${NC}"
az appservice plan create \
    --name "$PLAN_NAME" \
    --resource-group "$RESOURCE_GROUP" \
    --sku F1 \
    --is-linux \
    --output table

# Create web app
echo -e "${YELLOW}🌐 Creating web app...${NC}"
az webapp create \
    --name "$APP_NAME" \
    --resource-group "$RESOURCE_GROUP" \
    --plan "$PLAN_NAME" \
    --runtime "PYTHON|$PYTHON_VERSION" \
    --output table

# Configure startup command
echo -e "${YELLOW}⚙️  Configuring startup command...${NC}"
az webapp config set \
    --name "$APP_NAME" \
    --resource-group "$RESOURCE_GROUP" \
    --startup-file "startup.sh"

# Set app settings (you'll need to update these with your actual values)
echo -e "${YELLOW}🔧 Configuring environment variables...${NC}"
echo -e "${RED}⚠️  IMPORTANT: Update these with your actual GitHub App credentials!${NC}"

az webapp config appsettings set \
    --name "$APP_NAME" \
    --resource-group "$RESOURCE_GROUP" \
    --settings \
    GITHUB_APP_ID="your_app_id_here" \
    GITHUB_APP_INSTALLATION_ID="your_installation_id_here" \
    GITHUB_WEBHOOK_SECRET="your_webhook_secret_here" \
    GITHUB_PRIVATE_KEY_PATH="/home/site/wwwroot/github-private-key.pem" \
    DEFAULT_REPO="devesh950/Smart-Repository-Assistant" \
    FLASK_HOST="0.0.0.0" \
    FLASK_PORT="8000" \
    FLASK_DEBUG="False" \
    ENVIRONMENT="production" \
    SCM_DO_BUILD_DURING_DEPLOYMENT="true" \
    --output table

# Enable logging
echo -e "${YELLOW}📊 Enabling application logging...${NC}"
az webapp log config \
    --name "$APP_NAME" \
    --resource-group "$RESOURCE_GROUP" \
    --application-logging filesystem \
    --level information

# Deploy from GitHub (manual integration)
echo -e "${YELLOW}🚀 Configuring deployment from GitHub...${NC}"
az webapp deployment source config \
    --name "$APP_NAME" \
    --resource-group "$RESOURCE_GROUP" \
    --repo-url https://github.com/devesh950/Smart-Repository-Assistant \
    --branch main \
    --manual-integration

# Get app URL
APP_URL="https://$APP_NAME.azurewebsites.net"
WEBHOOK_URL="$APP_URL/webhook"

echo -e "${GREEN}🎉 Deployment completed successfully!${NC}"
echo -e "${GREEN}=================================${NC}"
echo -e "${BLUE}📱 App URL:        ${APP_URL}${NC}"
echo -e "${BLUE}🔗 Webhook URL:    ${WEBHOOK_URL}${NC}"
echo -e "${BLUE}💚 Health Check:   ${APP_URL}/health${NC}"
echo -e "${BLUE}📊 Dashboard:      ${APP_URL}:8501${NC}"
echo ""

echo -e "${YELLOW}📋 Next Steps:${NC}"
echo "1. 🔐 Update GitHub App credentials in Azure portal or run:"
echo "   az webapp config appsettings set --name $APP_NAME --resource-group $RESOURCE_GROUP --settings GITHUB_APP_ID=your_real_app_id"
echo ""
echo "2. 🔗 Update GitHub App webhook URL to:"
echo "   $WEBHOOK_URL"
echo ""
echo "3. 📄 Upload your GitHub App private key:"
echo "   - Go to Azure Portal > App Services > $APP_NAME > Advanced Tools > Go > Debug Console"
echo "   - Upload github-private-key.pem to /home/site/wwwroot/"
echo ""
echo "4. 🧪 Test the deployment:"
echo "   curl $APP_URL/health"
echo ""

echo -e "${GREEN}✨ Your Smart Repository Assistant is now running on Azure! ✨${NC}"

# Open browser to app URL
if command -v start &> /dev/null; then
    echo -e "${BLUE}🌐 Opening app in browser...${NC}"
    start "$APP_URL"
elif command -v open &> /dev/null; then
    echo -e "${BLUE}🌐 Opening app in browser...${NC}"
    open "$APP_URL"
fi

# Show logs
echo -e "${YELLOW}📊 You can view logs with:${NC}"
echo "az webapp log tail --name $APP_NAME --resource-group $RESOURCE_GROUP"