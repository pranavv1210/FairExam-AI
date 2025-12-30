# FairExam AI - Setup and Run Guide

## Quick Start Commands

### Backend Setup
```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

### Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

## Environment Configuration

1. Copy `.env.example` to `.env` in root directory
2. Fill in your Azure credentials:
   - Azure OpenAI endpoint and API key
   - Azure AI Language endpoint and API key

📖 **Need help getting Azure credentials? See [AZURE_SETUP.md](AZURE_SETUP.md)**

## Testing the Application

1. Start backend (runs on port 8000)
2. Start frontend (runs on port 3000)
3. Open http://localhost:3000
4. Upload `sample_exam.txt` and `sample_syllabus.txt`
5. Click "Analyze Paper"
6. View results in 30-60 seconds

## Troubleshooting

### Backend won't start
- Check Python version (3.10+)
- Ensure virtual environment is activated
- Verify all dependencies installed

### Frontend won't start
- Check Node.js version (18+)
- Delete node_modules and run `npm install` again
- Check for port conflicts

### Analysis fails
- Verify Azure credentials in .env file
- Check Azure service quotas
- Ensure files are in correct format (PDF or TXT)

## Demo Tips

1. Keep sample files ready
2. Ensure stable internet for Azure API calls
3. Test complete flow before demo
4. Explain Azure AI integration clearly
5. Show fairness score calculation transparency
