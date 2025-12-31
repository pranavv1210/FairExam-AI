# 🚀 Deployment Guide - FairExam AI

This guide walks you through deploying FairExam AI with **backend on Render** and **frontend on Vercel**.

---

## 📋 Prerequisites

- GitHub account
- Render account (free tier available)
- Vercel account (free tier available)
- Azure OpenAI and Azure AI Language credentials

📖 **Don't have Azure credentials yet? See [AZURE_SETUP.md](AZURE_SETUP.md) for complete setup guide**

---

## 🔧 Part 1: Deploy Backend on Render

### Step 1: Push Code to GitHub

```bash
# Initialize git (if not already done)
git init
git add .
git commit -m "Initial commit - FairExam AI"

# Create a new repository on GitHub and push
git remote add origin https://github.com/YOUR_USERNAME/fairexam-ai.git
git branch -M main
git push -u origin main
```

### Step 2: Deploy on Render

1. **Go to [Render Dashboard](https://dashboard.render.com/)**

2. **Click "New +" → "Web Service"**

3. **Connect your GitHub repository:**
   - Select "fairexam-ai" repository
   - Click "Connect"

4. **Configure the Web Service:**
   - **Name:** `fairexam-ai-backend`
   - **Region:** Choose closest to your location
   - **Branch:** `main`
   - **Root Directory:** `backend`
   - **Runtime:** `Python 3`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn main:app --host 0.0.0.0 --port $PORT`
   - **Instance Type:** `Free` (or paid for production)

5. **Add Environment Variables:**
   Click "Advanced" → "Add Environment Variable" and add:
   
   ```
   AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
   AZURE_OPENAI_API_KEY=your_api_key_here
   AZURE_OPENAI_DEPLOYMENT_NAME=gpt-4
   AZURE_OPENAI_API_VERSION=2024-02-15-preview
   AZURE_LANGUAGE_ENDPOINT=https://your-resource.cognitiveservices.azure.com/
   AZURE_LANGUAGE_API_KEY=your_api_key_here
   ```

6. **Click "Create Web Service"**

7. **Wait for deployment** (3-5 minutes)
   - Render will build and deploy your backend
   - You'll get a URL like: `https://fairexam-ai.onrender.com`

8. **Test the backend:**
   - Visit: `https://fairexam-ai.onrender.com/health`
   - Should see: `{"status": "healthy", ...}`

### Step 3: Update CORS Settings (if needed)

After deployment, if you need to update allowed origins:

1. Edit `backend/main.py`
2. Update the `allow_origins` in CORS middleware:
   ```python
   allow_origins=[
       "http://localhost:3000",
       "http://localhost:5173",
       "https://fair-exam-ai.vercel.app"  # Add your Vercel URL
   ],
   ```
3. Commit and push changes (Render auto-deploys)

---

## 🌐 Part 2: Deploy Frontend on Vercel

### Step 1: Update Frontend Configuration

1. **Create `.env` file in `frontend/` folder:**
   ```bash
   cd frontend
   # Copy the example
   cp .env.example .env
   ```

2. **Edit `.env` with your Render backend URL:**
   ```
   VITE_API_URL=https://fairexam-ai.onrender.com
   ```

3. **Update `vercel.json` with your backend URL:**
   - Open `frontend/vercel.json`
   - Replace `your-backend-url.onrender.com` with your actual Render URL

4. **Commit changes:**
   ```bash
   git add .
   git commit -m "Configure for Vercel deployment"
   git push
   ```

### Step 2: Deploy on Vercel

1. **Go to [Vercel Dashboard](https://vercel.com/dashboard)**

2. **Click "Add New..." → "Project"**

3. **Import Git Repository:**
   - Connect your GitHub account (if not already)
   - Select your `fairexam-ai` repository
   - Click "Import"

4. **Configure Project:**
   - **Framework Preset:** Vite
   - **Root Directory:** `frontend`
   - **Build Command:** `npm run build` (auto-detected)
   - **Output Directory:** `dist` (auto-detected)
   - **Install Command:** `npm install` (auto-detected)

5. **Add Environment Variables:**
   - Click "Environment Variables"
   - Add:
     ```
     Name: VITE_API_URL
     Value: https://fairexam-ai.onrender.com
     ```
   - Click "Add"

6. **Click "Deploy"**

7. **Wait for deployment** (1-2 minutes)
   - Vercel will build and deploy your frontend
   - You'll get a URL like: `https://fairexam-ai.vercel.app`

8. **Test the deployment:**
   - Visit your Vercel URL
   - Upload sample files and test the analysis

---

## 🔄 Part 3: Final Configuration

### Update Backend CORS for Production

1. **Update `backend/main.py`:**
   ```python
   app.add_middleware(
       CORSMiddleware,
       allow_origins=[
           "http://localhost:3000",
           "http://localhost:5173",
           "https://fairexam-ai.vercel.app",  # Your Vercel URL
           "https://*.vercel.app"  # All Vercel preview deployments
       ],
       allow_credentials=True,
       allow_methods=["*"],
       allow_headers=["*"],
   )
   ```

2. **Commit and push:**
   ```bash
   git add backend/main.py
   git commit -m "Update CORS for production"
   git push
   ```

3. **Render will auto-deploy** the changes

---

## ✅ Verification Checklist

After deployment, verify:

- [ ] Backend health check works: `https://your-backend.onrender.com/health`
- [ ] Frontend loads: `https://your-frontend.vercel.app`
- [ ] File upload works
- [ ] Analysis completes successfully
- [ ] Results display correctly
- [ ] Charts render properly
- [ ] Mobile responsive design works

---

## 🔧 Troubleshooting

### Backend Issues

**Problem:** "Application failed to start"
- Check Render logs in dashboard
- Verify all environment variables are set
- Check Python version compatibility

**Problem:** "Module not found"
- Ensure `requirements.txt` includes all dependencies
- Verify build command: `pip install -r requirements.txt`

**Problem:** Azure API errors
- Verify Azure credentials in environment variables
- Check Azure API quotas and limits
- Test credentials using `/api/test-azure-services` endpoint

### Frontend Issues

**Problem:** "Failed to load resource: net::ERR_FAILED"
- Verify `VITE_API_URL` environment variable
- Check backend CORS settings
- Ensure backend is running

**Problem:** "Network Error"
- Check backend URL in `vercel.json`
- Verify Render backend is running
- Test backend directly: `curl https://your-backend.onrender.com/health`

**Problem:** Environment variable not working
- Ensure variable starts with `VITE_`
- Redeploy after adding environment variables
- Check Vercel deployment logs

### CORS Errors

If you see CORS errors in browser console:

1. Add your Vercel URL to backend CORS settings
2. Ensure `allow_credentials=True`
3. Check that backend allows all methods and headers
4. Redeploy backend after changes

---

## 🔄 Continuous Deployment

Both platforms support automatic deployments:

### Render (Backend)
- Automatically redeploys on every push to `main` branch
- Manual deploy: Render Dashboard → "Manual Deploy" → "Deploy latest commit"

### Vercel (Frontend)
- Automatically redeploys on every push to `main` branch
- Preview deployments for pull requests
- Manual deploy: Vercel Dashboard → Project → "Deployments" → "Redeploy"

---

## 🌍 Custom Domains (Optional)

### For Backend (Render)
1. Go to Render Dashboard → Your service → "Settings"
2. Scroll to "Custom Domains"
3. Add your domain and follow DNS configuration

### For Frontend (Vercel)
1. Go to Vercel Dashboard → Your project → "Settings" → "Domains"
2. Add your domain
3. Update DNS records as instructed

---

## 💰 Free Tier Limitations

### Render Free Tier
- Spins down after 15 minutes of inactivity
- Cold starts take 30-60 seconds
- 750 hours/month free
- Upgrade to paid plan for always-on service

### Vercel Free Tier
- 100 GB bandwidth/month
- Unlimited deployments
- Automatic HTTPS
- Preview deployments included

---

## 📊 Monitoring

### Backend Monitoring (Render)
- View logs: Render Dashboard → Your service → "Logs"
- Check metrics: "Metrics" tab
- Set up alerts in settings

### Frontend Monitoring (Vercel)
- View analytics: Vercel Dashboard → Project → "Analytics"
- Check deployment logs: "Deployments" tab
- Real-time error tracking available

---

## 🎯 Production Checklist

Before showing to Imagine Cup judges:

- [ ] Backend deployed and accessible
- [ ] Frontend deployed and accessible
- [ ] All Azure credentials configured
- [ ] Test analysis works end-to-end
- [ ] Sample files ready for demo
- [ ] Mobile responsiveness tested
- [ ] HTTPS enabled (automatic on both platforms)
- [ ] Error handling works gracefully
- [ ] Custom domain configured (optional)

---

## 🆘 Getting Help

**Render Documentation:** https://render.com/docs  
**Vercel Documentation:** https://vercel.com/docs  

**Common Issues:**
- Render Build Errors → Check `requirements.txt`
- Vercel Build Errors → Check `package.json`
- CORS Errors → Update `allow_origins` in backend
- Environment Variables → Use Render/Vercel dashboards

---

**Your FairExam AI is now live! 🎉**

Share your URLs:
- Frontend: `https://fairexam-ai.vercel.app`
- Backend API: `https://fairexam-ai-backend.onrender.com`
