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
		const confirmPassword = form.get('confirmPassword') as string;

		if (!email || !password || !confirmPassword) {
			return fail(400, { error: 'Tüm alanlar zorunludur.', email });
		}

		if (password.length < 8) {
			return fail(400, { error: 'Şifre en az 8 karakter olmalıdır.', email });
		}

		if (password !== confirmPassword) {
			return fail(400, { error: 'Şifreler eşleşmiyor.', email });
		}

		try {
			const regRes = await fetch(`${PUBLIC_API_BASE_URL}/api/v1/auth/register`, {
				method: 'POST',
				headers: { 'Content-Type': 'application/json' },
				body: JSON.stringify({ email, password })
			});

			if (!regRes.ok) {
				if (regRes.status === 409) {
					return fail(409, { error: 'Bu e-posta adresi zaten kayıtlı.', email });
				}
				const err = await regRes.json().catch(() => ({ detail: 'Kayıt başarısız.' }));
				return fail(regRes.status, { error: err.detail ?? 'Kayıt başarısız.', email });
			}

			// Auto-login after registration
			const loginRes = await fetch(`${PUBLIC_API_BASE_URL}/api/v1/auth/login`, {
				method: 'POST',
				headers: { 'Content-Type': 'application/json' },
				body: JSON.stringify({ email, password })
			});

			if (loginRes.ok) {
				const { access_token } = await loginRes.json();
				cookies.set('jwt', access_token, {
					httpOnly: true,
					secure: false,
					sameSite: 'lax',
					maxAge: 60 * 60,
					path: '/'
				});
			}

			throw redirect(303, '/');
		} catch (e) {
			if (e instanceof Response || (e as any)?.status) throw e;
			return fail(500, { error: 'Sunucu hatası.', email });
		}
	}
};
