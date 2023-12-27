import { redirect } from '@sveltejs/kit';
import type { PageServerLoad } from './$types';
import type { PageServerLoadData, Config, PlayerSkin, Palette } from '$lib/types';

export const load: PageServerLoad<PageServerLoadData> = async (event) => {
    const session = await event.locals.getSession();
    if (!session?.user) {
        throw redirect(303, '/auth');
    }

    const INVALID_PALETTE_NAME = 'Unknown';
    const DEFAULT_EFFECT_NAME = 'None';

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

    let palettes: Palette[] = [];
    let playerSkins: Array<PlayerSkin> = [];

    for (const [key, value] of Object.entries(config.palettes)) {
        const isDefault = key === config.default_palette;
        palettes = [...palettes, { name: key, skin: value, default: isDefault }];
    }

    for (const [key, value] of Object.entries(config.player_skins)) {
        const playerPalette = value.palette || INVALID_PALETTE_NAME;
        const playerEffect = value.effect || DEFAULT_EFFECT_NAME;
        const playerDescription = value.description || '';
        playerSkins = [
            ...playerSkins,
            {
                discordId: key,
                description: playerDescription,
                palette: playerPalette,
                effect: playerEffect
            }
        ];
    }

    return {
        session,
        user,
        sides,
        config,
        effects,
        dice,
        palettes,
        playerSkins
    };
};
