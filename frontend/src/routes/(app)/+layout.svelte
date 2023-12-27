<script>
	import DarkModeToggle from '$lib/components/DarkModeToggle.svelte';
	import '../../app.pcss';
	import { ModeWatcher } from 'mode-watcher';
</script>

<svelte:head>
	<title>Diceable</title>
</svelte:head>

<DarkModeToggle />
<ModeWatcher />
<slot />
