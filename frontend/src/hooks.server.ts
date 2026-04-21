import type { Handle } from '@sveltejs/kit';
import { env } from '$env/dynamic/public';

export const handle: Handle = async ({ event, resolve }) => {
	const token = event.cookies.get('jwt');
	event.locals.token = token ?? null;

	if (token) {
		try {
			const res = await fetch(`${env.PUBLIC_API_BASE_URL}/api/v1/auth/me`, {
				headers: { Authorization: `Bearer ${token}` }
			});
			if (res.ok) {
				event.locals.user = await res.json();
			} else {
				event.locals.user = null;
				event.cookies.delete('jwt', { path: '/' });
			}
		} catch {
			event.locals.user = null;
		}
	} else {
		event.locals.user = null;
	}

	return resolve(event);
};
