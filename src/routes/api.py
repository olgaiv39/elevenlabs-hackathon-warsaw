import os
import hashlib
from flask import Blueprint, request, jsonify, Flask
from elevenlabs.client import ElevenLabs
from elevenlabs import play

from core import Core
from img_gen import ImgGen

CORE = Core()

# Retrieve FAL API key from environment variables.
fal_key = os.getenv('FAL_API_KEY')
if not fal_key:
    raise EnvironmentError("FAL_API_KEY is not set. Please check your .env file.")

# Instantiate the ImgGen class.
IMG_GEN = ImgGen(fal_key)

api_bp = Blueprint('api', __name__)

@api_bp.route('/start-story', methods=['POST'])
def start_story():
    response = CORE.start_conversation()
    return jsonify({'text': response[1]["content"]}), 200

@api_bp.route('/generate-story', methods=['POST'])
def generate_story():
    data = request.json
    text = data.get('text')
    response = CORE.get_assistant_response([{"role": "user", "content": text}])
    return jsonify({'text': response["content"]}), 200

@api_bp.route('/process-story', methods=['POST'])
def process_story():
    """
    Expects a JSON payload with a 'story' key containing the generated text.
    Evaluates the story for chapter ends and generates comic-style illustrations
    (2-3 images per chapter). Returns a dictionary mapping chapters to image URLs.
    """
    data = request.json
    story = data.get('story')
    if not story:
        return jsonify({'error': 'Story text is required'}), 400

    # Accept parameter 'n' to control the number of images per chapter (default is 3).
    n = data.get('n', 3)
    illustrations = IMG_GEN.process_story(story, images_per_chapter=n)
    return jsonify({'illustrations': illustrations}), 200

@api_bp.route('/tts', methods=['POST'])
def generate_audio():
    data = request.json
    text = data.get('text')
    if not text:
        return jsonify({'error': 'Text is required'}), 400

    # Generate a hash from the text to create a filename.
    text_hash = hashlib.md5(text.encode()).hexdigest()
    file_path = f"audio_{text_hash}.mp3"
    if os.path.exists(file_path):
        cached = True
        with open(file_path, 'rb') as audio_file:
            audio = audio_file.read()
    else:
        cached = False
        client = ElevenLabs()
        audio_iterator = client.text_to_speech.convert(
            text=text,
            voice_id="7fbQ7yJuEo56rYjrYaEh",
            model_id="eleven_multilingual_v2"
        )
        audio = b"".join(audio_iterator)
        with open(file_path, "wb") as audio_file:
            audio_file.write(audio)

    play(audio)
    return jsonify({'audio_file': file_path, 'cached': cached}), 200

def set_routes(app):
    app.register_blueprint(api_bp, url_prefix='/api')

# If this file is run directly, create a Flask app that also serves the temp_images folder.
if __name__ == '__main__':
    app = Flask(__name__, static_folder="temp_images", static_url_path="/temp_images")
    set_routes(app)
    app.run(debug=True)
