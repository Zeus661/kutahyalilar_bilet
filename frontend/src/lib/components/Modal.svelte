<script lang="ts">
	import type { Snippet } from 'svelte';

	interface Props {
		title: string;
		open: boolean;
		onclose: () => void;
		children: Snippet;
	}

	let { title, open, onclose, children }: Props = $props();

	function handleBackdrop(e: MouseEvent) {
		if (e.target === e.currentTarget) onclose();
	}

	function handleKeydown(e: KeyboardEvent) {
		if (e.key === 'Escape') onclose();
	}
</script>

{#if open}
	<!-- svelte-ignore a11y_no_noninteractive_element_interactions a11y_interactive_supports_focus -->
	<div
		class="fixed inset-0 z-50 flex items-center justify-center bg-black/50"
		onclick={handleBackdrop}
		onkeydown={handleKeydown}
		role="dialog"
		aria-modal="true"
		tabindex="-1"
	>
		<div class="w-full max-w-lg rounded-xl bg-white p-6 shadow-xl">
			<div class="mb-4 flex items-center justify-between">
				<h2 class="text-xl font-bold text-kutahya-dark">{title}</h2>
				<button onclick={onclose} class="text-gray-400 hover:text-gray-600 text-2xl leading-none">&times;</button>
			</div>
			{@render children()}
		</div>
	</div>
{/if}
