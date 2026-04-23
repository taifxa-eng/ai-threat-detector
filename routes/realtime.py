from fastapi import APIRouter, WebSocket
import asyncio
import random

router = APIRouter()

clients = []

@router.websocket("/ws/alerts")
async def websocket_alerts(websocket: WebSocket):
    await websocket.accept()
    clients.append(websocket)

    try:
        while True:
            # 🔥 محاكاة تنبيه مباشر
            alert = {
                "ip": f"192.168.1.{random.randint(1,255)}",
                "score": random.randint(20, 100),
                "behavior": random.choice(["DDoS", "SQL Injection", "Malware"]),
                "severity": random.choice(["Low", "Medium", "High", "Critical"])
            }

            await websocket.send_json(alert)
            await asyncio.sleep(3)

    except:
        clients.remove(websocket)