# 🚀 Manual GitHub Upload Instructions

Since Git authentication is having issues, here's how to upload your files manually:

## 📁 **Step 1: Prepare Files**

Your project is ready with these files:
- ✅ `app.py` - Flask backend
- ✅ `templates/index.html` - Frontend
- ✅ `requirements.txt` - Dependencies
- ✅ `Dockerfile` - Container config
- ✅ `README.md` - Documentation
- ✅ All other files

## 🌐 **Step 2: Upload to GitHub**

1. **Go to**: https://github.com/maneesh-sk/voice-to-text-app
2. **Click "uploading an existing file"** (green button)
3. **Drag and drop** all files from your project folder
4. **Commit message**: "Initial commit: Voice-to-Text app"
5. **Click "Commit changes"**

## 🎯 **Step 3: Deploy to Render**

Once files are on GitHub:

1. **Go to**: https://render.com
2. **Sign up/Login** with GitHub
3. **Click "New +" → "Web Service"**
4. **Connect repository**: `maneesh-sk/voice-to-text-app`
5. **Configure**:
   - **Name**: `voice-to-text-app`
   - **Environment**: `Docker`
   - **Port**: `8080`
6. **Add Environment Variables**:
   - `SARVAM_API_KEY`: `sk_8s5he58e_aitPINEGQjqM2Qb5NIszFs1q`
   - `SECRET_PIN`: `2214`
7. **Click "Create Web Service"**

## ✅ **Result**

Your app will be live at: `https://voice-to-text-app.onrender.com`

**Ready to upload manually?** 🚀
