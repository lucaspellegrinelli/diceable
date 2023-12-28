<script lang="ts">
	import { Separator } from '$lib/components/ui/separator';
	import Sidebar from '$lib/components/ui/sidebar/sidebar.svelte';
	import * as Select from '$lib/components/ui/select';
	import type { PageData } from './$types';

	export let data: PageData;
	const diceSides = data.palettes[0].skin.length;

	const createUrl = (path: string) => {
		return `/dashboard/d${diceSides}${path}`;
	};

	const sidebarNavItems = [
		{
			title: 'Home',
			href: createUrl('')
		},
		{
			title: 'Configuration',
			href: createUrl('/configuration')
		},
		{
			title: 'Palettes',
			href: createUrl('/palettes')
		},
		{
			title: 'Player Skins',
			href: createUrl('/playerskins')
		}
	];

	let selectedDiceSides = { value: `d${diceSides}`, label: `Configuring d${diceSides}` };

	const changeDiceSides = (e: any) => {
		selectedDiceSides = { value: e.value, label: e.label };
		window.location.href = `/dashboard/${e.value}`;
	};
</script>

<div class="space-y-6 p-5 md:p-10 pb-16 w-full">
	<div class="flex align-middle gap-2">
		<div class="space-y-0.5">
			<h2 class="text-2xl font-bold tracking-tight">Dashboard</h2>
			<p class="text-muted-foreground">Change the dice settings for your servers here.</p>
		</div>
	</div>
	<Separator class="my-6" />
	<div class="flex flex-col space-y-8 lg:flex-row lg:space-x-12 lg:space-y-0">
		<aside class="-mx-4 lg:w-1/5 space-y-4">
			<Select.Root bind:selected={selectedDiceSides} onSelectedChange={changeDiceSides}>
				<Select.Trigger class="w-full">
					<Select.Value placeholder="Sides" />
				</Select.Trigger>
				<Select.Content>
					<Select.Item value="d10">Configuring d10</Select.Item>
					<Select.Item value="d20">Configuring d20</Select.Item>
				</Select.Content>
			</Select.Root>
			<Sidebar items={sidebarNavItems} />
		</aside>
		<div class="flex-1">
			<slot />
		</div>
	</div>
</div>
