import { parseServerConfig } from '$lib/config';
import type { DiceConfig } from '$lib/types';
import { redirect } from '@sveltejs/kit';

export const load = async (event: any) => {
    const session = await event.locals.getSession();
    if (!session?.user) {
        throw redirect(303, '/auth');
    }

    const user = session?.user?.image?.split('avatars/')[1]?.split('/')[0] || '';

    const configRes = await event.fetch(`/api/config/${user}/d10`);
    const config: DiceConfig = await configRes.json();

    return {
        session,
        user,
        config: parseServerConfig(config)
    };
};
