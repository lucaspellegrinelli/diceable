import argparse
import os
import time

import requests
from dotenv import dotenv_values

parser = argparse.ArgumentParser()
parser.add_argument("--scope", "-s", type=str, required=True)
parser.add_argument("--name", "-n", type=str, required=True)
parser.add_argument("--remove", "-r", action="store_true")
parser.add_argument("--adddir", "-a", type=str, required=False)


def remove_dice_skin(
    skin: str, cloudflare_account_id: str, cloudflare_assets_api_token: str
):
    images_endpoint = f"https://api.cloudflare.com/client/v4/accounts/{cloudflare_account_id}/images/v2"
    headers = {
        "Authorization": f"Bearer {cloudflare_assets_api_token}",
        "Content-Type": "application/json",
    }

    response = requests.get(images_endpoint, headers=headers)
    response_json = response.json()
    all_images = response_json["result"]["images"]

    ids_to_remove = set()
    for dice_info in all_images:
        dice_name = dice_info["filename"].split("-")[0]
        if dice_name == skin:
            ids_to_remove.add(dice_info["id"])

    delete_images_endpoint = f"https://api.cloudflare.com/client/v4/accounts/{cloudflare_account_id}/images/v1"
    for image_id in ids_to_remove:
        response = requests.delete(
            os.path.join(delete_images_endpoint, image_id), headers=headers
        )
        if response.status_code == 200:
            print(f"Successfully deleted image {image_id}")
        else:
            print(f"Failed to delete image {image_id}")


def remove_effect(
    effect: str, cloudflare_account_id: str, cloudflare_assets_api_token: str
):
    videos_endpoint = (
        f"https://api.cloudflare.com/client/v4/accounts/{cloudflare_account_id}/stream"
    )
    headers = {
        "Authorization": f"Bearer {cloudflare_assets_api_token}",
        "Content-Type": "application/json",
    }

    response = requests.get(videos_endpoint, headers=headers)
    response_json = response.json()
    all_effects = response_json["result"]

    ids_to_remove = set()
    for effect_info in all_effects:
        effect_name = effect_info["meta"]["name"].split("-")[0]
        if effect_name == effect:
            ids_to_remove.add(effect_info["uid"])

    delete_videos_endpoint = (
        f"https://api.cloudflare.com/client/v4/accounts/{cloudflare_account_id}/stream"
    )
    for video_id in ids_to_remove:
        response = requests.delete(
            os.path.join(delete_videos_endpoint, video_id), headers=headers
        )
        if response.status_code == 200:
            print(f"Successfully deleted video {video_id}")
        else:
            print(f"Failed to delete video {video_id}")


def upload_dice_skin(
    dir: str, cloudflare_account_id: str, cloudflare_assets_api_token: str
):
    images_endpoint = f"https://api.cloudflare.com/client/v4/accounts/{cloudflare_account_id}/images/v1"
    headers = {
        "Authorization": f"Bearer {cloudflare_assets_api_token}",
    }

    for file in os.listdir(dir):
        if not file.endswith(".png"):
            continue

        print(f"Uploading {file}")
        response = requests.post(
            images_endpoint,
            headers=headers,
            files={"file": open(os.path.join(dir, file), "rb")},
        )
        if response.status_code == 200:
            print(f"Successfully uploaded {file}")
        else:
            print(f"Failed to upload {file} with status code {response.status_code}")
            print(response.json())


def upload_effect(
    dir: str, cloudflare_account_id: str, cloudflare_assets_api_token: str
):
    stream_endpoint = (
        f"https://api.cloudflare.com/client/v4/accounts/{cloudflare_account_id}/stream"
    )
    headers = {
        "Authorization": f"Bearer {cloudflare_assets_api_token}",
    }

    stream_ids = []
    for file in os.listdir(dir):
        if not file.endswith(".mp4"):
            continue

        response = requests.post(
            stream_endpoint,
            headers=headers,
            files={"file": open(os.path.join(dir, file), "rb")},
        )

        if response.status_code == 200:
            print(f"Successfully uploaded {file}")
        else:
            print(f"Failed to upload {file}")
            print(response.json())
            continue

        video_id = response.json()["result"]["uid"]
        stream_ids.append((video_id, file))

    time.sleep(60)

    for video_id, video_name in stream_ids:
        response = requests.post(
            os.path.join(stream_endpoint, video_id, "downloads"),
            headers=headers,
        )

        if response.status_code == 200:
            print(f"Successfully created download for {video_name}")
        else:
            print(f"Failed to create download for {video_name}")
            print(response.json())


if __name__ == "__main__":
    args = parser.parse_args()

    env_vars = dotenv_values("discordbot/.env")
    cloudflare_account_id = env_vars.get("CLOUDFLARE_ACCOUNT_ID") or ""
    cloudflare_assets_api_token = env_vars.get("CLOUDFLARE_ASSETS_API_TOKEN") or ""

    if args.remove:
        if args.scope == "dice":
            remove_dice_skin(
                args.name, cloudflare_account_id, cloudflare_assets_api_token
            )
        elif args.scope == "effect":
            remove_effect(args.name, cloudflare_account_id, cloudflare_assets_api_token)

    if args.adddir:
        if args.scope == "dice":
            upload_dice_skin(
                args.adddir, cloudflare_account_id, cloudflare_assets_api_token
            )
        elif args.scope == "effect":
            upload_effect(
                args.adddir, cloudflare_account_id, cloudflare_assets_api_token
            )
