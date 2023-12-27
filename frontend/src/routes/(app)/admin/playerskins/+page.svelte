<script lang="ts">
	import { Separator } from '$lib/components/ui/separator';
	import { Card } from '$lib/components/ui/card';
	import { Plus } from 'lucide-svelte';
	import type { PageData } from './$types';
	import PlayerSkinEditor from './player-skin-editor.svelte';

	export let data: PageData;

	let playerSkins = data.playerSkins;
	const effectOptions = data.effects;
	const palettes = data.palettes;

	const addNewPlayerSkin = () => {
		const newPlayerSkin = {
			discordId: '',
			description: '',
			palette: palettes[0].name,
			effect: 'None'
		};
		playerSkins = [...playerSkins, newPlayerSkin];
	};

	const deletePlayerSkin = (index: number) => {
		playerSkins = playerSkins.filter((_, i) => i !== index);
	};
</script>

<div class="space-y-6">
	<div>
		<h3 class="text-lg font-medium">Player Skins</h3>
		<p class="text-sm text-muted-foreground">
			Customize the skins and effects for each player in your discord
		</p>
	</div>
	<Separator />

	<div class="grid w-full grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-2 mb-6">
		{#each playerSkins as playerSkin, playerSkinIndex}
			<PlayerSkinEditor
				{playerSkin}
				{palettes}
				{effectOptions}
				on:delete={() => deletePlayerSkin(playerSkinIndex)}
			/>
		{/each}

		<Card>
			<button
				class="flex w-full h-full cursor-pointer items-center justify-center min-h-32"
				on:click={addNewPlayerSkin}
			>
				<Plus size={28} />
			</button>
		</Card>
	</div>
</div>
