import { apiFetch } from './client';
import type { AuthUser, LoginResponse } from '$lib/types';

export function register(email: string, password: string): Promise<AuthUser> {
	return apiFetch<AuthUser>('/api/v1/auth/register', {
		method: 'POST',
		body: JSON.stringify({ email, password })
	});
}

export function login(email: string, password: string): Promise<LoginResponse> {
	return apiFetch<LoginResponse>('/api/v1/auth/login', {
		method: 'POST',
		body: JSON.stringify({ email, password })
	});
}

export function getMe(token: string): Promise<AuthUser> {
	return apiFetch<AuthUser>('/api/v1/auth/me', { token });
}
