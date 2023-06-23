export const capitalize = (str: string | undefined) => {
    return str?.replace(/^\w/, (c) => c.toUpperCase());
};
