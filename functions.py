import os
from tiktok_downloader import tikmate, snaptik
import random
import string
import instaloader


def generate_random_string(length):
    return "".join(random.choice(string.ascii_lowercase) for i in range(length))


def download_instagram_media(url):
    loader = instaloader.Instaloader()

    try:
        # Download media
        video_name = generate_random_string(16) + ".mp4"
        video_path = "downloads/" + video_name
        loader.download_post(url, target=video_path)
        return video_path
    except Exception as e:
        print("Error:", e)
        return None


def download_tiktok(url):
    if not os.path.exists("downloads"):
        os.makedirs("downloads")

    try:
        d = snaptik(url)
        video_name = generate_random_string(16) + ".mp4"
        video_path = "downloads/" + video_name
        d[0].download(video_path)
        return video_path

    except Exception as e:
        print(f"Error downloading video: {e}")
        return None

