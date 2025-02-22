# flask-backend-app/flask-backend-app/README.md

# Flask Backend App

This project is a Flask application that serves as a backend for generating stories and converting text to audio using the Mistral and ElevenLabs APIs.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/flask-backend-app.git
   ```
2. Navigate to the project directory:
   ```
   cd flask-backend-app
   ```
3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

To run the application, execute the following command:
```
python src/app.py
```
The application will start on `http://127.0.0.1:5000/`.

## API Endpoints

### Generate Story

- **Endpoint:** `/generate_story`
- **Method:** `POST`
- **Description:** Generates a story based on the input provided in the request body.
- **Request Body:**
  ```json
  {
    "input": "Your story prompt here"
  }
  ```
- **Response:**
  ```json
  {
    "story": "Generated story text here"
  }
  ```

### Generate Audio

- **Endpoint:** `/generate_audio`
- **Method:** `POST`
- **Description:** Converts the provided text to audio.
- **Request Body:**
  ```json
  {
    "text": "Text to convert to audio"
  }
  ```
- **Response:**
  ```json
  {
    "audio_url": "URL to the generated audio file"
  }
  ```

## License

This project is licensed under the MIT License.