import { env } from '$env/dynamic/private';
import { listObjects } from '$lib/s3Connection';

export async function GET({ params, url }) {
    const diceSides = params.sides;
    const s3Response = await listObjects(env.S3_BUCKET, `effects/${diceSides}/`);

    const effectNames = new Set();
    if (s3Response.Contents) {
        for (const effectsInfo of s3Response.Contents) {
            if (!effectsInfo.Key) {
                continue;
            }

            const splittedPath = effectsInfo.Key.split('/');
            const effectsName = splittedPath[splittedPath.length - 2];
            effectNames.add(effectsName);
        }
    }

    return new Response(JSON.stringify(Array.from(effectNames)));
}
