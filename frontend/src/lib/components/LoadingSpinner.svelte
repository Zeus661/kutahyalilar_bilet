<script lang="ts">
	import type { Snippet } from 'svelte';

	interface Props {
		message?: string;
		children?: Snippet;
	}

	let { message = 'Yükleniyor...', children }: Props = $props();
</script>

<div class="flex flex-col items-center justify-center py-12">
	<div
		class="h-10 w-10 animate-spin rounded-full border-4 border-kutahya-muted border-t-kutahya-red"
	></div>
	{#if children}
		{@render children()}
	{:else}
		<p class="mt-3 text-kutahya-muted">{message}</p>
	{/if}
</div>
