<script lang="ts">
	import BookingCard from '$lib/components/BookingCard.svelte';
	import type { Booking } from '$lib/types';

	let { data } = $props();

	let activeTab = $state<'active' | 'past'>('active');

	let activeBookings = $derived(
		(data.bookings as Booking[]).filter((b: Booking) => b.status === 'confirmed' || b.status === 'pending')
	);
	let pastBookings = $derived(
		(data.bookings as Booking[]).filter((b: Booking) => b.status === 'cancelled' || b.status === 'refunded' || b.status === 'completed')
	);

	function handleCancel(bookingId: string) {
		if (confirm('Biletinizi iptal etmek istediğinize emin misiniz?')) {
			const form = document.createElement('form');
			form.method = 'POST';
			form.action = '?/cancel';
			const input = document.createElement('input');
			input.type = 'hidden';
			input.name = 'bookingId';
			input.value = bookingId;
			form.appendChild(input);
			document.body.appendChild(form);
			form.submit();
		}
	}
</script>

<svelte:head>
	<title>Biletlerim — Kütahyalılar</title>
</svelte:head>

<div class="mx-auto max-w-4xl px-4 py-8">
	<h1 class="mb-6 text-2xl font-bold text-kutahya-dark">Biletlerim</h1>

	{#if data.error}
		<div class="mb-4 rounded-lg bg-red-50 border border-red-200 px-4 py-3 text-red-700">{data.error}</div>
	{/if}

	<!-- Tabs -->
	<div class="mb-6 flex gap-1 border-b">
		<button
			onclick={() => (activeTab = 'active')}
			class="px-4 py-2 text-sm font-medium transition {activeTab === 'active' ? 'border-b-2 border-kutahya-red text-kutahya-red' : 'text-kutahya-muted hover:text-gray-700'}"
		>
			Aktif ({activeBookings.length})
		</button>
		<button
			onclick={() => (activeTab = 'past')}
			class="px-4 py-2 text-sm font-medium transition {activeTab === 'past' ? 'border-b-2 border-kutahya-red text-kutahya-red' : 'text-kutahya-muted hover:text-gray-700'}"
		>
			Geçmiş ({pastBookings.length})
		</button>
	</div>

	{#if activeTab === 'active'}
		{#if activeBookings.length === 0}
			<p class="py-12 text-center text-kutahya-muted">Aktif biletiniz bulunmamaktadır.</p>
		{:else}
			<div class="space-y-4">
				{#each activeBookings as booking (booking.id)}
					<BookingCard {booking} oncancel={handleCancel} />
				{/each}
			</div>
		{/if}
	{:else}
		{#if pastBookings.length === 0}
			<p class="py-12 text-center text-kutahya-muted">Geçmiş biletiniz bulunmamaktadır.</p>
		{:else}
			<div class="space-y-4">
				{#each pastBookings as booking (booking.id)}
					<BookingCard {booking} showActions={false} />
				{/each}
			</div>
		{/if}
	{/if}
</div>
