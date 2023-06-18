import { SvelteKitAuth } from '@auth/sveltekit';

import Discord from '@auth/core/providers/discord';
import { env as privEnv } from '$env/dynamic/private';

export const handle = SvelteKitAuth({
    providers: [
        // @ts-expect-error TS Bug
        Discord({
            clientId: privEnv.DISCORD_CLIENT_ID,
            clientSecret: privEnv.DISCORD_CLIENT_SECRET
        })
    ],
    callbacks: {
        async signIn(data) {
            const { account } = data;
            if (!account) {
                console.error('No account found.', data);
                return false;
            }

            const userDiscordId = account?.providerAccountId;

            fetch(`http://localhost:3000/api/config/${userDiscordId}/new`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({})
            });

            return true;
        }
    }
});
