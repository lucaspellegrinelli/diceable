<script lang="ts">
	import { signIn, signOut } from '@auth/sveltekit/client';
	import { page } from '$app/stores';
	import { Button, Heading, Modal, P } from 'flowbite-svelte';
	import Icon from '@iconify/svelte';

	let signOutModal = false;
</script>

<div class="flex h-screen justify-center items-center text-center">
	<div>
		<Heading tag="h1" class="mb-4" customSize="text-4xl font-extrabold  md:text-5xl lg:text-6xl">
			Diceable
		</Heading>
		<P class="mb-6 text-lg lg:text-xl sm:px-16 xl:px-48 dark:text-gray-400">
			Discord bot to roll dice in Discord and OBS simultaneously.
		</P>
		{#if $page.data.session}
			<Button color="blue" href="/admin" pill>
				Go to dashboard
				<Icon icon="mdi:wrench" class="ml-2" />
			</Button>
			<Button color="red" on:click={() => (signOutModal = true)} pill>
				Sign out
				<Icon icon="fa-solid:sign-out-alt" class="ml-2" />
			</Button>
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
