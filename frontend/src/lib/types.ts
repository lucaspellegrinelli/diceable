import type { Session } from '@auth/core/types';

export type Toast = {
    message: string;
    type: "success" | "error";
    createdAt: number;
};

export type PlayerSkin = {
    discordId: string;
    description: string;
    palette: string;
    effect?: string;
};

export type Palette = {
    name: string;
    skin: string[];
    default: boolean;
};

export type Config = {
    custom_colors: string;
    palettes: { [key: string]: string[] };
    default_palette: string;
    player_skins: { [key: string]: PlayerSkin };
};
