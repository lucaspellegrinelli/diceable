import { updateCurrentConfig } from '$lib/config';
import { redirect } from '@sveltejs/kit';

export const load = async (event: any) => {
    const session = await event.locals.getSession();
    if (!session?.user) {
        throw redirect(303, '/auth');
    }

    const user = session?.user?.image?.split('avatars/')[1]?.split('/')[0] || '';

    const { effects, diceSkins, config } = await updateCurrentConfig(user, 'd10', event.fetch);

    return {
        session,
        user,
        effects,
        diceSkins,
        config
    };
};
