import type { PageServerLoad } from './$types';
import { redirect } from '@sveltejs/kit';
import { PUBLIC_API_BASE_URL } from '$env/static/public';

export const load: PageServerLoad = async ({ url, locals }) => {
	if (!locals.user) throw redirect(303, '/auth/login?redirect=' + encodeURIComponent(url.pathname));

	const origin = url.searchParams.get('origin') ?? '';
	const destination = url.searchParams.get('destination') ?? '';
	const date = url.searchParams.get('date') ?? '';

	if (!origin || !destination || !date) {
		return { trips: [], origin, destination, date };
	}

	const token = locals.token!;
	const params = new URLSearchParams({ origin, destination, date });

	try {
		const res = await fetch(`${PUBLIC_API_BASE_URL}/api/v1/trips/search?${params}`, {
			headers: { Authorization: `Bearer ${token}` }
		});
		if (!res.ok) return { trips: [], origin, destination, date, error: 'Seferler yüklenemedi.' };
		const trips = await res.json();
		return { trips, origin, destination, date };
	} catch {
		return { trips: [], origin, destination, date, error: 'Sunucuya bağlanılamadı.' };
	}
};
