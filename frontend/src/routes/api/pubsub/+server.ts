import redisClient from '$lib/redisConnection';

export async function GET() {
    const readable = new ReadableStream({
        start(controller) {
            redisClient.subscribe('rolls', (message) => {
                controller.enqueue(message);
            });
        }
    });

    return new Response(readable, {
        headers: { 'Content-Type': 'text/event-stream' }
    });
}
