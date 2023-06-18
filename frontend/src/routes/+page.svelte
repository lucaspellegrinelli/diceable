<script lang="ts">
	import { signIn, signOut } from '@auth/sveltekit/client';
	import { page } from '$app/stores';
</script>

<div class="bg-gray-100">
	<div class="flex flex-col justify-center items-center h-screen">
		<h1 class="text-4xl font-bold text-gray-800 mb-6">Diceable</h1>
		<p class="text-gray-600 text-lg mb-8">
			Discord bot to roll dice in Discord and OBS simultaneously
		</p>
		{#if $page.data.session}
			<div class="flex space-x-4">
				<a
					href="/admin"
					class="px-6 py-3 bg-blue-500 text-white rounded-full shadow hover:bg-blue-600 transition-colors duration-300"
				>
					Go to Dashboard
				</a>
				<button
					class="px-6 py-3 bg-red-500 text-white rounded-full shadow hover:bg-red-600 transition-colors duration-300"
					on:click={() => signOut()}
				>
					Sign Out
				</button>
			</div>
		{:else}
			<button
				class="px-6 py-3 bg-blue-500 text-white rounded-full shadow hover:bg-blue-600 transition-colors duration-300"
				on:click={() => signIn("discord")}
			>
				Sign in with Discord
			</button>
		{/if}
	</div>
</div>
