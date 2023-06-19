<script lang="ts">
	import { signIn, signOut } from '@auth/sveltekit/client';
	import { page } from '$app/stores';
	import { Button, Modal } from 'flowbite-svelte';
	import Icon from '@iconify/svelte';

	let signOutModal = false;
</script>

<div class="bg-gray-100">
	<div class="flex flex-col justify-center items-center h-screen">
		<h1 class="text-4xl font-bold text-gray-800 mb-6">Diceable</h1>
		<p class="text-gray-600 text-lg mb-8">
			Discord bot to roll dice in Discord and OBS simultaneously
		</p>
		{#if $page.data.session}
			<div class="flex space-x-4">
				<Button color="blue" href="/admin" pill>
					Go to dashboard
					<Icon icon="mdi:wrench" class="ml-2" />
				</Button>
				<Button color="red" on:click={() => (signOutModal = true)} pill>
					Sign out
					<Icon icon="fa-solid:sign-out-alt" class="ml-2" />
				</Button>
			</div>
		{:else}
			<Button color="blue" on:click={() => signIn('discord')} pill>
				Sign in with Discord
				<Icon icon="mdi:discord" class="ml-2" />
			</Button>
		{/if}
	</div>
</div>

<Modal bind:open={signOutModal} size="xs" autoclose>
	<div class="text-center">
		<Icon icon="mdi:run" class="m-auto text-6xl mb-4" />
		<h3 class="mb-5 text-lg font-normal text-gray-500 dark:text-gray-400">
			Are you sure you want to sign out?
		</h3>
		<Button color="red" class="mr-2" on:click={() => signOut()}>Yes, I want to sign out</Button>
		<Button color="alternative">No, keep me signed in</Button>
	</div>
</Modal>
