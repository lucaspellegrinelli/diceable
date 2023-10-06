const getDiceUrl = (type: string, skin: string, number: number) =>
    `https://assets.togarashi.app/dice/${type}/${skin}/${number}.png`;

const getEffectUrl = (type: string, skin: string, number: number) =>
    `https://assets.togarashi.app/effects/${type}/${skin}/${number}.mp4`;

export async function GET({ url }) {
    const numberDice: number = parseInt(url.searchParams.get('number'));
    const palette: { name: string; number: number }[] = JSON.parse(url.searchParams.get('palette'));
    const effect: string = url.searchParams.get('effect');
    const diceSides: string = url.searchParams.get('sides');

    const ids: {
        dice: Record<number, string>;
        effect: string;
    } = { dice: {}, effect: '' };

    for (const paletteItem of palette) {
        ids.dice[paletteItem.number] = getDiceUrl(diceSides, paletteItem.name, paletteItem.number);
    }

    if (effect) {
        ids.effect = getEffectUrl(diceSides, effect, numberDice);
    }

    return new Response(JSON.stringify(ids));
}
