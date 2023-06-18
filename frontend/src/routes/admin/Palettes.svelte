<script lang="ts">
	export let palettes: Array<{ name: string; skin: string[] }>;
	export let diceSkinOptions: string[];

	const createNewPalette = (name: string) => ({
		name: name,
		skin: ['red', 'blue', 'blue', 'blue', 'blue', 'blue', 'blue', 'blue', 'blue', 'green']
	});

	const addNewPalette = () => {
		const id = Math.random().toString(36).substring(7);
		palettes = [...palettes, createNewPalette(id)];
	};

	const chooseSkin = (paletteIndex: number, skinIndex: number, skinName: string): any => {
		palettes[paletteIndex].skin[skinIndex] = skinName;
	};

	const backgroundFromSkin = (skin: string) => {
		const tailwindColor: Record<string, string> = {
			red: 'red',
			blue: 'blue',
			green: 'green',
			yellow: 'yellow',
			orange: 'orange',
			purple: 'purple',
			gray: 'gray'
		};

		const color = tailwindColor[skin] || 'gray';
		return `bg-${color}-400 hover:bg-${color}-500`;
	};
</script>

<h1 class="text-4xl font-bold my-4">Palettes</h1>

{#each palettes as palette, paletteIndex}
	<div class="flex items-center">
		<input
			type="text"
			class="input input-bordered w-52"
			placeholder="Palette name"
			bind:value={palette.name}
			disabled={paletteIndex === 0}
		/>
		<div class="flex-grow">
			<div class="flex">
				{#each palette.skin as skinName, skinIndex}
					<div class="dropdown flex-1 mx-1">
						<!-- svelte-ignore a11y-no-noninteractive-tabindex -->
						<!-- svelte-ignore a11y-label-has-associated-control -->
						<label tabindex="0" class="m-1 btn btn-block {backgroundFromSkin(skinName)} text-white"
							>{skinName}</label
						>
						<!-- svelte-ignore a11y-no-noninteractive-tabindex -->
						<ul
							tabindex="0"
							class="z-50 p-2 shadow menu dropdown-content bg-base-100 rounded-box w-52"
						>
							{#each diceSkinOptions as diceSkinName}
								<li>
									<!-- svelte-ignore a11y-click-events-have-key-events -->
									<!-- svelte-ignore a11y-missing-attribute -->
									<a on:click={chooseSkin(paletteIndex, skinIndex, diceSkinName)}>{diceSkinName}</a>
								</li>
							{/each}
						</ul>
					</div>
				{/each}
			</div>
		</div>
		<button
			on:click={() => {
				palettes = palettes.filter((_, i) => i !== paletteIndex);
			}}
			disabled={paletteIndex === 0}
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

<button class="btn btn-success mt-1 text-white" on:click={addNewPalette}>Add new palette</button>
