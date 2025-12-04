# main.py
from fastapi import FastAPI, UploadFile, File, WebSocket, WebSocketDisconnect
from fastapi.responses import JSONResponse
import uvicorn
import asyncio
import json
import os
import tempfile
from .model import IDSModel
from .feature_extractor import extract_basic_flow_features_from_pcap
from .simulate import Simulator

app = FastAPI(title="AI-IDS Backend")

# load model
MODEL = None
try:
    MODEL = IDSModel()
except Exception as e:
    print("Warning: model failed to load:", e)

# WebSocket manager
class ConnectionManager:
    def __init__(self):
        self.active = []

    async def connect(self, ws: WebSocket):
        await ws.accept()
        self.active.append(ws)

    def disconnect(self, ws: WebSocket):
        if ws in self.active:
            self.active.remove(ws)

    async def broadcast(self, message: dict):
        data = json.dumps(message)
        to_remove = []
        for ws in list(self.active):
            try:
                await ws.send_text(data)
            except Exception:
                to_remove.append(ws)
        for ws in to_remove:
            if ws in self.active:
                self.active.remove(ws)

manager = ConnectionManager()
sim = Simulator()

# connect simulator to broadcaster
def sim_cb(ev):
    # when sim creates an event, schedule broadcast
    asyncio.create_task(manager.broadcast(ev))
sim.register_callback(sim_cb)

@app.get("/health")
async def health():
    return {"status":"ok"}

@app.post("/upload_pcap")
async def upload_pcap(file: UploadFile = File(...)):
    # save temp file
    contents = await file.read()
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pcap") as tmpf:
        tmpf.write(contents)
        tmp_path = tmpf.name
    try:
        df = extract_basic_flow_features_from_pcap(tmp_path)
    except Exception as e:
        try:
            os.remove(tmp_path)
        except:
            pass
        return JSONResponse({"error": f"failed to parse pcap: {e}"}, status_code=400)

    events = []
    for i, row in df.iterrows():
        features = row.values.tolist()
        if MODEL is not None:
            res = MODEL.predict(features)
            label = res.get("label")
            confidence = res.get("confidence")
        else:
            label = "unknown"
            confidence = 0.0
        events.append({
            "timestamp": None,
            "src": None,
            "dst": None,
            "features": features,
            "label": label,
            "confidence": confidence
        })
    try:
        os.remove(tmp_path)
    except:
        pass
    return JSONResponse({"events": events})

@app.post("/simulate/start")
async def start_sim(interval: float = 1.0):
    sim.start(interval)
    return {"sim": "started", "interval": interval}

@app.post("/simulate/stop")
async def stop_sim():
    sim.stop()
    return {"sim":"stopped"}

@app.websocket("/ws")
async def websocket_endpoint(ws: WebSocket):
    await manager.connect(ws)
    try:
        while True:
            data = await ws.receive_text()  # allow client to send pings/requests
            # we simply echo control messages; real implementation could accept commands
            await ws.send_text(json.dumps({"echo": data}))
    except WebSocketDisconnect:
        manager.disconnect(ws)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
