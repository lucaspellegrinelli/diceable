<script lang="ts">
	import { Button } from '$lib/components/ui/button';
	import { Card } from '$lib/components/ui/card';
	import * as Dialog from '$lib/components/ui/dialog';
	import Icon from '@iconify/svelte';
	import { onMount } from 'svelte';
	import type { PageData } from './$types';

	export let data: PageData;
	let obsTutorialModal = false;

	let obsLink = '';

	const openObsTutorialModal = () => {
		obsTutorialModal = true;
	};

	onMount(() => {
		const currentHost = window.location.host;
		obsLink = `https://${currentHost}/${data.user}`;
	});
</script>

<div class="grid grid-cols-1 md:grid-cols-2 gap-2">
	<Card class="flex flex-col items-center p-4 text-center">
		<Icon icon="mdi:discord" class="text-4xl" />
		<h3 class="mb-2 text-2xl font-bold">Discord bot invite link</h3>
		<p>Invite our bot to your Discord server to enhance your gaming experience.</p>
		<Button
			href="https://discord.com/api/oauth2/authorize?client_id=1116110919953563729&permissions=1024&scope=bot"
			target="_blank"
			class="w-full mt-2">Add bot to your server</Button
		>
	</Card>
	<Card class="flex flex-col items-center p-4 text-center">
		<Icon icon="simple-icons:obsstudio" class="text-4xl" />
		<h3 class="mb-2 text-2xl font-bold">OBS overlay page</h3>
		<p>Display your dice rolls on stream with our OBS overlay page.</p>
		<Button on:click={openObsTutorialModal} class="w-full mt-2">How to set up</Button>
	</Card>
</div>

<Dialog.Root bind:open={obsTutorialModal}>
	<Dialog.Trigger />
	<Dialog.Portal>
		<Dialog.Content>
			<Dialog.Title>Setting up OBS scene</Dialog.Title>
			<Dialog.Description>
				<p class="text-justify">
					In the target OBS scene create two <strong>Browser</strong> sources. One for the dice rolls
					and one for the effects. Put the effect browser source on top of the dice rolls browser source
					and configure them as follows (everything else should be left as default):
				</p>

				<ul class="list-disc list-inside space-y-2 my-4">
					<li>URL: <strong><a href={obsLink} target="_blank">{obsLink}</a></strong></li>
					<li>Width: <strong>1920</strong></li>
					<li>Height: <strong>2160</strong></li>
					<li>Custom CSS: <strong>{'body{margin:0}'}<strong></strong></strong></li>
				</ul>

				<p class="text-justify">
					Aditionally, for the <strong>Effects</strong> browser source, you need to set the following:
				</p>

				<ul class="list-disc list-inside space-y-2 my-4">
					<li>Right click &gt Blending Mode &gt Screen</li>
					<li>
						Right click &gt Transform &gt Edit Transform &gt Position should be 0px for the first
						one and -1080px for the second one
					</li>
				</ul>

                <Button on:click={() => obsTutorialModal = false} class="w-full mt-2">Close</Button>
			</Dialog.Description>
		</Dialog.Content>
	</Dialog.Portal>
</Dialog.Root>
