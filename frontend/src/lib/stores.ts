import { writable } from "svelte/store";
import type {
    LocalDiceConfig,
    Toast
} from "./types";


export const toasts = writable<Toast[]>([]);

export const currentSides = writable<"d10" | "d20">("d10");
export const availableDiceSkins = writable<string[]>([]);
export const availableEffects = writable<string[]>([]);
export const diceConfig = writable<LocalDiceConfig>({
    customColors: false,
    palettes: [],
    playerSkins: [],

});
