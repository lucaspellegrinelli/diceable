import requests


def get_dice_cdn_urls(cloudflare_account_id, cloudflare_assets_api_token):
    def _get_dice_url_from_id(id):
        return f"https://imagedelivery.net/qzTQhwVAd5ZPCy9exIQX3g/{id}/public"

    images_endpoint = f"https://api.cloudflare.com/client/v4/accounts/{cloudflare_account_id}/images/v2"
    headers = {
        "Authorization": f"Bearer {cloudflare_assets_api_token}",
        "Content-Type": "application/json",
    }

    dice_cdn: dict[str, dict[int, str]] = {}

    response = requests.get(images_endpoint, headers=headers)
    response_json = response.json()
    all_images = response_json["result"]["images"]

    for dice_info in all_images:
        dice_name = dice_info["filename"].split("-")[0]
        dice_number = int(dice_info["filename"].split("-")[1].split(".")[0])

        if dice_name not in dice_cdn:
            dice_cdn[dice_name] = {}

        dice_cdn[dice_name][dice_number] = _get_dice_url_from_id(dice_info["id"])

    return dice_cdn
