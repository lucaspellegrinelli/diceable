<script lang="ts">
	import { signIn, signOut } from '@auth/sveltekit/client';
	import { page } from '$app/stores';
	import Icon from '@iconify/svelte';
	import { Button } from '$lib/components/ui/button';
	import * as Dialog from '$lib/components/ui/dialog';
	import { LogOut, Wrench } from 'lucide-svelte';

	let signOutModal = false;
</script>

<div class="flex h-screen justify-center items-center text-center">
	<div>
		<h1 class="mb-4 text-4xl font-extrabold md:text-5xl lg:text-6xl">Diceable</h1>
		<p class="mb-6 text-lg lg:text-xl sm:px-16 xl:px-48 dark:text-gray-400 text-center">
			Discord bot to roll dice in Discord and OBS simultaneously.
		</p>
		{#if $page.data.session}
			<Button href="/dashboard/d10">
				Go to dashboard
				<Wrench size={16} class="ml-2" />
			</Button>
			<Button variant="destructive" on:click={() => (signOutModal = true)}>
				Sign out
				<LogOut size={16} class="ml-2" />
			</Button>
		{:else}
			<Button on:click={() => signIn('discord')}>
				Sign in with Discord
				<Icon icon="mdi:discord" class="ml-2" />
			</Button>
		{/if}
	</div>
</div>

<Dialog.Root bind:open={signOutModal}>
	<Dialog.Trigger />
	<Dialog.Portal>
		<Dialog.Content>
			<Dialog.Title>Sign out</Dialog.Title>
			<Dialog.Description>
				Are you sure you want to sign out?
				<div class="flex justify-start mt-4">
					<Button variant="destructive" class="mr-2" on:click={() => signOut()}
						>Yes, I want to sign out</Button
					>
					<Button on:click={() => (signOutModal = false)}>No, keep me signed in</Button>
				</div></Dialog.Description
			>
		</Dialog.Content>
	</Dialog.Portal>
</Dialog.Root>
