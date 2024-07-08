import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig } from 'vite';

export default defineConfig({
	server: {
		port: parseInt(process.env.PORT || '3000'),
		watch: {
			usePolling: true,
			interval: 100
		}
	},
	preview: {
		port: parseInt(process.env.PORT || '3000')
	},
	plugins: [sveltekit()]
});
