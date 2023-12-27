<script lang="ts">
	import { Separator } from '$lib/components/ui/separator';
	import { Label } from '$lib/components/ui/label';
	import { Switch } from '$lib/components/ui/switch';
	import type { PageData } from './$types';

	export let data: PageData;

	let customColors = false;

	$: data.config.custom_colors = customColors ? 'true' : 'false';
</script>

<div class="space-y-6 lg:max-w-2xl">
	<div>
		<h3 class="text-lg font-medium">Configurations</h3>
		<p class="text-sm text-muted-foreground">Define the configurations for your server.</p>
	</div>
	<Separator />

	<div class="flex items-center justify-between space-x-2">
		<Label for="custom_colors" class="flex flex-col space-y-1">
			<span>Custom colors</span>
			<span class="text-xs font-normal leading-snug text-muted-foreground">
				Enable this to use the custom color palettes chosen below for the players.
			</span>
		</Label>
		<Switch id="custom_colors" aria-label="Custom Colors" bind:checked={customColors} />
	</div>
</div>
