<script lang="ts">
	import '../app.css';
	import type { AuthUser } from '$lib/types';
	import Navbar from '$lib/components/Navbar.svelte';
	import Footer from '$lib/components/Footer.svelte';

	let { data, children } = $props();
	let user: AuthUser | null = $derived(data.user);
</script>

<div class="flex min-h-screen flex-col">
	<Navbar {user} />
	<main class="flex-1">
		{@render children()}
	</main>
	<Footer />
</div>
