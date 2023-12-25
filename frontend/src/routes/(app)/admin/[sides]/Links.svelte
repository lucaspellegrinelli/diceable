<script lang="ts">
	import Icon from '@iconify/svelte';
	import { Button, Card, Modal } from 'flowbite-svelte';
	import { onMount } from 'svelte';

	export let user: string;
	let obsTutorialModal = false;

	let obsLink = '';

	const openObsTutorialModal = () => {
		obsTutorialModal = true;
	};

	onMount(() => {
		const currentHost = window.location.host;
		obsLink = `https://${currentHost}/${user}`;
	});
</script>

<div class="grid w-full grid-cols-2 gap-2 mb-6">
	<Card size="xl" class="flex flex-col items-center">
		<Icon icon="mdi:discord" class="text-4xl text-center text-gray-900 dark:text-white" />
		<h5 class="mb-2 text-2xl font-bold tracking-tight text-gray-900 dark:text-white">
			Discord bot invite link
		</h5>
		<p class="font-normal text-gray-700 dark:text-gray-400 leading-tight">
			Invite our bot to your Discord server to enhance your gaming experience.
		</p>
		<Button
			href="https://discord.com/api/oauth2/authorize?client_id=1116110919953563729&permissions=1024&scope=bot"
			target="_blank"
			class="w-full mt-4"
			color="primary">Add bot to your server</Button
		>
	</Card>
	<Card size="xl" class="flex flex-col items-center">
		<Icon
			icon="simple-icons:obsstudio"
			class="text-4xl text-center text-gray-900 dark:text-white"
		/>
		<h5 class="mb-2 text-2xl font-bold tracking-tight text-gray-900 dark:text-white">
			OBS overlay page
		</h5>
		<p class="font-normal text-gray-700 dark:text-gray-400 leading-tight">
			Display your dice rolls on stream with our OBS overlay page.
		</p>
		<Button class="w-full mt-4" on:click={openObsTutorialModal} color="primary"
			>How to set up</Button
		>
	</Card>
</div>

<Modal title="OBS Setup" bind:open={obsTutorialModal} autoclose class="space-y-2">
	<p class="text-base leading-relaxed text-gray-500 dark:text-gray-400">
		In the target OBS scene create two <strong>Browser</strong> sources. One for the dice rolls and one
		for the effects. Put the effect browser source on top of the dice rolls browser source and configure
		them as follows (everything else should be left as default):
	</p>

	<ul class="list-disc list-inside space-y-2">
		<li>URL: <strong><a href={obsLink} target="_blank">{obsLink}</a></strong></li>
		<li>Width: <strong>1920</strong></li>
		<li>Height: <strong>2160</strong></li>
		<li>Custom CSS: <strong>{'body{margin:0}'}<strong></strong></strong></li>
	</ul>
	<p class="text-base leading-relaxed text-gray-500 dark:text-gray-400">
		Aditionally, for the <strong>Effects</strong> browser source, you need to set the following:
	</p>

	<ul class="list-disc list-inside space-y-2">
		<li>Right click &gt Blending Mode &gt Screen</li>
		<li>
			Right click &gt Transform &gt Edit Transform &gt Position should be 0px for the first one and
			-1080px for the second one
		</li>
	</ul>

	<Button color="alternative">Close</Button>
</Modal>
