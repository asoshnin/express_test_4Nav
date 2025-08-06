# 🚀 AI Navigator Profiler - Production Deployment Guide

## **Overview**
This guide will walk you through deploying the AI Navigator Profiler backend to Azure Functions with all necessary Azure services.

## **📋 Prerequisites**

### **Azure Resources Required:**
- Azure Subscription
- Azure Functions App (Consumption Plan)
- Azure Cosmos DB (Serverless Mode)
- Azure OpenAI Service
- Azure Application Insights (Optional but recommended)

### **Local Development Setup:**
- Python 3.11+
- Azure Functions Core Tools v4
- Azure CLI
- Git

## **🔧 Step-by-Step Deployment**

### **1. Azure Resource Creation**

#### **Create Resource Group:**
```bash
az group create --name navigator-profiler-rg --location eastus
```

#### **Create Cosmos DB Account:**
```bash
az cosmosdb create \
  --name navigator-profiler-cosmos \
  --resource-group navigator-profiler-rg \
  --capabilities EnableServerless
```

#### **Create Cosmos DB Database and Container:**
```bash
# Create database
az cosmosdb sql database create \
  --account-name navigator-profiler-cosmos \
  --resource-group navigator-profiler-rg \
  --name navigator_profiler

# Create container
az cosmosdb sql container create \
  --account-name navigator-profiler-cosmos \
  --resource-group navigator-profiler-rg \
  --database-name navigator_profiler \
  --name sessions \
  --partition-key-path "/id"
```

#### **Create Azure OpenAI Service:**
```bash
az cognitiveservices account create \
  --name navigator-profiler-openai \
  --resource-group navigator-profiler-rg \
  --kind OpenAI \
  --sku S0 \
  --location eastus
```

#### **Create Function App:**
```bash
az functionapp create \
  --name navigator-profiler-func \
  --resource-group navigator-profiler-rg \
  --consumption-plan-location eastus \
  --runtime python \
  --runtime-version 3.11 \
  --functions-version 4 \
  --storage-account navigatorprofilerstorage \
  --os-type Linux
```

### **2. Configure Application Settings**

#### **Get Connection Strings:**
```bash
# Get Cosmos DB connection string
COSMOS_ENDPOINT=$(az cosmosdb show --name navigator-profiler-cosmos --resource-group navigator-profiler-rg --query documentEndpoint -o tsv)
COSMOS_KEY=$(az cosmosdb keys list --name navigator-profiler-cosmos --resource-group navigator-profiler-rg --query primaryMasterKey -o tsv)

# Get OpenAI connection string
OPENAI_ENDPOINT=$(az cognitiveservices account show --name navigator-profiler-openai --resource-group navigator-profiler-rg --query properties.endpoint -o tsv)
OPENAI_KEY=$(az cognitiveservices account keys list --name navigator-profiler-openai --resource-group navigator-profiler-rg --query key1 -o tsv)
```

#### **Set Application Settings:**
```bash
az functionapp config appsettings set \
  --name navigator-profiler-func \
  --resource-group navigator-profiler-rg \
  --settings \
    COSMOS_ENDPOINT="$COSMOS_ENDPOINT" \
    COSMOS_KEY="$COSMOS_KEY" \
    COSMOS_DATABASE_NAME="navigator_profiler" \
    COSMOS_CONTAINER_NAME="sessions" \
    AZURE_OPENAI_ENDPOINT="$OPENAI_ENDPOINT" \
    AZURE_OPENAI_KEY="$OPENAI_KEY"
```

### **3. Deploy the Function App**

#### **From Local Development:**
```bash
# Login to Azure
az login

# Set subscription (if needed)
az account set --subscription "your-subscription-id"

# Deploy function app
func azure functionapp publish navigator-profiler-func
```

#### **From GitHub Actions (Recommended):**
Create `.github/workflows/deploy.yml`:

```yaml
name: Deploy to Azure Functions

on:
  push:
    branches: [ main ]

jobs:
  build-and-deploy:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Setup Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
    
    - name: Deploy to Azure Functions
      uses: Azure/functions-action@v1
      with:
        app-name: 'navigator-profiler-func'
        package: '.'
        publish-profile: ${{ secrets.AZURE_FUNCTIONAPP_PUBLISH_PROFILE }}
```

### **4. Test the Deployment**

#### **Health Check:**
```bash
curl https://navigator-profiler-func.azurewebsites.net/api/health
```

#### **Start Assessment:**
```bash
curl -X POST https://navigator-profiler-func.azurewebsites.net/api/assessment \
  -H "Content-Type: application/json"
```

## **🔒 Security Considerations**

### **CORS Configuration:**
```bash
az functionapp cors add \
  --name navigator-profiler-func \
  --resource-group navigator-profiler-rg \
  --allowed-origins "https://your-frontend-domain.com"
```

### **Authentication (Optional):**
For admin endpoints, consider implementing Azure AD authentication:

```bash
# Enable Azure AD authentication
az functionapp auth set \
  --name navigator-profiler-func \
  --resource-group navigator-profiler-rg \
  --aad-allowed-token-audiences "api://your-app-id"
```

## **📊 Monitoring Setup**

### **Application Insights:**
```bash
# Create Application Insights
az monitor app-insights component create \
  --app navigator-profiler-insights \
  --location eastus \
  --resource-group navigator-profiler-rg \
  --application-type web

# Connect to Function App
az functionapp config appsettings set \
  --name navigator-profiler-func \
  --resource-group navigator-profiler-rg \
  --settings \
    APPINSIGHTS_INSTRUMENTATIONKEY="your-instrumentation-key"
```

## **💰 Cost Optimization**

### **Cosmos DB Serverless Mode:**
- Already configured for pay-per-use
- No minimum monthly fee
- Automatic scaling

### **Function App Consumption Plan:**
- Pay only for executions
- Automatic scaling
- No idle costs

### **OpenAI Service:**
- Pay per token usage
- Consider setting usage limits
- Monitor costs in Azure portal

## **🚨 Troubleshooting**

### **Common Issues:**

1. **Cosmos DB Connection Errors:**
   - Verify connection string format
   - Check firewall settings
   - Ensure database/container exist

2. **OpenAI Service Errors:**
   - Verify API key is correct
   - Check deployment model names
   - Ensure service is in same region

3. **Function App Deployment Issues:**
   - Check Python version compatibility
   - Verify all dependencies in requirements.txt
   - Check application settings

### **Logs and Monitoring:**
```bash
# View function logs
az functionapp logs tail --name navigator-profiler-func --resource-group navigator-profiler-rg

# Check function app status
az functionapp show --name navigator-profiler-func --resource-group navigator-profiler-rg
```

## **🎯 Next Steps After Deployment**

1. **Frontend Integration** - Connect your React frontend to the deployed API
2. **Load Testing** - Test with realistic user volumes
3. **Monitoring Setup** - Configure alerts and dashboards
4. **Backup Strategy** - Implement Cosmos DB backup policies
5. **CI/CD Pipeline** - Set up automated deployments

## **📞 Support**

For issues with this deployment:
1. Check Azure Function logs
2. Review Application Insights
3. Verify all environment variables
4. Test individual endpoints

**The AI Navigator Profiler is now ready for production use!** 🚀 