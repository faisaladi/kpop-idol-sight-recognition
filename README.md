# K-POP Artist Recognizer

A real-time face recognition app that identifies K-POP artists using your phone camera.

## Features

- Real-time camera access (mobile-friendly)
- Face detection and recognition
- Artist information display (name + group)
- Click to search on Google for more details
- Responsive design for mobile and desktop

## Tech Stack

- **Frontend**: React + Vite, react-webcam
- **Backend**: Python FastAPI, face-recognition library
- **Deployment**: Docker with nginx + supervisord

## Setup

### 1. Install Dependencies

```bash
./setup.sh
```

### 2. Add K-POP Artists

To recognize artists, you need to add their photos to the database:

```bash
# Create photos directory
mkdir -p backend/photos

# Add artist photos (clear face photos work best)
# Example: backend/photos/jisoo.jpg

# Add artist to database
python backend/add_artist.py "Jisoo" "BLACKPINK" "backend/photos/jisoo.jpg"
python backend/add_artist.py "Jennie" "BLACKPINK" "backend/photos/jennie.jpg"
python backend/add_artist.py "Lisa" "BLACKPINK" "backend/photos/lisa.jpg"
python backend/add_artist.py "Rosé" "BLACKPINK" "backend/photos/rose.jpg"
```

**Tips for best results:**
- Use clear, front-facing photos
- Good lighting
- Only one person in the photo
- High resolution (at least 640x480)

### 3. Run the App

The server will start automatically after setup completes.

- Frontend: http://localhost:3000
- Backend API: http://localhost:8080

## How to Use

1. Open the app on your phone or computer
2. Allow camera permissions when prompted
3. Point the camera at K-POP artists (on screen or posters)
4. Green boxes will appear around detected faces with artist info
5. Click on the box to search Google for more details

## API Endpoints

- `GET /` - API documentation
- `GET /health` - Health check
- `GET /artists` - List all known artists
- `POST /detect` - Detect artists in image (multipart/form-data)

## Project Structure

```
.
├── frontend/               # React frontend
│   ├── src/
│   │   ├── App.jsx        # Main app component
│   │   ├── App.css        # Styles
│   │   └── main.jsx       # Entry point
│   └── package.json
│
├── backend/               # Python FastAPI backend
│   ├── main.py           # API server
│   ├── add_artist.py     # Script to add artists
│   ├── data/
│   │   └── known_faces.json  # Artist database
│   └── requirements.txt
│
├── Dockerfile            # Production deployment
├── setup.sh             # Setup script
└── run.sh              # Development server script
```

## Deployment

### Docker

```bash
# Build image
docker build -t kpop-recognizer .

# Run container
docker run -p 3000:3000 kpop-recognizer
```

### Railway/Render

1. Connect your Git repository
2. Railway will automatically detect the Dockerfile
3. Deploy!

The app will be available at your deployment URL.

## Performance Tips

- The face recognition runs every 1 second (adjustable in App.jsx)
- Add more artists to improve recognition accuracy
- Use multiple photos of the same artist for better matching

## Troubleshooting

### No artists detected
- Make sure you've added artists to the database
- Check if the backend is running: http://localhost:8080
- Verify face photos are clear and well-lit

### Camera not working
- Check browser permissions
- Use HTTPS in production (required for camera access)
- Try a different browser

### Backend errors
- Check backend.log for errors
- Verify Python dependencies are installed
- Make sure face_recognition library is properly installed

## License

MIT
