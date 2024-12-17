import os
import uuid
import json
from flask import Flask, render_template, request, jsonify
import requests
from cerebras.cloud.sdk import Cerebras
from elevenlabs import ElevenLabs, Voice, VoiceSettings
from config import PERSONALIZED_COMPANION_PROMPT
from pydub import AudioSegment
from flask_mail import Mail, Message
from dotenv import load_dotenv

# Load environment variables
load_dotenv(dotenv_path='../.env')

# Initialize Flask app
app = Flask(__name__, static_url_path='/static', static_folder='static')

# Email configuration
app.config['MAIL_SERVER'] = os.getenv("MAIL_SERVER")
app.config['MAIL_PORT'] = int(os.getenv("MAIL_PORT"))
app.config['MAIL_USERNAME'] = os.getenv("MAIL_USERNAME")
app.config['MAIL_PASSWORD'] = os.getenv("MAIL_PASSWORD")
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
mail = Mail(app)

# Initialize clients
cerebras_client = Cerebras(api_key=os.getenv("CEREBRAS_API_KEY"))
elevenlabs_client = ElevenLabs(api_key=os.getenv("ELEVEN_LABS_API_KEY"))
deepgram_api_key = os.getenv("DEEPGRAM_API_KEY")

# Conversation history and user audio file storage
conversation_history = [{"role": "system", "content": PERSONALIZED_COMPANION_PROMPT}]
user_audio_files = []

# Landing page
@app.route('/')
def index():
    return render_template('index.html')

# Conversation page
@app.route('/conversation', methods=['GET'])
def conversation_page():
    return render_template('conversation.html')

# API to handle audio input, AI response, and voice generation
@app.route('/api/message', methods=['POST'])
def handle_message():
    try:
        # Save user audio
        audio_file = request.files['audio']
        audio_filename = f"user_input_{uuid.uuid4().hex}.wav"
        audio_path = os.path.join("static", "audio", audio_filename)
        audio_file.save(audio_path)
        user_audio_files.append(audio_path)

        # Transcribe audio using Deepgram
        user_message = transcribe_audio(audio_path)
        if not user_message:
            return jsonify({"error": "Failed to transcribe audio."}), 400

        # Append user message to conversation history
        conversation_history.append({"role": "user", "content": user_message})

        # Get AI response from Cerebras
        ai_response = get_cerebras_response(conversation_history)
        if not ai_response:
            return jsonify({"error": "Failed to generate AI response."}), 500

        conversation_history.append({"role": "assistant", "content": ai_response})

        # Generate AI voice response
        audio_url = generate_ai_voice(ai_response)

        return jsonify({
            "user_message": user_message,
            "ai_response": ai_response,
            "audio_url": audio_url
        })
    except Exception as e:
        print(f"Error in /api/message: {e}")
        return jsonify({"error": "An unexpected error occurred."}), 500

def transcribe_audio(audio_path):
    """Transcribe user audio using Deepgram."""
    try:
        url = "https://api.deepgram.com/v1/listen"
        headers = {"Authorization": f"Token {deepgram_api_key}", "Content-Type": "audio/wav"}
        with open(audio_path, "rb") as audio_file:
            response = requests.post(url, headers=headers, data=audio_file)
        return response.json()['results']['channels'][0]['alternatives'][0]['transcript']
    except Exception as e:
        print(f"Error transcribing audio: {e}")
        return None

def get_cerebras_response(history):
    """Fetch AI response from Cerebras."""
    try:
        response = cerebras_client.chat.completions.create(messages=history, model="llama3.1-8b")
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error fetching Cerebras response: {e}")
        return None

def generate_ai_voice(text):
    """Generate AI voice response."""
    try:
        voice_settings = VoiceSettings(stability=0.8, similarity_boost=0.9, style=0.2, use_speaker_boost=True)
        audio_generator = elevenlabs_client.generate(
            text=text, voice=Voice(voice_id=os.getenv("ELEVENLABS_VOICE_ID"), settings=voice_settings)
        )
        filename = f"ai_response_{uuid.uuid4().hex}.mp3"
        audio_path = os.path.join("static", "audio", filename)
        with open(audio_path, "wb") as audio_file:
            for chunk in audio_generator:
                if isinstance(chunk, bytes):
                    audio_file.write(chunk)
        return f"/static/audio/{filename}"
    except Exception as e:
        print(f"Error generating AI voice: {e}")
        return None

@app.route('/api/end-chat', methods=['POST'])
def end_chat():
    """End chat, stitch user audio, generate transcript, and send via email."""
    try:
        send_transcript = request.form.get('send_transcript') == 'true'
        if send_transcript:
            stitched_audio = stitch_user_audio(user_audio_files)
            transcript = generate_transcript(conversation_history)
            send_email_with_attachment(transcript, stitched_audio)

        cleanup_files(user_audio_files)
        conversation_history.clear()
        conversation_history.append({"role": "system", "content": PERSONALIZED_COMPANION_PROMPT})
        return '', 204
    except Exception as e:
        print(f"Error ending chat: {e}")
        return jsonify({"error": "Failed to end chat."}), 500

def stitch_user_audio(audio_files):
    """Stitch user audio files into a single MP3."""
    combined = AudioSegment.empty()
    for file in audio_files:
        combined += AudioSegment.from_file(file)
    stitched_path = os.path.join("static", "audio", "user_combined.mp3")
    combined.export(stitched_path, format="mp3")
    return stitched_path

def generate_transcript(history):
    """Generate transcript from conversation history."""
    return "\n".join(f"{entry['role'].capitalize()}: {entry['content']}" for entry in history)

def send_email_with_attachment(transcript, audio_path):
    """Send email with transcript and audio file attachment."""
    msg = Message("AlwaysHere: Conversation Summary", sender=os.getenv("MAIL_USERNAME"), recipients=[os.getenv("MAIL_USERNAME")])
    msg.body = transcript
    with open(audio_path, "rb") as audio_file:
        msg.attach("user_combined.mp3", "audio/mpeg", audio_file.read())
    mail.send(msg)

def cleanup_files(files):
    """Clean up temporary audio files."""
    for file in files:
        if os.path.exists(file):
            os.remove(file)

if __name__ == '__main__':
    app.run(debug=True)
