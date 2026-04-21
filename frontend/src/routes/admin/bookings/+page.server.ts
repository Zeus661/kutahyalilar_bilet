import type { PageServerLoad } from './$types';
import { env } from '$env/dynamic/public';

export const load: PageServerLoad = async ({ locals }) => {
	const token = locals.token!;
	try {
		const res = await fetch(`${env.PUBLIC_API_BASE_URL}/api/v1/bookings/`, {
			headers: { Authorization: `Bearer ${token}` }
		});
		if (!res.ok) return { bookings: [] };
		const bookings = await res.json();
		return { bookings };
	} catch {
		return { bookings: [] };
	}
};
