<script lang="ts">
	interface Props {
		message: string;
		onclose?: () => void;
	}

	let { message, onclose }: Props = $props();
</script>

<div
	class="flex items-center gap-3 rounded-lg bg-red-50 border border-red-200 px-4 py-3 text-red-800"
>
	<span class="text-lg">&#9888;&#65039;</span>
	<p class="flex-1">{message}</p>
	{#if onclose}
		<button onclick={onclose} class="text-red-500 hover:text-red-700 text-xl leading-none">&times;</button>
	{/if}
</div>
