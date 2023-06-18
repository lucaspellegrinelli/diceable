import { redirect } from '@sveltejs/kit';
import type { PageServerLoad } from './$types';
import type { PageServerLoadData, Config } from '$lib/types';

export const load: PageServerLoad<PageServerLoadData> = async (event) => {
    const session = await event.locals.getSession();
    if (!session?.user) {
        throw redirect(303, '/auth');
    }

    const user = session?.user?.image?.split('avatars/')[1]?.split('/')[0] || '';

    const [configRes, effectRes, diceRes] = await Promise.all([
        event.fetch(`/api/config/${user}`),
        event.fetch(`/api/assets/effects`),
        event.fetch(`/api/assets/dice`)
    ]);

    const [config, effects, dice]: [Config, string[], string[]] = await Promise.all([
        configRes.json(),
        effectRes.json(),
        diceRes.json()
    ]);

    return {
        session,
        user,
        config,
        effects,
        dice
    };
};

export const actions = {
    default: async (event) => {
        const { request } = event;
        const session = await event.locals.getSession();
        const sessionUser = session?.user?.image?.split('avatars/')[1]?.split('/')[0] || '';

        const data = await request.formData();
        const user = data.get('user');

        if (sessionUser !== user) {
            return {
                status: 403,
                body: {
                    message: 'You are not authorized to perform this action.'
                }
            };
        }

        const customColors = data.get('custom_colors');
        const palettes = JSON.parse(data.get('palettes') || '{}');
        const playerSkins = JSON.parse(data.get('player_skins') || '{}');

        const response = await event.fetch(`/api/config/${user}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                custom_colors: customColors,
                palettes: palettes,
                player_skins: playerSkins
            })
        });

        return await response.json();
    }
};
