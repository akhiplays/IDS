# AI-Assisted Intrusion Detection System (AI-IDS)

This repository contains a college-project-ready AI-IDS demo: a FastAPI backend with an XGBoost model trained on NSL-KDD, and a React + Tailwind dashboard that displays detections via WebSocket.

Quick start (Backend):

1. Create a Python virtual environment and install dependencies:

```powershell
cd "c:\Users\User\Downloads\New Project\backend\app"
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

2. (Optional) Train model using NSL-KDD data placed in `data/NSL-KDD/`:

```powershell
cd "c:\Users\User\Downloads\New Project\backend\scripts"
python train_xgboost.py
```

3. Run backend:

```powershell
cd "c:\Users\User\Downloads\New Project\backend\app"
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Frontend:

1. Install node deps and start dev server:

```powershell
cd "c:\Users\User\Downloads\New Project\frontend"
npm install
npm run dev
```

2. Open the Vite URL (usually `http://localhost:5173`) and the dashboard should connect to the backend WebSocket at `ws://localhost:8000/ws`.

Notes:
- Live packet capture requires admin privileges and additional system dependencies (Npcap/WinPcap on Windows). The app supports PCAP upload for analysis without admin access.
- See `docs/` for the abstract and PRD. Add training metrics to `docs/report.md` after training.

