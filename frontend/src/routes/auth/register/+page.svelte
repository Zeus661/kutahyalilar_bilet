<script lang="ts">
	let { form } = $props();
	let email = $state(form?.email ?? '');
	let password = $state('');
	let confirmPassword = $state('');
	let error = $derived(form?.error ?? '');
	let mismatch = $derived(password !== confirmPassword && confirmPassword.length > 0);
</script>

<svelte:head>
	<title>Kayıt Ol — Kütahyalılar</title>
</svelte:head>

<div class="mx-auto max-w-md px-4 py-12">
	<h1 class="mb-8 text-center text-3xl font-bold text-kutahya-dark">Kayıt Ol</h1>

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
				minlength="8"
				required
				class="w-full rounded-lg border-gray-300 focus:border-kutahya-red focus:ring-kutahya-red"
			/>
		</div>
		<div>
			<label for="confirmPassword" class="mb-1 block text-sm font-medium text-gray-700">Şifre Tekrar</label>
			<input
				id="confirmPassword"
				name="confirmPassword"
				type="password"
				bind:value={confirmPassword}
				minlength="8"
				required
				class="w-full rounded-lg border-gray-300 focus:border-kutahya-red focus:ring-kutahya-red {mismatch ? 'border-red-500' : ''}"
			/>
			{#if mismatch}
				<p class="mt-1 text-xs text-red-500">Şifreler eşleşmiyor.</p>
			{/if}
		</div>
		<button
			type="submit"
			disabled={mismatch}
			class="w-full rounded-lg bg-kutahya-red py-2.5 font-semibold text-white transition hover:bg-red-700 disabled:opacity-50"
		>
			Kayıt Ol
		</button>
	</form>

	<p class="mt-6 text-center text-sm text-kutahya-muted">
		Zaten hesabınız var mı?
		<a href="/auth/login" class="font-medium text-kutahya-red hover:underline">Giriş Yap</a>
	</p>
</div>
