# simulate.py
import threading
import time
import random

# A generator that yields synthetic attack events for the dashboard
ATTACK_TYPES = [
    "normal", "dos", "probe", "r2l", "u2r",
    "port_scan", "ddos", "brute_force", "sql_injection", "arp_spoofing", "malware"
]

def random_ip():
    return "{}.{}.{}.{}".format(*(random.randint(1,254) for _ in range(4)))

def make_event():
    t = time.time()
    attack = random.choice(ATTACK_TYPES[1:])  # exclude "normal"
    return {
        "timestamp": t,
        "src_ip": random_ip(),
        "dst_ip": random_ip(),
        "src_port": random.randint(1024,65535),
        "dst_port": random.choice([22,80,443,8080,53,3306]),
        "attack_type": attack,
        "confidence": round(random.uniform(0.6,0.99), 3)
    }

class Simulator:
    def __init__(self):
        self.running = False
        self.interval = 1.0
        self.callbacks = []  # functions to call with event

    def register_callback(self, fn):
        self.callbacks.append(fn)

    def start(self, interval=1.0):
        self.interval = interval
        self.running = True
        threading.Thread(target=self._loop, daemon=True).start()

    def stop(self):
        self.running = False

    def _loop(self):
        while self.running:
            ev = make_event()
            for cb in self.callbacks:
                try:
                    cb(ev)
                except Exception as e:
                    print("sim cb error:", e)
            time.sleep(self.interval)
