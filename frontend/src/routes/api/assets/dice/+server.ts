import { env } from '$env/dynamic/private';
import { listObjects } from '$lib/s3Connection';

export async function GET({ url }) {
    const params = {
        Bucket: env.S3_BUCKET,
        Prefix: 'dice/'
    };

    const s3Response = await listObjects(params.Bucket, params.Prefix);

    const diceNames = new Set();
    if (s3Response.Contents) {
        for (const diceInfo of s3Response.Contents) {
            if (!diceInfo.Key) {
                continue;
            }

            const splittedPath = diceInfo.Key.split('/');
            const diceName = splittedPath[splittedPath.length - 2];
            diceNames.add(diceName);
        }
    }

    return new Response(JSON.stringify(Array.from(diceNames)));
}
