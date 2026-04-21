# API Reference

All services share the `/api/v1` route prefix. Each service also exposes a `GET /health` endpoint returning `{"status": "ok", "service": "<name>"}`.

Authentication uses **Bearer JWT** tokens obtained via the Auth Service. Some endpoints require the `is_admin` flag in the JWT payload.

---

## Auth Service (port 8001)

Handles registration, login, token refresh, and current-user lookup.

### POST /api/v1/auth/register

**Auth:** None

**Request Body:**

| Field    | Type                       | Required |
|----------|----------------------------|----------|
| email    | string (valid email)       | yes      |
| password | string (min 8 chars)       | yes      |

**Response (201):**

| Field     | Type    |
|-----------|---------|
| id        | UUID    |
| email     | string  |
| is_admin  | boolean |

**Kafka Emits:** `user.registered`

---

### POST /api/v1/auth/login

**Auth:** None

**Request Body:**

| Field    | Type                   | Required |
|----------|------------------------|----------|
| email    | string (valid email)   | yes      |
| password | string                 | yes      |

**Response:**

| Field        | Type   |
|--------------|--------|
| access_token | string |
| token_type   | string |

**Kafka Emits:** None

---

### GET /api/v1/auth/me

**Auth:** Bearer JWT

**Request Body:** None

**Response:**

| Field     | Type    |
|-----------|---------|
| id        | UUID    |
| email     | string  |
| is_admin  | boolean |

**Kafka Emits:** None

---

### POST /api/v1/auth/refresh

**Auth:** Bearer JWT

**Request Body:** None

**Response:**

| Field        | Type   |
|--------------|--------|
| access_token | string |
| token_type   | string |

**Kafka Emits:** None

---

## User Service (port 8002)

Manages user profiles. Consumes `user.registered` Kafka events to auto-create profiles. All endpoints require authentication.

### GET /api/v1/users/me

**Auth:** Bearer JWT

**Request Body:** None

**Response:**

| Field         | Type             |
|---------------|------------------|
| id            | UUID             |
| auth_user_id  | UUID             |
| first_name    | string or null   |
| last_name     | string or null   |
| phone         | string or null   |
| date_of_birth | date or null     |
| tc_kimlik     | string or null   |
| gender        | string or null   |

**Kafka Emits:** None

---

### PUT /api/v1/users/me

**Auth:** Bearer JWT

**Request Body:**

| Field         | Type             | Required |
|---------------|------------------|----------|
| first_name    | string           | no       |
| last_name     | string           | no       |
| phone         | string           | no       |
| date_of_birth | date             | no       |
| tc_kimlik     | string           | no       |
| gender        | string           | no       |

**Response:**

| Field         | Type             |
|---------------|------------------|
| id            | UUID             |
| auth_user_id  | UUID             |
| first_name    | string or null   |
| last_name     | string or null   |
| phone         | string or null   |
| date_of_birth | date or null     |
| tc_kimlik     | string or null   |
| gender        | string or null   |

**Kafka Emits:** None

---

### GET /api/v1/users/{user_id}

**Auth:** Bearer JWT (admin only)

**Request Body:** None

**Path Parameters:**

| Parameter | Type |
|-----------|------|
| user_id   | UUID |

**Response:** Same as `GET /api/v1/users/me`

**Kafka Emits:** None

---

### GET /api/v1/users/

**Auth:** Bearer JWT (admin only)

**Request Body:** None

**Response:** Array of same shape as `GET /api/v1/users/me`

**Kafka Emits:** None

---

## Trip Service (port 8003)

Manages routes, buses, trips, and seat reservations. All endpoints require authentication; write operations require admin.

### GET /api/v1/trips/search

**Auth:** Bearer JWT

**Query Parameters:**

| Parameter   | Type | Required |
|-------------|------|----------|
| origin      | string | yes    |
| destination | string | yes    |
| date        | date   | yes    |

**Response:** Array of:

| Field            | Type            |
|------------------|-----------------|
| id               | UUID            |
| route_id         | UUID            |
| bus_id           | UUID            |
| departure_time   | datetime        |
| arrival_time     | datetime        |
| price            | Decimal         |
| available_seats  | integer         |
| status           | string          |

**Kafka Emits:** None

---

### GET /api/v1/trips/{trip_id}

**Auth:** Bearer JWT

**Path Parameters:**

| Parameter | Type |
|-----------|------|
| trip_id   | UUID |

**Response:**

| Field            | Type            |
|------------------|-----------------|
| id               | UUID            |
| route_id         | UUID            |
| bus_id           | UUID            |
| departure_time   | datetime        |
| arrival_time     | datetime        |
| price            | Decimal         |
| available_seats  | integer         |
| status           | string          |
| seats            | array of SeatOut |

**SeatOut:**

| Field              | Type            |
|--------------------|-----------------|
| id                 | UUID            |
| trip_id            | UUID            |
| seat_number        | integer         |
| is_reserved        | boolean         |
| gender_restriction | string or null  |

**Kafka Emits:** None

---

### GET /api/v1/trips/{trip_id}/seats

**Auth:** Bearer JWT

**Path Parameters:**

| Parameter | Type |
|-----------|------|
| trip_id   | UUID |

**Response:** Array of SeatOut (see above)

**Kafka Emits:** None

---

### POST /api/v1/trips/

**Auth:** Bearer JWT (admin only)

**Request Body:**

| Field           | Type      | Required |
|-----------------|-----------|----------|
| route_id        | UUID      | yes      |
| bus_id          | UUID      | yes      |
| departure_time  | datetime  | yes      |
| arrival_time    | datetime  | yes      |
| price           | Decimal   | yes      |

**Response (201):** TripOut (same as search result)

**Kafka Emits:** None

---

### PUT /api/v1/trips/{trip_id}

**Auth:** Bearer JWT (admin only)

> **Note:** Returns "Not implemented yet" — endpoint is a placeholder.

**Kafka Emits:** None

---

### DELETE /api/v1/trips/{trip_id}

**Auth:** Bearer JWT (admin only)

**Path Parameters:**

| Parameter | Type |
|-----------|------|
| trip_id   | UUID |

**Response:**

| Field  | Type   |
|--------|--------|
| status | string |

**Kafka Emits:** None

---

### POST /api/v1/trips/{trip_id}/seats/{seat_id}/reserve

**Auth:** Bearer JWT

**Path Parameters:**

| Parameter | Type |
|-----------|------|
| trip_id   | UUID |
| seat_id   | UUID |

**Request Body:** None

**Response:**

| Field        | Type     |
|--------------|----------|
| seat_id      | UUID     |
| trip_id      | UUID     |
| seat_number  | integer  |
| reserved     | boolean  |

**Kafka Emits:** None

---

### POST /api/v1/trips/{trip_id}/seats/{seat_id}/release

**Auth:** Bearer JWT

**Path Parameters:**

| Parameter | Type |
|-----------|------|
| trip_id   | UUID |
| seat_id   | UUID |

**Request Body:** None

**Response:**

| Field   | Type   |
|---------|--------|
| status  | string |
| seat_id | string |

**Kafka Emits:** None

---

### POST /api/v1/routes/

**Auth:** Bearer JWT (admin only)

**Request Body:**

| Field                 | Type            | Required |
|-----------------------|-----------------|----------|
| origin                | string          | yes      |
| destination           | string          | yes      |
| distance_km           | integer         | no       |
| estimated_duration_min| integer         | no       |

**Response (201):**

| Field                  | Type            |
|------------------------|-----------------|
| id                     | UUID            |
| origin                 | string          |
| destination            | string          |
| distance_km            | integer or null |
| estimated_duration_min | integer or null |

**Kafka Emits:** None

---

### GET /api/v1/routes/

**Auth:** Bearer JWT

**Request Body:** None

**Response:** Array of RouteOut (see above)

**Kafka Emits:** None

---

### POST /api/v1/buses/

**Auth:** Bearer JWT (admin only)

**Request Body:**

| Field        | Type            | Required | Default    |
|--------------|-----------------|----------|------------|
| plate        | string          | yes      |            |
| total_seats  | integer         | no       | 45         |
| bus_type     | string          | no       | "standard" |

**Response (201):**

| Field        | Type            |
|--------------|-----------------|
| id           | UUID            |
| plate        | string          |
| total_seats  | integer         |
| bus_type     | string or null  |

**Kafka Emits:** None

---

## Booking Service (port 8004)

Handles ticket booking with seat reservation and payment orchestration. Makes service-to-service calls to Trip Service and Payment Service.

### POST /api/v1/bookings/

**Auth:** Bearer JWT

**Request Body:**

| Field            | Type    | Required |
|------------------|---------|----------|
| trip_id          | UUID    | yes      |
| seat_id          | UUID    | yes      |
| passenger_name   | string  | yes      |
| passenger_tc     | string  | yes      |
| passenger_gender | string  | yes      |
| passenger_dob    | date    | yes      |

**Response (201):**

| Field            | Type            |
|------------------|-----------------|
| id               | UUID            |
| user_id          | UUID            |
| trip_id          | UUID            |
| seat_id          | UUID            |
| seat_number      | integer         |
| passenger_name   | string          |
| passenger_tc     | string          |
| passenger_gender | string          |
| passenger_dob    | date            |
| total_price      | Decimal         |
| status           | string          |
| payment_id       | UUID or null    |
| ticket_code      | string          |

**Kafka Emits:** `booking.created` (on payment success)

---

### GET /api/v1/bookings/my

**Auth:** Bearer JWT

**Request Body:** None

**Response:** Array of BookingOut (see above)

**Kafka Emits:** None

---

### GET /api/v1/bookings/{booking_id}

**Auth:** Bearer JWT

**Path Parameters:**

| Parameter   | Type |
|-------------|------|
| booking_id  | UUID |

**Response:** BookingOut (see above)

**Kafka Emits:** None

---

### DELETE /api/v1/bookings/{booking_id}

**Auth:** Bearer JWT (owner or admin)

**Path Parameters:**

| Parameter   | Type |
|-------------|------|
| booking_id  | UUID |

**Response:** BookingOut with `status: "cancelled"`

**Kafka Emits:** `booking.cancelled`

---

### GET /api/v1/bookings/

**Auth:** Bearer JWT (admin only)

**Request Body:** None

**Response:** Array of BookingOut (see above)

**Kafka Emits:** None

---

## Payment Service (port 8005)

Processes mock payments with 90% success rate. Refunds are admin-only and restricted to within 2 hours of payment.

### POST /api/v1/payments/

**Auth:** Bearer JWT

**Request Body:**

| Field           | Type    | Required | Default       |
|-----------------|---------|----------|---------------|
| booking_id      | UUID    | yes      |               |
| user_id         | UUID    | yes      |               |
| amount          | Decimal | yes      |               |
| currency        | string  | no       | "TRY"         |
| method          | string  | no       | "credit_card" |
| mock_card_last4 | string  | no       | "4242"        |

**Response (201):**

| Field           | Type            |
|-----------------|-----------------|
| id              | UUID            |
| booking_id      | UUID            |
| user_id         | UUID            |
| amount          | Decimal         |
| currency        | string          |
| method          | string          |
| status          | string          |
| mock_card_last4 | string or null  |
| failure_reason  | string or null  |

**Kafka Emits:** `payment.completed` or `payment.failed`

---

### GET /api/v1/payments/{payment_id}

**Auth:** Bearer JWT

**Path Parameters:**

| Parameter  | Type |
|------------|------|
| payment_id | UUID |

**Response:** PaymentOut (see above)

**Kafka Emits:** None

---

### POST /api/v1/payments/{payment_id}/refund

**Auth:** Bearer JWT (admin only)

**Path Parameters:**

| Parameter  | Type |
|------------|------|
| payment_id | UUID |

**Request Body:** None

**Response:**

| Field       | Type   |
|-------------|--------|
| payment_id  | UUID   |
| status      | string |
| message     | string |

**Kafka Emits:** None

---

## Notification Service (port 8006)

No HTTP endpoints. Consumes Kafka events and sends email/SMS notifications.

**Kafka Consumes:** `user.registered`, `booking.created`, `booking.cancelled`, `payment.completed`, `payment.failed`

---

## Health Endpoints (all services)

Every service exposes an unauthenticated health check:

| Service              | Endpoint     |
|----------------------|--------------|
| Auth Service         | GET /health  |
| User Service         | GET /health  |
| Trip Service         | GET /health  |
| Booking Service      | GET /health  |
| Payment Service      | GET /health  |
| Notification Service | GET /health  |

---

## Kafka Event Summary

| Topic              | Producer         | Consumers               |
|--------------------|------------------|-------------------------|
| `user.registered`  | Auth Service     | User Service, Notification Service |
| `booking.created`  | Booking Service  | Notification Service    |
| `booking.cancelled`| Booking Service  | Notification Service    |
| `payment.completed`| Payment Service  | Notification Service    |
| `payment.failed`   | Payment Service  | Notification Service    |
