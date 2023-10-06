import { env } from '$env/dynamic/private';
import { listObjects } from '$lib/s3Connection';

export async function GET({ params, url }) {
    const diceSides = params.sides;
    const s3Response = await listObjects(env.S3_BUCKET, `dice/${diceSides}/`);

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
