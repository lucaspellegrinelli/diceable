import type { Session } from '@auth/core/types';

export type PlayerSkin = {
	palette?: string;
	effect?: string;
};

export type Config = {
	custom_colors: string;
	palettes: { [key: string]: string[] };
	player_skins: { [key: string]: PlayerSkin };
};

export type PageServerLoadData = {
	user: string;
	config: Config;
	effects: string[];
	dice: string[];
	session: Session | null;
};

type CloudflareImageInfo = {
    filename: string;
    id: string;
};

export type CloudflareImageResponse = {
    result: {
        images: CloudflareImageInfo[];
    };
};

type CloudflareVideoInfo = {
    meta: {
        filename: string;
    };
    uid: string;
};

export type CloudflareVideoResponse = {
    result: CloudflareVideoInfo[];
};
