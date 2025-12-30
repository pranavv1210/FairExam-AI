# 🎯 Deployment Checklist

## ✅ Problem Solved
Azure subscription region restrictions preventing Azure AI Language service creation have been resolved by consolidating all AI features into Azure OpenAI (GPT-4).

---

## 📋 Your Action Items

### 1. Azure Account Setup (15 minutes)

- [ ] Apply for Azure for Students → https://azure.microsoft.com/free/students/
  - Sign in with .edu email
  - Complete verification
  - Get $100 free credit (no credit card needed)

- [ ] Request Azure OpenAI access → https://aka.ms/oai/access
  - Fill out form (mention Imagine Cup 2026)
  - Wait for approval email (1-3 business days)
  - ⚠️ **DO THIS NOW** - approval takes time

### 2. Create Azure Resources (20 minutes) - After approval

- [ ] Login to [Azure Portal](https://portal.azure.com)
- [ ] Create Azure OpenAI resource
  - Resource Group: `fairexam-ai`
  - Region: **East US**
  - Name: `fairexam-ai-openai`
  - Pricing: Standard S0
- [ ] Deploy GPT-4 model
  - Open Azure OpenAI Studio
  - Deployments → Create new
  - Model: `gpt-4`
  - Deployment name: `gpt-4`
  - Tokens per minute: 10K
- [ ] Copy credentials
  - Keys and Endpoint → Copy KEY 1
  - Copy Endpoint URL

📖 **Detailed guide**: [AZURE_SETUP.md](AZURE_SETUP.md)

### 3. Local Testing (10 minutes)

```powershell
# Backend setup
cd C:\Users\Pranav\Desktop\FairExam-AI\backend

# Create .env file (if not exists)
Copy-Item .env.example .env

# Edit .env with your credentials
notepad .env

# Add these values:
AZURE_OPENAI_ENDPOINT=https://fairexam-ai-openai.openai.azure.com/
AZURE_OPENAI_API_KEY=your-key-here
AZURE_OPENAI_DEPLOYMENT_NAME=gpt-4
AZURE_OPENAI_API_VERSION=2024-02-15-preview

# Start backend
python -m uvicorn main:app --reload
```

Test: http://localhost:8000/health

Expected response:
```json
{
  "status": "healthy",
  "azure_openai_configured": true,
  "message": "Azure OpenAI handles all AI features"
}
```

```powershell
# Frontend setup (new terminal)
cd C:\Users\Pranav\Desktop\FairExam-AI\frontend

# Start frontend
npm run dev
```

Test: http://localhost:5173

- [ ] Upload sample exam ([sample_exam.txt](sample_exam.txt))
- [ ] Upload sample syllabus ([sample_syllabus.txt](sample_syllabus.txt))
- [ ] Click **Analyze**
- [ ] Verify results display correctly

### 4. Deployment (30 minutes)

#### Backend on Render

- [ ] Create account at [render.com](https://render.com)
- [ ] Connect GitHub account
- [ ] Create new Web Service
  - Repository: Your FairExam-AI repo
  - Root directory: `backend`
  - Build command: `pip install -r requirements.txt`
  - Start command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
- [ ] Add environment variables:
  - `AZURE_OPENAI_ENDPOINT`
  - `AZURE_OPENAI_API_KEY`
  - `AZURE_OPENAI_DEPLOYMENT_NAME=gpt-4`
  - `AZURE_OPENAI_API_VERSION=2024-02-15-preview`
- [ ] Deploy
- [ ] Copy your backend URL (e.g., `https://fairexam-ai-backend.onrender.com`)

#### Frontend on Vercel

- [ ] Create account at [vercel.com](https://vercel.com)
- [ ] Connect GitHub account
- [ ] Import FairExam-AI repository
  - Root directory: `frontend`
  - Framework: Vite
- [ ] Add environment variable:
  - `VITE_API_BASE_URL=https://your-backend-url.onrender.com`
- [ ] Deploy
- [ ] Visit your live URL

### 5. Final Testing (10 minutes)

- [ ] Visit production frontend URL
- [ ] Upload test files
- [ ] Run analysis
- [ ] Verify all features work:
  - [ ] Difficulty distribution chart
  - [ ] Bloom's taxonomy chart
  - [ ] Syllabus coverage analysis
  - [ ] Bias detection
  - [ ] Fairness score
  - [ ] Suggestions

---

## 📝 Documentation Files

All updated to reflect the simplified architecture:

- ✅ [README.md](README.md) - Project overview and setup
- ✅ [AZURE_SETUP.md](AZURE_SETUP.md) - Step-by-step Azure OpenAI setup
- ✅ [DEPLOYMENT.md](DEPLOYMENT.md) - Render + Vercel deployment guide
- ✅ [SOLUTION_SUMMARY.md](SOLUTION_SUMMARY.md) - What changed and why

---

## 💰 Cost Estimate

### With $100 Azure for Students Credit:

- **Setup**: $0 (free tier for students)
- **Per analysis**: $0.10-0.20 (GPT-4 tokens)
- **Total analyses possible**: 500-1000
- **Imagine Cup demo**: ~20-50 analyses = **$5-10 total**
- **Remaining credit**: $90-95 for development/testing

### After free credit expires:
- GPT-4: ~$0.10-0.20 per analysis
- Render: Free tier (sufficient for demo)
- Vercel: Free tier (sufficient for demo)

---

## 🆘 Troubleshooting

### "Azure OpenAI access pending"
→ Wait for approval email (1-3 days). App works with fallback heuristics meanwhile.

### "Region not available"
→ Use **East US** - it's the most compatible region for student accounts.

### "Deployment name not found"
→ Ensure GPT-4 deployment is named exactly `gpt-4` (lowercase).

### "Invalid API key"
→ Copy KEY 1 from Azure Portal → Keys and Endpoint. Check for extra spaces.

### Render backend not starting
→ Check environment variables are set correctly in Render dashboard.

### Frontend can't reach backend
→ Update `VITE_API_BASE_URL` in Vercel environment variables.

---

## 🏆 Ready for Imagine Cup 2026!

Once all checkboxes are complete, your FairExam AI application is:
- ✅ Fully functional with Azure OpenAI GPT-4
- ✅ Deployed on production infrastructure
- ✅ Cost-effective within free credits
- ✅ Meeting all Imagine Cup requirements

**Next**: Prepare your Imagine Cup submission with:
- Demo video showing the application
- Architecture diagram (included in README)
- Problem statement and solution (included in README)
- Screenshots of the application
- Impact statement on educational fairness

Good luck with Microsoft Imagine Cup 2026! 🚀
