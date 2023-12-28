<script lang="ts">
	import { Card } from '$lib/components/ui/card';
	import * as Tooltip from '$lib/components/ui/tooltip';
	import * as Accordion from '$lib/components/ui/accordion';
	import type { LocalPalette } from '$lib/types';
	import { Button } from '$lib/components/ui/button';
	import { Input } from '$lib/components/ui/input';
	import { Flame, Trash2 } from 'lucide-svelte';
	import PaletteDiceEditor from './palette-dice-editor.svelte';
	import { createEventDispatcher } from 'svelte';

	export let palette: LocalPalette;
	export let dice: string[];

	const dispatch = createEventDispatcher();
</script>

<Card class="p-4">
	<div class="flex flex-row gap-2">
		<Tooltip.Root openDelay={0}>
			<Tooltip.Trigger class="w-full">
				<Input type="text" placeholder="Palette name" bind:value={palette.name} />
			</Tooltip.Trigger>
			<Tooltip.Content>
				<p>Palette name</p>
			</Tooltip.Content>
		</Tooltip.Root>
		<div>
			<Tooltip.Root openDelay={0}>
				<Tooltip.Trigger asChild let:builder>
					<Button
						builders={[builder]}
						class="w-full {palette.default ? 'bg-violet-500 hover:bg-violet-600' : ''}"
						on:click={() => dispatch('setdefault')}
					>
						<Flame size={16} />
					</Button>
				</Tooltip.Trigger>
				<Tooltip.Content>
					<p>Set as default</p>
				</Tooltip.Content>
			</Tooltip.Root>
		</div>
		<div>
			<Tooltip.Root openDelay={0}>
				<Tooltip.Trigger asChild let:builder>
					<Button
						builders={[builder]}
						variant="destructive"
						class="w-full"
						on:click={() => dispatch('delete')}
					>
						<Trash2 size={16} />
					</Button>
				</Tooltip.Trigger>
				<Tooltip.Content>
					<p>Delete palette</p>
				</Tooltip.Content>
			</Tooltip.Root>
		</div>
	</div>
	<Accordion.Root class="w-full">
		<Accordion.Item value="item-1">
			<Accordion.Trigger>See / Edit dice</Accordion.Trigger>
			<Accordion.Content>
				<PaletteDiceEditor {dice} {palette} />
			</Accordion.Content>
		</Accordion.Item>
	</Accordion.Root>
</Card>
