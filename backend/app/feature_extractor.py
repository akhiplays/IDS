# feature_extractor.py
# Simple example: convert a packet flow or a single packet into features compatible
# with the trainer. For a production-level mapping you'd align these to NSL-KDD features.
try:
    from scapy.all import rdpcap, IP
except Exception:
    rdpcap = None
    IP = None

import numpy as np
import pandas as pd
from collections import Counter
import time


def extract_basic_flow_features_from_pcap(pcap_path, max_flows=5000):
    """
    Very simple extractor: aggregates packets by 5-tuple (src,dst, sport,dport,proto)
    and returns numeric features per flow:
      - pkt_count, byte_count, avg_pkt_size, duration, src_port, dst_port, protocol_num, flags_count
    """
    if rdpcap is None or IP is None:
        raise RuntimeError("scapy is not available. Install scapy or use pyshark fallback.")
    pkts = rdpcap(pcap_path)
    flows = {}
    for pkt in pkts:
        if not IP in pkt:
            continue
        ip = pkt[IP]
        proto = ip.proto
        sport = getattr(pkt, 'sport', 0)
        dport = getattr(pkt, 'dport', 0)
        key = (ip.src, ip.dst, sport, dport, proto)
        ts = float(getattr(pkt, 'time', time.time()))
        if key not in flows:
            flows[key] = {"first_ts": ts, "last_ts": ts, "pkt_count": 0, "byte_count": 0, "flags": Counter()}
        flows[key]["pkt_count"] += 1
        flows[key]["byte_count"] += len(pkt)
        flows[key]["last_ts"] = ts
        # TCP flags
        if proto == 6 and hasattr(pkt, 'flags'):
            flows[key]["flags"][str(pkt.flags)] += 1
    # convert to list
    rows = []
    for k,v in list(flows.items())[:max_flows]:
        duration = v["last_ts"] - v["first_ts"]
        avg_pkt = v["byte_count"] / v["pkt_count"] if v["pkt_count"]>0 else 0
        protocol = k[4]
        flags_count = sum(v["flags"].values())
        rows.append([
            v["pkt_count"], v["byte_count"], avg_pkt, duration,
            k[2], k[3], protocol, flags_count
        ])
    df = pd.DataFrame(rows, columns=[
        "pkt_count","byte_count","avg_pkt_size","duration",
        "src_port","dst_port","protocol","flags_count"
    ])
    return df
