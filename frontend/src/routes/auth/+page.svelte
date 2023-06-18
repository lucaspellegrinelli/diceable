<script lang="ts">
	import '../../app.postcss';

	import { page } from '$app/stores';
</script>

{#if $page.data.session}
	<a href="/auth/signout" class="btn btn-primary" data-sveltekit-preload-data="off">Sign out</a>
{:else}
	<a href="/auth/signin" class="btn btn-primary" data-sveltekit-preload-data="off">Sign in</a>
{/if}
