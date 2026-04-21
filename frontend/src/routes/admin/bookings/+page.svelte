<script lang="ts">
	import type { Booking } from '$lib/types';

	let { data } = $props();
	let bookings: Booking[] = $derived(data.bookings);
	let statusFilter = $state('');
	let page = $state(0);
	const perPage = 20;

	let filtered = $derived(
		statusFilter ? bookings.filter((b) => b.status === statusFilter) : bookings
	);
	let paged = $derived(filtered.slice(page * perPage, (page + 1) * perPage));
	let totalPages = $derived(Math.max(1, Math.ceil(filtered.length / perPage)));

	$effect(() => {
		page = 0;
	});
</script>

<svelte:head>
	<title>Rezervasyon Yönetimi — Kütahyalılar</title>
</svelte:head>

<h1 class="mb-4 text-2xl font-bold text-kutahya-dark">Rezervasyon Yönetimi</h1>

<!-- Filters -->
<div class="mb-4 flex gap-3">
	<select bind:value={statusFilter} class="rounded-lg border-gray-300 text-sm focus:border-kutahya-red focus:ring-kutahya-red">
		<option value="">Tüm Durumlar</option>
		<option value="confirmed">Onaylandı</option>
		<option value="pending">Beklemede</option>
		<option value="cancelled">İptal Edildi</option>
		<option value="refunded">İade Edildi</option>
		<option value="completed">Tamamlandı</option>
	</select>
</div>

<div class="rounded-xl bg-white shadow-sm overflow-hidden">
	<div class="overflow-x-auto">
		<table class="w-full text-sm">
			<thead class="bg-gray-50">
				<tr class="text-left text-kutahya-muted">
					<th class="px-4 py-3">Bilet Kodu</th>
					<th class="px-4 py-3">Yolcu</th>
					<th class="px-4 py-3">Route</th>
					<th class="px-4 py-3">Koltuk</th>
					<th class="px-4 py-3">Tutar</th>
					<th class="px-4 py-3">Durum</th>
				</tr>
			</thead>
			<tbody>
				{#each paged as b (b.id)}
					<tr class="border-t hover:bg-gray-50">
						<td class="px-4 py-3 font-mono text-xs">{b.ticket_code}</td>
						<td class="px-4 py-3">{b.passenger_name}</td>
						<td class="px-4 py-3 text-xs">{b.trip_id.slice(0, 8)}</td>
						<td class="px-4 py-3">{b.seat_number}</td>
						<td class="px-4 py-3 font-semibold">{Number(b.total_price).toFixed(2)} TL</td>
						<td class="px-4 py-3">
							<span class="rounded-full px-2 py-0.5 text-xs font-medium
								{b.status === 'confirmed' ? 'bg-green-100 text-green-800' :
								b.status === 'pending' ? 'bg-yellow-100 text-yellow-800' :
								b.status === 'cancelled' ? 'bg-red-100 text-red-800' :
								b.status === 'refunded' ? 'bg-gray-100 text-gray-600' :
								'bg-blue-100 text-blue-800'}">
								{b.status}
							</span>
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
