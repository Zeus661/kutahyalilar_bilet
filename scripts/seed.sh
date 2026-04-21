#!/bin/bash
# Seed script for Kütahyalılar bus ticket system
# Creates routes, buses, and upcoming trips via the API gateway.
# Usage: ./scripts/seed.sh

set -e

BASE="http://localhost:8000/api/v1"

echo "=== Creating admin user ==="
ADMIN_RES=$(curl -s -X POST "$BASE/auth/register" \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@kutahyalilar.com","password":"admin1234"}')
echo "$ADMIN_RES"
# Manually set admin flag in DB
ADMIN_ID=$(echo "$ADMIN_RES" | python3 -c "import sys,json; print(json.load(sys.stdin)['id'])" 2>/dev/null || echo "")

echo ""
echo "=== Logging in as admin ==="
LOGIN_RES=$(curl -s -X POST "$BASE/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@kutahyalilar.com","password":"admin1234"}')
TOKEN=$(echo "$LOGIN_RES" | python3 -c "import sys,json; print(json.load(sys.stdin)['access_token'])")
AUTH="Authorization: Bearer $TOKEN"

echo ""
echo "=== Seeding routes ==="
declare -A ROUTES
ROUTES["r1"]='{"origin":"İstanbul","destination":"Ankara","distance_km":450,"estimated_duration_min":360}'
ROUTES["r2"]='{"origin":"İstanbul","destination":"İzmir","distance_km":560,"estimated_duration_min":480}'
ROUTES["r3"]='{"origin":"Ankara","destination":"İstanbul","distance_km":450,"estimated_duration_min":360}'
ROUTES["r4"]='{"origin":"Ankara","destination":"Antalya","distance_km":550,"estimated_duration_min":420}'
ROUTES["r5"]='{"origin":"İzmir","destination":"İstanbul","distance_km":560,"estimated_duration_min":480}'
ROUTES["r6"]='{"origin":"Kütahya","destination":"İstanbul","distance_km":300,"estimated_duration_min":270}'
ROUTES["r7"]='{"origin":"İstanbul","destination":"Kütahya","distance_km":300,"estimated_duration_min":270}'
ROUTES["r8"]='{"origin":"Kütahya","destination":"Ankara","distance_km":310,"estimated_duration_min":280}'
ROUTES["r9"]='{"origin":"Ankara","destination":"Kütahya","distance_km":310,"estimated_duration_min":280}'
ROUTES["r10"]='{"origin":"İzmir","destination":"Kütahya","distance_km":340,"estimated_duration_min":300}'
ROUTES["r11"]='{"origin":"Kütahya","destination":"İzmir","distance_km":340,"estimated_duration_min":300}'
ROUTES["r12"]='{"origin":"Kütahya","destination":"Antalya","distance_km":400,"estimated_duration_min":360}'
ROUTES["r13"]='{"origin":"Antalya","destination":"Kütahya","distance_km":400,"estimated_duration_min":360}'
ROUTES["r14"]='{"origin":"Bursa","destination":"İstanbul","distance_km":155,"estimated_duration_min":150}'
ROUTES["r15"]='{"origin":"İstanbul","destination":"Bursa","distance_km":155,"estimated_duration_min":150}'

ROUTE_IDS=()
for key in $(echo "${!ROUTES[@]}" | tr ' ' '\n' | sort); do
  RES=$(curl -s -X POST "$BASE/routes/" -H "Content-Type: application/json" -H "$AUTH" -d "${ROUTES[$key]}")
  RID=$(echo "$RES" | python3 -c "import sys,json; print(json.load(sys.stdin)['id'])" 2>/dev/null || echo "skip")
  echo "Route $key: $RID"
  ROUTE_IDS+=("$RID")
done

echo ""
echo "=== Seeding buses ==="
declare -A BUSES
BUSES["b1"]='{"plate":"34 KTH 01","total_seats":45,"bus_type":"standard"}'
BUSES["b2"]='{"plate":"34 KTH 02","total_seats":45,"bus_type":"standard"}'
BUSES["b3"]='{"plate":"34 KTH 03","total_seats":36,"bus_type":"luxury"}'
BUSES["b4"]='{"plate":"34 KTH 04","total_seats":45,"bus_type":"standard"}'
BUSES["b5"]='{"plate":"34 KTH 05","total_seats":36,"bus_type":"luxury"}'

BUS_IDS=()
for key in $(echo "${!BUSES[@]}" | tr ' ' '\n' | sort); do
  RES=$(curl -s -X POST "$BASE/buses/" -H "Content-Type: application/json" -H "$AUTH" -d "${BUSES[$key]}")
  BID=$(echo "$RES" | python3 -c "import sys,json; print(json.load(sys.stdin)['id'])" 2>/dev/null || echo "skip")
  echo "Bus $key: $BID"
  BUS_IDS+=("$BID")
done

echo ""
echo "=== Seeding trips (next 7 days) ==="
NUM_ROUTES=${#ROUTE_IDS[@]}
NUM_BUSES=${#BUS_IDS[@]}

for DAY_OFFSET in $(seq 0 6); do
  DATE=$(date -d "+${DAY_OFFSET} days" +%Y-%m-%d 2>/dev/null || date -v+${DAY_OFFSET}d +%Y-%m-%d)

  for I in $(seq 0 $((NUM_ROUTES - 1))); do
    RID=${ROUTE_IDS[$I]}
    BID=${BUS_IDS[$((I % NUM_BUSES))]}

    # Departures at 08:00 and 16:00
    for HOUR in 08 16; do
      ARR_HOUR=$((10#$HOUR + 5))
      ARR_HOUR_STR=$(printf "%02d" $ARR_HOUR)

      TRIP_DATA="{\"route_id\":\"$RID\",\"bus_id\":\"$BID\",\"departure_time\":\"${DATE}T${HOUR}:00:00\",\"arrival_time\":\"${DATE}T${ARR_HOUR_STR}:00:00\",\"price\":$(shuf -i 250-650 -n 1)}"

      RES=$(curl -s -X POST "$BASE/trips/" -H "Content-Type: application/json" -H "$AUTH" -d "$TRIP_DATA")
      TID=$(echo "$RES" | python3 -c "import sys,json; print(json.load(sys.stdin).get('id','skip'))" 2>/dev/null || echo "skip")
      echo "Trip: $DATE ${HOUR}:00 route=$RID bus=$BID -> $TID"
    done
  done
done

echo ""
echo "=== Promoting admin ==="
if [ -n "$ADMIN_ID" ]; then
  docker compose exec -T postgres psql -U kutahyalilar -d auth_db -c "UPDATE users SET is_admin = true WHERE id = '$ADMIN_ID';" 2>/dev/null
  echo "Admin user promoted: admin@kutahyalilar.com / admin1234"
fi

echo ""
echo "=== Seed complete ==="
echo "Admin: admin@kutahyalilar.com / admin1234"
echo "Routes: ${#ROUTE_IDS[@]} created"
echo "Buses: ${#BUS_IDS[@]} created"
