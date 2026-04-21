<script lang="ts">
	import Modal from '$lib/components/Modal.svelte';
	import type { Trip, Route } from '$lib/types';

	let { data } = $props();
	let trips: Trip[] = $derived(data.trips);
	let showCreateModal = $state(false);
	let page = $state(0);
	const perPage = 20;

	let paged = $derived(trips.slice(page * perPage, (page + 1) * perPage));
	let totalPages = $derived(Math.max(1, Math.ceil(trips.length / perPage)));

	function fmt(iso: string) {
		return new Date(iso).toLocaleString('tr-TR', { day: 'numeric', month: 'short', hour: '2-digit', minute: '2-digit' });
	}

	function cancelTrip(tripId: string) {
		if (!confirm('Bu seferi iptal etmek istediğinize emin misiniz?')) return;
		const form = document.createElement('form');
		form.method = 'POST';
		form.action = '?/cancel';
		const input = document.createElement('input');
		input.type = 'hidden';
		input.name = 'tripId';
		input.value = tripId;
		form.appendChild(input);
		document.body.appendChild(form);
		form.submit();
	}
</script>

<svelte:head>
	<title>Sefer Yönetimi — Kütahyalılar</title>
</svelte:head>

<div class="mb-4 flex items-center justify-between">
	<h1 class="text-2xl font-bold text-kutahya-dark">Sefer Yönetimi</h1>
	<button onclick={() => (showCreateModal = true)} class="rounded-lg bg-kutahya-accent px-4 py-2 text-sm font-semibold text-white hover:bg-orange-600">
		Yeni Sefer Ekle
	</button>
</div>

<div class="rounded-xl bg-white shadow-sm overflow-hidden">
	<div class="overflow-x-auto">
		<table class="w-full text-sm">
			<thead class="bg-gray-50">
				<tr class="text-left text-kutahya-muted">
					<th class="px-4 py-3">ID</th>
					<th class="px-4 py-3">Route ID</th>
					<th class="px-4 py-3">Kalkış</th>
					<th class="px-4 py-3">Varış</th>
					<th class="px-4 py-3">Fiyat</th>
					<th class="px-4 py-3">Boş Koltuk</th>
					<th class="px-4 py-3">Durum</th>
					<th class="px-4 py-3">İşlemler</th>
				</tr>
			</thead>
			<tbody>
				{#each paged as trip (trip.id)}
					<tr class="border-t hover:bg-gray-50">
						<td class="px-4 py-3 font-mono text-xs">{trip.id.slice(0, 8)}</td>
						<td class="px-4 py-3 font-mono text-xs">{trip.route_id.slice(0, 8)}</td>
						<td class="px-4 py-3">{fmt(trip.departure_time)}</td>
						<td class="px-4 py-3">{fmt(trip.arrival_time)}</td>
						<td class="px-4 py-3 font-semibold">{Number(trip.price).toFixed(2)} TL</td>
						<td class="px-4 py-3">{trip.available_seats}</td>
						<td class="px-4 py-3">{trip.status}</td>
						<td class="px-4 py-3">
							{#if trip.status !== 'cancelled'}
								<button onclick={() => cancelTrip(trip.id)} class="text-red-600 hover:underline text-xs">İptal Et</button>
							{:else}
								<span class="text-kutahya-muted text-xs">İptal</span>
							{/if}
						</td>
					</tr>
				{/each}
			</tbody>
		</table>
	</div>

	{#if totalPages > 1}
		<div class="flex items-center justify-center gap-2 border-t px-4 py-3">
			<button onclick={() => (page = Math.max(0, page - 1))} disabled={page === 0} class="px-3 py-1 rounded border text-sm disabled:opacity-50">&laquo;</button>
			<span class="text-sm text-kutahya-muted">{page + 1} / {totalPages}</span>
			<button onclick={() => (page = Math.min(totalPages - 1, page + 1))} disabled={page >= totalPages - 1} class="px-3 py-1 rounded border text-sm disabled:opacity-50">&raquo;</button>
		</div>
	{/if}
</div>

<Modal title="Yeni Sefer Ekle" open={showCreateModal} onclose={() => (showCreateModal = false)}>
	<form method="POST" action="?/create" class="space-y-4">
		<div>
			<label class="mb-1 block text-sm font-medium">Route ID</label>
			<select name="route_id" required class="w-full rounded-lg border-gray-300 focus:border-kutahya-red focus:ring-kutahya-red">
				{#each data.routes as r (r.id)}
					<option value={r.id}>{r.origin} → {r.destination}</option>
				{/each}
			</select>
		</div>
		<div>
			<label class="mb-1 block text-sm font-medium">Bus ID</label>
			<input name="bus_id" type="text" required class="w-full rounded-lg border-gray-300 focus:border-kutahya-red focus:ring-kutahya-red" />
		</div>
		<div class="grid grid-cols-2 gap-3">
			<div>
				<label class="mb-1 block text-sm font-medium">Kalkış</label>
				<input name="departure_time" type="datetime-local" required class="w-full rounded-lg border-gray-300 focus:border-kutahya-red focus:ring-kutahya-red" />
			</div>
			<div>
				<label class="mb-1 block text-sm font-medium">Varış</label>
				<input name="arrival_time" type="datetime-local" required class="w-full rounded-lg border-gray-300 focus:border-kutahya-red focus:ring-kutahya-red" />
			</div>
		</div>
		<div>
			<label class="mb-1 block text-sm font-medium">Fiyat</label>
			<input name="price" type="number" step="0.01" required class="w-full rounded-lg border-gray-300 focus:border-kutahya-red focus:ring-kutahya-red" />
		</div>
		<button type="submit" class="w-full rounded-lg bg-kutahya-accent py-2 font-semibold text-white hover:bg-orange-600">Oluştur</button>
	</form>
</Modal>
