<script lang="ts">
	import type { Trip, Seat } from '$lib/types';
	import SeatMap from '$lib/components/SeatMap.svelte';
	import { cart } from '$lib/stores/cart';
	import { goto } from '$app/navigation';

	let { data } = $props();
	let trip: Trip = $derived(data.trip);
	let selectedSeat = $state<Seat | null>(null);

	function fmt(iso: string) {
		return new Date(iso).toLocaleString('tr-TR', {
			hour: '2-digit',
			minute: '2-digit',
			day: 'numeric',
			month: 'long',
			year: 'numeric'
		});
	}

	function handleSelect(seat: Seat) {
		selectedSeat = selectedSeat?.id === seat.id ? null : seat;
	}

	function proceed() {
		if (!selectedSeat) return;
		$cart = { trip, seat: selectedSeat };
		goto('/checkout');
	}
</script>

<svelte:head>
	<title>Sefer Detayı — Kütahyalılar</title>
</svelte:head>

<div class="mx-auto max-w-5xl px-4 py-8">
	<div class="grid gap-8 lg:grid-cols-2">
		<!-- Trip summary -->
		<div class="rounded-xl bg-white p-6 shadow-sm">
			<h2 class="mb-4 text-xl font-bold text-kutahya-dark">Sefer Detayı</h2>
			<dl class="space-y-3 text-sm">
				<div class="flex justify-between">
					<dt class="text-kutahya-muted">Kalkış</dt>
					<dd class="font-semibold">{fmt(trip.departure_time)}</dd>
				</div>
				<div class="flex justify-between">
					<dt class="text-kutahya-muted">Varış</dt>
					<dd class="font-semibold">{fmt(trip.arrival_time)}</dd>
				</div>
				<div class="flex justify-between">
					<dt class="text-kutahya-muted">Fiyat</dt>
					<dd class="text-lg font-bold text-kutahya-red">{Number(trip.price).toFixed(2)} TL</dd>
				</div>
				<div class="flex justify-between">
					<dt class="text-kutahya-muted">Boş Koltuk</dt>
					<dd>{trip.available_seats}</dd>
				</div>
				<div class="flex justify-between">
					<dt class="text-kutahya-muted">Durum</dt>
					<dd>{trip.status}</dd>
				</div>
			</dl>

			{#if selectedSeat}
				<div class="mt-4 rounded-lg bg-green-50 border border-green-200 p-3 text-sm text-green-800">
					Seçilen koltuk: <strong>{selectedSeat.seat_number}</strong>
				</div>
			{/if}

			<button
				onclick={proceed}
				disabled={!selectedSeat}
				class="mt-4 w-full rounded-lg bg-kutahya-accent py-3 font-semibold text-white transition hover:bg-orange-600 disabled:opacity-50 disabled:cursor-not-allowed"
			>
				Devam Et
			</button>
		</div>

		<!-- Seat map -->
		<div>
			{#if trip.seats && trip.seats.length > 0}
				<SeatMap seats={trip.seats} {selectedSeat} onselect={handleSelect} />
			{:else}
				<p class="text-center text-kutahya-muted py-12">Koltuk bilgisi yüklenemedi.</p>
			{/if}
		</div>
	</div>
</div>
