import os
from flask import Blueprint, request, jsonify
from elevenlabs.client import ElevenLabs

from elevenlabs import play
import hashlib

from core import Core

CORE = Core()

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

@api_bp.route('/tts', methods=['POST'])
def generate_audio():
    data = request.json
    text = data.get('text')
    if not text:
        return jsonify({'error': 'Text is required'}), 400

    # Generate hash from text
    text_hash = hashlib.md5(text.encode()).hexdigest()
    file_path = f"audio_{text_hash}.mp3"
    # Check if file already exists
    if os.path.exists(file_path):
        cached = True
        with open(file_path, 'rb') as audio_file:
            audio = audio_file.read()
    else:
        cached = False
        # Generate new audio if file doesn't exist
        client = ElevenLabs()
        audio_iterator = client.text_to_speech.convert(
            text=text,
            voice_id="7fbQ7yJuEo56rYjrYaEh",
            model_id="eleven_multilingual_v2"
        )
        # Save the audio bytes to a file
        audio = b"".join(audio_iterator)

        with open(file_path, "wb") as audio_file:
            audio_file.write(audio)

    play(audio)

    return jsonify({'audio_file': file_path, 'cached': cached}), 200

def set_routes(app):
    app.register_blueprint(api_bp, url_prefix='/api')