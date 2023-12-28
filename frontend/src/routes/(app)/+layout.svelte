<script lang="ts">
	import LoadingBlocker from '$lib/LoadingBlocker.svelte';
	import DarkModeToggle from '$lib/components/DarkModeToggle.svelte';
	import '../../app.pcss';
	import { ModeWatcher } from 'mode-watcher';

	import { loadingBlocker } from '$lib/stores';
	import ToastHandler from '$lib/ToastHandler.svelte';
</script>

<svelte:head>
	<title>Diceable</title>
</svelte:head>

<ToastHandler />
<LoadingBlocker bind:enabled={$loadingBlocker} />
<DarkModeToggle />
<ModeWatcher />
<slot />
