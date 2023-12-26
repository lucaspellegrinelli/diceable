<script lang="ts">
	import type { PlayerSkin } from '$lib/types';
	import Icon from '@iconify/svelte';
	import { Button, Card, Dropdown, DropdownItem, Heading, Input, Tooltip } from 'flowbite-svelte';
	import { capitalize } from '$lib/utils';

	export let palettes: Array<{ name: string; skin: string[] }>;
	export let playerSkins: Array<PlayerSkin>;
	export let effectOptions: string[];

	const addNewPlayerSkin = () => {
		const newPlayerSkin = {
			discordId: '',
			description: '',
			palette: palettes[0].name,
			effect: 'None'
		};
		playerSkins = [...playerSkins, newPlayerSkin];
	};

	const choosePalette = (playerIndex: number, paletteName: string): any => {
		playerSkins[playerIndex].palette = paletteName;
	};

	const chooseEffect = (playerIndex: number, effectName: string): any => {
		playerSkins[playerIndex].effect = effectName;
	};
</script>

<Heading class="mb-4" tag="h2">player skins</Heading>

<div class="grid w-full grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-2 mb-6">
	{#each playerSkins as playerSkin, playerIndex}
		<Card size="xl">
			<div class="flex flex-row gap-2 mb-2">
				<div class="w-full">
					<Input
						label="Discord ID"
						class="mr-1"
						placeholder="Discord ID"
						bind:value={playerSkin.discordId}
						color={playerSkin.discordId ? 'base' : 'red'}
					/>
					<Tooltip>Discord ID of the player</Tooltip>
				</div>
				<div>
					<Button
						on:click={() => {
							playerSkins = playerSkins.filter((_, i) => i !== playerIndex);
						}}
						color="red"
					>
						<Icon icon="typcn:delete" class="text-xl inline-block" />
					</Button>
					<Tooltip>Delete player skin</Tooltip>
				</div>
			</div>
			<div class="mb-2">
				<Input
					label="Description"
					class="mr-1"
					placeholder="Description"
					bind:value={playerSkin.description}
				/>
				<Tooltip>Just a description for you to remember who is who</Tooltip>
			</div>
			<div class="flex flex-row gap-2">
				<div class="w-full">
					<Button
						outline={!palettes.find((p) => p.name === playerSkin.palette)}
						color={palettes.find((p) => p.name === playerSkin.palette) ? 'light' : 'red'}
						class="w-full"
					>
						{playerSkin.palette}
					</Button>
					<Dropdown>
						{#each palettes as palette}
							<DropdownItem on:click={choosePalette(playerIndex, palette.name)} class="w-48">
								{palette.name}
							</DropdownItem>
						{/each}
					</Dropdown>
				</div>

				<div class="w-full">
					<Button color="light" class="w-full">{capitalize(playerSkin.effect)}</Button>
					<Dropdown>
						{#each ['None', ...effectOptions] as effectName}
							<DropdownItem on:click={chooseEffect(playerIndex, effectName)} class="w-48">
								{capitalize(effectName)}
							</DropdownItem>
						{/each}
					</Dropdown>
				</div>
			</div>
		</Card>
	{/each}
	<Card
		size="xl"
		on:click={addNewPlayerSkin}
		class="flex flex-col justify-center items-center cursor-pointer"
	>
		<div class="flex flex-col items-center py-7">
			<Icon icon="material-symbols:add" class="text-5xl text-gray-400" />
			<span class="text-gray-400">Add new player skin</span>
		</div>
	</Card>
</div>
