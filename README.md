# 🎓 FairExam AI

**AI-Powered Exam Paper Fairness & Bias Detection System**

[![Microsoft Imagine Cup 2026](https://img.shields.io/badge/Imagine%20Cup-2026-blue)](https://imaginecup.microsoft.com/)
[![Azure OpenAI](https://img.shields.io/badge/Azure-OpenAI-orange)](https://azure.microsoft.com/en-us/products/ai-services/openai-service)

---

## 🎯 Problem Statement

Educational institutions lack automated tools to ensure exam question papers are **fair, balanced, and unbiased**. This leads to:

- ❌ Uneven difficulty distribution
- ❌ Over-focus on certain syllabus units
- ❌ Ignoring Bloom's taxonomy balance
- ❌ Subjective human judgment
- ❌ Unfair academic outcomes, especially for diverse student populations

---

## 💡 Solution

**FairExam AI** is a web application that analyzes exam papers using **Microsoft Azure OpenAI** to provide:

✅ **Difficulty Distribution Analysis** - GPT-4 powered classification  
✅ **Bloom's Taxonomy Mapping** - Cognitive level assessment  
✅ **Syllabus Coverage Analysis** - AI-powered topic extraction & matching  
✅ **Bias Detection** - Identifies cultural, gender, or socioeconomic bias  
✅ **Fairness Score (0-100)** - Comprehensive fairness metric  
✅ **Actionable Suggestions** - Clear recommendations for improvement  

---

## 🏗️ Architecture

```
┌─────────────────┐
│   Frontend      │
│   (React +      │
│    Vite)        │
└────────┬────────┘
         │
         │ HTTP/REST API
         ▼
┌─────────────────┐
│   Backend       │
│   (FastAPI)     │
└────────┬────────┘
         │
         ▼
    ┌─────────┐
    │ Azure   │
    │ OpenAI  │
    │ (GPT-4) │
    └─────────┘
```

### Technology Stack

**Frontend:**
- React 18
- Vite
- Chart.js (visualizations)
- Axios (API calls)

**Backend:**
- Python 3.10+
- FastAPI
- PyPDF2 (document parsing)

**Microsoft AI Services (Core):**
- **Azure OpenAI Service (GPT-4)**
  - Difficulty classification
  - Bloom's taxonomy mapping
  - Bias/ambiguity detection
  - Topic extraction from syllabus
  - Semantic question-topic matching

---

## 🚀 Quick Start

### Prerequisites

- Python 3.10 or higher
- Node.js 18 or higher
- Azure subscription with Azure OpenAI Service

### 1. Clone Repository

```bash
cd FairExam-AI
```

### 2. Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure environment variables
cp ../.env.example .env
# Edit .env with your Azure credentials

# Run backend server
python main.py
```

Backend will run on: `http://localhost:8000`

### 3. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Run development server
npm run dev
```

Frontend will run on: `http://localhost:3000`

---

## ⚙️ Configuration

Create a `.env` file in the root directory with your Azure credentials:

```env
# Azure OpenAI Configuration
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_API_KEY=your_api_key_here
AZURE_OPENAI_DEPLOYMENT_NAME=gpt-4
AZURE_OPENAI_API_VERSION=2024-02-15-preview

# Azure OpenAI Configuration
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_API_KEY=your_api_key_here
AZURE_OPENAI_DEPLOYMENT_NAME=gpt-4
AZURE_OPENAI_API_VERSION=2024-02-15-preview
```

### Getting Azure Credentials

📖 **See [AZURE_SETUP.md](AZURE_SETUP.md) for complete step-by-step instructions**

Quick summary:

1. **Azure OpenAI Service:**
   - Request access: https://aka.ms/oai/access (approval needed)
   - Create Azure OpenAI resource in [Azure Portal](https://portal.azure.com)
   - Deploy GPT-4 model in Azure OpenAI Studio
   - Get endpoint and API key from "Keys and Endpoint"

💡 **Students:** Get $100 free Azure credit at https://azure.microsoft.com/free/students/

---

## 🎥 Demo Flow

1. **Upload Files:**
   - Upload exam question paper (PDF/TXT)
   - Upload course syllabus (PDF/TXT)

2. **Click "Analyze Paper"**
   - AI analysis takes 30-60 seconds

3. **View Results:**
   - **Fairness Score** (0-100) with interpretation
   - **Difficulty Distribution** chart
   - **Bloom's Taxonomy** distribution chart
   - **Syllabus Coverage** analysis
   - **Bias Analysis** report
   - **Actionable Suggestions** for improvement

---

## 📊 Fairness Score Calculation

The fairness score is calculated using a weighted formula:

```
Fairness Score = 
  40% × Difficulty Balance Score +
  30% × Bloom's Balance Score +
  30% × Syllabus Coverage Score
```

### Component Breakdown

1. **Difficulty Balance (40%)**
   - Ideal: 30% Easy, 50% Medium, 20% Hard
   - Score based on deviation from ideal distribution

2. **Bloom's Balance (30%)**
   - Questions should span multiple cognitive levels
   - Penalizes over-concentration in single level

3. **Syllabus Coverage (30%)**
   - Percentage of topics covered
   - Penalizes over-represented and ignored topics

---

## 🧠 Responsible AI

FairExam AI follows Microsoft's Responsible AI principles:

- ✅ **Transparency:** All AI decisions are explained
- ✅ **Fairness:** Detects and reports bias in questions
- ✅ **Accountability:** Clear reasoning for all scores
- ✅ **No Hallucination:** Results based on actual analysis

### Limitations

- Works best with well-formatted exam papers
- Requires clear syllabus structure
- English language only (current version)
- Not a replacement for human judgment

---

## 📁 Project Structure

```
fairexam-ai/
├── backend/
│   ├── main.py                 # FastAPI application entry
│   ├── requirements.txt        # Python dependencies
│   ├── routes/
│   │   ├── __init__.py
│   │   └── analysis.py         # Analysis API endpoints
│   ├── services/
│   │   ├── __init__.py
│   │   ├── azure_openai.py     # Azure OpenAI GPT-4 integration
│   │   ├── azure_language.py   # Topic extraction (powered by GPT-4)
│   │   └── fairness_engine.py  # Fairness score calculation
│   └── utils/
│       ├── __init__.py
│       ├── pdf_parser.py       # PDF/text extraction
│       └── text_cleaner.py     # Text preprocessing
├── frontend/
│   ├── package.json            # Node dependencies
│   ├── vite.config.js          # Vite configuration
│   ├── index.html              # HTML entry point
│   ├── src/
│   │   ├── main.jsx            # React entry point
│   │   ├── App.jsx             # Main App component
│   │   ├── index.css           # Global styles
│   │   ├── components/
│   │   │   ├── UploadForm.jsx
│   │   │   ├── ResultsDisplay.jsx
│   │   │   └── FairnessScoreCard.jsx
│   │   └── charts/
│   │       ├── DifficultyChart.jsx
│   │       ├── BloomsChart.jsx
│   │       └── CoverageChart.jsx
├── .env.example                # Environment template
├── .gitignore
└── README.md
```

---

## 🔍 API Documentation

### POST `/api/analyze`

Analyze exam paper for fairness.

**Request:**
- `exam_paper` (file): PDF or TXT file
- `syllabus` (file): PDF or TXT file

**Response:**
```json
{
  "fairness_score": 78.5,
  "interpretation": "Good - This exam paper shows...",
  "component_scores": { ... },
  "suggestions": [ ... ],
  "difficulty_analysis": { ... },
  "blooms_analysis": { ... },
  "coverage_analysis": { ... },
  "bias_analysis": { ... }
}
```

### GET `/health`

Health check endpoint.

### GET `/api/test-azure-services`

Test Azure service connectivity.

---

## 🎯 Microsoft Imagine Cup Alignment

This project addresses **UN Sustainable Development Goal 4: Quality Education** by:

1. **Reducing Educational Inequality** - Ensures fair assessment for all students
2. **Responsible AI** - Transparent, explainable AI with bias detection
3. **Meaningful Azure Integration** - Core functionality depends on Azure AI
4. **Scalable Impact** - Can be used by any educational institution
5. **Demo-Ready** - Works end-to-end within 2 minutes

---

## 🛠️ Development

### Running Tests

```bash
cd backend
pytest
```

### Building for Production

**Backend:**
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8000
```

**Frontend:**
```bash
cd frontend
npm run build
npm run preview
```

## 🚀 Deployment

This application can be deployed with:
- **Backend:** Render (or any Python hosting platform)
- **Frontend:** Vercel (or any static hosting platform)

📖 **See [DEPLOYMENT.md](DEPLOYMENT.md) for complete deployment instructions**

Quick deployment:
1. Deploy backend on Render
2. Deploy frontend on Vercel
3. Configure environment variables
4. Update CORS settings

Your app will be live at:
- Frontend: `https://your-app.vercel.app`
- Backend API: `https://your-backend.onrender.com`

---

## 📝 Sample Files

For testing, you can use sample exam papers and syllabi from VTU (Visvesvaraya Technological University) or create your own:

**Exam Paper Format:**
```
1. Define machine learning.
2. Explain the TCP/IP protocol stack.
3. Analyze the time complexity of merge sort.
```

**Syllabus Format:**
```
Unit 1: Introduction to Networks
Unit 2: Data Link Layer
Unit 3: Network Layer
```

---

## 🤝 Contributing

This is a Microsoft Imagine Cup 2026 MVP project. Contributions are welcome after the competition.

---

## 📄 License

This project is created for Microsoft Imagine Cup 2026.

---

## 👥 Team

**Project Creator:** Pranav  
**Competition:** Microsoft Imagine Cup 2026  
**Category:** AI for Social Good  

---

## 📧 Contact

For questions about this project, please reach out via GitHub Issues.

---

## 🙏 Acknowledgments

- **Microsoft Azure** for AI services
- **Microsoft Imagine Cup** for the opportunity
- **Educational institutions** for inspiration

---

**Built with ❤️ for fair education**
