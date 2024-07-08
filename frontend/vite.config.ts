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
				onProxyReqWs: (proxyReq, req, socket, options, head) => {
					console.log('proxyReqWs');
					proxyReq.setHeader('authorization', `${process.env.SUBURB_TOKEN}`);
					console.log('suburb token', process.env.SUBURB_TOKEN);
				}
			}
		}
	},
	preview: {
		port: parseInt(process.env.PORT || '3000')
	},
	plugins: [sveltekit()]
});
