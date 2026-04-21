#!/usr/bin/env python3
"""Seed Kütahyalılar with routes, buses, and trips."""
import json, sys, random
from datetime import datetime, timedelta
import urllib.request

BASE = "http://localhost:8000/api/v1"

def api(method, path, token=None, data=None):
    body = json.dumps(data).encode() if data else None
    headers = {"Content-Type": "application/json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    req = urllib.request.Request(f"{BASE}{path}", data=body, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req) as res:
            return json.loads(res.read())
    except urllib.error.HTTPError as e:
        return json.loads(e.read()) if e.fp else {}

# Login
login = api("POST", "/auth/login", data={"email": "admin@kutahyalilar.com", "password": "admin1234"})
token = login.get("access_token")
if not token:
    print("ERROR: Could not login as admin. Run seed.sh first.")
    sys.exit(1)

# Seed routes
routes_data = [
    ("İstanbul", "Ankara", 450, 360), ("İstanbul", "İzmir", 560, 480),
    ("Ankara", "İstanbul", 450, 360), ("Ankara", "Antalya", 550, 420),
    ("İzmir", "İstanbul", 560, 480), ("Kütahya", "İstanbul", 300, 270),
    ("İstanbul", "Kütahya", 300, 270), ("Kütahya", "Ankara", 310, 280),
    ("Ankara", "Kütahya", 310, 280), ("İzmir", "Kütahya", 340, 300),
    ("Kütahya", "İzmir", 340, 300), ("Kütahya", "Antalya", 400, 360),
    ("Antalya", "Kütahya", 400, 360), ("Bursa", "İstanbul", 155, 150),
    ("İstanbul", "Bursa", 155, 150),
]

route_ids = []
for origin, dest, km, dur in routes_data:
    r = api("POST", "/routes/", token, {"origin": origin, "destination": dest, "distance_km": km, "estimated_duration_min": dur})
    rid = r.get("id", "")
    if rid:
        route_ids.append(rid)
        print(f"  Route: {origin} → {dest} ({rid[:8]})")
    else:
        print(f"  SKIP:  {origin} → {dest} ({r})")
print(f"Routes: {len(route_ids)}")

# Seed buses
buses_data = [
    ("34 KTH 01", 45, "standard"), ("34 KTH 02", 45, "standard"),
    ("34 KTH 03", 36, "luxury"), ("34 KTH 04", 45, "standard"),
    ("34 KTH 05", 36, "luxury"),
]
bus_ids = []
for plate, seats, btype in buses_data:
    b = api("POST", "/buses/", token, {"plate": plate, "total_seats": seats, "bus_type": btype})
    bid = b.get("id", "")
    if bid:
        bus_ids.append(bid)
        print(f"  Bus:   {plate} ({bid[:8]})")
    else:
        print(f"  SKIP:  {plate} ({b})")
print(f"Buses: {len(bus_ids)}")

# Seed trips for next 7 days
if not route_ids or not bus_ids:
    print("ERROR: No routes or buses.")
    sys.exit(1)

trip_count = 0
for day in range(7):
    dt = datetime.now() + timedelta(days=day)
    date_str = dt.strftime("%Y-%m-%d")
    for ri, rid in enumerate(route_ids):
        bid = bus_ids[ri % len(bus_ids)]
        for hour in [8, 10, 14, 18]:
            dep = f"{date_str}T{hour:02d}:00:00"
            arr_h = hour + random.randint(4, 6)
            arr = f"{date_str}T{arr_h:02d}:00:00"
            price = random.randint(250, 650)
            t = api("POST", "/trips/", token, {
                "route_id": rid, "bus_id": bid,
                "departure_time": dep, "arrival_time": arr, "price": price
            })
            if t.get("id"):
                trip_count += 1
print(f"Trips: {trip_count}")
print(f"\nDone! Admin: admin@kutahyalilar.com / admin1234")
