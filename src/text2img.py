import os
from dotenv import load_dotenv
import fal_client

load_dotenv()


fal_key = os.getenv('FAL_API_KEY')
if not fal_key:
    raise EnvironmentError("FAL_KEY is not set. Please check your .env file and ensure it contains 'FAL_KEY=your_api_key_here'.")

def on_queue_update(update):
    if isinstance(update, fal_client.InProgress):
        for log in update.logs:
            print(log["message"])

# Use fal_client with the loaded API key
result = fal_client.subscribe(
    "fal-ai/flux/dev",
    arguments={
        "prompt": "Extreme close-up of a single tiger eye, direct frontal view. Detailed iris and pupil. Sharp focus on eye texture and color. Natural lighting to capture authentic eye shine and depth. The word \"FLUX\" is painted over it in big, white brush strokes with visible texture."
    },
    with_logs=True,
    on_queue_update=on_queue_update,
)

print(result)