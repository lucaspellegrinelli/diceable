ORIGINAL_EFFECT_W = 2000
ORIGINAL_EFFECT_H = 2160

ORIGINAL_DICE_W = 550
ORIGINAL_DICE_H = 450

EFFECT_SIZE_SCALE = 0.66
DICE_SIZE_SCALE = 0.66

EFFECT_W = int(ORIGINAL_EFFECT_W * EFFECT_SIZE_SCALE)
EFFECT_H = int(ORIGINAL_EFFECT_H * EFFECT_SIZE_SCALE)

DICE_W = int(ORIGINAL_DICE_W * DICE_SIZE_SCALE)
DICE_H = int(ORIGINAL_DICE_H * DICE_SIZE_SCALE)

OUTPUT_W = 1920
OUTPUT_H = 1080


def get_dice_positions(
    n: int,
    dice_full_w: int,
    dice_full_h: int,
    dice_w: int,
    dice_h: int,
    container_w: int,
    container_h: int,
    border_w: int,
    border_h: int,
    max_cols: int = 4,
):
    positions = []

    total_rows = (n // max_cols) + (1 if n % max_cols != 0 else 0)
    image_w = max_cols * dice_w + border_w * (max_cols - 1)
    image_h = total_rows * dice_h + border_h * (total_rows - 1)

    for i in range(n):
        row = i // max_cols
        row_count = min(n - row * max_cols, max_cols)
        col = i % max_cols

        x = (
            container_w // 2
            - dice_full_w // 2
            + col * dice_w
            + col * border_w
            - image_w // 2
            + dice_w // 2
        )
        y = (
            container_h // 2
            - dice_full_h // 2
            + row * dice_h
            + row * border_h
            - image_h // 2
            + dice_h // 2
        )

        x += (max_cols - row_count) * (dice_w + border_w) // 2

        positions.append((x, y))

    return positions
