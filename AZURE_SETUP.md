# Azure Setup Guide for FairExam AI

This guide will walk you through setting up Azure OpenAI for FairExam AI.

## What Changed?

**Good news!** Due to Azure subscription restrictions on Azure AI Language service, we've simplified the setup:
- **Before**: Required Azure OpenAI + Azure Language (2 services)
- **Now**: Only requires **Azure OpenAI** (1 service handles everything)

GPT-4 now handles ALL AI features including difficulty analysis, Bloom's taxonomy, bias detection, topic extraction, and semantic matching.

## Prerequisites

- Azure subscription (Azure for Students recommended - **$100 FREE credit**)
- Microsoft account (.edu email for student benefits)

---

## Step 1: Get Azure for Students

1. Go to [Azure for Students](https://azure.microsoft.com/free/students/)
2. Click **Activate now**
3. Sign in with your **.edu email** (or any student-verified Microsoft account)
4. Complete verification (instant or may require document upload)
5. You'll receive **$100 free credit** (no credit card required)

---

## Step 2: Request Azure OpenAI Access

Azure OpenAI requires approval (1-3 business days).

1. Go to [Azure OpenAI Access Request](https://aka.ms/oai/access)
2. Fill out the form:
   - **Email**: Your student email
   - **Subscription**: Azure for Students
   - **Use case**: "Educational project for Microsoft Imagine Cup 2026 - AI-powered exam fairness analysis tool"
   - **Expected usage**: "Low volume for demonstration and testing (~100 requests)"
3. Submit and wait for approval email (usually 1-3 days)

**While waiting**: Continue with the next steps to prepare your project.

---

## Step 3: Create Azure OpenAI Resource

### 3.1: Create the Resource

1. Go to [Azure Portal](https://portal.azure.com)
2. Click **Create a resource**
3. Search for **Azure OpenAI**
4. Click **Create**

### 3.2: Configure Settings

**Basics tab:**
- **Subscription**: Azure for Students
- **Resource group**: Click "Create new" → Name it `fairexam-ai`
- **Region**: Select **East US** (most compatible region)
- **Name**: `fairexam-ai-openai` (must be globally unique)
- **Pricing tier**: **Standard S0**

Click **Next** through remaining tabs, then click **Review + Create** → **Create**

Wait 2-3 minutes for deployment.

---

## Step 4: Deploy GPT-4 Model

1. Once deployment completes, click **Go to resource**
2. In the left menu, click **Resource Management** → **Keys and Endpoint**
3. **Copy and save**:
   - **Endpoint**: (e.g., `https://fairexam-ai-openai.openai.azure.com/`)
   - **KEY 1**: (32-character string)

4. Go to **Model deployments** → Click **Manage Deployments**
5. This opens **Azure OpenAI Studio** → Click **Deployments**
6. Click **+ Create new deployment**
7. Configure deployment:
   - **Model**: Select **gpt-4**
   - **Deployment name**: `gpt-4` (exactly this - code expects this name)
   - **Model version**: Latest (auto-updates)
   - **Deployment type**: Standard
   - **Tokens per minute rate limit**: 10K (adjust as needed)
8. Click **Create**

---

## Step 5: Update Your .env File

Create a `.env` file in the `backend` directory (if not already exists):

```bash
# Create .env file from template
Copy-Item .env.example .env
```

Edit `.env` with your credentials:

```env
# Azure OpenAI Configuration (handles ALL AI features)
AZURE_OPENAI_ENDPOINT=https://fairexam-ai-openai.openai.azure.com/
AZURE_OPENAI_API_KEY=your-32-character-key-here
AZURE_OPENAI_DEPLOYMENT_NAME=gpt-4
AZURE_OPENAI_API_VERSION=2024-02-15-preview
```

**Replace**:
- `AZURE_OPENAI_ENDPOINT`: Your endpoint from Step 4 (with trailing `/`)
- `AZURE_OPENAI_API_KEY`: KEY 1 from Step 4
- `AZURE_OPENAI_DEPLOYMENT_NAME`: Must be `gpt-4` (what you named it in Step 4)

---

## Step 6: Test Locally

```powershell
# Navigate to backend
cd C:\Users\Pranav\Desktop\FairExam-AI\backend

# Start the server
python -m uvicorn main:app --reload
```

Visit `http://localhost:8000/health` - You should see:
```json
{
  "status": "healthy",
  "azure_openai": "connected"
}
```

---

## Cost Breakdown

### Azure for Students
- **$100 free credit** (lasts 12 months)
- No credit card required
- Renews annually if you're still a student

### Azure OpenAI Pricing
- **GPT-4**: ~$0.03 per 1K input tokens, ~$0.06 per 1K output tokens
- **Per analysis**: ~$0.10-0.20 (5-10K tokens total)
- **Your free credit**: ~500-1000 full analyses
- **More than enough for Imagine Cup demo + testing**

---

## Troubleshooting

### "Azure OpenAI access not yet approved"
- **Solution**: Wait for approval email (1-3 days). App will use fallback heuristics until then.

### "Region 'X' not available"
- **Solution**: Use **East US** - it's the most widely available region for student accounts.

### "Deployment name not found"
- **Solution**: Make sure you named the deployment exactly `gpt-4` in Step 4.

### "Invalid API key"
- **Solution**: Copy KEY 1 again from Keys and Endpoint page. Make sure no extra spaces.

---

## Next Steps

1. ✅ Azure OpenAI configured
2. Test locally (see Step 6)
3. Deploy to Render (see [DEPLOYMENT.md](DEPLOYMENT.md))
4. Test production deployment
5. Submit to Microsoft Imagine Cup 2026!

---

## Need Help?

- [Azure OpenAI Documentation](https://learn.microsoft.com/azure/ai-services/openai/)
- [Azure for Students FAQ](https://azure.microsoft.com/free/students/faq/)
- [Azure Support](https://azure.microsoft.com/support/)

**For Imagine Cup participants**: You can get additional support through the Microsoft Imagine Cup support channels.
