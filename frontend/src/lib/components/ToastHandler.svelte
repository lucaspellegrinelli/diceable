<script lang="ts">
	import * as Alert from '$lib/components/ui/alert';
	import { toasts } from '$lib/stores';
    import type { Toast } from '$lib/types';
	import { AlertTriangle, Check, ChevronRight } from 'lucide-svelte';
	import { fade } from 'svelte/transition';

	const successClasses = 'bg-green-200 border-green-400 dark:bg-slate-900 dark:border-green-600';
	const errorClasses = 'bg-red-200 border-red-400 dark:bg-slate-900 dark:border-red-600';
	const neutralClasses = 'bg-white border-gray-300 dark:bg-slate-900 dark:border-gray-600';

	const getToastClasses = (toast: Toast): string => {
		if (toast.type === 'success') {
			return successClasses;
		} else if (toast.type === 'error') {
			return errorClasses;
		} else {
			return neutralClasses;
		}
	};

	const getToastTitle = (toast: Toast): string => {
		if (toast.type === 'success') {
			return 'Success';
		} else if (toast.type === 'error') {
			return 'Error';
		} else {
			return 'Info';
		}
	};
</script>

<div class="fixed top-0 right-0 m-4 space-y-2 w-1/2 md:w-1/3 lg:w-1/4">
	{#each $toasts as toast}
		<div transition:fade>
			<Alert.Root class={getToastClasses(toast)}>
				{#if toast.type === 'success'}
					<Check class="h-4 w-4" />
				{:else if toast.type === 'error'}
					<AlertTriangle class="h-4 w-4" />
				{:else}
					<ChevronRight class="h-4 w-4" />
				{/if}
				<Alert.Title>{getToastTitle(toast)}</Alert.Title>
				<Alert.Description>{toast.message}</Alert.Description>
			</Alert.Root>
		</div>
	{/each}
</div>
