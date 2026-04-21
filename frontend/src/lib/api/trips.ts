import { apiFetch } from './client';
import type { Trip, Route } from '$lib/types';

export function searchTrips(
	token: string,
	origin: string,
	destination: string,
	date: string
): Promise<Trip[]> {
	const params = new URLSearchParams({ origin, destination, date });
	return apiFetch<Trip[]>(`/api/v1/trips/search?${params}`, { token });
}

export function getTrip(token: string, tripId: string): Promise<Trip> {
	return apiFetch<Trip>(`/api/v1/trips/${tripId}`, { token });
}

export function createTrip(
	token: string,
	data: {
		route_id: string;
		bus_id: string;
		departure_time: string;
		arrival_time: string;
		price: string;
	}
): Promise<Trip> {
	return apiFetch<Trip>('/api/v1/trips/', {
		method: 'POST',
		token,
		body: JSON.stringify(data)
	});
}

export function deleteTrip(token: string, tripId: string): Promise<{ status: string }> {
	return apiFetch<{ status: string }>(`/api/v1/trips/${tripId}`, {
		method: 'DELETE',
		token
	});
}

export function getRoutes(token: string): Promise<Route[]> {
	return apiFetch<Route[]>('/api/v1/routes/', { token });
}

export function createRoute(
	token: string,
	data: { origin: string; destination: string; distance_km?: number; estimated_duration_min?: number }
): Promise<Route> {
	return apiFetch<Route>('/api/v1/routes/', {
		method: 'POST',
		token,
		body: JSON.stringify(data)
	});
}
