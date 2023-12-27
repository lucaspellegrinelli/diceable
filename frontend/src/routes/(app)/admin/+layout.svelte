<script lang="ts">
	import { Separator } from '$lib/components/ui/separator';
	import Sidebar from '$lib/components/ui/sidebar/sidebar.svelte';
	import * as Select from '$lib/components/ui/select';

	const sidebarNavItems = [
		{
			title: 'Home',
			href: '/admin'
		},
		{
			title: 'Configuration',
			href: '/admin/configuration'
		},
		{
			title: 'Palettes',
			href: '/admin/palettes'
		},
		{
			title: 'Player Skins',
			href: '/admin/playerskins'
		}
	];

	const diceOptions = [
		{ value: 'd10', label: 'Configuring d10' },
		{ value: 'd20', label: 'Configuring d20' }
	];

	let selectedDice = diceOptions[0];
</script>

<div class="space-y-6 p-5 md:p-10 pb-16 w-full">
	<div class="space-y-0.5">
		<h2 class="text-2xl font-bold tracking-tight">Dashboard</h2>
		<p class="text-muted-foreground">Change the dice settings for your servers here.</p>
	</div>
	<Separator class="my-6" />
	<div class="flex flex-col space-y-8 lg:flex-row lg:space-x-12 lg:space-y-0">
		<aside class="-mx-4 lg:w-1/5">
			<Select.Root portal={null} items={diceOptions} bind:selected={selectedDice}>
				<Select.Trigger class="w-full ml-3">
					<Select.Value />
				</Select.Trigger>
				<Select.Content>
					{#each diceOptions as diceOption}
						<Select.Item value={diceOption.value} label={diceOption.label}
							>{diceOption.label}</Select.Item
						>
					{/each}
				</Select.Content>
			</Select.Root>
			<div class="mt-2">
				<Sidebar items={sidebarNavItems} />
			</div>
		</aside>
		<div class="flex-1">
			<slot />
		</div>
	</div>
</div>
