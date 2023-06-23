<script lang="ts">
	import Icon from '@iconify/svelte';
	import { Input, Dropdown, DropdownItem, Tooltip, Button, Heading, Search } from 'flowbite-svelte';
	import { capitalize } from '$lib/utils';

	export let palettes: Array<{ name: string; skin: string[]; default: boolean }>;
	export let diceSkinOptions: string[];

	let searchTerm = '';

	const createNewPalette = (name: string) => ({
		name: name,
		skin: Array(10).fill(diceSkinOptions[0]),
		default: palettes.length === 0
	});

	const addNewPalette = () => {
		const id = Math.random().toString(36).substring(7);
		palettes = [...palettes, createNewPalette(id)];
	};

	const chooseSkin = (paletteIndex: number, skinIndex: number, skinName: string): any => {
		palettes[paletteIndex].skin[skinIndex] = skinName;
	};

	const setDefaultPalette = (paletteIndex: number) => {
		palettes = palettes.map((palette, index) => {
			palette.default = index === paletteIndex;
			return palette;
		});
	};

	const skinUrl = (skin: string, number: number, type: string = 'd10') => {
		return `https://assets.togarashi.app/dice/${type}/${skin}/${number}.png`;
	};
</script>

<Heading class="mb-4" tag="h2">palettes</Heading>

{#each palettes as palette, paletteIndex}
	<div class="flex items-center my-2">
		<Input
			label="Palette name"
			class="w-72 mr-1 self-stretch"
			placeholder="Palette name"
			bind:value={palette.name}
			color={palette.name ? 'base' : 'red'}
		/>
		<Tooltip>Palette name</Tooltip>

		<div class="grid w-full gap-1 grid-cols-4 md:grid-cols-6 lg:grid-cols-12">
			{#each palette.skin as skinName, skinIndex}
				<Button class="py-1" color="light">
					<img
						src={skinUrl(skinName, (skinIndex + 1) % palette.skin.length)}
						class="w-14"
						alt="{skinName} dice"
					/>
				</Button>
				<Dropdown id="diceDropdown" class="overflow-y-auto max-h-96">
					<div class="p-2">
						<Search bind:value={searchTerm} size="md" />
					</div>
					{#each diceSkinOptions.sort() as diceSkinName}
						{#if diceSkinName.toLowerCase().includes(searchTerm.toLowerCase())}
							<DropdownItem on:click={chooseSkin(paletteIndex, skinIndex, diceSkinName)}>
								<div class="flex items-center">
									<img
										src={skinUrl(diceSkinName, (skinIndex + 1) % palette.skin.length)}
										class="w-24 mr-2"
										alt="{skinName} dice"
									/>
									<span class="flex-1">{capitalize(diceSkinName)}</span>
								</div>
							</DropdownItem>
						{/if}
					{/each}
				</Dropdown>
			{/each}
			<Button
				color={palette.default ? 'green' : 'purple'}
				on:click={() => setDefaultPalette(paletteIndex)}
				disabled={palette.default}
			>
				<Icon icon="fluent:book-default-28-filled" class="text-xl inline-block" />
			</Button>
			<Tooltip>Set as default</Tooltip>

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
