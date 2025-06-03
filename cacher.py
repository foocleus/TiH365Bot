import os
import json

CACHE_PATH = "./cache"


def deserializePageContent(date, language):
    path = f"{CACHE_PATH}/{language}"
    os.makedirs(path, exist_ok=True)
    if not os.path.exists(f"{path}/{date}.json"): return {}
    with open(f"{path}/{date}.json") as cacheFile:
        return json.load(cacheFile)

def serializePageContent(content, date, language):
    path = f"{CACHE_PATH}/{language}"
    os.makedirs(path, exist_ok=True)
    with open(f"{path}/{date}.json", "w", encoding="UTF-8") as cacheFile:
        json.dump(content, cacheFile, indent=4)
        