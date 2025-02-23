import os
from flask import Blueprint, request, jsonify
from elevenlabs.client import ElevenLabs

from elevenlabs import play
import hashlib

from core import Core
import re

CORE = Core()

api_bp = Blueprint('api', __name__)
cache = []

def parse_text(text):
    # Find and move chapter marker to beginning if present
    chapter_match = re.search(r'\[CHAPTER_[^\]]*\]', text)
    if chapter_match:
        chapter = chapter_match.group(0)
        text = re.sub(r'\[CHAPTER_[^\]]*\]', '', text)
        chapter = chapter.replace("_", " ").replace("[", "").replace("]", "")
        text = "**" + chapter + "**\n\n" + text.strip()

    # Remove decisions
    text = re.sub(r'\[DECISIONS_[^\]]*\]', '', text)

    return text

@api_bp.route('/get-image', methods=['POST'])
def get_image():
    global cache
    return jsonify({'imagePath': "https://media.istockphoto.com/id/627795510/photo/example.jpg?s=612x612&w=0&k=20&c=lpUf5rjPVd6Kl_M6heqC8sUncR4FLmtsRzeYdTr5X_I="}), 200

@api_bp.route('/start-story', methods=['POST'])
def start_story():
    global cache
    response = CORE.start_conversation()
    cache = response
    return jsonify({'text': parse_text(response[1]["content"])}), 200

@api_bp.route('/generate-story', methods=['POST'])
def generate_story():
    global cache
    data = request.json
    text = data.get('text')
    cache.append({"role": "user", "content": text})
    response = CORE.get_assistant_response(cache)
    cache.append(response) 
    return jsonify({'text': parse_text(response["content"])}), 200

@api_bp.route('/tts', methods=['POST'])
def generate_audio():
    data = request.json
    text = data.get('text')
    if not text:
        return jsonify({'error': 'Text is required'}), 400
    return jsonify({'error': 'Text is required'}), 200

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