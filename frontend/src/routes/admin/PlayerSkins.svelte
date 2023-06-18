<script lang="ts">
	export let palettes: Array<{ name: string; skin: string[] }>;
	export let playerSkins: Array<{ discordId: string; palette: string; effect: string }>;
	export let effectOptions: string[];

	const addNewPlayerSkin = () => {
		const newPlayerSkin = { discordId: '', palette: palettes[0].name, effect: 'None' };
		playerSkins = [...playerSkins, newPlayerSkin];
	};

	const choosePalette = (playerIndex: number, paletteName: string): any => {
		playerSkins[playerIndex].palette = paletteName;
	};

	const chooseEffect = (playerIndex: number, effectName: string): any => {
		playerSkins[playerIndex].effect = effectName;
	};
</script>

<h1 class="text-4xl font-bold my-4">Player Skins</h1>

{#each playerSkins as playerSkin, playerIndex}
	<div class="flex items-center my-2">
		<input
			type="text"
			class="input input-bordered w-72"
			placeholder="Discord ID"
			bind:value={playerSkin.discordId}
		/>

		<div class="dropdown flex-1 mx-1">
			<!-- svelte-ignore a11y-no-noninteractive-tabindex -->
			<!-- svelte-ignore a11y-label-has-associated-control -->
			<label tabindex="0" class="m-1 btn btn-block">{playerSkin.palette}</label>
			<!-- svelte-ignore a11y-no-noninteractive-tabindex -->
			<ul tabindex="0" class="z-50 p-2 shadow menu dropdown-content bg-base-100 rounded-box w-52">
				{#each palettes as palette}
					<li>
						<!-- svelte-ignore a11y-click-events-have-key-events -->
						<!-- svelte-ignore a11y-missing-attribute -->
						<a on:click={choosePalette(playerIndex, palette.name)}>{palette.name}</a>
					</li>
				{/each}
			</ul>
		</div>

		<div class="dropdown flex-1 mx-1">
			<!-- svelte-ignore a11y-no-noninteractive-tabindex -->
			<!-- svelte-ignore a11y-label-has-associated-control -->
			<label tabindex="0" class="m-1 btn btn-block">{playerSkin.effect}</label>
			<!-- svelte-ignore a11y-no-noninteractive-tabindex -->
			<ul tabindex="0" class="z-50 p-2 shadow menu dropdown-content bg-base-100 rounded-box w-52">
				{#each ['None', ...effectOptions] as effectName}
					<!-- svelte-ignore a11y-click-events-have-key-events -->
					<!-- svelte-ignore a11y-missing-attribute -->
					<li>
						<!-- svelte-ignore a11y-click-events-have-key-events -->
						<!-- svelte-ignore a11y-missing-attribute -->
						<a on:click={chooseEffect(playerIndex, effectName)}>{effectName}</a>
					</li>
				{/each}
			</ul>
		</div>

		<button
			on:click={() => {
				playerSkins = playerSkins.filter((_, i) => i !== playerIndex);
			}}
			class="btn btn-error ml-2"
		>
			<svg
				xmlns="http://www.w3.org/2000/svg"
				class="h-6 w-6"
				fill="none"
				viewBox="0 0 24 24"
				stroke="currentColor"
			>
				<path
					stroke-linecap="round"
					stroke-linejoin="round"
					stroke-width="2"
					d="M6 18L18 6M6 6l12 12"
				/>
			</svg>
		</button>
	</div>
{/each}

<button class="btn btn-success mt-1 text-white" on:click={addNewPlayerSkin}
	>Add new player skin</button
>
