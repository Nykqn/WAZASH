"""Endpoint Simulator — Simule des endpoints qui envoient des heartbeats périodiquement."""

import os
import time
import random
from datetime import datetime, timezone

import requests

API_BASE = os.environ.get("API_BASE", "http://wazash-backend:8000/api/v1")
ENDPOINTS = os.environ.get("ENDPOINTS", "ep-web-01,ep-db-01,ep-fw-01,ep-wks-01").split(",")
INTERVAL = int(os.environ.get("INTERVAL_SECONDS", "10"))


def send_heartbeat(endpoint_id: str) -> None:
    status = random.choices(["up", "down"], weights=[95, 5])[0]
    payload = {
        "endpoint_id": endpoint_id,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "status": status,
    }
    try:
        resp = requests.post(f"{API_BASE}/heartbeat", json=payload, timeout=5)
        result = "OK" if resp.status_code == 200 else f"HTTP {resp.status_code}"
        print(f"[{datetime.now(timezone.utc).isoformat()}] HB {endpoint_id} -> {status} ({result})")
    except Exception as e:
        print(f"[{datetime.now(timezone.utc).isoformat()}] HB {endpoint_id} -> ERROR: {e}")


def main():
    print(f"Endpoint Simulator started — {len(ENDPOINTS)} endpoints, every {INTERVAL}s")
    print(f"API: {API_BASE}")
    print(f"Endpoints: {', '.join(ENDPOINTS)}")

    while True:
        for ep in ENDPOINTS:
            send_heartbeat(ep)
        time.sleep(INTERVAL)


if __name__ == "__main__":
    main()
