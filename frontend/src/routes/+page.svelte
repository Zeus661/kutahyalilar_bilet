<script lang="ts">
	let origin = $state('');
	let destination = $state('');
	let date = $state('');

	function search(e: Event) {
		e.preventDefault();
		if (!origin || !destination || !date) return;
		const params = new URLSearchParams({ origin, destination, date });
		window.location.href = `/trips?${params}`;
	}
</script>

<svelte:head>
	<title>Kütahyalılar Turizm — Güvenli Yolculuk</title>
</svelte:head>

<!-- Hero -->
<section class="bg-gradient-to-br from-kutahya-dark to-kutahya-red px-4 py-20 text-white">
	<div class="mx-auto max-w-4xl text-center">
		<h1 class="text-4xl font-extrabold leading-tight md:text-5xl">
			Kütahya'dan Her Yere<br />Güvenli Yolculuk
		</h1>
		<p class="mt-4 text-lg text-gray-200">Konforlu ve güvenli seyahat deneyimi için biletinizi hemen alın.</p>

		<!-- Search form -->
		<form onsubmit={search} class="mx-auto mt-10 max-w-3xl">
			<div class="grid gap-4 rounded-xl bg-white/10 p-6 backdrop-blur sm:grid-cols-4">
				<div>
					<label for="origin" class="mb-1 block text-sm font-medium text-gray-200">Kalkış</label>
					<input
						id="origin"
						bind:value={origin}
						type="text"
						placeholder="İstanbul"
						class="w-full rounded-lg border-0 bg-white/20 px-4 py-2.5 text-white placeholder-gray-300 focus:ring-2 focus:ring-kutahya-accent"
						required
					/>
				</div>
				<div>
					<label for="destination" class="mb-1 block text-sm font-medium text-gray-200">Varış</label>
					<input
						id="destination"
						bind:value={destination}
						type="text"
						placeholder="Ankara"
						class="w-full rounded-lg border-0 bg-white/20 px-4 py-2.5 text-white placeholder-gray-300 focus:ring-2 focus:ring-kutahya-accent"
						required
					/>
				</div>
				<div>
					<label for="date" class="mb-1 block text-sm font-medium text-gray-200">Tarih</label>
					<input
						id="date"
						bind:value={date}
						type="date"
						class="w-full rounded-lg border-0 bg-white/20 px-4 py-2.5 text-white focus:ring-2 focus:ring-kutahya-accent"
						required
					/>
				</div>
				<div class="flex items-end">
					<button
						type="submit"
						class="w-full rounded-lg bg-kutahya-accent px-6 py-2.5 font-semibold text-white transition hover:bg-orange-600"
					>
						Ara
					</button>
				</div>
			</div>
		</form>
	</div>
</section>

<!-- Features -->
<section class="mx-auto max-w-5xl px-4 py-16">
	<h2 class="mb-10 text-center text-2xl font-bold text-kutahya-dark">Neden Kütahyalılar?</h2>
	<div class="grid gap-6 md:grid-cols-3">
		<div class="rounded-xl bg-white p-6 text-center shadow-sm">
			<div class="mb-3 text-4xl">&#128737;&#65039;</div>
			<h3 class="text-lg font-semibold text-kutahya-dark">Güvenli Ödeme</h3>
			<p class="mt-2 text-sm text-kutahya-muted">256-bit SSL şifreleme ile ödemeleriniz güvende.</p>
		</div>
		<div class="rounded-xl bg-white p-6 text-center shadow-sm">
			<div class="mb-3 text-4xl">&#128652;</div>
			<h3 class="text-lg font-semibold text-kutahya-dark">Modern Araçlar</h3>
			<p class="mt-2 text-sm text-kutahya-muted">Konforlu koltuklar ve güncel filo ile yolculuk.</p>
		</div>
		<div class="rounded-xl bg-white p-6 text-center shadow-sm">
			<div class="mb-3 text-4xl">&#128241;</div>
			<h3 class="text-lg font-semibold text-kutahya-dark">Kolay Rezervasyon</h3>
			<p class="mt-2 text-sm text-kutahya-muted">Birkaç tıklamayla biletinizi ayırtın.</p>
		</div>
	</div>
</section>
