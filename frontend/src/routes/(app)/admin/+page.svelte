<script lang="ts">
	import { Card, Heading } from 'flowbite-svelte';
</script>

<div class="p-8">
	<Heading class="mb-6" tag="h2">which dice to configure</Heading>

	<div class="grid w-full grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
		<Card img="https://assets.togarashi.app/dice/d10/indigo/0.png" href="/admin/d10" horizontal>
			<h5 class="mb-2 text-2xl font-bold tracking-tight text-gray-900 dark:text-white">D10</h5>
			<p class="font-normal text-gray-700 dark:text-gray-400 leading-tight">Ten-sided dice</p>
		</Card>

		<Card img="https://assets.togarashi.app/dice/d20/indigo/0.png" href="/admin/d20" horizontal>
			<h5 class="mb-2 text-2xl font-bold tracking-tight text-gray-900 dark:text-white">D20</h5>
			<p class="font-normal text-gray-700 dark:text-gray-400 leading-tight">Twenty-sided dice</p>
		</Card>
	</div>
</div>

