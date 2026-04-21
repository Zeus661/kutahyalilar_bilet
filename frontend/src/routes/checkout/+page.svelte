<script lang="ts">
	import { cart } from '$lib/stores/cart';
	import { goto } from '$app/navigation';
	import ErrorBanner from '$lib/components/ErrorBanner.svelte';

	let { form } = $props();
	let cartItem = $derived($cart);
	let submitting = $state(false);

	let passenger_name = $derived(form?.passenger_name ?? '');
	let passenger_tc = $derived(form?.passenger_tc ?? '');
	let passenger_gender = $derived(form?.passenger_gender ?? '');
	let passenger_dob = $derived(form?.passenger_dob ?? '');
	let cardNumber = $state('');
	let cardExpiry = $state('');
	let cardCvv = $state('');
	let cardName = $state('');

	let tcError = $derived(passenger_tc.length > 0 && (!/^\d+$/.test(passenger_tc) || passenger_tc.length !== 11));

	function formatCardNumber(e: Event) {
		const raw = (e.target as HTMLInputElement).value.replace(/\D/g, '').slice(0, 16);
		cardNumber = raw.replace(/(.{4})/g, '$1 ').trim();
	}

	function formatExpiry(e: Event) {
		let raw = (e.target as HTMLInputElement).value.replace(/\D/g, '').slice(0, 4);
		if (raw.length >= 3) raw = raw.slice(0, 2) + '/' + raw.slice(2);
		cardExpiry = raw;
	}

	// If cart is empty, redirect
	$effect(() => {
		if (!cartItem) goto('/');
	});
</script>

<svelte:head>
	<title>Ödeme — Kütahyalılar</title>
</svelte:head>

{#if cartItem}
	<div class="mx-auto max-w-5xl px-4 py-8">
		<h1 class="mb-8 text-2xl font-bold text-kutahya-dark">Ödeme</h1>

		{#if form?.error}
			<ErrorBanner message={form.error} />
		{/if}

		<div class="grid gap-8 lg:grid-cols-5">
			<!-- Passenger + Payment form (left) -->
			<form method="POST" class="space-y-6 lg:col-span-3">
				<input type="hidden" name="trip_id" value={cartItem.trip.id} />
				<input type="hidden" name="seat_id" value={cartItem.seat.id} />

				<!-- Passenger details -->
				<div class="rounded-xl bg-white p-6 shadow-sm">
					<h2 class="mb-4 text-lg font-semibold text-kutahya-dark">Yolcu Bilgileri</h2>
					<div class="space-y-4">
						<div>
							<label for="passenger_name" class="mb-1 block text-sm font-medium text-gray-700">Ad Soyad</label>
							<input id="passenger_name" name="passenger_name" type="text" bind:value={passenger_name} required
								class="w-full rounded-lg border-gray-300 focus:border-kutahya-red focus:ring-kutahya-red" />
						</div>
						<div>
							<label for="passenger_tc" class="mb-1 block text-sm font-medium text-gray-700">TC Kimlik No</label>
							<input id="passenger_tc" name="passenger_tc" type="text" bind:value={passenger_tc} maxlength="11" required
								class="w-full rounded-lg border-gray-300 focus:border-kutahya-red focus:ring-kutahya-red {tcError ? 'border-red-500' : ''}" />
							{#if tcError}
								<p class="mt-1 text-xs text-red-500">TC Kimlik No 11 haneli rakam olmalıdır.</p>
							{/if}
						</div>
						<div>
							<label for="passenger_gender" class="mb-1 block text-sm font-medium text-gray-700">Cinsiyet</label>
							<select id="passenger_gender" name="passenger_gender" bind:value={passenger_gender} required
								class="w-full rounded-lg border-gray-300 focus:border-kutahya-red focus:ring-kutahya-red">
								<option value="">Seçiniz</option>
								<option value="Erkek">Erkek</option>
								<option value="Kadın">Kadın</option>
								<option value="Diğer">Diğer</option>
							</select>
						</div>
						<div>
							<label for="passenger_dob" class="mb-1 block text-sm font-medium text-gray-700">Doğum Tarihi</label>
							<input id="passenger_dob" name="passenger_dob" type="date" bind:value={passenger_dob} required
								class="w-full rounded-lg border-gray-300 focus:border-kutahya-red focus:ring-kutahya-red" />
						</div>
					</div>
				</div>

				<!-- Mock payment -->
				<div class="rounded-xl bg-white p-6 shadow-sm">
					<h2 class="mb-4 text-lg font-semibold text-kutahya-dark">Ödeme Bilgileri</h2>
					<p class="mb-4 text-xs text-kutahya-muted">(Test: herhangi bir değer girin — ödeme simülasyondur)</p>
					<div class="space-y-4">
						<div>
							<label for="cardNumber" class="mb-1 block text-sm font-medium text-gray-700">Kart Numarası</label>
							<input id="cardNumber" type="text" bind:value={cardNumber} oninput={formatCardNumber} placeholder="XXXX XXXX XXXX XXXX"
								class="w-full rounded-lg border-gray-300 focus:border-kutahya-red focus:ring-kutahya-red" />
						</div>
						<div class="grid grid-cols-2 gap-4">
							<div>
								<label for="cardExpiry" class="mb-1 block text-sm font-medium text-gray-700">Son Kullanma Tarihi</label>
								<input id="cardExpiry" type="text" bind:value={cardExpiry} oninput={formatExpiry} placeholder="MM/YY"
									class="w-full rounded-lg border-gray-300 focus:border-kutahya-red focus:ring-kutahya-red" />
							</div>
							<div>
								<label for="cardCvv" class="mb-1 block text-sm font-medium text-gray-700">CVV</label>
								<input id="cardCvv" type="text" bind:value={cardCvv} maxlength="3" placeholder="123"
									class="w-full rounded-lg border-gray-300 focus:border-kutahya-red focus:ring-kutahya-red" />
							</div>
						</div>
						<div>
							<label for="cardName" class="mb-1 block text-sm font-medium text-gray-700">Kart Üzerindeki İsim</label>
							<input id="cardName" type="text" bind:value={cardName}
								class="w-full rounded-lg border-gray-300 focus:border-kutahya-red focus:ring-kutahya-red" />
						</div>
					</div>
				</div>

				<button
					type="submit"
					class="w-full rounded-lg bg-kutahya-accent py-3 text-lg font-bold text-white transition hover:bg-orange-600"
				>
					Ödemeyi Tamamla
				</button>
			</form>

			<!-- Order summary (right) -->
			<div class="lg:col-span-2">
				<div class="sticky top-24 rounded-xl bg-white p-6 shadow-sm">
					<h2 class="mb-4 text-lg font-semibold text-kutahya-dark">Sipariş Özeti</h2>
					<dl class="space-y-2 text-sm">
						<div class="flex justify-between">
							<dt class="text-kutahya-muted">Koltuk No</dt>
							<dd class="font-semibold">{cartItem.seat.seat_number}</dd>
						</div>
						<div class="flex justify-between">
							<dt class="text-kutahya-muted">Bilet Fiyatı</dt>
							<dd class="font-semibold">{Number(cartItem.trip.price).toFixed(2)} TL</dd>
						</div>
						<hr class="my-3" />
						<div class="flex justify-between text-base font-bold">
							<dt>Toplam</dt>
							<dd class="text-kutahya-red">{Number(cartItem.trip.price).toFixed(2)} TL</dd>
						</div>
					</dl>
				</div>
			</div>
		</div>
	</div>
{/if}
