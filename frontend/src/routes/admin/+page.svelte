<script lang="ts">
	let { data } = $props();
	const { stats, recentBookings } = data;
</script>

<svelte:head>
	<title>Admin Dashboard — Kütahyalılar</title>
</svelte:head>

<h1 class="mb-6 text-2xl font-bold text-kutahya-dark">Admin Dashboard</h1>

<!-- Stats cards -->
<div class="mb-8 grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
	<div class="rounded-xl bg-white p-5 shadow-sm">
		<p class="text-sm text-kutahya-muted">Toplam Rezervasyon</p>
		<p class="mt-1 text-3xl font-bold text-kutahya-dark">{stats.totalBookings}</p>
	</div>
	<div class="rounded-xl bg-white p-5 shadow-sm">
		<p class="text-sm text-kutahya-muted">Toplam Gelir</p>
		<p class="mt-1 text-3xl font-bold text-kutahya-red">{stats.totalRevenue.toFixed(2)} TL</p>
	</div>
	<div class="rounded-xl bg-white p-5 shadow-sm">
		<p class="text-sm text-kutahya-muted">Aktif Seferler</p>
		<p class="mt-1 text-3xl font-bold text-kutahya-dark">{stats.activeTrips}</p>
	</div>
	<div class="rounded-xl bg-white p-5 shadow-sm">
		<p class="text-sm text-kutahya-muted">Kayıtlı Kullanıcılar</p>
		<p class="mt-1 text-3xl font-bold text-kutahya-dark">{stats.registeredUsers}</p>
	</div>
</div>

<!-- Recent bookings -->
<div class="rounded-xl bg-white p-5 shadow-sm">
	<h2 class="mb-4 text-lg font-semibold text-kutahya-dark">Son Rezervasyonlar</h2>
	{#if recentBookings.length === 0}
		<p class="text-kutahya-muted">Henüz rezervasyon yok.</p>
	{:else}
		<div class="overflow-x-auto">
			<table class="w-full text-sm">
				<thead>
					<tr class="border-b text-left text-kutahya-muted">
						<th class="pb-2">Bilet Kodu</th>
						<th class="pb-2">Yolcu</th>
						<th class="pb-2">Koltuk</th>
						<th class="pb-2">Tutar</th>
						<th class="pb-2">Durum</th>
					</tr>
				</thead>
				<tbody>
					{#each recentBookings as b (b.id)}
						<tr class="border-b last:border-0">
							<td class="py-2 font-mono">{b.ticket_code}</td>
							<td class="py-2">{b.passenger_name}</td>
							<td class="py-2">{b.seat_number}</td>
							<td class="py-2 font-semibold">{Number(b.total_price).toFixed(2)} TL</td>
							<td class="py-2">{b.status}</td>
						</tr>
					{/each}
				</tbody>
			</table>
		</div>
	{/if}
</div>
