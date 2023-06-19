import { writable } from "svelte/store";
import type { Toast } from "./types";


export const toasts = writable<Toast[]>([]);
