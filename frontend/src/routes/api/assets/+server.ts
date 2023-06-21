import { env } from '$env/dynamic/private';
import type { CloudflareImageResponse, CloudflareVideoResponse } from '$lib/types';

// const getCloudflareImageUrl = (id: string) =>
//     `https://imagedelivery.net/qzTQhwVAd5ZPCy9exIQX3g/${id}/public`;
//
// const getCloudflareVideoUrl = (id: string) =>
//     `https://customer-w3hebi5t5ry9tdrc.cloudflarestream.com/${id}/downloads/default.mp4`;

const getDiceUrl = (type: string, skin: string, number: number) =>
    `https://assets.togarashi.app/dice/${type}/${skin}/${number}.png`;

const getEffectUrl = (type: string, skin: string, number: number) =>
    `https://assets.togarashi.app/effects/${type}/${skin}/${number}.mp4`;

export async function GET({ url }) {
    const numberDice: number = parseInt(url.searchParams.get('number'));
    const palette: { name: string; number: number }[] = JSON.parse(url.searchParams.get('palette'));
    const effect: string = url.searchParams.get('effect');

    const ids: {
        dice: Record<number, string>;
        effect: string;
    } = { dice: {}, effect: '' };

    for (const paletteItem of palette) {
        ids.dice[paletteItem.number] = getDiceUrl('d10', paletteItem.name, paletteItem.number);
    }

    if (effect) {
        ids.effect = getEffectUrl('d10', effect, numberDice);
    }

    // const imagesEndpoint = `https://api.cloudflare.com/client/v4/accounts/${env.CLOUDFLARE_ACCOUNT_ID}/images/v2`;
    // const videosEndpoint = `https://api.cloudflare.com/client/v4/accounts/${env.CLOUDFLARE_ACCOUNT_ID}/stream`;
    //
    // const headers = {
    //     Authorization: `Bearer ${env.CLOUDFLARE_ASSETS_API_TOKEN}`,
    //     'Content-Type': 'application/json'
    // };
    //
    // const ids: {
    //     dice: Record<number, string>;
    //     effect: string;
    // } = { dice: {}, effect: '' };
    //
    // const response = await fetch(imagesEndpoint, { headers });
    // const responseJson: CloudflareImageResponse = await response.json();
    // const allImages = responseJson.result.images;
    //
    // for (const paletteItem of palette) {
    //     const fileName = `${paletteItem.name}-${paletteItem.number}.png`;
    //
    //     for (const diceInfo of allImages) {
    //         if (diceInfo.filename === fileName) {
    //             ids.dice[paletteItem.number] = getCloudflareImageUrl(diceInfo.id);
    //         }
    //     }
    // }
    //
    // if (effect) {
    //     const response = await fetch(videosEndpoint, { headers });
    //     const responseJson: CloudflareVideoResponse = await response.json();
    //     const allVideos = responseJson.result;
    //
    //     for (const videoInfo of allVideos) {
    //         const fileName = videoInfo.meta.filename.split('.')[0];
    //         const effectName = fileName.split('-')[0];
    //         const effectNDice = parseInt(fileName.split('-')[1]);
    //         const effectId = videoInfo.uid;
    //
    //         if (effectName === effect && effectNDice === numberDice) {
    //             ids.effect = getCloudflareVideoUrl(effectId);
    //             break;
    //         }
    //     }
    // }

    return new Response(JSON.stringify(ids));
}
