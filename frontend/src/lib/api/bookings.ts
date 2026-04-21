import { apiFetch } from './client';
import type { Booking } from '$lib/types';

export function createBooking(
	token: string,
	data: {
		trip_id: string;
		seat_id: string;
		passenger_name: string;
		passenger_tc: string;
		passenger_gender: string;
		passenger_dob: string;
	}
): Promise<Booking> {
	return apiFetch<Booking>('/api/v1/bookings/', {
		method: 'POST',
		token,
		body: JSON.stringify(data)
	});
}

export function getMyBookings(token: string): Promise<Booking[]> {
	return apiFetch<Booking[]>('/api/v1/bookings/my', { token });
}

export function getBooking(token: string, bookingId: string): Promise<Booking> {
	return apiFetch<Booking>(`/api/v1/bookings/${bookingId}`, { token });
}

export function cancelBooking(token: string, bookingId: string): Promise<Booking> {
	return apiFetch<Booking>(`/api/v1/bookings/${bookingId}`, {
		method: 'DELETE',
		token
	});
}

export function getAllBookings(token: string): Promise<Booking[]> {
	return apiFetch<Booking[]>('/api/v1/bookings/', { token });
}
