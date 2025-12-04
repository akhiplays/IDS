# Product Requirements Document (PRD)

**Title:** AI-Assisted Intrusion Detection System (AI-IDS) for Network Traffic

## 1. Purpose & Scope

Build a functioning AI-IDS suitable for a college submission that:

- Detects attacks in real time from live capture, logs, and PCAP uploads.
- Labels attack type (multi-class: dos, probe, r2l, u2r, and common network attack labels used for demo).
- Provides a modern dashboard showing active attacks, details, timelines, and simulated attack injection for demos.
- Uses an offline-trained XGBoost model (trained on NSL-KDD) with the model file bundled with the app.

## 2. Stakeholders

- Primary: Student (developer/submitter), course instructor / grader.
- Secondary: Demonstration audience (classmates, TA).

## 3. Goals & Success Criteria

- Functional backend with endpoints for prediction, PCAP upload, live capture control, and WebSocket streaming.
- Dashboard displays live and simulated attacks with details and filtering.
- Reasonable detection accuracy on NSL-KDD test split; include classification metrics in `docs/report.md` and `README.md`.
- Deliver a single folder containing code, model artifacts, dataset pointers, and a clear README to run locally.

## 4. Non-Goals

- Not a production-ready IDS (no clustering, high-availability, hardened security, or optimized throughput).
- No online continuous retraining — model retraining is offline only.

## 5. User Stories

- As an instructor, I can run the app locally and observe simulated attacks on a dashboard.
- As a student, I can upload a PCAP and see detected attack types in the UI.
- As a demo user, I can enable live capture on a test network and see detection events in real time.

## 6. Functional Requirements

- Model: XGBoost classifier trained on NSL-KDD, serialized as `joblib` artifacts.
- Backend endpoints (FastAPI):
  - `POST /predict`: Accepts feature vector or extracted flow and returns class + confidence.
  - `POST /upload_pcap`: Accepts PCAP, parses flows, runs inference, returns events.
  - `POST /start_capture` & `POST /stop_capture`: Start/stop live capture (admin required).
  - `WebSocket /ws`: Push detection events and receive simple client messages.
  - `POST /simulate/start` & `POST /simulate/stop`: Server-side virtual attack simulator for demos.
- Frontend features (React + Tailwind):
  - Live events timeline, recent event list, event details pane, filters, and charts for counts and top sources.
  - Virtual attack controller to start/stop demo events.
- Feature extraction:
  - Extract numeric features for each flow matching the mapping used during training.
  - Provide clear mapping documentation between capture features and training features.
- Packaging:
  - Single deliverable folder structure with `backend/`, `frontend/`, `model/`, `data/`, and `docs/`.

## 7. Nonfunctional Requirements

- Usable on local Windows/Linux with admin permissions for live capture.
- Inference latency: target <200ms per flow.
- Dashboard responsive and mobile-friendly.

## 8. Data & Privacy

- NSL-KDD dataset used for training; include only pointers and preprocessing scripts (do not redistribute copyrighted raw dataset files).
- Sample PCAPs (if included) will contain no PII.
- When using live capture, only capture traffic on test networks or with explicit permission.

## 9. Risks & Mitigations

- Risk: Live packet capture requires admin privileges — mitigate by providing PCAP upload and simulator.
- Risk: Feature mismatch between live flow extraction and NSL-KDD training features — mitigate with a documented mapping and fallback heuristics in the backend.
- Risk: Model performance may vary on real network traces — report evaluation metrics and emphasize that this is a demo-grade model.

## 10. High-level Architecture

- Frontend (React + Tailwind) ↔ Backend (FastAPI, Uvicorn) via HTTPS and WebSocket.
- Backend handles feature extraction from PCAPs or live capture (Scapy/pyshark), loads the XGBoost model, performs predictions, and pushes events to the UI.
- Backend supports a simulator that generates synthetic labeled events for demonstration.

## 11. Acceptance Criteria

- Backend serves `/health`, `/upload_pcap`, `/predict`, simulation endpoints, and `/ws` working with the frontend.
- Frontend connects to `/ws` and visualizes incoming events; simulator can generate events visible in the dashboard.
- Training script can produce `model/xgb_model.joblib` and print classification metrics saved to `docs/report.md`.
- README includes step-by-step setup, training instructions, and notes on feature mapping and permissions.

## 12. Deliverables

- `backend/` with FastAPI app, feature extraction, simulator, and training scripts.
- `frontend/` with React/Tailwind dashboard source.
- `model/` folder with serialized model artifacts (created after training).
- `data/` with instructions to download NSL-KDD.
- `docs/` with `abstract.md`, `PRD.md`, and `report.md`.
- `README.md` with run instructions and grading checklist.

---

If you want, I can now:

- Generate the `README.md` summary and `docs/report.md` (with suggested content and placeholder for training metrics),
- Create a small sample PCAP and a simple upload UI in the frontend,
- Or produce a downloadable zip of the full project skeleton.

Tell me which next step you'd like me to implement.