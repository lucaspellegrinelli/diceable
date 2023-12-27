<script lang="ts">
	import { Card } from '$lib/components/ui/card';
	import * as Tooltip from '$lib/components/ui/tooltip';
	import * as Select from '$lib/components/ui/select';
	import { Button } from '$lib/components/ui/button';
	import { Input } from '$lib/components/ui/input';
	import { Trash2 } from 'lucide-svelte';
	import { createEventDispatcher } from 'svelte';

	import type { Palette, PlayerSkin } from '$lib/types';

	export let palettes: Palette[];
	export let playerSkin: PlayerSkin;
	export let effectOptions: string[];

	const selectEffectOptions = ['None', ...effectOptions].map((effect) => ({
		label: effect,
		value: effect
	}));

	const selectPaletteOptions = palettes.map((palette) => ({
		label: palette.name,
		value: palette.name
	}));

	let selectedEffect = selectEffectOptions.find((effect) => effect.value === playerSkin.effect);
	let selectedPalette = selectPaletteOptions.find(
		(palette) => palette.value === playerSkin.palette
	);

	const dispatch = createEventDispatcher();
</script>

<Card class="p-4 space-y-2">
	<div class="flex flex-row gap-2">
		<Tooltip.Root openDelay={0}>
			<Tooltip.Trigger class="w-full">
				<Input type="text" placeholder="Discord ID" bind:value={playerSkin.discordId} />
			</Tooltip.Trigger>
			<Tooltip.Content>
				<p>Discord ID of the player</p>
			</Tooltip.Content>
		</Tooltip.Root>
		<div>
			<Tooltip.Root openDelay={0}>
				<Tooltip.Trigger asChild let:builder>
					<Button
						builders={[builder]}
						variant="destructive"
						class="w-full"
						on:click={() => dispatch('delete')}
					>
						<Trash2 size={16} />
					</Button>
				</Tooltip.Trigger>
				<Tooltip.Content>
					<p>Delete player skin</p>
				</Tooltip.Content>
			</Tooltip.Root>
		</div>
	</div>
	<Tooltip.Root openDelay={0}>
		<Tooltip.Trigger class="w-full">
			<Input type="text" placeholder="Player description" bind:value={playerSkin.description} />
		</Tooltip.Trigger>
		<Tooltip.Content>
			<p>Just a description for you to remember who is who</p>
		</Tooltip.Content>
	</Tooltip.Root>

	<div class="flex flex-row gap-2">
		<Select.Root portal={null} items={selectPaletteOptions} bind:selected={selectedPalette}>
			<Select.Trigger class="w-full">
				<Select.Value />
			</Select.Trigger>
			<Select.Content>
				{#each selectPaletteOptions as paletteOption}
					<Select.Item value={paletteOption.value} label={paletteOption.label}
						>{paletteOption.label}</Select.Item
					>
				{/each}
			</Select.Content>
		</Select.Root>
		<Select.Root portal={null} items={selectEffectOptions} bind:selected={selectedEffect}>
			<Select.Trigger class="w-full">
				<Select.Value />
			</Select.Trigger>
			<Select.Content>
				{#each selectEffectOptions as effectOption}
					<Select.Item value={effectOption.value} label={effectOption.label}
						>{effectOption.label}</Select.Item
					>
				{/each}
			</Select.Content>
		</Select.Root>
	</div>
</Card>
