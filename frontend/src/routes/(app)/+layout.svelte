<script lang="ts">
	import LoadingBlocker from '$lib/components/LoadingBlocker.svelte';
	import DarkModeToggle from '$lib/components/DarkModeToggle.svelte';
	import { Toaster } from '$lib/components/ui/sonner';
	import '../../app.pcss';
	import { ModeWatcher } from 'mode-watcher';

	import { loadingBlocker } from '$lib/stores';
</script>

<svelte:head>
	<title>Diceable</title>
</svelte:head>

<Toaster position="top-right" richColors />
<LoadingBlocker bind:enabled={$loadingBlocker} />
<DarkModeToggle />
<ModeWatcher />
<slot />
