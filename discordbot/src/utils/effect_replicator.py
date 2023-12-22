import argparse
import os

import cv2
import numpy as np
from src.utils.common import get_dice_positions

SIZE_FACTOR = 0.7
EFFECT_WIDTH = int(round(2000 * SIZE_FACTOR))
EFFECT_HEIGHT = int(round(2160 * SIZE_FACTOR))
DICE_WIDTH = int(round(469 * SIZE_FACTOR))
DICE_HEIGHT = int(round(456 * SIZE_FACTOR))
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
MARGIN_X = 10
MARGIN_Y = 10

parser = argparse.ArgumentParser()
parser.add_argument("--effect_path", "-e", type=str, required=True)
parser.add_argument("--effect_name", "-n", type=str, required=True)
parser.add_argument("--output_dir", "-o", type=str, required=True)
args = parser.parse_args()


def _paste_image(background, image, x, y):
    # Calculate the region of interest
    x1 = max(0, x)
    y1 = max(0, y)
    x2 = min(background.shape[1], x + image.shape[1])
    y2 = min(background.shape[0], y + image.shape[0])

    # Calculate the offset for the image paste
    img_x1 = max(0, -x)
    img_y1 = max(0, -y)
    img_x2 = img_x1 + (x2 - x1)
    img_y2 = img_y1 + (y2 - y1)

    # Crop the image if necessary
    if img_x1 >= img_x2 or img_y1 >= img_y2:
        return background

    cropped_image = image[img_y1:img_y2, img_x1:img_x2, :]

    # Paste the cropped image onto the background
    background[y1:y2, x1:x2] = cropped_image
    return background


def create_effect_video(
    effect_video: cv2.VideoCapture,
    effect_name: str,
    n_dice: int,
    save_dir: str,
):
    output_path = os.path.join(save_dir, f"{effect_name}-{n_dice}.mp4")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    effect_fps = int(effect_video.get(cv2.CAP_PROP_FPS))
    fourcc = cv2.VideoWriter_fourcc(*"avc1")
    output = cv2.VideoWriter(
        output_path, fourcc, effect_fps, (SCREEN_WIDTH, SCREEN_HEIGHT)
    )

    dice_positions = get_dice_positions(
        n_dice,
        EFFECT_WIDTH,
        EFFECT_HEIGHT,
        DICE_WIDTH,
        DICE_HEIGHT,
        SCREEN_WIDTH,
        SCREEN_HEIGHT,
        MARGIN_X,
        MARGIN_Y,
    )

    while effect_video.isOpened():
        ret, effect_frame = effect_video.read()

        if ret:
            out_frame = np.zeros((SCREEN_HEIGHT, SCREEN_WIDTH, 3), np.uint8)
            effect_frame = cv2.resize(
                effect_frame, (EFFECT_WIDTH, EFFECT_HEIGHT))
            effect_frame = cv2.cvtColor(effect_frame, cv2.COLOR_BGR2RGB)

            for x, y in dice_positions:
                background = np.zeros(
                    (SCREEN_HEIGHT, SCREEN_WIDTH, 3), np.uint8)
                resized_effect = _paste_image(background, effect_frame, x, y)
                out_frame = cv2.addWeighted(out_frame, 1, resized_effect, 1, 0)

            out_frame = cv2.cvtColor(out_frame, cv2.COLOR_RGB2BGR)

            output.write(out_frame)
        else:
            break

    output.write(np.zeros((SCREEN_HEIGHT, SCREEN_WIDTH, 3), np.uint8))

    effect_video.release()
    output.release()

    return output_path


if __name__ == "__main__":
    for n_dice in range(1, 13):
        effect_video = cv2.VideoCapture(args.effect_path)
        path = create_effect_video(
            effect_video, args.effect_name, n_dice, args.output_dir
        )
        print(path)
