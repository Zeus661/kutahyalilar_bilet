<script lang="ts">
	let { children } = $props();
</script>

<div class="mx-auto max-w-6xl px-4 py-6">
	<div class="mb-6 flex gap-4 border-b pb-3">
		<a href="/admin" class="text-sm font-medium text-kutahya-muted hover:text-kutahya-red">Dashboard</a>
		<a href="/admin/trips" class="text-sm font-medium text-kutahya-muted hover:text-kutahya-red">Seferler</a>
		<a href="/admin/bookings" class="text-sm font-medium text-kutahya-muted hover:text-kutahya-red">Rezervasyonlar</a>
	</div>
	{@render children()}
</div>
