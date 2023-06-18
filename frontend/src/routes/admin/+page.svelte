<script lang="ts">
	import { page } from '$app/stores';
	import Configurations from './Configurations.svelte';
	import Palettes from './Palettes.svelte';
	import PlayerSkins from './PlayerSkins.svelte';
	import type { PlayerSkin } from '$lib/types';

	const INVALID_PALETTE_NAME = 'Unknown';
	const DEFAULT_EFFECT_NAME = 'None';

	export let data;

	let palettes: Array<{ name: string; skin: string[] }> = [];
	let playerSkins: Array<{ discordId: string; palette: string; effect: string }> = [];
	let customColors = data.config.custom_colors === 'true';

	for (const [key, value] of Object.entries(data.config.palettes)) {
		palettes = [...palettes, { name: key, skin: value }];
	}

	for (const [key, value] of Object.entries(data.config.player_skins)) {
		const playerPalette = value.palette || INVALID_PALETTE_NAME;
		const playerEffect = value.effect || DEFAULT_EFFECT_NAME;
		playerSkins = [
			...playerSkins,
			{ discordId: key, palette: playerPalette, effect: playerEffect }
		];
	}

	const canSaveData = () => {
		const existsEmptyDiscordId = playerSkins.some((playerSkin) => playerSkin.discordId === '');
		const existsEmptyPaletteName = palettes.some((palette) => palette.name === '');

		return !existsEmptyDiscordId && !existsEmptyPaletteName;
	};

	const saveData = () => {
		if (!canSaveData()) {
			return;
		}

		const palettesDict = palettes.reduce((acc: Record<string, string[]>, palette) => {
			acc[palette.name] = palette.skin;
			return acc;
		}, {});

		const playerSkinsDict = playerSkins.reduce((acc: Record<string, PlayerSkin>, playerSkin) => {
			if (playerSkin.palette !== INVALID_PALETTE_NAME) {
				acc[playerSkin.discordId] = {
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

		fetch(`/admin`, {
			method: 'POST',
			body: formData
		})
			.then(() => {
				console.log('saved');
			})
			.catch((err) => {
				console.error(err);
			});
	};
</script>

{#if $page.data.session}
	<div
		class="hidden bg-red-400 hover:bg-red-500 bg-blue-400 hover:bg-blue-500 bg-green-400 hover:bg-green-500 bg-yellow-400 hover:bg-yellow-500 bg-orange-400 hover:bg-orange-500 bg-purple-400 hover:bg-purple-500 bg-gray-400 hover:bg-gray-500"
	/>

	<div class="container mx-auto mt-6">
		<Configurations bind:customColors />

		<div class="divider" />

		<Palettes bind:palettes diceSkinOptions={data.dice} />

		<div class="divider" />

		<PlayerSkins {palettes} bind:playerSkins effectOptions={data.effects} />

		<button class="btn btn-primary mt-1 text-white" on:click={saveData}>Save</button>
	</div>
{:else}
	<a href="/auth/signin" class="btn btn-primary" data-sveltekit-preload-data="off">Sign in</a>
{/if}
