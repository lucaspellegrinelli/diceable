<script lang="ts">
	import { page } from '$app/stores';
	import Configurations from './Configurations.svelte';
	import Palettes from './Palettes.svelte';
	import PlayerSkins from './PlayerSkins.svelte';
	import type { PlayerSkin } from '$lib/types';
	import { addToast } from '$lib/toasts';
	import { Button, Hr, Spinner } from 'flowbite-svelte';

	const INVALID_PALETTE_NAME = 'Unknown';
	const DEFAULT_EFFECT_NAME = 'None';

	export let data;

	let palettes: Array<{ name: string; skin: string[] }> = [];
	let playerSkins: Array<PlayerSkin> = [];
	let customColors = data.config.custom_colors === 'true';

	let isSubmitting = false;

	for (const [key, value] of Object.entries(data.config.palettes)) {
		palettes = [...palettes, { name: key, skin: value }];
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

		const formData = new FormData();
		formData.append('user', data.user);
		formData.append('custom_colors', customColors ? 'true' : 'false');
		formData.append('palettes', JSON.stringify(palettesDict));
		formData.append('player_skins', JSON.stringify(playerSkinsDict));

		isSubmitting = true;
		fetch(`/admin`, {
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
	<div class="container mx-auto mt-6">
		<Configurations bind:customColors />

		<Hr class="my-8" height="h-px" />

		<Palettes bind:palettes diceSkinOptions={data.dice} />

		<Hr class="my-8" height="h-px" />

		<PlayerSkins {palettes} bind:playerSkins effectOptions={data.effects} />

		<Hr class="my-8" height="h-px" />

		<Button class="w-48" on:click={saveData}>
			{#if isSubmitting}
				<Spinner class="mr-4" size="4" color="white" />
				Saving...
			{:else}
				Save
			{/if}
		</Button>
	</div>
{:else}
	<a href="/auth/signin" class="btn btn-primary" data-sveltekit-preload-data="off">Sign in</a>
{/if}
