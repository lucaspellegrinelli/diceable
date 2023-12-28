<script lang="ts">
	import { Loader } from 'lucide-svelte';

	export let enabled = false;
</script>

{#if enabled}
	<div class="fixed w-full h-full bg-black bg-opacity-50 z-50 flex justify-center items-center">
		<Loader size={64} class="text-white" />
	</div>
{/if}
