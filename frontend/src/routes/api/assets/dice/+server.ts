import { env } from '$env/dynamic/private';

type CloudflareImageInfo = {
    filename: string;
    id: string;
};

type CloudflareImageResponse = {
    result: {
        images: CloudflareImageInfo[];
    };
};

export async function GET({ url }) {
    const imagesEndpoint = `https://api.cloudflare.com/client/v4/accounts/${env.CLOUDFLARE_ACCOUNT_ID}/images/v2`;

    const headers = {
        Authorization: `Bearer ${env.CLOUDFLARE_ASSETS_API_TOKEN}`,
        'Content-Type': 'application/json'
    };

    const diceNames = new Set();

    const response = await fetch(imagesEndpoint, { headers });
    const responseJson: CloudflareImageResponse = await response.json();
    const allImages = responseJson.result.images;

    for (const diceInfo of allImages) {
        const diceName = diceInfo.filename.split('-')[0];
        diceNames.add(diceName);
    }

    return new Response(JSON.stringify(Array.from(diceNames)));
}
