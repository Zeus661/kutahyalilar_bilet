import type { PageServerLoad, Actions } from './$types';
import { redirect, fail } from '@sveltejs/kit';
import { PUBLIC_API_BASE_URL } from '$env/static/public';

export const load: PageServerLoad = async ({ locals, url }) => {
	if (!locals.user) {
		throw redirect(303, '/auth/login?redirect=' + encodeURIComponent(url.pathname));
	}
	return {};
};

export const actions: Actions = {
	default: async ({ request, cookies, locals }) => {
		const token = locals.token;
		if (!token) throw redirect(303, '/auth/login');

		const form = await request.formData();
		const trip_id = form.get('trip_id') as string;
		const seat_id = form.get('seat_id') as string;
		const passenger_name = form.get('passenger_name') as string;
		const passenger_tc = form.get('passenger_tc') as string;
		const passenger_gender = form.get('passenger_gender') as string;
		const passenger_dob = form.get('passenger_dob') as string;

		if (!trip_id || !seat_id || !passenger_name || !passenger_tc || !passenger_gender || !passenger_dob) {
			return fail(400, {
				error: 'Tüm alanlar zorunludur.',
				trip_id, seat_id, passenger_name, passenger_tc, passenger_gender, passenger_dob
			});
		}

		try {
			const res = await fetch(`${PUBLIC_API_BASE_URL}/api/v1/bookings/`, {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json',
					Authorization: `Bearer ${token}`
				},
				body: JSON.stringify({
					trip_id, seat_id, passenger_name, passenger_tc, passenger_gender, passenger_dob
				})
			});

			if (!res.ok) {
				const err = await res.json().catch(() => ({ detail: 'Rezervasyon başarısız.' }));
				return fail(res.status, {
					error: err.detail ?? 'Rezervasyon başarısız.',
					trip_id, seat_id, passenger_name, passenger_tc, passenger_gender, passenger_dob
				});
			}

			const booking = await res.json();
			throw redirect(303, `/bookings/${booking.id}?success=true`);
		} catch (e) {
			if (e instanceof Response || (e as any)?.status) throw e;
			return fail(500, { error: 'Sunucu hatası.' });
		}
	}
};
