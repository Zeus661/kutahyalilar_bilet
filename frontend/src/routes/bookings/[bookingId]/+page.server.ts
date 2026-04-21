import type { PageServerLoad } from './$types';
import { redirect } from '@sveltejs/kit';
import { env } from '$env/dynamic/public';

export const load: PageServerLoad = async ({ params, locals, url }) => {
	if (!locals.user) {
		throw redirect(303, '/auth/login?redirect=' + encodeURIComponent(url.pathname));
	}

	const token = locals.token!;
	const { bookingId } = params;
	const success = url.searchParams.get('success') === 'true';

	try {
		const res = await fetch(`${env.PUBLIC_API_BASE_URL}/api/v1/bookings/${bookingId}`, {
			headers: { Authorization: `Bearer ${token}` }
		});
		if (!res.ok) throw redirect(303, '/bookings');
		const booking = await res.json();
		return { booking, success };
	} catch (e) {
		if (e instanceof Response || (e as any)?.status) throw e;
		throw redirect(303, '/bookings');
	}
};
