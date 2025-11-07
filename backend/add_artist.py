#!/usr/bin/env python3
"""
Script to add K-POP artists to the recognition database

Usage: python add_artist.py <artist_name> <group_name> <image_path>
Example: python add_artist.py "Jisoo" "BLACKPINK" "photos/jisoo.jpg"
"""

import mediapipe as mp
import json
import sys
import os
from PIL import Image
import numpy as np

KNOWN_FACES_FILE = "data/known_faces.json"

# Initialize MediaPipe Face Mesh
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(static_image_mode=True, max_num_faces=1, min_detection_confidence=0.5)

def load_database():
    """Load existing database"""
    if os.path.exists(KNOWN_FACES_FILE):
        with open(KNOWN_FACES_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {"artists": [], "instructions": "Artist database"}

def save_database(data):
    """Save database"""
    os.makedirs(os.path.dirname(KNOWN_FACES_FILE), exist_ok=True)
    with open(KNOWN_FACES_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def extract_face_landmarks(image_np):
    """Extract face landmarks using MediaPipe"""
    results = face_mesh.process(image_np)
    if not results.multi_face_landmarks:
        return None

    # Get the first face's landmarks
    face_landmarks = results.multi_face_landmarks[0]
    landmarks = []
    for landmark in face_landmarks.landmark:
        landmarks.extend([landmark.x, landmark.y, landmark.z])

    return landmarks

def add_artist(name, group, image_path):
    """Add an artist to the database"""
    if not os.path.exists(image_path):
        print(f"Error: Image file '{image_path}' not found")
        return False

    print(f"Loading image: {image_path}")

    try:
        # Load image
        image = Image.open(image_path)

        # Convert to RGB if needed
        if image.mode != 'RGB':
            image = image.convert('RGB')

        # Convert to numpy array
        image_np = np.array(image)

        # Extract face landmarks
        landmarks = extract_face_landmarks(image_np)

        if landmarks is None:
            print("Error: No face detected in the image")
            print("Tips: Make sure the image has:")
            print("  - Clear, front-facing face")
            print("  - Good lighting")
            print("  - Only one person in the photo")
            return False

        # Load existing database
        db = load_database()

        # Check if artist already exists
        for artist in db['artists']:
            if artist['name'] == name and artist['group'] == group:
                print(f"Artist '{name}' from '{group}' already exists. Updating...")
                artist['landmarks'] = landmarks
                save_database(db)
                print(f"✓ Updated {name} ({group})")
                return True

        # Add new artist
        db['artists'].append({
            'name': name,
            'group': group,
            'landmarks': landmarks
        })

        save_database(db)
        print(f"✓ Added {name} ({group}) to database")
        print(f"Total artists: {len(db['artists'])}")
        return True

    except Exception as e:
        import traceback
        print(f"Error processing image: {e}")
        traceback.print_exc()
        return False

def main():
    if len(sys.argv) != 4:
        print("Usage: python add_artist.py <artist_name> <group_name> <image_path>")
        print("Example: python add_artist.py 'Jisoo' 'BLACKPINK' 'photos/jisoo.jpg'")
        sys.exit(1)

    name = sys.argv[1]
    group = sys.argv[2]
    image_path = sys.argv[3]

    print(f"Adding artist: {name} ({group})")
    success = add_artist(name, group, image_path)

    if success:
        print("\n✓ Artist added successfully!")
        print("Restart the backend server to load the new artist.")
    else:
        print("\n✗ Failed to add artist")
        sys.exit(1)

if __name__ == "__main__":
    main()
