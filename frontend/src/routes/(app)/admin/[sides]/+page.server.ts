import { redirect } from '@sveltejs/kit';
import type { PageServerLoad } from './$types';
import type { PageServerLoadData, Config } from '$lib/types';

export const load: PageServerLoad<PageServerLoadData> = async (event) => {
    const session = await event.locals.getSession();
    if (!session?.user) {
        throw redirect(303, '/auth');
    }

    const user = session?.user?.image?.split('avatars/')[1]?.split('/')[0] || '';
    const sides = event.params.sides || "d10";

    const [configRes, effectRes, diceRes] = await Promise.all([
        event.fetch(`/api/config/${user}/${sides}`),
        event.fetch(`/api/assets/effects/${sides}`),
        event.fetch(`/api/assets/dice/${sides}`)
    ]);

    const [config, effects, dice]: [Config, string[], string[]] = await Promise.all([
        configRes.json(),
        effectRes.json(),
        diceRes.json()
    ]);

    return {
        session,
        user,
        sides,
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
        const sides = data.get('sides');

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
        const defaultPalette = data.get('default_palette');

        const response = await event.fetch(`/api/config/${user}/${sides}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                custom_colors: customColors,
                palettes: palettes,
                player_skins: playerSkins,
                default_palette: defaultPalette
            })
        });

        return await response.json();
    }
};