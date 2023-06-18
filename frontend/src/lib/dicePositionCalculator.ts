export const getDicePositions = (
    n: number,
    diceFullW: number,
    diceFullH: number,
    diceW: number,
    diceH: number,
    containerW: number,
    containerH: number,
    borderW: number,
    borderH: number,
    maxCols: number = 4
): Array<[number, number]> => {
    const positions: Array<[number, number]> = [];

    const totalRows = Math.floor(n / maxCols) + (n % maxCols !== 0 ? 1 : 0);
    const imageW = maxCols * diceW + borderW * (maxCols - 1);
    const imageH = totalRows * diceH + borderH * (totalRows - 1);

    for (let i = 0; i < n; i++) {
        const row = Math.floor(i / maxCols);
        const rowCount = Math.min(n - row * maxCols, maxCols);
        const col = i % maxCols;

        let x = containerW / 2 - diceFullW / 2 + col * diceW + col * borderW - imageW / 2 + diceW / 2;
        let y = containerH / 2 - diceFullH / 2 + row * diceH + row * borderH - imageH / 2 + diceH / 2;

        x += ((maxCols - rowCount) * (diceW + borderW)) / 2;

        positions.push([x, y]);
    }

    return positions;
};
