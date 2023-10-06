import os
import random
import uuid
from io import BytesIO
from typing import Literal

import requests
from PIL import Image

from .common import DICE_H, DICE_W, OUTPUT_H, OUTPUT_W, get_dice_positions

dice_cache = {}


def _dice_url(type: str, skin: str, number: int):
    return f"https://assets.togarashi.app/dice/{type}/{skin}/{number}.png"


def _load_dice_image(sides: Literal["d10"] | Literal["d20"], number: int, skin: str):
    if skin in dice_cache.get(number, {}):
        return dice_cache[number][skin]

    cdn_url = _dice_url(sides, skin, number)
    response = requests.get(cdn_url)

    img = Image.open(BytesIO(response.content))
    img = img.convert("RGBA")
    img = img.resize((DICE_W, DICE_H))

    dice_cache.setdefault(number, {})
    dice_cache[number][skin] = img

    return img


def _load_dice_palette(sides: Literal["d10"] | Literal["d20"], palette: list[str]):
    dice_images = []
    for i, skin in enumerate([palette[-1]] + palette[:-1]):
        dice_img = _load_dice_image(sides, i, skin)
        dice_images.append(dice_img)

    return dice_images


def _create_rolls_animation(
    sides: Literal["d10"] | Literal["d20"],
    rolls: list[int],
    palette: list[str],
    n_frames: int,
    size_multiplier: int = 0.5,
):
    colored_dice = _load_dice_palette(sides, palette)
    dice_positions = get_dice_positions(
        len(rolls), DICE_W, DICE_H, DICE_W, DICE_H, OUTPUT_W, OUTPUT_H, 0, 0
    )

    resized_colored_dice = []
    for dice in colored_dice:
        target_w = int(DICE_W * size_multiplier)
        target_h = int(DICE_H * size_multiplier)
        resized_dice = dice.resize((target_w, target_h))
        resized_colored_dice.append(resized_dice)

    frames = []
    for i in range(n_frames):
        is_last = i == n_frames - 1

        real_w = int(OUTPUT_W * size_multiplier)
        real_h = int(OUTPUT_H * size_multiplier)
        frame = Image.new("RGBA", (real_w, real_h), (0, 0, 0, 0))
        for (x, y), roll in zip(dice_positions, rolls):
            roll_i = roll % len(colored_dice)

            dice = resized_colored_dice[roll_i]
            if not is_last:
                dice = random.choice(resized_colored_dice)

            target_x = int(x * size_multiplier)
            target_y = int(y * size_multiplier)
            frame.paste(dice, (target_x, target_y), dice)

        frames.append(frame)

    return frames


def create_roll_gif(
    sides: Literal["d10"] | Literal["d20"],
    rolls: list[int],
    palette: list[str],
    n_frames: int,
    save_path: str,
):
    anim = _create_rolls_animation(sides, rolls, palette, n_frames)

    roll_id = str(uuid.uuid4())
    path = os.path.join(save_path, f"roll-{roll_id}.gif")
    os.makedirs(os.path.dirname(path), exist_ok=True)

    anim[0].save(
        path,
        append_images=anim[1:],
        save_all=True,
        duration=1,
        loop=1,
    )

    return path
