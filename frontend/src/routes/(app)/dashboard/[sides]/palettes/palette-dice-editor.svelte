<script lang="ts">
	import { Button } from '$lib/components/ui/button';
	import * as DropdownMenu from '$lib/components/ui/dropdown-menu';
	import type { Palette } from '$lib/types';

	export let dice: string[];
	export let palette: Palette;
	const diceSides = palette.skin.length;

	const chooseSkin = (skinIndex: number, skinName: string): any => {
		palette.skin[skinIndex] = skinName;
	};

	const skinUrl = (skin: string, number: number) => {
		return `https://assets.togarashi.app/dice/d${diceSides}/${skin}/${number}.png`;
	};

	const capitalize = (str: string | undefined) => {
		return str?.replace(/^\w/, (c) => c.toUpperCase());
	};
</script>

<div class="grid w-full grid-cols-3 sm:grid-cols-5 gap-1">
	{#each palette.skin as skinName, skinIndex}
		<DropdownMenu.Root>
			<DropdownMenu.Trigger asChild let:builder>
				<Button variant="ghost" builders={[builder]} class="h-20 w-20 p-0">
					<img
						src={skinUrl(skinName, (skinIndex + 1) % palette.skin.length)}
						class="h-full w-full object-cover p-1"
						alt="{skinName} dice"
					/>
				</Button>
			</DropdownMenu.Trigger>
			<DropdownMenu.Content class="w-56">
				<div class="overflow-y-auto max-h-64">
					{#each dice.sort() as diceSkinName}
						<DropdownMenu.Item
							class="cursor-pointer"
							on:click={() => chooseSkin(skinIndex, diceSkinName)}
						>
							<img
								src={skinUrl(diceSkinName, (skinIndex + 1) % palette.skin.length)}
								class="w-24 mr-2"
								alt="{skinName} dice"
								loading="lazy"
							/>
							<span class="flex-1">{capitalize(diceSkinName)}</span>
						</DropdownMenu.Item>
					{/each}
				</div>
			</DropdownMenu.Content>
		</DropdownMenu.Root>
	{/each}
</div>
