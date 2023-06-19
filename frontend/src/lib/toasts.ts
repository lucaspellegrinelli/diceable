import { toasts } from "./stores";
import type { Toast } from "./types";

export const addToast = (message: string, type: 'success' | 'error') => {
    const createdAt: number = new Date().getTime();
    const toast: Toast = { message, type, createdAt };
    toasts.update((t) => [...t, toast]);
    setTimeout(() => removeToast(toast), 10000);
};

export const removeToast = (toast: Toast) => {
    toasts.update((t) => t.filter((t) => t.createdAt !== toast.createdAt));
}
