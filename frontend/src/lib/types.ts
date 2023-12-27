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

export type DiceConfig = {
    custom_colors: string;
    palettes: { [key: string]: string[] };
    player_skins: { [key: string]: PlayerSkin };
    default_palette: string;
};

export type UserConfig = {
    [key: string]: DiceConfig;
};
