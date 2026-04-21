<script lang="ts">
	let { form } = $props();
	let email = $state(form?.email ?? '');
	let password = $state('');
	let error = $derived(form?.error ?? '');
</script>

<svelte:head>
	<title>Giriş Yap — Kütahyalılar</title>
</svelte:head>

<div class="mx-auto max-w-md px-4 py-12">
	<h1 class="mb-8 text-center text-3xl font-bold text-kutahya-dark">Giriş Yap</h1>

	{#if error}
		<div class="mb-4 rounded-lg bg-red-50 border border-red-200 px-4 py-3 text-sm text-red-700">
			{error}
		</div>
	{/if}

	<form method="POST" class="space-y-5">
		<div>
			<label for="email" class="mb-1 block text-sm font-medium text-gray-700">E-posta</label>
			<input
				id="email"
				name="email"
				type="email"
				bind:value={email}
				required
				class="w-full rounded-lg border-gray-300 focus:border-kutahya-red focus:ring-kutahya-red"
			/>
		</div>
		<div>
			<label for="password" class="mb-1 block text-sm font-medium text-gray-700">Şifre</label>
			<input
				id="password"
				name="password"
				type="password"
				bind:value={password}
				required
				class="w-full rounded-lg border-gray-300 focus:border-kutahya-red focus:ring-kutahya-red"
			/>
		</div>
		<button
			type="submit"
			class="w-full rounded-lg bg-kutahya-red py-2.5 font-semibold text-white transition hover:bg-red-700"
		>
			Giriş Yap
		</button>
	</form>

	<p class="mt-6 text-center text-sm text-kutahya-muted">
		Hesabınız yok mu?
		<a href="/auth/register" class="font-medium text-kutahya-red hover:underline">Kayıt Ol</a>
	</p>
</div>
