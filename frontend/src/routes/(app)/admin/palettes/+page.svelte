<script lang="ts">
	import { Separator } from '$lib/components/ui/separator';
    import { Card } from '$lib/components/ui/card';
	import { Plus } from 'lucide-svelte';
	import type { PageData } from './$types';
	import PaletteEditor from './palette-editor.svelte';

	export let data: PageData;

	let palettes = data.palettes;
	const dice = data.dice;
	const diceSides = dice.length;

	const createNewPalette = (name: string) => ({
		name: name,
		skin: Array(diceSides).fill(dice[0]),
		default: palettes.length === 0
	});

	const addNewPalette = () => {
		const id = Math.random().toString(36).substring(7);
		palettes = [...palettes, createNewPalette(id)];
	};

	const removePalette = (paletteIndex: number) => {
		palettes = palettes.filter((_, index) => index !== paletteIndex);
	};

	const setDefaultPalette = (paletteIndex: number) => {
		palettes = palettes.map((palette, index) => {
			palette.default = index === paletteIndex;
			return palette;
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
		{#each palettes as palette, paletteIndex}
			<PaletteEditor
				{palette}
				{dice}
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
