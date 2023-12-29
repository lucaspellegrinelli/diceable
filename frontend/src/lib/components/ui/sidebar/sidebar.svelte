<script lang="ts">
	import { cn } from '$lib/utils';
	import { page } from '$app/stores';
	import { Button } from '$lib/components/ui/button';
	let className: string | undefined | null = undefined;
	export let items: { href: string; title: string }[];
	export { className as class };
</script>

<nav
	class={cn(
		'grid grid-cols-3 min-[420px]:flex min-[420px]:space-x-2 lg:flex-col lg:space-x-0 lg:space-y-1',
		className
	)}
>
	{#each items as item}
		<Button
			href={item.href}
			variant="ghost"
			class={cn(
				$page.url.pathname === item.href
					? 'bg-muted hover:bg-muted'
					: 'hover:bg-transparent hover:underline',
				'justify-center md:justify-start'
			)}
		>
			{item.title}
		</Button>
	{/each}
</nav>
