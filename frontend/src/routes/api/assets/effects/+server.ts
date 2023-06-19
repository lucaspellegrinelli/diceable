import { env } from '$env/dynamic/private';
import type { CloudflareVideoResponse } from '$lib/types';

export async function GET({ url }) {
    const videosEndpoint = `https://api.cloudflare.com/client/v4/accounts/${env.CLOUDFLARE_ACCOUNT_ID}/stream`;

    const headers = {
        Authorization: `Bearer ${env.CLOUDFLARE_ASSETS_API_TOKEN}`,
        'Content-Type': 'application/json'
    };

    const effectNames = new Set();

    const response = await fetch(videosEndpoint, { headers });
    const responseJson: CloudflareVideoResponse = await response.json();
    const allVideos = responseJson.result;

    for (const effectInfo of allVideos) {
        const effectName = effectInfo.meta.filename.split('-')[0];
        effectNames.add(effectName);
    }

    return new Response(JSON.stringify(Array.from(effectNames)));
}
