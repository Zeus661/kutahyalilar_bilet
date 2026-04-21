import type { PageServerLoad, Actions } from './$types';
import { redirect, fail } from '@sveltejs/kit';
import { PUBLIC_API_BASE_URL } from '$env/static/public';

export const load: PageServerLoad = async ({ locals, url }) => {
	const token = locals.token!;
	const headers = { Authorization: `Bearer ${token}` };

	const [routesRes, tripsRes] = await Promise.all([
		fetch(`${PUBLIC_API_BASE_URL}/api/v1/routes/`, { headers }).catch(() => null),
		fetch(`${PUBLIC_API_BASE_URL}/api/v1/trips/search?origin=&destination=&date=2025-01-01`, { headers }).catch(() => null)
	]);

	const routes = routesRes?.ok ? await routesRes.json() : [];
	const trips = tripsRes?.ok ? await tripsRes.json() : [];

	return { routes, trips };
};

export const actions: Actions = {
	create: async ({ request, locals }) => {
		const token = locals.token!;
		const form = await request.formData();
		const route_id = form.get('route_id') as string;
		const bus_id = form.get('bus_id') as string;
		const departure_time = form.get('departure_time') as string;
		const arrival_time = form.get('arrival_time') as string;
		const price = form.get('price') as string;

		try {
			await fetch(`${PUBLIC_API_BASE_URL}/api/v1/trips/`, {
				method: 'POST',
				headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${token}` },
				body: JSON.stringify({ route_id, bus_id, departure_time, arrival_time, price })
			});
		} catch {}

		throw redirect(303, '/admin/trips');
	},

	cancel: async ({ request, locals }) => {
		const token = locals.token!;
		const form = await request.formData();
		const tripId = form.get('tripId') as string;

		try {
			await fetch(`${PUBLIC_API_BASE_URL}/api/v1/trips/${tripId}`, {
				method: 'DELETE',
				headers: { Authorization: `Bearer ${token}` }
			});
		} catch {}

		throw redirect(303, '/admin/trips');
	}
};
