import { env } from '$env/dynamic/private';
import { listObjects } from '$lib/s3Connection';

export async function GET({ url }) {
    const params = {
        Bucket: env.S3_BUCKET,
        Prefix: 'effects/'
    };

    const s3Response = await listObjects(params.Bucket, params.Prefix);

    const effectsNames = new Set();
    if (s3Response.Contents) {
        for (const effectsInfo of s3Response.Contents) {
            if (!effectsInfo.Key) {
                continue;
            }

            const splittedPath = effectsInfo.Key.split('/');
            const effectsName = splittedPath[splittedPath.length - 2];
            effectsNames.add(effectsName);
        }
    }

    return new Response(JSON.stringify(Array.from(effectsNames)));
}
