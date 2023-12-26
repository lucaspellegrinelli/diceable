<script lang="ts">
	import { Card, Heading, Toggle } from 'flowbite-svelte';

	export let customColors: boolean;
</script>

<Heading class="mb-6" tag="h2">configurations</Heading>

<div class="grid w-full grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-2 mb-6">
	<Card size="xl" class="flex flex-col">
		<div class="flex flex-row items-center justify-start mb-2">
			<h5 class="mr-3 text-2xl font-bold tracking-tight text-gray-900 dark:text-white">
				Custom colors
			</h5>
			<Toggle bind:checked={customColors}></Toggle>
		</div>
		<p class="font-normal text-gray-700 dark:text-gray-400 leading-tight">
			Enable this to use the custom color palettes chosen below for the players.
		</p>
	</Card>
	<Card size="xl" class="flex flex-col">
		<div class="flex flex-row items-center justify-start mb-2">
			<h5 class="mr-3 text-2xl font-bold tracking-tight text-gray-900 dark:text-white">
				Custom colors
			</h5>
			<Toggle bind:checked={customColors}></Toggle>
		</div>
		<p class="font-normal text-gray-700 dark:text-gray-400 leading-tight">
			Enable this to use the custom color palettes chosen below for the players.
		</p>
	</Card>
	<Card size="xl" class="flex flex-col">
		<div class="flex flex-row items-center justify-start mb-2">
			<h5 class="mr-3 text-2xl font-bold tracking-tight text-gray-900 dark:text-white">
				Custom colors
			</h5>
			<Toggle bind:checked={customColors}></Toggle>
		</div>
		<p class="font-normal text-gray-700 dark:text-gray-400 leading-tight">
			Enable this to use the custom color palettes chosen below for the players.
		</p>
	</Card>
</div>
