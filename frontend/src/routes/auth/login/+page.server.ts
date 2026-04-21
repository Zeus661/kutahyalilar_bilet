import type { PageServerLoad, Actions } from './$types';
import { redirect, fail } from '@sveltejs/kit';
import { PUBLIC_API_BASE_URL } from '$env/static/public';

export const load: PageServerLoad = async ({ locals }) => {
	if (locals.user) throw redirect(303, '/');
	return {};
};

export const actions: Actions = {
	default: async ({ request, cookies }) => {
		const form = await request.formData();
		const email = form.get('email') as string;
		const password = form.get('password') as string;

		if (!email || !password) {
			return fail(400, { error: 'E-posta ve şifre zorunludur.', email });
		}

		try {
			const res = await fetch(`${PUBLIC_API_BASE_URL}/api/v1/auth/login`, {
				method: 'POST',
				headers: { 'Content-Type': 'application/json' },
				body: JSON.stringify({ email, password })
			});

			if (!res.ok) {
				const err = await res.json().catch(() => ({ detail: 'Giriş başarısız.' }));
				return fail(res.status, { error: err.detail ?? 'Giriş başarısız.', email });
			}

			const { access_token } = await res.json();
			cookies.set('jwt', access_token, {
				httpOnly: true,
				secure: false,
				sameSite: 'lax',
				maxAge: 60 * 60,
				path: '/'
			});

			throw redirect(303, '/bookings');
		} catch (e) {
			if (e instanceof Response || (e as any)?.status) throw e;
			return fail(500, { error: 'Sunucu hatası.', email });
		}
	}
};
