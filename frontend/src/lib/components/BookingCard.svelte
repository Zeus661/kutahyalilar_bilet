<script lang="ts">
	import type { Booking } from '$lib/types';

	interface Props {
		booking: Booking;
		oncancel?: (bookingId: string) => void;
		showActions?: boolean;
	}

	let { booking, oncancel, showActions = true }: Props = $props();

	const statusConfig: Record<string, { label: string; cls: string }> = {
		confirmed: { label: 'Onaylandı', cls: 'bg-green-100 text-green-800' },
		pending: { label: 'Beklemede', cls: 'bg-yellow-100 text-yellow-800' },
		cancelled: { label: 'İptal Edildi', cls: 'bg-red-100 text-red-800' },
		refunded: { label: 'İade Edildi', cls: 'bg-gray-100 text-gray-600' },
		completed: { label: 'Tamamlandı', cls: 'bg-blue-100 text-blue-800' }
	};

	function fmt(iso: string) {
		return new Date(iso).toLocaleString('tr-TR', {
			hour: '2-digit',
			minute: '2-digit',
			day: 'numeric',
			month: 'long'
		});
	}

	const cfg = $derived(statusConfig[booking.status] ?? { label: booking.status, cls: 'bg-gray-100 text-gray-600' });
</script>

<div class="rounded-xl border border-gray-200 bg-white p-5 shadow-sm">
	<div class="flex items-start justify-between">
		<div>
			<p class="font-mono text-lg font-bold text-kutahya-dark">{booking.ticket_code}</p>
			<p class="mt-1 text-sm text-gray-600">{booking.passenger_name}</p>
			<p class="mt-1 text-sm text-kutahya-muted">Koltuk {booking.seat_number}</p>
		</div>
		<span class="rounded-full px-3 py-1 text-xs font-semibold {cfg.cls}">
			{cfg.label}
		</span>
	</div>

	<div class="mt-3 border-t pt-3 text-sm text-kutahya-muted">
		<p>{fmt(booking.passenger_dob)}</p>
		<p class="mt-1 font-semibold text-kutahya-dark">{Number(booking.total_price).toFixed(2)} TL</p>
	</div>

	{#if showActions}
		<div class="mt-4 flex gap-2">
			<a
				href="/bookings/{booking.id}"
				class="rounded-lg border border-kutahya-red px-4 py-1.5 text-sm font-medium text-kutahya-red transition hover:bg-kutahya-red hover:text-white"
			>
				Detay
			</a>
			{#if booking.status === 'confirmed' && oncancel}
				<button
					onclick={() => oncancel(booking.id)}
					class="rounded-lg border border-red-300 px-4 py-1.5 text-sm font-medium text-red-600 transition hover:bg-red-50"
				>
					İptal Et
				</button>
			{/if}
		</div>
	{/if}
</div>
