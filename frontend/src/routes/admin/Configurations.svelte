<script lang="ts">
	import { Heading, Toggle } from 'flowbite-svelte';

	export let customColors: boolean;
</script>

<Heading class="mb-6" tag="h2">configurations</Heading>

<Toggle bind:checked={customColors}>Custom Colors</Toggle>
