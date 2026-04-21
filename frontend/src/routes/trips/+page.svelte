<script lang="ts">
	import TripCard from '$lib/components/TripCard.svelte';
	import LoadingSpinner from '$lib/components/LoadingSpinner.svelte';
	import { goto } from '$app/navigation';

	let { data } = $props();

	let origin = $state(data.origin);
	let destination = $state(data.destination);
	let date = $state(data.date);

	function search(e: Event) {
		e.preventDefault();
		if (!origin || !destination || !date) return;
		const params = new URLSearchParams({ origin, destination, date });
		goto(`/trips?${params}`);
	}

	function selectTrip(tripId: string) {
		goto(`/trips/${tripId}`);
	}
</script>

<svelte:head>
	<title>Sefer Ara — Kütahyalılar</title>
</svelte:head>

<div class="mx-auto max-w-4xl px-4 py-8">
	<!-- Refine search -->
	<form onsubmit={search} class="mb-8 rounded-xl bg-white p-4 shadow-sm">
		<div class="grid gap-3 sm:grid-cols-4">
			<input bind:value={origin} type="text" placeholder="Kalkış" class="rounded-lg border-gray-300 focus:border-kutahya-red focus:ring-kutahya-red" required />
			<input bind:value={destination} type="text" placeholder="Varış" class="rounded-lg border-gray-300 focus:border-kutahya-red focus:ring-kutahya-red" required />
			<input bind:value={date} type="date" class="rounded-lg border-gray-300 focus:border-kutahya-red focus:ring-kutahya-red" required />
			<button type="submit" class="rounded-lg bg-kutahya-red py-2 font-semibold text-white hover:bg-red-700">Ara</button>
		</div>
	</form>

	{#if data.error}
		<div class="mb-4 rounded-lg bg-red-50 border border-red-200 px-4 py-3 text-red-700">{data.error}</div>
	{/if}

	{#if data.trips.length === 0 && data.origin}
		<div class="py-12 text-center text-kutahya-muted">Bu güzergahta sefer bulunamadı.</div>
	{:else if data.trips.length === 0}
		<LoadingSpinner message="Seferleri aramak için yukarıdaki formu doldurun." />
	{:else}
		<div class="space-y-4">
			{#each data.trips as trip (trip.id)}
				<TripCard {trip} onselect={selectTrip} />
			{/each}
		</div>
	{/if}
</div>
