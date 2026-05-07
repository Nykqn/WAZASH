"""Attacker Simulator — Simule des attaques en envoyant des événements de sécurité."""

import os
import time
import random
from datetime import datetime, timezone

import requests

API_BASE = os.environ.get("API_BASE", "http://wazash-backend:8000/api/v1")
INTERVAL = int(os.environ.get("INTERVAL_SECONDS", "30"))
API_KEY = os.environ.get("API_KEY", "wazash-agent-key-2026")
HEADERS = {"X-API-Key": API_KEY, "Content-Type": "application/json"}

ATTACK_TYPES = [
    {"event_type": "intrusion", "severity": "high", "details": {"source_ip": "10.0.0.50", "target_port": 22, "method": "ssh_bruteforce"}},
    {"event_type": "malware", "severity": "critical", "details": {"file": "/tmp/payload.exe", "signature": "Trojan.Gen", "hash": "abc123"}},
    {"event_type": "intrusion", "severity": "high", "details": {"source_ip": "172.16.0.99", "target_port": 443, "method": "sql_injection"}},
    {"event_type": "scan", "severity": "low", "details": {"source_ip": "10.0.0.200", "ports_scanned": 1024, "type": "nmap"}},
]

TARGETS = ["ep-web-01", "ep-db-01", "ep-fw-01", "ep-wks-01"]


def send_attack() -> None:
    attack = random.choice(ATTACK_TYPES)
    target = random.choice(TARGETS)
    payload = {
        "endpoint_id": target,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "event_type": attack["event_type"],
        "severity": attack["severity"],
        "details": attack["details"],
    }
    try:
        resp = requests.post(f"{API_BASE}/events", json=payload, headers=HEADERS, timeout=5)
        result = "OK" if resp.status_code == 200 else f"HTTP {resp.status_code}"
        print(f"[{datetime.now(timezone.utc).isoformat()}] ATTACK {attack['event_type']} -> {target} ({result})")
    except Exception as e:
        print(f"[{datetime.now(timezone.utc).isoformat()}] ATTACK -> ERROR: {e}")


def main():
    print(f"Attacker Simulator started — attacks every ~{INTERVAL}s")
    print(f"API: {API_BASE}")

    while True:
        send_attack()
        # Random delay between attacks (50-150% of interval)
        delay = INTERVAL * random.uniform(0.5, 1.5)
        time.sleep(delay)


if __name__ == "__main__":
    main()
