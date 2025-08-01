# AI Product Approval System - Setup Instructions

## Overview
This system automatically approves/rejects products in your student marketplace using a local AI/LLM (Ollama) that runs on your laptop.

## Prerequisites

### 1. Python 3.8+ (Already installed: Python 3.13.2 ✅)
### 2. Required Python Packages
Run these commands in Command Prompt:
```bash
pip install pyodbc==4.0.39
pip install Pillow==10.1.0
pip install requests==2.31.0
pip install python-dotenv==1.0.0
```

### 3. SQL Server ODBC Driver
Download and install: [Microsoft ODBC Driver 17 for SQL Server](https://docs.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server)

## Step 1: Install Ollama

### Download Ollama
1. Go to https://ollama.ai/
2. Download the Windows installer
3. Run the installer as Administrator
4. Follow the installation prompts

### Install Mistral Model
Open Command Prompt and run:
```bash
ollama pull mistral:7b
```
This will download ~4GB model file.

### Test Ollama
```bash
ollama run mistral:7b "Hello, are you working?"
```
You should see a response from the AI.

## Step 2: Database Setup

### Run Database Schema Changes
1. Open SQL Server Management Studio or Azure Data Studio
2. Connect to your Azure SQL Database: `kykmarketserver.database.windows.net`
3. Run the SQL script: `database_schema_changes.sql`

### Verify Changes
```sql
SELECT 
    COUNT(*) as TotalProducts,
    SUM(CASE WHEN PStatus = 0 THEN 1 ELSE 0 END) as PendingProducts,
    SUM(CASE WHEN RequiresManualReview = 1 THEN 1 ELSE 0 END) as ManualReviewNeeded
FROM Product;
```

## Step 3: Test the Python Script

### Manual Test
1. Open Command Prompt
2. Navigate to the project directory
3. Run: `python product_approval_ai.py`

### Expected Output
```
2024-01-XX XX:XX:XX - INFO - Database connection established successfully
2024-01-XX XX:XX:XX - INFO - Found X pending products
2024-01-XX XX:XX:XX - INFO - Processing product X: Product Name
2024-01-XX XX:XX:XX - INFO - Product X: AI APPROVE - Reason
2024-01-XX XX:XX:XX - INFO - Processing complete: X total, X successful, X failed
```

### Check Logs
Logs are saved to: `C:\AI_Approval_Logs\ai_approval_YYYYMMDD.log`

## Step 4: Deploy ASP.NET Changes

### Build and Deploy
1. Open the project in Visual Studio
2. Build the solution (Ctrl+Shift+B)
3. Publish to Azure (Right-click project → Publish)

### Verify Admin Panel
1. Go to your website: https://yurtlar.azurewebsites.net/
2. Login as admin
3. Go to Admin → Approvals
4. You should see new columns: "AI Durumu" and override buttons

## Step 5: Setup Automatic Processing

### Option A: Using Batch Script (Recommended)
1. Right-click `setup_task_scheduler.bat`
2. "Run as Administrator"
3. Follow the prompts

### Option B: Manual Task Scheduler Setup
1. Press `Win + R`, type `taskschd.msc`
2. Click "Create Basic Task"
3. Name: "AI Product Approval"
4. Trigger: Every 10 minutes
5. Action: Start a program
6. Program: `python`
7. Arguments: `"C:\path\to\product_approval_ai.py"`
8. Start in: `C:\path\to\project\`

## Step 6: Testing with Sample Data

### Add Test Products
1. Login to your website
2. Add a few test products with different scenarios:
   - Normal student item (should be approved)
   - Item with inappropriate content (should be rejected)
   - Item with unclear description (might need manual review)

### Monitor Processing
1. Check logs: `C:\AI_Approval_Logs\`
2. Check admin panel for AI decisions
3. Test override functionality

## Troubleshooting

### Common Issues

#### 1. "Cannot connect to Ollama API"
- Make sure Ollama is running: `ollama serve`
- Check if port 11434 is available
- Restart Ollama if needed

#### 2. "Database connection failed"
- Verify connection string in `product_approval_ai.py`
- Check if Azure SQL Database is accessible
- Verify ODBC Driver installation

#### 3. "Model not found"
- Run: `ollama list` to see installed models
- Install missing model: `ollama pull mistral:7b`

#### 4. Task Scheduler not working
- Check if Python is in PATH
- Verify script path in task
- Run task manually to see errors

### Performance Optimization

#### 1. Model Selection
- **Mistral:7b** (~4GB) - Good balance of speed/accuracy
- **Llama2:7b** (~4GB) - Faster, slightly less accurate
- **CodeLlama:7b** (~4GB) - Better for structured responses

#### 2. Processing Frequency
- Default: Every 10 minutes
- Adjust in Task Scheduler if needed
- Consider reducing frequency during low activity

## Monitoring

### Log Files
- **Location**: `C:\AI_Approval_Logs\`
- **Format**: `ai_approval_YYYYMMDD.log`
- **Rotation**: Daily files

### Admin Panel Indicators
- **AI Approved**: Green robot icon
- **AI Rejected**: Red robot icon
- **Manual Review**: Yellow warning icon
- **Pending**: Gray clock icon

### Database Queries
```sql
-- Check AI processing status
SELECT 
    PStatus,
    AIApproved,
    RequiresManualReview,
    COUNT(*) as Count
FROM Product 
GROUP BY PStatus, AIApproved, RequiresManualReview;

-- Check recent AI decisions
SELECT TOP 10 
    PName, 
    AIReason, 
    AIDecisionDate,
    AIApproved
FROM Product 
WHERE AIDecisionDate IS NOT NULL
ORDER BY AIDecisionDate DESC;
```

## Security Considerations

### 1. Local Processing
- ✅ No data sent to external services
- ✅ Complete privacy
- ✅ No API costs

### 2. Database Security
- Connection string contains credentials
- Consider using Azure Key Vault for production
- Monitor database access logs

### 3. Log Security
- Logs contain product information
- Secure the log directory
- Consider log rotation and cleanup

## Support

### Getting Help
1. Check logs first: `C:\AI_Approval_Logs\`
2. Test Ollama manually: `ollama run mistral:7b "test"`
3. Verify database connection
4. Check Task Scheduler status

### Emergency Stop
To stop AI processing:
```bash
schtasks /delete /tn "AI Product Approval" /f
```

### Manual Override
All AI decisions can be overridden in the admin panel:
1. Go to Admin → Approvals
2. Click the override button (undo icon)
3. Choose approve/reject
4. Add optional reason

## Next Steps

1. **Monitor** AI decisions for accuracy
2. **Adjust** prompts based on results
3. **Fine-tune** approval criteria
4. **Scale** to handle more products
5. **Consider** cloud deployment for 24/7 availability 