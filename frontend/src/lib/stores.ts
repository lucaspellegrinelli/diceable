import { writable } from 'svelte/store';
import type { LocalDiceConfig } from './types';

export const loadingBlocker = writable<boolean>(false);

export const currentSides = writable<'d10' | 'd20'>('d10');
export const availableDiceSkins = writable<string[]>([]);
export const availableEffects = writable<string[]>([]);
export const diceConfig = writable<LocalDiceConfig>({
	customColors: false,
	palettes: [],
	playerSkins: []
});
