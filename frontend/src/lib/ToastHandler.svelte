<script lang="ts">
	import { Toast } from 'flowbite-svelte';
	import Icon from '@iconify/svelte';
	import { toasts } from './stores';

	const toastColor = (type: string) => {
		switch (type) {
			case 'success':
				return 'green';
			case 'error':
				return 'red';
			default:
				return 'gray';
		}
	};
</script>

<div class="w-full h-full">
	{#each $toasts as toast}
		<Toast position="bottom-right" color={toastColor(toast.type)}>
			<svelte:fragment slot="icon">
				{#if toast.type === 'success'}
					<Icon icon="mdi:check" class="inline-block" />
				{:else if toast.type === 'error'}
					<Icon icon="mdi:alert" class="inline-block" />
				{/if}
			</svelte:fragment>
			<span>{toast.message}</span>
		</Toast>
	{/each}
</div>
