<script lang="ts">
	import type { PlayerSkin } from '$lib/types';
	import Icon from '@iconify/svelte';
	import { Button, Dropdown, DropdownItem, Heading, Input, Tooltip } from 'flowbite-svelte';

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

{#each playerSkins as playerSkin, playerIndex}
	<div class="grid w-full gap-2 grid-cols-5 my-2">
		<Input
			label="Discord ID"
			class="mr-1"
			placeholder="Discord ID"
			bind:value={playerSkin.discordId}
			color={playerSkin.discordId ? 'base' : 'red'}
		/>
		<Tooltip>Discord ID of the player</Tooltip>

		<Input
			label="Description"
			class="mr-1"
			placeholder="Description"
			bind:value={playerSkin.description}
		/>
		<Tooltip>Just a description for you to remember who is who</Tooltip>

		<Button
			outline={!palettes.find((p) => p.name === playerSkin.palette)}
			color={palettes.find((p) => p.name === playerSkin.palette) ? 'light' : 'red'}
		>
			{playerSkin.palette}
		</Button>
		<Dropdown>
			{#each palettes as palette}
				<DropdownItem on:click={choosePalette(playerIndex, palette.name)}>
					{palette.name}
				</DropdownItem>
			{/each}
		</Dropdown>

		<Button color="light">{playerSkin.effect}</Button>
		<Dropdown>
			{#each ['None', ...effectOptions] as effectName}
				<DropdownItem on:click={chooseEffect(playerIndex, effectName)}>
					{effectName}
				</DropdownItem>
			{/each}
		</Dropdown>

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
{/each}

<Button color="blue" on:click={addNewPlayerSkin}>add new player skin</Button>
