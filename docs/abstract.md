# AI-Assisted Intrusion Detection System (AI-IDS)

Project Abstract

This project implements an AI-assisted Intrusion Detection System that analyzes network traffic in real time and from uploaded PCAPs/logs to detect and label malicious activity. The system pairs a Python/FastAPI backend with an XGBoost model trained offline on the NSL-KDD dataset and a modern React + Tailwind dashboard (dark cyber theme). The dashboard shows live and simulated attacks (port scans, DDoS, brute-force, SQL injection, ARP spoofing, malware-like flows and others) with detailed metadata and an events timeline. The backend supports packet capture (Scapy/pyshark), PCAP upload, log ingestion, model inference, and a WebSocket feed to push events to the UI.

Intended as a college project, the deliverable demonstrates the full pipeline: dataset preprocessing and feature engineering for NSL-KDD, offline model training (XGBoost), feature extraction from PCAPs/packets, real-time inference, and a usable security dashboard that visualizes and labels attacks. The project is packaged as a single app folder including backend, frontend, model artifacts, training scripts, and documentation so instructors can run it locally or deploy to the cloud for evaluation.

Key capabilities

- Multi-source input: live capture, PCAP upload, and log ingestion.
- Multi-class labeling: XGBoost model classifies flows into attack categories (dos, probe, r2l, u2r, and others).
- Real-time UI: WebSocket stream pushes detection events to a React/Tailwind dashboard with timeline, details pane, and charts.
- Demo support: server-side virtual attack simulator to demonstrate events without needing destructive network traffic or admin permissions.
- Reproducibility: training scripts for NSL-KDD, packaged model artifacts, and a clear README for setup and evaluation.

Use-case & audience

This project is targeted for academic evaluation and demonstration. Instructors and graders can validate architecture, inspect the training pipeline and metrics, run the app locally, and evaluate detection behavior using bundled sample PCAPs or the simulator. Students and classmates can interactively explore how flows map to model inputs and how the UI surfaces detections for rapid comprehension.

Limitations

This is a demonstration-grade IDS: it is not hardened for production throughput or availability. Live capture requires administrative privileges; the system mitigates this by offering PCAP upload and the simulator for classroom demos.

Deliverables

- `backend/` (FastAPI app, feature extractor, simulator, training scripts)
- `frontend/` (React + Vite + Tailwind dashboard)
- `model/` (trained XGBoost model artifacts)
- `data/` (instructions to obtain NSL-KDD)
- `docs/` (this abstract, PRD, report)
- `README.md` (setup & run instructions)

Contact: see `README.md` for run instructions and reproducibility details.
