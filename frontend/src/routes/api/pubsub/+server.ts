import { redisPubsubClient } from '$lib/redisConnection';

export async function GET() {
    const readable = new ReadableStream({
        start(controller) {
            try {
                redisPubsubClient.subscribe('rolls', (message) => {
                    try {
                        controller.enqueue(message);
                    } catch (error) {
                        console.error('Failed to enqueue message', error);
                    }
                });
            } catch (error) {
                console.error('Failed to subscribe to redis channel', error);
            }
        },
        cancel() {
            redisPubsubClient.unsubscribe('rolls');
        }
    });

    return new Response(readable, {
        headers: { 'Content-Type': 'text/event-stream' }
    });
}
