<script lang="ts">
	import Icon from '@iconify/svelte';
	import {
		Input,
		Dropdown,
		DropdownItem,
		Tooltip,
		Button,
		Heading,
		Search,
		Card,
		Accordion,
		AccordionItem
	} from 'flowbite-svelte';
	import { capitalize } from '$lib/utils';

	export let palettes: Array<{ name: string; skin: string[]; default: boolean }>;
	export let diceSkinOptions: string[];

	let searchTerm = '';

	const diceSides = palettes[0].skin.length;

	const createNewPalette = (name: string) => ({
		name: name,
		skin: Array(diceSides).fill(diceSkinOptions[0]),
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

	const skinUrl = (skin: string, number: number) => {
		return `https://assets.togarashi.app/dice/d${diceSides}/${skin}/${number}.png`;
	};
</script>

<Heading class="mb-4" tag="h2">palettes</Heading>

<div class="grid w-full grid-cols-1 lg:grid-cols-2 gap-2 mb-6">
	{#each palettes as palette, paletteIndex}
		<div key={paletteIndex}>
			<Card size="xl">
				<div class="flex flex-row">
					<div class="mr-2 w-full">
						<Input
							label="Palette name"
							class="w-full h-full mr-1 self-stretch"
							placeholder="Palette name"
							bind:value={palette.name}
							color={palette.name ? 'base' : 'red'}
						/>
						<Tooltip>Palette name</Tooltip>
					</div>
					<div class="mr-2">
						<Button
							color={palette.default ? 'green' : 'purple'}
							on:click={() => setDefaultPalette(paletteIndex)}
							disabled={palette.default}
						>
							<Icon icon="fluent:book-default-28-filled" class="text-xl inline-block" />
						</Button>
						<Tooltip>Set as default</Tooltip>
					</div>
					<div>
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

				<Accordion flush class="px-2">
					<AccordionItem transitionType="fade" transitionParams={{ duration: 100 }}>
						<span slot="header">See/edit dice</span>
						<div class="grid w-full grid-cols-3 sm:grid-cols-5 gap-2">
							{#each palette.skin as skinName, skinIndex}
								<Button color="light">
									<img
										src={skinUrl(skinName, (skinIndex + 1) % palette.skin.length)}
										class="w-14"
										alt="{skinName} dice"
									/>
								</Button>
								<Dropdown id="diceDropdown" class="overflow-y-auto max-h-96 z-50">
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
						</div>
					</AccordionItem>
				</Accordion>
			</Card>
		</div>
	{/each}
	<Card
		size="xl"
		on:click={addNewPalette}
		class="flex flex-col justify-center items-center cursor-pointer"
	>
		<div class="flex flex-col items-center py-3">
			<Icon icon="material-symbols:add" class="text-5xl text-gray-400" />
			<span class="text-gray-400">Add new palette</span>
		</div>
	</Card>
</div>
