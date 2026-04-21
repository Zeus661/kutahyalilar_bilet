import type { PageServerLoad } from './$types';
import { env } from '$env/dynamic/public';

export const load: PageServerLoad = async ({ locals }) => {
	const token = locals.token!;
	const headers = { Authorization: `Bearer ${token}` };

	const [tripsRes, bookingsRes] = await Promise.all([
		fetch(`${env.PUBLIC_API_BASE_URL}/api/v1/trips/search?origin=&destination=&date=2025-01-01`, { headers }).catch(() => null),
		fetch(`${env.PUBLIC_API_BASE_URL}/api/v1/bookings/`, { headers }).catch(() => null)
	]);

	const bookings = bookingsRes?.ok ? await bookingsRes.json() : [];

	return {
		stats: {
			totalBookings: bookings.length,
			totalRevenue: bookings.reduce((sum: number, b: any) => sum + Number(b.total_price || 0), 0),
			activeTrips: 0,
			registeredUsers: 0
		},
		recentBookings: bookings.slice(0, 10)
	};
};
