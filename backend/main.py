from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import mediapipe as mp
import numpy as np
from PIL import Image
import io
import json
import os
from sklearn.metrics.pairwise import cosine_similarity

app = FastAPI(title="K-POP Artist Recognizer API")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize MediaPipe Face Detection and Face Mesh
mp_face_detection = mp.solutions.face_detection
mp_face_mesh = mp.solutions.face_mesh
face_detection = mp_face_detection.FaceDetection(min_detection_confidence=0.5)
face_mesh = mp_face_mesh.FaceMesh(static_image_mode=True, max_num_faces=10, min_detection_confidence=0.5)

# Load known faces database
KNOWN_FACES = []
KNOWN_FACES_FILE = "data/known_faces.json"

def load_known_faces():
    """Load known faces from JSON file"""
    global KNOWN_FACES
    if os.path.exists(KNOWN_FACES_FILE):
        try:
            with open(KNOWN_FACES_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                KNOWN_FACES = data.get('artists', [])
                print(f"Loaded {len(KNOWN_FACES)} known artists")
        except Exception as e:
            print(f"Error loading known faces: {e}")
            KNOWN_FACES = []
    else:
        print(f"No known faces database found at {KNOWN_FACES_FILE}")
        KNOWN_FACES = []

@app.on_event("startup")
async def startup_event():
    """Load known faces on startup"""
    load_known_faces()

@app.get("/")
async def root():
    return {
        "message": "K-POP Artist Recognizer API",
        "endpoints": {
            "/detect": "POST - Detect K-POP artists in image",
            "/artists": "GET - List all known artists",
            "/health": "GET - Health check"
        },
        "known_artists": len(KNOWN_FACES)
    }

@app.get("/health")
async def health():
    return {"status": "healthy", "known_artists": len(KNOWN_FACES)}

@app.get("/artists")
async def list_artists():
    """List all known artists"""
    artists = [{"name": artist["name"], "group": artist["group"]} for artist in KNOWN_FACES]
    return {"artists": artists, "count": len(artists)}

def extract_face_landmarks(image_np):
    """Extract face landmarks using MediaPipe"""
    results = face_mesh.process(image_np)
    if not results.multi_face_landmarks:
        return []

    landmarks_list = []
    for face_landmarks in results.multi_face_landmarks:
        # Convert landmarks to numpy array
        landmarks = []
        for landmark in face_landmarks.landmark:
            landmarks.extend([landmark.x, landmark.y, landmark.z])
        landmarks_list.append(np.array(landmarks))

    return landmarks_list

@app.post("/detect")
async def detect_artists(file: UploadFile = File(...)):
    """Detect K-POP artists in uploaded image"""
    try:
        # Read image
        contents = await file.read()
        image = Image.open(io.BytesIO(contents))

        # Convert to RGB if needed
        if image.mode != 'RGB':
            image = image.convert('RGB')

        # Convert to numpy array
        image_np = np.array(image)
        img_height, img_width = image_np.shape[:2]

        # Detect faces using MediaPipe
        detection_results = face_detection.process(image_np)

        detected_artists = []

        if not detection_results.detections:
            return JSONResponse(content={
                'artists': [],
                'faces_detected': 0
            })

        # Extract landmarks for each detected face
        face_landmarks_list = extract_face_landmarks(image_np)

        # Process each detected face
        for idx, detection in enumerate(detection_results.detections):
            if idx >= len(face_landmarks_list):
                continue

            face_landmarks = face_landmarks_list[idx]

            # Get bounding box
            bbox = detection.location_data.relative_bounding_box

            matches = []

            # Compare with each known artist
            for known_artist in KNOWN_FACES:
                if 'landmarks' not in known_artist or not known_artist['landmarks']:
                    continue

                known_landmarks = np.array(known_artist['landmarks'])

                # Calculate cosine similarity
                similarity = cosine_similarity([face_landmarks], [known_landmarks])[0][0]

                if similarity > 0.85:  # Threshold for match
                    matches.append({
                        'artist': known_artist,
                        'similarity': float(similarity)
                    })

            # Get best match
            if matches:
                best_match = max(matches, key=lambda x: x['similarity'])
                artist = best_match['artist']

                # Calculate box position as percentage
                box = {
                    'left': bbox.xmin * 100,
                    'top': bbox.ymin * 100,
                    'width': bbox.width * 100,
                    'height': bbox.height * 100
                }

                detected_artists.append({
                    'name': artist['name'],
                    'group': artist['group'],
                    'box': box,
                    'confidence': best_match['similarity']
                })

        return JSONResponse(content={
            'artists': detected_artists,
            'faces_detected': len(detection_results.detections) if detection_results.detections else 0
        })

    except Exception as e:
        import traceback
        traceback.print_exc()
        return JSONResponse(
            status_code=500,
            content={'error': str(e), 'artists': []}
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
