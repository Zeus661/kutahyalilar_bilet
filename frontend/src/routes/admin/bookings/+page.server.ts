import type { PageServerLoad } from './$types';
import { PUBLIC_API_BASE_URL } from '$env/static/public';

export const load: PageServerLoad = async ({ locals }) => {
	const token = locals.token!;
	try {
		const res = await fetch(`${PUBLIC_API_BASE_URL}/api/v1/bookings/`, {
			headers: { Authorization: `Bearer ${token}` }
		});
		if (!res.ok) return { bookings: [] };
		const bookings = await res.json();
		return { bookings };
	} catch {
		return { bookings: [] };
	}
};
