<script lang="ts">
	import { Separator } from '$lib/components/ui/separator';
	import { Card } from '$lib/components/ui/card';
	import { Plus } from 'lucide-svelte';
	import PlayerSkinEditor from './player-skin-editor.svelte';
	import { availableEffects, diceConfig } from '$lib/stores';
	import { get } from 'svelte/store';

	const addNewPlayerSkin = () => {
		const newPlayerSkin = {
			discordId: '',
			description: '',
			palette: get(diceConfig).palettes[0].name,
			effect: 'None'
		};

        diceConfig.update((value) => {
            value.playerSkins = [...value.playerSkins, newPlayerSkin];
            return value;
        });
	};

	const deletePlayerSkin = (index: number) => {
        diceConfig.update((value) => {
            value.playerSkins = value.playerSkins.filter((_, i) => i !== index);
            return value;
        });
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
		{#each $diceConfig.playerSkins as playerSkin, playerSkinIndex}
			<PlayerSkinEditor
				{playerSkin}
				palettes={$diceConfig.palettes}
				effectOptions={$availableEffects}
				on:delete={() => deletePlayerSkin(playerSkinIndex)}
			/>
		{/each}

		<Card>
			<button
				class="flex w-full h-full cursor-pointer items-center justify-center min-h-56"
				on:click={addNewPlayerSkin}
			>
				<div class="flex flex-col items-center justify-center">
					<Plus size={28} />
					<p>Add new player skin</p>
				</div>
			</button>
		</Card>
	</div>
</div>
