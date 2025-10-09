import os
import tempfile
import subprocess
import logging
from datetime import datetime
from flask import Flask, request, jsonify, render_template
from werkzeug.utils import secure_filename
from sarvamai import SarvamAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Configuration
SARVAM_API_KEY = os.getenv('SARVAM_API_KEY')
SECRET_PIN = os.getenv('SECRET_PIN', '1234')
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'wav', 'mp3', 'm4a', 'webm'}

# Ensure upload directory exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def convert_to_wav(input_path, output_path):
    """Convert audio file to WAV format using ffmpeg"""
    try:
        # Check if ffmpeg is available
        ffmpeg_check = subprocess.run(['which', 'ffmpeg'], capture_output=True, text=True)
        if ffmpeg_check.returncode != 0:
            logger.warning("FFmpeg not found, trying to use original file")
            # If ffmpeg is not available, try to use the original file if it's already WAV
            if input_path.lower().endswith('.wav'):
                import shutil
                shutil.copy2(input_path, output_path)
                return True
            else:
                logger.error("FFmpeg not available and file is not WAV format")
                return False
        
        cmd = [
            'ffmpeg', '-i', input_path, 
            '-acodec', 'pcm_s16le', 
            '-ar', '16000', 
            '-ac', '1', 
            '-y', output_path
        ]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            logger.error(f"FFmpeg error: {result.stderr}")
            return False
        return True
    except Exception as e:
        logger.error(f"Error converting audio: {e}")
        return False

def split_audio_ffmpeg(audio_path, chunk_duration=29, output_dir="chunks"):
    """Split long audio into chunks using ffmpeg"""
    try:
        # Check if ffmpeg is available
        ffmpeg_check = subprocess.run(['which', 'ffmpeg'], capture_output=True, text=True)
        if ffmpeg_check.returncode != 0:
            logger.warning("FFmpeg not found, cannot split long audio files")
            return []
        
        os.makedirs(output_dir, exist_ok=True)
        base_name = os.path.splitext(os.path.basename(audio_path))[0]
        output_pattern = os.path.join(output_dir, f"{base_name}_%03d.wav")
        
        command = [
            "ffmpeg", "-i", audio_path,
            "-f", "segment",
            "-segment_time", str(chunk_duration),
            "-c:a", "pcm_s16le",
            "-ar", "16000",
            "-ac", "1",
            output_pattern
        ]
        
        result = subprocess.run(command, capture_output=True, text=True)
        if result.returncode != 0:
            logger.error(f"FFmpeg split error: {result.stderr}")
            return []
        
        # Get generated chunk files
        chunk_files = []
        for file in os.listdir(output_dir):
            if file.startswith(base_name) and file.endswith('.wav'):
                chunk_files.append(os.path.join(output_dir, file))
        
        return sorted(chunk_files)
    except Exception as e:
        logger.error(f"Error splitting audio: {e}")
        return []

def transcribe_audio_chunks(chunk_paths, client):
    """Transcribe audio chunks and combine results"""
    full_transcript = []
    
    for idx, chunk_path in enumerate(chunk_paths):
        logger.info(f"Transcribing chunk {idx + 1}/{len(chunk_paths)}: {chunk_path}")
        try:
            with open(chunk_path, "rb") as audio_file:
                response = client.speech_to_text.transcribe(
                    file=audio_file,
                    model="saarika:v2.5",
                    language_code="te-IN"
                )
                # Extract only the transcript text from the response
                if hasattr(response, 'transcript'):
                    full_transcript.append(response.transcript)
                else:
                    full_transcript.append(str(response))
        except Exception as e:
            logger.error(f"Error transcribing chunk {chunk_path}: {e}")
            full_transcript.append(f"[Error in chunk {idx + 1}]")
    
    return " ".join(full_transcript).strip()

def get_audio_duration(file_path):
    """Get audio duration using ffprobe"""
    try:
        # Check if ffprobe is available
        ffprobe_check = subprocess.run(['which', 'ffprobe'], capture_output=True, text=True)
        if ffprobe_check.returncode != 0:
            logger.warning("FFprobe not found, assuming short audio")
            return 25  # Assume short audio if ffprobe not available
        
        cmd = [
            'ffprobe', '-v', 'quiet', '-show_entries', 
            'format=duration', '-of', 'csv=p=0', file_path
        ]
        result = subprocess.run(cmd, capture_output=True, text=True)
        return float(result.stdout.strip())
    except:
        return 25  # Default to short audio

@app.route('/')
def index():
    """Serve the main page"""
    return render_template('index.html')

@app.route('/transcribe', methods=['POST'])
def transcribe():
    """Handle audio transcription requests"""
    try:
        # Check PIN
        pin = request.form.get('pin')
        if pin != SECRET_PIN:
            return jsonify({'error': 'Invalid PIN'}), 401
        
        # Check if file is present
        if 'audio' not in request.files:
            return jsonify({'error': 'No audio file provided'}), 400
        
        file = request.files['audio']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': 'Invalid file type. Please use WAV, MP3, M4A, or WEBM'}), 400
        
        # Save uploaded file
        filename = secure_filename(file.filename)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{timestamp}_{filename}"
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(file_path)
        
        logger.info(f"Processing file: {filename}")
        
        # Convert to WAV if needed
        wav_path = file_path
        if not file_path.lower().endswith('.wav'):
            wav_path = file_path.rsplit('.', 1)[0] + '.wav'
            if not convert_to_wav(file_path, wav_path):
                # If conversion fails, try to use the original file for short audio
                logger.warning("Audio conversion failed, trying original file")
                wav_path = file_path
        
        # Check audio duration
        duration = get_audio_duration(wav_path)
        logger.info(f"Audio duration: {duration} seconds")
        
        # Initialize Sarvam client
        if not SARVAM_API_KEY:
            return jsonify({'error': 'Sarvam API key not configured'}), 500
        
        client = SarvamAI(api_subscription_key=SARVAM_API_KEY)
        
        # Handle long audio by splitting into chunks
        if duration > 30:
            logger.info("Audio longer than 30 seconds, splitting into chunks")
            chunks = split_audio_ffmpeg(wav_path)
            if not chunks:
                # If splitting fails, try direct transcription anyway
                logger.warning("Audio splitting failed, trying direct transcription")
                with open(wav_path, "rb") as audio_file:
                    response = client.speech_to_text.transcribe(
                        file=audio_file,
                        model="saarika:v2.5",
                        language_code="te-IN"
                    )
                    # Extract only the transcript text from the response
                    if hasattr(response, 'transcript'):
                        transcript = response.transcript
                    else:
                        transcript = str(response)
            else:
                transcript = transcribe_audio_chunks(chunks, client)
                
                # Clean up chunk files
                for chunk in chunks:
                    try:
                        os.remove(chunk)
                    except:
                        pass
        else:
            # Direct transcription for short audio
            with open(wav_path, "rb") as audio_file:
                response = client.speech_to_text.transcribe(
                    file=audio_file,
                    model="saarika:v2.5",
                    language_code="te-IN"
                )
                # Extract only the transcript text from the response
                if hasattr(response, 'transcript'):
                    transcript = response.transcript
                else:
                    transcript = str(response)
        
        # Clean up temporary files
        try:
            os.remove(file_path)
            if wav_path != file_path:
                os.remove(wav_path)
        except:
            pass
        
        # Log successful transcription
        logger.info(f"Transcription completed. Length: {len(transcript)} characters")
        
        return jsonify({
            'transcript': transcript,
            'success': True
        })
        
    except Exception as e:
        logger.error(f"Transcription error: {e}")
        return jsonify({'error': f'Transcription failed: {str(e)}'}), 500

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({'status': 'healthy'})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
