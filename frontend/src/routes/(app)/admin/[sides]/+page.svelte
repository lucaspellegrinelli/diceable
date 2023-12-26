<script lang="ts">
	import { page } from '$app/stores';
	import Configurations from './Configurations.svelte';
	import Palettes from './Palettes.svelte';
	import PlayerSkins from './PlayerSkins.svelte';
	import type { PlayerSkin } from '$lib/types';
	import { addToast } from '$lib/toasts';
	import {
		A,
		Button,
		Card,
		Heading,
		Hr,
		SpeedDial,
		SpeedDialButton,
		Spinner,
		Tooltip
	} from 'flowbite-svelte';
	import Icon from '@iconify/svelte';
	import Links from './Links.svelte';

	const INVALID_PALETTE_NAME = 'Unknown';
	const DEFAULT_EFFECT_NAME = 'None';

	export let data;

	let palettes: Array<{ name: string; skin: string[]; default: boolean }> = [];
	let playerSkins: Array<PlayerSkin> = [];
	let customColors = data.config.custom_colors === 'true';

	let isSubmitting = false;

	for (const [key, value] of Object.entries(data.config.palettes)) {
		const isDefault = key === data.config.default_palette;
		palettes = [...palettes, { name: key, skin: value, default: isDefault }];
	}

	for (const [key, value] of Object.entries(data.config.player_skins)) {
		const playerPalette = value.palette || INVALID_PALETTE_NAME;
		const playerEffect = value.effect || DEFAULT_EFFECT_NAME;
		const playerDescription = value.description || '';
		playerSkins = [
			...playerSkins,
			{
				discordId: key,
				description: playerDescription,
				palette: playerPalette,
				effect: playerEffect
			}
		];
	}

	const getFormProblems = () => {
		const emptyDiscordId = playerSkins.some((playerSkin) => playerSkin.discordId === '');
		if (emptyDiscordId) return 'Discord ID cannot be empty';

		const emptyPaletteName = palettes.some((palette) => palette.name === '');
		if (emptyPaletteName) return 'Palette name cannot be empty';

		const playerWithInvalidPalette = playerSkins.find((playerSkin) =>
			palettes.every((palette) => palette.name !== playerSkin.palette)
		);

		if (playerWithInvalidPalette) {
			const identifier = playerWithInvalidPalette.description || playerWithInvalidPalette.discordId;
			return `Player "${identifier}" has an invalid palette`;
		}

		const isThereDefaultPalette = palettes.some((palette) => palette.default);
		if (!isThereDefaultPalette) return 'There must be a default palette';
	};

	const saveData = () => {
		const formProblems = getFormProblems();
		if (formProblems) {
			addToast(formProblems, 'error');
			return;
		}

		const palettesDict = palettes.reduce((acc: Record<string, string[]>, palette) => {
			acc[palette.name] = palette.skin;
			return acc;
		}, {});

		const playerSkinsDict = playerSkins.reduce((acc: Record<string, PlayerSkin>, playerSkin) => {
			if (playerSkin.palette !== INVALID_PALETTE_NAME) {
				acc[playerSkin.discordId] = {
					discordId: playerSkin.discordId,
					description: playerSkin.description,
					palette: playerSkin.palette,
					effect: playerSkin.effect === DEFAULT_EFFECT_NAME ? undefined : playerSkin.effect
				};
			}
			return acc;
		}, {});

		const defaultPalette = palettes.find((palette) => palette.default)!;

		const formData = new FormData();
		formData.append('user', data.user);
		formData.append('sides', data.sides);
		formData.append('custom_colors', customColors ? 'true' : 'false');
		formData.append('palettes', JSON.stringify(palettesDict));
		formData.append('default_palette', defaultPalette.name);
		formData.append('player_skins', JSON.stringify(playerSkinsDict));

		isSubmitting = true;
		fetch('', {
			method: 'POST',
			body: formData
		})
			.then(() => {
				addToast('Saved successfully', 'success');
			})
			.catch((err) => {
				addToast('Failed to save', 'error');
				console.error(err);
			})
			.finally(() => {
				isSubmitting = false;
			});
	};
</script>

{#if $page.data.session}
	<div class="container mx-auto my-6 px-4">
		<Heading tag="h2" class="mb-4">dashboard</Heading>

		<Links user={data.user} />

		<Configurations bind:customColors />

		<Hr class="my-8" height="h-px" style="z-index: -99" />

		<Palettes bind:palettes diceSkinOptions={data.dice} />

		<Hr class="my-8" height="h-px" style="z-index: -99" />

		<PlayerSkins {palettes} bind:playerSkins effectOptions={data.effects} />

		<SpeedDial defaultClass="fixed end-6 md:end-24 bottom-6" tooltip="none" textOutside>
			<SpeedDialButton name="Save" on:click={saveData}>
				{#if isSubmitting}
					<Spinner class="absolute top-0 left-0 w-full h-full" />
                {:else}
                    <Icon icon="mdi:content-save" class="text-2xl" />
				{/if}
			</SpeedDialButton>
		</SpeedDial>
	</div>
{:else}
	<a href="/auth/signin" class="btn btn-primary" data-sveltekit-preload-data="off">Sign in</a>
{/if}
