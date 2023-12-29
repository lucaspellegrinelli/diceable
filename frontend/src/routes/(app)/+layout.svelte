<script lang="ts">
	import LoadingBlocker from '$lib/components/LoadingBlocker.svelte';
	import ToastHandler from '$lib/components/ToastHandler.svelte';
	import DarkModeToggle from '$lib/components/DarkModeToggle.svelte';
	import '../../app.pcss';
	import { ModeWatcher } from 'mode-watcher';

	import { loadingBlocker } from '$lib/stores';
</script>

<svelte:head>
	<title>Diceable</title>
</svelte:head>

<ToastHandler />
<LoadingBlocker bind:enabled={$loadingBlocker} />
<DarkModeToggle />
<ModeWatcher />
<slot />
