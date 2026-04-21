<script lang="ts">
	import type { Trip } from '$lib/types';

	interface Props {
		trip: Trip;
		onselect: (tripId: string) => void;
	}

	let { trip, onselect }: Props = $props();

	function fmt(iso: string) {
		return new Date(iso).toLocaleString('tr-TR', {
			hour: '2-digit',
			minute: '2-digit',
			day: 'numeric',
			month: 'short'
		});
	}
</script>

<div class="rounded-xl border border-gray-200 bg-white p-5 shadow-sm transition hover:shadow-md">
	<div class="flex items-center justify-between">
		<div>
			<div class="flex items-center gap-2 text-lg font-semibold text-kutahya-dark">
				<span>{fmt(trip.departure_time)}</span>
				<span class="text-kutahya-muted">&rarr;</span>
				<span>{fmt(trip.arrival_time)}</span>
			</div>
			<p class="mt-1 text-sm text-kutahya-muted">
				{trip.available_seats} boş koltuk
			</p>
		</div>
		<div class="text-right">
			<p class="text-2xl font-bold text-kutahya-red">{Number(trip.price).toFixed(2)} TL</p>
			<span
				class="mt-1 inline-block rounded-full bg-kutahya-light px-2 py-0.5 text-xs font-medium text-kutahya-muted"
			>
				{trip.status}
			</span>
		</div>
	</div>
	<div class="mt-4 flex justify-end">
		<button
			onclick={() => onselect(trip.id)}
			class="rounded-lg bg-kutahya-accent px-6 py-2 text-sm font-semibold text-white transition hover:bg-orange-600"
		>
			Seç
		</button>
	</div>
</div>
