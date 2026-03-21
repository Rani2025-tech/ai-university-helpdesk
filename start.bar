@echo off
echo Starting AI University Helpdesk...
cd "C:\Users\RANI NAYAK\OneDrive\Projects\ai-university-helpdesk"

echo Activating virtual environment...
call rag_env\Scripts\activate

echo Starting FastAPI backend...
start cmd /k "cd /d C:\Users\RANI NAYAK\OneDrive\Projects\ai-university-helpdesk && rag_env\Scripts\activate && python -m uvicorn backend.main:app --reload"

echo Waiting for backend to start...
timeout /t 5

echo Starting Streamlit frontend...
start cmd /k "cd /d C:\Users\RANI NAYAK\OneDrive\Projects\ai-university-helpdesk && rag_env\Scripts\activate && streamlit run frontend/app.py"

echo.
echo Both servers are starting!
echo Backend: http://localhost:8000
echo Frontend: http://localhost:8501
echo.
pause