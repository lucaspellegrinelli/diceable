<script lang="ts">
	import { Heading, Helper, Toggle } from 'flowbite-svelte';

	export let customColors: boolean;
</script>

<Heading class="mb-6" tag="h2">configurations</Heading>

<Toggle bind:checked={customColors}>Custom Colors</Toggle>
<Helper class="mt-1">
	With this disabled, the default color palette is selected with no effect for all players. If you
	want to choose the palettes for your players, enable this
</Helper>
