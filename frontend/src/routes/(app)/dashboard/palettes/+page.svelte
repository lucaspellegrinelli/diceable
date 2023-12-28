<script lang="ts">
	import { Separator } from '$lib/components/ui/separator';
	import { Card } from '$lib/components/ui/card';
	import { Plus } from 'lucide-svelte';
	import PaletteEditor from './palette-editor.svelte';
	import { get } from 'svelte/store';
	import { availableDiceSkins, currentSides, diceConfig } from '$lib/stores';

	let diceSideCount = parseInt(get(currentSides).slice(1));
	currentSides.subscribe((value) => {
		diceSideCount = parseInt(value.slice(1));
	});

    $: {
        console.log(diceSideCount);
        console.log(get(diceConfig));
    }

	const createNewPalette = (name: string) => ({
		name: name,
		skin: Array(diceSideCount).fill(get(availableDiceSkins)[0]),
		default: get(diceConfig).palettes.length === 0
	});

	const addNewPalette = () => {
		const id = Math.random().toString(36).substring(7);
		diceConfig.update((value) => {
			value.palettes = [...value.palettes, createNewPalette(id)];
			return value;
		});
	};

	const removePalette = (paletteIndex: number) => {
		diceConfig.update((value) => {
			value.palettes = value.palettes.filter((_, index) => index !== paletteIndex);
			return value;
		});
	};

	const setDefaultPalette = (paletteIndex: number) => {
		diceConfig.update((value) => {
			value.palettes = value.palettes.map((palette, index) => {
				palette.default = index === paletteIndex;
				return palette;
			});
			return value;
		});
	};
</script>

<div class="space-y-6">
	<div>
		<h3 class="text-lg font-medium">Palettes</h3>
		<p class="text-sm text-muted-foreground">Define the custom dice skins for your server.</p>
	</div>
	<Separator />

	<div class="grid w-full grid-cols-1 lg:grid-cols-2 gap-2 mb-6">
		{#each $diceConfig.palettes as palette, paletteIndex}
			<PaletteEditor
				{palette}
				dice={$availableDiceSkins}
				on:delete={() => removePalette(paletteIndex)}
				on:setdefault={() => setDefaultPalette(paletteIndex)}
			/>
		{/each}

		<Card>
			<button
				class="flex w-full h-full cursor-pointer items-center justify-center min-h-32"
				on:click={addNewPalette}
			>
				<Plus size={28} />
			</button>
		</Card>
	</div>
</div>
