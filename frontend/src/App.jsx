import { useState, useRef, useEffect } from 'react'
import Webcam from 'react-webcam'
import './App.css'

function App() {
  const webcamRef = useRef(null)
  const [detectedArtists, setDetectedArtists] = useState([])
  const [isProcessing, setIsProcessing] = useState(false)
  const [permissionGranted, setPermissionGranted] = useState(false)
  const [error, setError] = useState(null)
  const intervalRef = useRef(null)

  useEffect(() => {
    if (permissionGranted) {
      // Start continuous detection every 1 second
      intervalRef.current = setInterval(() => {
        captureAndDetect()
      }, 1000)
    }

    return () => {
      if (intervalRef.current) {
        clearInterval(intervalRef.current)
      }
    }
  }, [permissionGranted])

  const captureAndDetect = async () => {
    if (!webcamRef.current || isProcessing) return

    setIsProcessing(true)
    try {
      const imageSrc = webcamRef.current.getScreenshot()
      if (!imageSrc) {
        setIsProcessing(false)
        return
      }

      // Convert base64 to blob
      const response = await fetch(imageSrc)
      const blob = await response.blob()

      // Send to backend
      const formData = new FormData()
      formData.append('file', blob, 'capture.jpg')

      const apiResponse = await fetch('/api/detect', {
        method: 'POST',
        body: formData,
      })

      const data = await apiResponse.json()
      setDetectedArtists(data.artists || [])
      setError(null)
    } catch (err) {
      console.error('Detection error:', err)
      setError('Failed to detect artists')
    } finally {
      setIsProcessing(false)
    }
  }

  const handleUserMedia = () => {
    setPermissionGranted(true)
    setError(null)
  }

  const handleUserMediaError = (err) => {
    console.error('Camera error:', err)
    setError('Camera permission denied or not available')
    setPermissionGranted(false)
  }

  const openArtistInfo = (artistName, groupName) => {
    const searchQuery = encodeURIComponent(`${artistName} ${groupName} kpop`)
    window.open(`https://www.google.com/search?q=${searchQuery}`, '_blank')
  }

  return (
    <div className="app">
      <header className="header">
        <h1>K-POP Artist Recognizer</h1>
        <p>Point your camera at K-POP artists to identify them</p>
      </header>

      <div className="camera-container">
        {!permissionGranted && !error && (
          <div className="permission-prompt">
            <p>Please allow camera access to start</p>
          </div>
        )}

        {error && (
          <div className="error-message">
            <p>{error}</p>
          </div>
        )}

        <div className="webcam-wrapper">
          <Webcam
            ref={webcamRef}
            audio={false}
            screenshotFormat="image/jpeg"
            videoConstraints={{
              facingMode: 'user',
              width: 1280,
              height: 720,
            }}
            onUserMedia={handleUserMedia}
            onUserMediaError={handleUserMediaError}
            className="webcam"
          />

          {/* Detected Artists Overlay */}
          {detectedArtists.map((artist, index) => (
            <div
              key={index}
              className="face-box"
              style={{
                left: `${artist.box.left}%`,
                top: `${artist.box.top}%`,
                width: `${artist.box.width}%`,
                height: `${artist.box.height}%`,
              }}
              onClick={() => openArtistInfo(artist.name, artist.group)}
            >
              <div className="artist-label">
                <div className="artist-name">{artist.name}</div>
                <div className="artist-group">{artist.group}</div>
                <div className="click-hint">Click for more info</div>
              </div>
            </div>
          ))}

          {isProcessing && (
            <div className="processing-indicator">
              <div className="spinner"></div>
            </div>
          )}
        </div>

        {permissionGranted && (
          <div className="info-text">
            {detectedArtists.length > 0 ? (
              <p>Detected {detectedArtists.length} artist(s) - Click on boxes for details</p>
            ) : (
              <p>Scanning for K-POP artists...</p>
            )}
          </div>
        )}
      </div>
    </div>
  )
}

export default App
