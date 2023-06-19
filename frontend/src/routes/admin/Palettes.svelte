<script lang="ts">
	import Icon from '@iconify/svelte';
	import { Input, Dropdown, DropdownItem, Tooltip, Button, Heading } from 'flowbite-svelte';

	export let palettes: Array<{ name: string; skin: string[] }>;
	export let formErrors: { [key: string]: boolean };
	export let diceSkinOptions: string[];

	const createNewPalette = (name: string) => ({
		name: name,
		skin: Array(10).fill(diceSkinOptions[0])
	});

	const addNewPalette = () => {
		const id = Math.random().toString(36).substring(7);
		palettes = [...palettes, createNewPalette(id)];
	};

	const chooseSkin = (paletteIndex: number, skinIndex: number, skinName: string): any => {
		palettes[paletteIndex].skin[skinIndex] = skinName;
	};
</script>

<Heading class="mb-4" tag="h2">palettes</Heading>

{#each palettes as palette, paletteIndex}
	<div class="flex items-center my-2">
		<Input
			label="Palette name"
			class="w-72 mr-1"
			placeholder="Palette name"
			bind:value={palette.name}
		/>
		<Tooltip>Palette name</Tooltip>

		<div class="grid w-full gap-1 grid-cols-4 md:grid-cols-6 lg:grid-cols-11">
			{#each palette.skin as skinName, skinIndex}
				<Button color="light">{skinName}</Button>
				<Dropdown>
					{#each diceSkinOptions as diceSkinName}
						<DropdownItem on:click={chooseSkin(paletteIndex, skinIndex, diceSkinName)}>
							{diceSkinName}
						</DropdownItem>
					{/each}
				</Dropdown>
			{/each}
			<Button
				color="red"
				on:click={() => {
					palettes = palettes.filter((_, index) => index !== paletteIndex);
				}}
			>
				<Icon icon="typcn:delete" class="text-xl inline-block" />
			</Button>
			<Tooltip>Delete palette</Tooltip>
		</div>
	</div>
{/each}

<Button color="blue" on:click={addNewPalette}>add new palette</Button>
