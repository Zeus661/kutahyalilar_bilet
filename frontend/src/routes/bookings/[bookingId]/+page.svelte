<script lang="ts">
	import type { Booking } from '$lib/types';

	let { data } = $props();
	let booking: Booking = $derived(data.booking);

	function fmt(iso: string) {
		return new Date(iso).toLocaleString('tr-TR', {
			hour: '2-digit',
			minute: '2-digit',
			day: 'numeric',
			month: 'long',
			year: 'numeric'
		});
	}

	function maskTc(tc: string) {
		if (tc.length < 4) return tc;
		return '*'.repeat(tc.length - 4) + tc.slice(-4);
	}

	const statusLabels: Record<string, string> = {
		confirmed: 'Onaylandı',
		pending: 'Beklemede',
		cancelled: 'İptal Edildi',
		refunded: 'İade Edildi',
		completed: 'Tamamlandı'
	};
</script>

<svelte:head>
	<title>Bilet Detayı — Kütahyalılar</title>
</svelte:head>

<div class="mx-auto max-w-xl px-4 py-8">
	{#if data.success}
		<div class="mb-6 rounded-lg bg-green-50 border border-green-200 px-4 py-3 text-green-800 text-center">
			Biletiniz başarıyla satın alındı!
		</div>
	{/if}

	<!-- E-Ticket card -->
	<div class="rounded-xl bg-white shadow-lg overflow-hidden">
		<!-- Header -->
		<div class="flex items-center justify-between bg-kutahya-dark px-6 py-4 text-white">
			<span class="text-xl font-bold">Kütahyalılar</span>
			<span class="font-mono text-lg tracking-wider">{booking.ticket_code}</span>
		</div>

		<!-- Dashed divider -->
		<div class="border-b-2 border-dashed border-gray-300 mx-6"></div>

		<!-- Body -->
		<div class="px-6 py-5 space-y-4">
			<div>
				<p class="text-xs text-kutahya-muted uppercase">Yolcu</p>
				<p class="text-lg font-semibold text-kutahya-dark">{booking.passenger_name}</p>
			</div>
			<div class="grid grid-cols-2 gap-4 text-sm">
				<div>
					<p class="text-xs text-kutahya-muted uppercase">TC Kimlik</p>
					<p class="font-mono">{maskTc(booking.passenger_tc)}</p>
				</div>
				<div>
					<p class="text-xs text-kutahya-muted uppercase">Koltuk No</p>
					<p class="text-lg font-bold text-kutahya-red">{booking.seat_number}</p>
				</div>
				<div>
					<p class="text-xs text-kutahya-muted uppercase">Cinsiyet</p>
					<p>{booking.passenger_gender}</p>
				</div>
				<div>
					<p class="text-xs text-kutahya-muted uppercase">Doğum Tarihi</p>
					<p>{booking.passenger_dob}</p>
				</div>
			</div>

			<div class="border-t pt-4">
				<div class="flex items-center justify-between">
					<div>
						<p class="text-xs text-kutahya-muted uppercase">Tutar</p>
						<p class="text-xl font-bold text-kutahya-red">{Number(booking.total_price).toFixed(2)} TL</p>
					</div>
					<span class="rounded-full bg-green-100 px-3 py-1 text-xs font-semibold text-green-800">
						{statusLabels[booking.status] ?? booking.status}
					</span>
				</div>
			</div>
		</div>
	</div>

	<!-- Actions -->
	<div class="mt-6 flex gap-3">
		<button
			onclick={() => window.print()}
			class="flex-1 rounded-lg bg-kutahya-dark py-2.5 font-semibold text-white transition hover:bg-gray-800"
		>
			Yazdır
		</button>
		<a
			href="/bookings"
			class="flex-1 rounded-lg border border-kutahya-red py-2.5 text-center font-semibold text-kutahya-red transition hover:bg-kutahya-red hover:text-white"
		>
			Geri
		</a>
	</div>
</div>
