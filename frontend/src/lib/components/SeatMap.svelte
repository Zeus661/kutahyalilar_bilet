<script lang="ts">
	import type { Seat } from '$lib/types';

	interface Props {
		seats: Seat[];
		selectedSeat: Seat | null;
		onselect: (seat: Seat) => void;
	}

	let { seats, selectedSeat, onselect }: Props = $props();

	function seatState(seat: Seat): 'available' | 'reserved' | 'selected' {
		if (selectedSeat?.id === seat.id) return 'selected';
		if (seat.is_reserved) return 'reserved';
		return 'available';
	}

	const seatClasses = {
		available: 'bg-white border-gray-300 text-gray-700 cursor-pointer hover:border-kutahya-red hover:bg-red-50',
		reserved: 'bg-gray-200 border-gray-300 text-gray-400 cursor-not-allowed',
		selected: 'bg-kutahya-red border-kutahya-red text-white cursor-pointer'
	};

	function handleClick(seat: Seat) {
		if (!seat.is_reserved) onselect(seat);
	}

	// Build 2+1 layout rows: 4 seats per row (2 + aisle + 1), skip seat 13 (driver)
	let rows: Seat[][] = $derived.by(() => {
		const sorted = [...seats].sort((a, b) => a.seat_number - b.seat_number);
		const r: Seat[][] = [];
		for (let i = 0; i < sorted.length; i += 4) {
			r.push(sorted.slice(i, i + 4));
		}
		return r;
	});
</script>

<div class="mx-auto max-w-md">
	<div class="mb-4 flex items-center gap-4 text-sm">
		<span class="flex items-center gap-1"><span class="inline-block h-5 w-5 rounded border bg-white"></span> Boş</span>
		<span class="flex items-center gap-1"><span class="inline-block h-5 w-5 rounded bg-kutahya-red"></span> Seçili</span>
		<span class="flex items-center gap-1"><span class="inline-block h-5 w-5 rounded bg-gray-200"></span> Dolu</span>
	</div>

	<div class="rounded-xl border-2 border-gray-300 bg-gray-50 p-4">
		<div class="mb-2 flex justify-end text-xs text-kutahya-muted">Koltuk Düzeni</div>
		{#each rows as row}
			<div class="mb-1 flex items-center gap-1">
				{#each row as seat, i}
					{#if i === 2}
						<div class="w-6"></div>
					{/if}
					<button
						onclick={() => handleClick(seat)}
						disabled={seat.is_reserved}
						class="flex h-10 w-10 items-center justify-center rounded border text-xs font-semibold transition {seatClasses[seatState(seat)]}"
					>
						{seat.seat_number}
					</button>
				{/each}
			</div>
		{/each}
	</div>
</div>
