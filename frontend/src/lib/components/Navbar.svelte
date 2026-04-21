<script lang="ts">
	import type { AuthUser } from '$lib/types';

	interface Props {
		user: AuthUser | null;
	}

	let { user }: Props = $props();
	let menuOpen = $state(false);
	let dropdownOpen = $state(false);
</script>

<nav class="sticky top-0 z-40 bg-kutahya-dark shadow-lg no-print">
	<div class="mx-auto flex max-w-6xl items-center justify-between px-4 py-3">
		<a href="/" class="text-2xl font-bold text-white">
			K<span class="text-kutahya-accent">u</span>tahyalılar
		</a>

		<!-- Desktop -->
		<div class="hidden items-center gap-6 md:flex">
			<a href="/" class="text-gray-300 transition hover:text-white">Ana Sayfa</a>
			<a href="/trips" class="text-gray-300 transition hover:text-white">Seferler</a>
			{#if user}
				<a href="/bookings" class="text-gray-300 transition hover:text-white">Biletlerim</a>
				<div class="relative">
					<button
						onclick={() => (dropdownOpen = !dropdownOpen)}
						class="text-gray-300 transition hover:text-white"
					>
						{user.email}
					</button>
					{#if dropdownOpen}
						<div class="absolute right-0 mt-2 w-40 rounded-lg bg-white py-1 shadow-lg">
							{#if user.is_admin}
								<a href="/admin" class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100">Admin Paneli</a>
							{/if}
							<form method="POST" action="/auth/logout">
								<button type="submit" class="block w-full px-4 py-2 text-left text-sm text-red-600 hover:bg-gray-100">
									Çıkış Yap
								</button>
							</form>
						</div>
					{/if}
				</div>
			{:else}
				<a href="/auth/login" class="rounded-lg bg-kutahya-accent px-4 py-2 text-sm font-semibold text-white transition hover:bg-orange-600">Giriş Yap</a>
				<a href="/auth/register" class="text-gray-300 transition hover:text-white">Kayıt Ol</a>
			{/if}
		</div>

		<!-- Mobile hamburger -->
		<button class="text-white md:hidden" onclick={() => (menuOpen = !menuOpen)}>
			<svg class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
				{#if menuOpen}
					<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
				{:else}
					<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
				{/if}
			</svg>
		</button>
	</div>

	<!-- Mobile menu -->
	{#if menuOpen}
		<div class="border-t border-gray-700 px-4 pb-4 md:hidden">
			<a href="/" class="block py-2 text-gray-300">Ana Sayfa</a>
			<a href="/trips" class="block py-2 text-gray-300">Seferler</a>
			{#if user}
				<a href="/bookings" class="block py-2 text-gray-300">Biletlerim</a>
				{#if user.is_admin}
					<a href="/admin" class="block py-2 text-gray-300">Admin Paneli</a>
				{/if}
				<form method="POST" action="/auth/logout">
					<button type="submit" class="block w-full py-2 text-left text-red-400">Çıkış Yap</button>
				</form>
			{:else}
				<a href="/auth/login" class="block py-2 text-gray-300">Giriş Yap</a>
				<a href="/auth/register" class="block py-2 text-gray-300">Kayıt Ol</a>
			{/if}
		</div>
	{/if}
</nav>
