import { env as privEnv } from '$env/dynamic/private';
import Discord from '@auth/core/providers/discord';
import { SvelteKitAuth } from '@auth/sveltekit';

const { handle, signIn, signOut } = SvelteKitAuth({
    trustHost: true,
    providers: [
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

            // Initialize user config by trying to GET d10 config, which will create default config if it doesn't exist
            try {
                await fetch(`http://localhost:3000/api/config/${userDiscordId}/d10`, {
                    method: 'GET',
                    headers: {
                        'Content-Type': 'application/json'
                    }
                });
            } catch (error) {
                console.error('Failed to initialize user config:', error);
            }

            return true;
        }
    }
});

export { handle, signIn, signOut };

