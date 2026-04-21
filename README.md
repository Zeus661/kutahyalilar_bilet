# Kütahyalılar Bus Ticket System
Microservice-based bus ticketing platform.

## Services
| Service | Port | Description |
|---|---|---|
| api-gateway | 8000 | Entry point (Nginx reverse proxy) |
| auth-service | 8001 | JWT auth, login/register |
| user-service | 8002 | User profiles |
| trip-service | 8003 | Routes and schedules |
| booking-service | 8004 | Ticket purchases |
| payment-service | 8005 | Mock payment processor |
| notification-service | 8006 | Email/SMS dispatch |

## Quick Start
```bash
cp .env.example .env
docker-compose up --build
```
