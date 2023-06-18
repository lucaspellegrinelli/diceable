<script lang="ts">
	export let customColors: boolean;
</script>

<h1 class="text-4xl font-bold mb-4">Configurations</h1>

<div class="flex">
	<label class="cursor-pointer label">
		<span class="label-text mr-4">Custom Colors</span>
		<input type="checkbox" class="checkbox" bind:checked={customColors} />
	</label>
</div>
