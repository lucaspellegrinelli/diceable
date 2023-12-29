export type Toast = {
    message: string;
    type: "success" | "error" | "info";
    createdAt: number;
};

export type PlayerSkin = {
    discordId: string;
    description: string;
    palette: string;
    effect?: string;
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

// Client types
export type LocalPalette = {
    name: string;
    skin: string[];
    default: boolean;
};

export type LocalDiceConfig = {
    customColors: boolean;
    palettes: LocalPalette[];
    playerSkins: PlayerSkin[];
};

export type LocalUserConfig = {
    [key: string]: LocalDiceConfig;
};
