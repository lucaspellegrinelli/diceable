import { env } from '$env/dynamic/private';
import { S3Client, ListObjectsV2Command } from "@aws-sdk/client-s3";

const S3 = new S3Client({
    region: env.S3_REGION,
    endpoint: env.S3_ENDPOINT,
    credentials: {
        accessKeyId: env.S3_ACCESS_KEY_ID,
        secretAccessKey: env.S3_SECRET_ACCESS_KEY,
    },
});

export default S3;

export const listObjects = async (bucket: string, prefix: string) => {
    const params = {
        Bucket: bucket,
        Prefix: prefix,
    };

    return await S3.send(new ListObjectsV2Command(params));
}
