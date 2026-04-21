import { PUBLIC_API_BASE_URL as STATIC_URL } from '$env/static/public';
import { env } from '$env/dynamic/public';

function getBaseUrl(): string {
	return env.PUBLIC_API_BASE_URL || STATIC_URL;
}

export async function apiFetch<T>(
	path: string,
	options: RequestInit & { token?: string } = {}
): Promise<T> {
	const { token, ...fetchOptions } = options;

	const res = await fetch(`${getBaseUrl()}${path}`, {
		...fetchOptions,
		headers: {
			'Content-Type': 'application/json',
			...(token ? { Authorization: `Bearer ${token}` } : {}),
			...fetchOptions.headers
		}
	});

	if (!res.ok) {
		const err = await res.json().catch(() => ({ detail: 'Bilinmeyen bir hata oluştu' }));
		throw new Error(err.detail ?? `HTTP ${res.status}`);
	}

	return res.json() as Promise<T>;
}
