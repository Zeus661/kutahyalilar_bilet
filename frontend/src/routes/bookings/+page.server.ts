import type { PageServerLoad, Actions } from './$types';
import { redirect } from '@sveltejs/kit';
import { env } from '$env/dynamic/public';

export const load: PageServerLoad = async ({ locals, url }) => {
	if (!locals.user) {
		throw redirect(303, '/auth/login?redirect=' + encodeURIComponent(url.pathname));
	}

	const token = locals.token!;
	try {
		const res = await fetch(`${env.PUBLIC_API_BASE_URL}/api/v1/bookings/my`, {
			headers: { Authorization: `Bearer ${token}` }
		});
		if (!res.ok) return { bookings: [], error: 'Biletler yüklenemedi.' };
		const bookings = await res.json();
		return { bookings };
	} catch {
		return { bookings: [], error: 'Sunucuya bağlanılamadı.' };
	}
};

export const actions: Actions = {
	cancel: async ({ request, locals }) => {
		const token = locals.token;
		if (!token) throw redirect(303, '/auth/login');
		const form = await request.formData();
		const bookingId = form.get('bookingId') as string;

		await fetch(`${env.PUBLIC_API_BASE_URL}/api/v1/bookings/${bookingId}`, {
			method: 'DELETE',
			headers: { Authorization: `Bearer ${token}` }
		});

		throw redirect(303, '/bookings');
	}
};
