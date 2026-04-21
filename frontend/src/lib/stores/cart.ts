import { writable } from 'svelte/store';
import type { CartItem } from '$lib/types';

export const cart = writable<CartItem | null>(null);
