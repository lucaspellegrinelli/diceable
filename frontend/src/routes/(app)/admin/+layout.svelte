<script lang="ts">
	import { Separator } from '$lib/components/ui/separator';
	import Sidebar from '$lib/components/ui/sidebar/sidebar.svelte';

	const sidebarNavItems = [
		{
			title: 'Home',
			href: '/admin'
		},
		{
			title: 'Configuration',
			href: '/admin/configuration'
		},
		{
			title: 'Palettes',
			href: '/admin/palettes'
		}
	];
</script>

<div class="space-y-6 p-5 md:p-10 pb-16 w-full">
	<div class="space-y-0.5">
		<h2 class="text-2xl font-bold tracking-tight">Dashboard</h2>
		<p class="text-muted-foreground">Change the dice settings for your servers here.</p>
	</div>
	<Separator class="my-6" />
	<div class="flex flex-col space-y-8 lg:flex-row lg:space-x-12 lg:space-y-0">
		<aside class="-mx-4 lg:w-1/5">
			<Sidebar items={sidebarNavItems} />
		</aside>
		<div class="flex-1">
			<slot />
		</div>
	</div>
</div>
