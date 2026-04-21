// TypeScript interfaces derived from docs/API_REFERENCE.md

export interface AuthUser {
	id: string;
	email: string;
	is_admin: boolean;
}

export interface LoginResponse {
	access_token: string;
	token_type: string;
}

export interface UserProfile {
	id: string;
	auth_user_id: string;
	first_name: string | null;
	last_name: string | null;
	phone: string | null;
	date_of_birth: string | null;
	tc_kimlik: string | null;
	gender: string | null;
}

export interface Seat {
	id: string;
	trip_id: string;
	seat_number: number;
	is_reserved: boolean;
	gender_restriction: string | null;
}

export interface Trip {
	id: string;
	route_id: string;
	bus_id: string;
	departure_time: string;
	arrival_time: string;
	price: string;
	available_seats: number;
	status: string;
	seats?: Seat[];
}

export interface Booking {
	id: string;
	user_id: string;
	trip_id: string;
	seat_id: string;
	seat_number: number;
	passenger_name: string;
	passenger_tc: string;
	passenger_gender: string;
	passenger_dob: string;
	total_price: string;
	status: string;
	payment_id: string | null;
	ticket_code: string;
}

export interface Payment {
	id: string;
	booking_id: string;
	user_id: string;
	amount: string;
	currency: string;
	method: string;
	status: string;
	mock_card_last4: string | null;
	failure_reason: string | null;
}

export interface Route {
	id: string;
	origin: string;
	destination: string;
	distance_km: number | null;
	estimated_duration_min: number | null;
}

export interface Bus {
	id: string;
	plate: string;
	total_seats: number;
	bus_type: string | null;
}

export interface CartItem {
	trip: Trip;
	seat: Seat;
}
