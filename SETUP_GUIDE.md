# K-POP Artist Recognizer - Setup Guide

## Overview

This app uses your phone/computer camera to recognize K-POP artists in real-time using AI face recognition technology.

## Quick Start

### 1. Dependencies Installation (Already Done!)

```bash
./setup.sh
```

This installs:
- Frontend dependencies (React, Vite, react-webcam)
- Backend dependencies (FastAPI, MediaPipe, scikit-learn)

### 2. Add K-POP Artists to Database

Before using the app, you need to add K-POP artists:

```bash
# Create photos directory
mkdir -p backend/photos

# Add your artist photos (get clear, front-facing photos)
# Example: backend/photos/jisoo.jpg

# Activate Python virtual environment
cd backend
source venv/bin/activate

# Add artists to the database
python add_artist.py "Jisoo" "BLACKPINK" "photos/jisoo.jpg"
python add_artist.py "Jennie" "BLACKPINK" "photos/jennie.jpg"
python add_artist.py "Lisa" "BLACKPINK" "photos/lisa.jpg"
python add_artist.py "Rosé" "BLACKPINK" "photos/rose.jpg"

# Add more artists as needed!
```

**Where to get photos:**
- Official social media accounts
- Press releases
- Promotional photos
- Music video screenshots

**Photo requirements:**
- Clear, front-facing face
- Good lighting
- High resolution (640x480 or higher)
- Only one person per photo

### 3. Start the App

The app will start automatically when setup completes!

- **Frontend**: http://localhost:3000 (User interface)
- **Backend API**: http://localhost:8080 (Face recognition service)

## How to Use the App

1. **Open** http://localhost:3000 in your browser (or on your phone)
2. **Allow camera permissions** when prompted
3. **Point camera** at K-POP artists (on screen, posters, photos, etc.)
4. **See results** - Green boxes appear around detected faces with name and group
5. **Click boxes** to search Google for more information about the artist

## Project Structure

```
.
├── frontend/                 # React web app
│   ├── src/
│   │   ├── App.jsx          # Main camera interface
│   │   ├── App.css          # Styles
│   │   └── main.jsx         # Entry point
│   └── package.json
│
├── backend/                  # Python FastAPI server
│   ├── main.py              # API server with face detection
│   ├── add_artist.py        # Script to add new artists
│   ├── venv/                # Python virtual environment
│   ├── data/
│   │   └── known_faces.json # Artist database
│   ├── photos/              # Training photos
│   └── requirements.txt
│
├── setup.sh                 # Install dependencies
├── run.sh                   # Start dev server
├── Dockerfile               # Production deployment
└── README.md
```

## Technology Stack

### Frontend
- **React 18** - Modern UI library
- **Vite** - Fast build tool
- **react-webcam** - Camera access
- **CSS3** - Responsive styling

### Backend
- **FastAPI** - High-performance Python API framework
- **MediaPipe** - Google's ML solution for face detection
- **scikit-learn** - Machine learning for face matching
- **NumPy** - Numerical computing

### Deployment
- **Docker** - Containerization
- **nginx** - Web server for production
- **supervisord** - Process management

## API Endpoints

### GET /
API documentation and status

### GET /health
Health check endpoint

### GET /artists
List all known artists in the database

```json
{
  "artists": [
    {"name": "Jisoo", "group": "BLACKPINK"},
    {"name": "Jennie", "group": "BLACKPINK"}
  ],
  "count": 2
}
```

### POST /detect
Detect K-POP artists in an image

**Request:** Multipart form data with image file

**Response:**
```json
{
  "artists": [
    {
      "name": "Jisoo",
      "group": "BLACKPINK",
      "box": {
        "left": 25.5,
        "top": 30.2,
        "width": 20.0,
        "height": 35.5
      },
      "confidence": 0.92
    }
  ],
  "faces_detected": 1
}
```

## Troubleshooting

### Camera not working
- Check browser permissions (Settings > Privacy > Camera)
- Use HTTPS in production (required for camera access)
- Try a different browser (Chrome recommended)

### No artists detected
- Make sure you've added artists to the database
- Check backend is running: `curl http://localhost:8080/health`
- Verify photos are clear and well-lit

### "No face detected" error when adding artist
- Use a clearer photo with better lighting
- Make sure only one person is in the photo
- Try a different photo angle

### Backend won't start
- Check backend.log for errors: `cat backend.log`
- Make sure virtual environment is activated
- Reinstall dependencies: `cd backend && source venv/bin/activate && pip install -r requirements.txt`

## Performance Tips

1. **Add multiple photos per artist** for better accuracy
2. **Use high-quality photos** - better input = better recognition
3. **Adjust detection interval** in `frontend/src/App.jsx` (default: 1 second)
   ```javascript
   intervalRef.current = setInterval(() => {
     captureAndDetect()
   }, 1000) // Change to 500 for faster, 2000 for slower
   ```

## Production Deployment

### Using Docker

```bash
# Build image
docker build -t kpop-recognizer .

# Run container
docker run -p 3000:3000 kpop-recognizer
```

### Deploying to Railway/Render

1. Push code to GitHub
2. Connect repository to Railway/Render
3. Platform will auto-detect Dockerfile
4. Deploy!

The app will be available at your deployment URL.

## Adding More Artists

You can add as many artists as you want! Here's a quick script to add multiple:

```bash
#!/bin/bash
cd backend
source venv/bin/activate

# BLACKPINK
python add_artist.py "Jisoo" "BLACKPINK" "photos/jisoo.jpg"
python add_artist.py "Jennie" "BLACKPINK" "photos/jennie.jpg"
python add_artist.py "Lisa" "BLACKPINK" "photos/lisa.jpg"
python add_artist.py "Rosé" "BLACKPINK" "photos/rose.jpg"

# BTS
python add_artist.py "RM" "BTS" "photos/rm.jpg"
python add_artist.py "Jin" "BTS" "photos/jin.jpg"
python add_artist.py "Suga" "BTS" "photos/suga.jpg"
python add_artist.py "J-Hope" "BTS" "photos/jhope.jpg"
python add_artist.py "Jimin" "BTS" "photos/jimin.jpg"
python add_artist.py "V" "BTS" "photos/v.jpg"
python add_artist.py "Jungkook" "BTS" "photos/jungkook.jpg"

# NewJeans
python add_artist.py "Minji" "NewJeans" "photos/minji.jpg"
python add_artist.py "Hanni" "NewJeans" "photos/hanni.jpg"
python add_artist.py "Danielle" "NewJeans" "photos/danielle.jpg"
python add_artist.py "Haerin" "NewJeans" "photos/haerin.jpg"
python add_artist.py "Hyein" "NewJeans" "photos/hyein.jpg"

echo "✅ All artists added!"
```

## Support

If you encounter issues:

1. Check the logs:
   - Backend: `cat backend.log`
   - Browser console: F12 > Console tab

2. Verify setup:
   ```bash
   # Check backend health
   curl http://localhost:8080/health

   # List artists
   curl http://localhost:8080/artists
   ```

3. Restart the server if needed

## License

MIT License - Feel free to use and modify!
