import { env } from '$env/dynamic/private';

export async function GET({ params }) {
	const userUUID = params.user;
	const suburb_host = env.SUBURB_HOST;
	const suburb_api_key = env.SUBURB_API_KEY;
	const namespace = 'diceable';
	const queue_name = `roll-${userUUID}`;

	return await fetch(`${suburb_host}/queues/${namespace}/${queue_name}/pop`, {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json',
			Authorization: `${suburb_api_key}`
		},
		body: JSON.stringify({})
	});
}
