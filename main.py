from typing import Optional
import json
import sys

#import matplotlib.pyplot as plt
import pixivpy3 as pixiv

def get_max_bookmark_id(result: dict) -> Optional[int]:
    if not result.get("next_url"):
        return

    params = dict(param.split("=") for param in result["next_url"].split("?")[1].split("&"))
    value = params.get("max_bookmark_id", None)

    return value

MOST_COMMON_TAGS = ["R-18", "R-18G", "original"]

with open("credentials.json", "r", encoding="utf-8") as file:
    credentials = json.load(file)

api = pixiv.AppPixivAPI()
api.set_auth(credentials["access_token"], credentials["refresh_token"])

max_bookmark_id = None
count = {}

while True:
    result = api.user_bookmarks_illust(int(sys.argv[-1]), max_bookmark_id=max_bookmark_id)

    for illust in result.get("illusts", []):
        for tag in illust.get("tags", []):
            if not tag.get("translated_name"):
                name = tag["name"]
            else:
                name = tag["translated_name"]

            if name not in count:
                count[name] = 0

            count[name] += 1

    max_bookmark_id = get_max_bookmark_id(result)

    if max_bookmark_id is None:
        break

for tag in MOST_COMMON_TAGS:
    if tag in count:
        count.pop(tag)

count = dict(sorted(count.items(), key=lambda tag: tag[1], reverse=True))

with open("count.json", "w", encoding="utf-8") as file:
    json.dump(count, file, indent=4, ensure_ascii=False)