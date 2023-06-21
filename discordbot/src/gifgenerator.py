import os
import random
import uuid
from io import BytesIO

import requests
from PIL import Image

from .common import DICE_H, DICE_W, OUTPUT_H, OUTPUT_W, get_dice_positions

dice_cache = {}


def _dice_url(type: str, skin: str, number: int):
    return f"https://assets.togarashi.app/dice/{type}/{skin}/{number}.png"


def _load_dice_image(number: int, skin: str):
    # cdn_url = dice_cdn_urls[skin][number]
    cdn_url = _dice_url("d10", skin, number)
    response = requests.get(cdn_url)

    img = Image.open(BytesIO(response.content))
    img = img.convert("RGBA")
    img = img.resize((DICE_W, DICE_H), Image.ANTIALIAS)

    if number not in dice_cache:
        dice_cache[number] = {}
        dice_cache[number][skin] = img

    return img


def _load_dice_palette(palette: list[str]):
    dice_images = []
    for i, skin in enumerate(palette):
        dice_img = _load_dice_image(i, skin)
        dice_images.append(dice_img)

    return dice_images


def _create_rolls_animation(
    rolls: list[int],
    palette: list[str],
    n_frames: int,
):
    colored_dice = _load_dice_palette(palette)
    dice_positions = get_dice_positions(
        len(rolls), DICE_W, DICE_H, DICE_W, DICE_H, OUTPUT_W, OUTPUT_H, 0, 0
    )

    frames = []
    for i in range(n_frames):
        is_last = i == n_frames - 1
        frame = Image.new("RGBA", (OUTPUT_W, OUTPUT_H), (0, 0, 0, 0))
        for (x, y), roll in zip(dice_positions, rolls):
            roll_i = roll % len(colored_dice)
            dice = colored_dice[roll_i] if is_last else random.choice(colored_dice)
            frame.paste(dice, (x, y), dice)

        frames.append(frame)

    return frames


def create_roll_gif(
    rolls: list[int],
    palette: list[str],
    n_frames: int,
    save_path: str,
):
    anim = _create_rolls_animation(rolls, palette, n_frames)

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
