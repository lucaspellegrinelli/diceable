import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig } from 'vite';
import dotenv from 'dotenv';

dotenv.config();

export default defineConfig({
	server: {
		port: parseInt(process.env.PORT || '3000'),
		watch: {
			usePolling: true,
			interval: 100
		},
		proxy: {
			'/rolls': {
				target: `wss://${process.env.SUBURB_HOST}/pubsub/rolls/listen`,
				ws: true,
				changeOrigin: true,
				rewrite: (path) => path.replace(/^\/rolls/, ''),
				configure: (proxy, options) => {
					proxy.on('proxyReqWs', (proxyReq, req, socket, options, head) => {
						proxyReq.setHeader('authorization', `${process.env.SUBURB_TOKEN}`);
					});
				}
			}
		}
	},
	preview: {
		port: parseInt(process.env.PORT || '3000')
	},
	plugins: [sveltekit()]
});
