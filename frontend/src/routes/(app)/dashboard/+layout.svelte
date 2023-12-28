<script lang="ts">
	import type { PageData } from './$types';
	import { Separator } from '$lib/components/ui/separator';
	import Sidebar from '$lib/components/ui/sidebar/sidebar.svelte';
	import * as Select from '$lib/components/ui/select';
	import { Loader, Save } from 'lucide-svelte';
	import {
		availableDiceSkins,
		availableEffects,
		currentSides,
		diceConfig,
		loadingBlocker
	} from '$lib/stores';
	import { get } from 'svelte/store';
	import { saveConfig, updateCurrentConfig } from '$lib/config';
	import { goto } from '$app/navigation';
	import { addToast } from '$lib/toasts';
	import type { LocalDiceConfig } from '$lib/types';

	export let data: PageData;

	diceConfig.set(data.config);
	availableEffects.set(data.effects);
	availableDiceSkins.set(data.diceSkins);
    currentSides.set(data.dice);

	let isSubmitting = false;

	let diceSides = get(currentSides);
	currentSides.subscribe((value) => {
		diceSides = value;
	});

	const sidebarNavItems = [
		{
			title: 'Home',
			href: '/dashboard'
		},
		{
			title: 'Configuration',
			href: '/dashboard/configuration'
		},
		{
			title: 'Palettes',
			href: '/dashboard/palettes'
		},
		{
			title: 'Player Skins',
			href: '/dashboard/playerskins'
		}
	];

	let selectedDiceSides = { value: `${diceSides}`, label: `Configuring ${diceSides}` };

	const changeDiceSides = async (e: any) => {
		selectedDiceSides = { value: e.value, label: e.label };
		currentSides.set(e.value);

		loadingBlocker.set(true);

		try {
			const newData = await updateCurrentConfig(data.user, e.value);
			diceConfig.set(newData.config);
			availableEffects.set(newData.effects);
			availableDiceSkins.set(newData.diceSkins);

            document.cookie = `defaultdice=${e.value}; path=/`;
			await goto('/dashboard');
		} catch (e) {
			console.error(e);
			addToast('An error occurred while changing the dice sides.', 'error');
		} finally {
			loadingBlocker.set(false);
		}
	};

	const getFormProblems = (config: LocalDiceConfig) => {
		const emptyDiscordId = config.playerSkins.some((playerSkin) => playerSkin.discordId === '');
		if (emptyDiscordId) return 'Discord ID of player skin cannot be empty';

		const emptyPaletteName = config.palettes.some((palette) => palette.name === '');
		if (emptyPaletteName) return 'Palette name cannot be empty';

		const playerWithInvalidPalette = config.playerSkins.find((playerSkin) =>
			config.palettes.every((palette) => palette.name !== playerSkin.palette)
		);

		if (playerWithInvalidPalette) {
			const identifier = playerWithInvalidPalette.description || playerWithInvalidPalette.discordId;
			return `Player "${identifier}" has an invalid palette ("${playerWithInvalidPalette.palette}")`;
		}

		const isThereDefaultPalette = config.palettes.some((palette) => palette.default);
		if (!isThereDefaultPalette) return 'There must be a default palette';
	};

	const saveChanges = async () => {
		const userDiceConfig = get(diceConfig);
		const diceSides = get(currentSides);

		const formProblem = getFormProblems(userDiceConfig);
		if (formProblem) {
			addToast(formProblem, 'error');
			return;
		}

		isSubmitting = true;

		try {
			await saveConfig(data.user, diceSides, userDiceConfig);
			addToast('Configuration saved successfully.', 'success');
		} catch (e) {
			console.error(e);
			addToast('An error occurred while saving the configuration.', 'error');
		} finally {
			isSubmitting = false;
		}
	};
</script>

<button
	class="fixed bottom-0 right-0 mb-5 mr-5 rounded-full bg-slate-900 text-white dark:bg-slate-100 dark:text-black cursor-pointer p-5"
	on:click={saveChanges}
>
	{#if isSubmitting}
		<Loader size={36} />
	{:else}
		<Save size={36} />
	{/if}
</button>

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
