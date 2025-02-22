import os
from flask import Blueprint, request, jsonify
from elevenlabs.client import ElevenLabs

from elevenlabs import play

api_bp = Blueprint('api', __name__)

@api_bp.route('/generate-story', methods=['POST'])
def generate_story():
    pass

@api_bp.route('/tts', methods=['POST'])
def generate_audio():
    data = request.json
    text = data.get('text')
    if not text:
        return jsonify({'error': 'Text is required'}), 400
    client = ElevenLabs()
    audio = client.text_to_speech.convert(
        text=text,
        voice_id="JBFqnCBsd6RMkjVDRZzb",
        model_id="eleven_multilingual_v2"
    )

    play(audio)
    # Save the audio bytes to a file
    file_path = "output.mp3"
    audio_bytes = b"".join(audio)

    with open(file_path, "wb") as audio_file:
        audio_file.write(audio_bytes)

    return jsonify({'audio_file': file_path}), 200

def set_routes(app):
    app.register_blueprint(api_bp, url_prefix='/api')