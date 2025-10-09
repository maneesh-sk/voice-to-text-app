# 🎤 Voice to Text - Telugu Speech Recognition

A simple, mobile-friendly web application that converts Telugu speech to text using Sarvam AI's STT API. Perfect for elderly users with large buttons and clear Telugu interface.

## 🌟 Features

- **🎤 Voice Recording**: Record audio directly in the browser
- **📁 File Upload**: Upload WAV, MP3, M4A, or WEBM files
- **🔐 PIN Protection**: Simple PIN-based security
- **📱 Mobile Friendly**: Responsive design for all devices
- **🌐 Telugu Support**: Full Telugu language interface
- **⚡ Fast Processing**: Optimized for quick transcription
- **💾 Save Results**: Download transcripts as TXT files

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- Docker (for containerized deployment)
- Sarvam AI API key

### 1. Get Your Sarvam AI API Key

1. Visit [Sarvam AI Dashboard](https://sarvam.ai)
2. Sign up for an account
3. Get your API subscription key

### 2. Local Development

```bash
# Clone the repository
git clone <your-repo-url>
cd Speech-to-text

# Copy environment file
cp env.example .env

# Edit .env file with your API key and PIN
nano .env
```

Edit the `.env` file:
```env
SARVAM_API_KEY=your_actual_api_key_here
SECRET_PIN=1234
```

```bash
# Install dependencies
pip install -r requirements.txt

# Run the application
python app.py
```

Visit `http://localhost:8080` in your browser.

### 3. Docker Deployment

```bash
# Build and run with Docker Compose
docker-compose up --build

# Or run with Docker directly
docker build -t voice-to-text .
docker run -p 8080:8080 -e SARVAM_API_KEY=your_key -e SECRET_PIN=1234 voice-to-text
```

## 🌐 Deploy to Render

### Step 1: Prepare Your Repository

1. Push your code to GitHub
2. Make sure all files are committed

### Step 2: Deploy on Render

1. **Go to [Render Dashboard](https://dashboard.render.com)**
2. **Click "New +" → "Web Service"**
3. **Connect your GitHub repository**
4. **Configure the service:**

   - **Name**: `voice-to-text` (or your preferred name)
   - **Environment**: `Docker`
   - **Dockerfile Path**: `Dockerfile`
   - **Port**: `8080`

5. **Add Environment Variables:**
   - `SARVAM_API_KEY`: Your Sarvam AI API key
   - `SECRET_PIN`: Your chosen PIN (e.g., `1234`)

6. **Click "Create Web Service"**

### Step 3: Access Your App

- Render will provide a URL like `https://your-app-name.onrender.com`
- Your app will be live and accessible worldwide!

## 🛠️ Configuration

### Environment Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `SARVAM_API_KEY` | Your Sarvam AI API key | `sk-...` |
| `SECRET_PIN` | PIN for app access | `1234` |

### Supported Audio Formats

- **Recording**: WebM (browser default)
- **Upload**: WAV, MP3, M4A, WEBM
- **Processing**: Automatically converted to WAV

### Audio Length Handling

- **Short audio (< 30s)**: Direct transcription
- **Long audio (> 30s)**: Automatically split into 29-second chunks
- **Result**: Seamlessly combined transcript

## 📱 Usage Guide

### For Users (Telugu + English)

1. **Enter PIN**: Type your 4-digit PIN
2. **Record Audio**: 
   - Click "🎤 రికార్డ్ / Record"
   - Speak clearly into microphone
   - Click "⏹️ స్టాప్ / Stop" when done
3. **Or Upload File**:
   - Click "📁 ఆడియో ఫైల్ అప్‌లోడ్ / Upload Audio"
   - Select your audio file
4. **Transcribe**: Click "📝 ట్రాన్‌స్క్రిప్ట్ / Transcribe"
5. **Save**: Click "💾 సేవ్ / Save as TXT" to download

### Tips for Best Results

- **Speak clearly** and at normal pace
- **Use good microphone** for recording
- **Minimize background noise**
- **Speak in Telugu** for best accuracy

## 🔧 Technical Details

### Architecture

- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **Backend**: Python Flask
- **AI Service**: Sarvam AI STT API
- **Audio Processing**: FFmpeg
- **Deployment**: Docker + Render

### API Endpoints

- `GET /` - Main application page
- `POST /transcribe` - Audio transcription
- `GET /health` - Health check

### Security Features

- PIN-based access control
- Server-side API key storage
- Input validation and sanitization
- Error handling and logging

## 🐛 Troubleshooting

### Common Issues

**"Invalid PIN" Error**
- Check your PIN in the `.env` file
- Ensure PIN matches what you're entering

**"No audio to transcribe" Error**
- Make sure you've recorded or uploaded audio
- Check browser microphone permissions

**"Network error"**
- Check your internet connection
- Verify Sarvam AI API key is correct

**"Failed to convert audio"**
- Try uploading a different audio format
- Ensure file is not corrupted

### Browser Compatibility

- **Chrome**: Full support
- **Firefox**: Full support  
- **Safari**: Full support
- **Edge**: Full support
- **Mobile browsers**: Full support

## 📊 Performance

- **Response Time**: 2-5 seconds for short audio
- **File Size Limit**: No hard limit (handled by chunks)
- **Concurrent Users**: Supports multiple users
- **Uptime**: 99.9% with Render hosting

## 🔒 Privacy & Security

- **No data storage**: Audio files are processed and deleted
- **Secure transmission**: HTTPS encryption
- **PIN protection**: Prevents unauthorized access
- **No tracking**: No user analytics or tracking

## 📞 Support

### Getting Help

1. **Check this README** for common solutions
2. **Verify your API key** is correct and active
3. **Test with short audio** first
4. **Check browser console** for JavaScript errors

### API Key Issues

- Ensure your Sarvam AI account is active
- Check API key has sufficient quota
- Verify key format is correct

## 🚀 Advanced Usage

### Custom PIN

Change the PIN in your `.env` file:
```env
SECRET_PIN=your_custom_pin
```

### Different Languages

The app is configured for Telugu (`te-IN`). To change:

1. Edit `app.py` line with `language_code="te-IN"`
2. Change to your preferred language code
3. Redeploy the application

### Custom Styling

Edit `templates/index.html` to customize:
- Colors and fonts
- Button sizes
- Layout and spacing
- Language text

## 📄 License

This project is open source and available under the MIT License.

## 🙏 Acknowledgments

- **Sarvam AI** for providing the STT API
- **Render** for hosting platform
- **Telugu community** for language support

---

**Made with ❤️ for Telugu speakers**

*Simple, fast, and reliable voice-to-text conversion*
