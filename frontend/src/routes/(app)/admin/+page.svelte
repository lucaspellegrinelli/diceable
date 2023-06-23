<script lang="ts">
	import { page } from '$app/stores';
	import Configurations from './Configurations.svelte';
	import Palettes from './Palettes.svelte';
	import PlayerSkins from './PlayerSkins.svelte';
	import type { PlayerSkin } from '$lib/types';
	import { addToast } from '$lib/toasts';
	import { A, Button, Heading, Hr, Spinner, Tooltip } from 'flowbite-svelte';
	import Icon from '@iconify/svelte';

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
		formData.append('custom_colors', customColors ? 'true' : 'false');
		formData.append('palettes', JSON.stringify(palettesDict));
		formData.append('default_palette', defaultPalette.name);
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
		<Heading class="inline-flex" tag="h2">
			discord invite link
			<A
				href="https://discord.com/api/oauth2/authorize?client_id=1116110919953563729&permissions=1024&scope=bot"
				target="_blank"
			>
				<Icon icon="mdi:discord" class="ml-3 mt-1" />
			</A>
			<Tooltip placement="right">click here to invite the bot to your server</Tooltip>
		</Heading>

		<Hr class="mb-4 mt-6" height="h-px" style="z-index: -99" />

		<Configurations bind:customColors />

		<Hr class="my-8" height="h-px" style="z-index: -99" />

		<Palettes bind:palettes diceSkinOptions={data.dice} />

		<Hr class="my-8" height="h-px" style="z-index: -99" />

		<PlayerSkins {palettes} bind:playerSkins effectOptions={data.effects} />

		<Hr class="my-8" height="h-px" style="z-index: -99" />

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
