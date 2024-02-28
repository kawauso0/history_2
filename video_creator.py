import requests
from moviepy.editor import ImageClip, concatenate_videoclips
from io import BytesIO
from PIL import Image
import numpy as np
import openai
import time

def initialize_openai_api():
    openai.api_key = OPENAI_API_KEY

def generate_image(prompt):
    try:
        response = openai.Image.create(
            model="dall-e-2",
            prompt=prompt,
            n=1,
        )
        return response['data'][0]['url']
    except openai.error.RateLimitError as e:
        print(f"Rate limit exceeded: {e}")
        return None

def generate_image_with_retry(prompt, retries=5, delay=12):
    for attempt in range(retries):
        image_url = generate_image(prompt)
        if image_url:
            return image_url
        print(f"Waiting {delay} seconds to retry...")
        time.sleep(delay)
    raise Exception("Failed to generate image after several retries.")

def create_clip_from_url(url, duration):
    response = requests.get(url, stream=True)
    img = Image.open(BytesIO(response.content))
    clip = ImageClip(np.array(img)).set_duration(duration)
    return clip

def create_video_from_images(image_urls_with_durations, output_filename="output.mp4"):
    clips = [create_clip_from_url(url, duration) for url, duration in image_urls_with_durations if url is not None]
    if clips:
        final_clip = concatenate_videoclips(clips, method="compose")
        # videoフォルダにoutput.mp4を書き込む
        final_clip.write_videofile(f"./voicevox/video/{output_filename}", fps=24)  
    else:
        print("No valid images were found to create a video.")