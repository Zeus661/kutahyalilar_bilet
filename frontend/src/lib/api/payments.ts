import { apiFetch } from './client';
import type { Payment } from '$lib/types';

export function getPayment(token: string, paymentId: string): Promise<Payment> {
	return apiFetch<Payment>(`/api/v1/payments/${paymentId}`, { token });
}
