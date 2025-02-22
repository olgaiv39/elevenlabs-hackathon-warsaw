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
    print(1)
    data = request.json
    text = data.get('text')
    if not text:
        return jsonify({'error': 'Text is required'}), 400
    client = ElevenLabs()
    audio = client.text_to_speech.convert(
        text="The first move is what sets everything in motion.",
        voice_id="JBFqnCBsd6RMkjVDRZzb",
        model_id="eleven_multilingual_v2",
        output_format="mp3_44100_128",
    )

    play(audio)
    return jsonify({'audio_url': audio_url}), 200

def set_routes(app):
    app.register_blueprint(api_bp, url_prefix='/api')