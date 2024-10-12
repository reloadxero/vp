import React, { useState, useRef, useCallback } from 'react';
import Webcam from 'react-webcam';
import './App.css'; // Import the CSS for full-screen handling

function App() {
  const [isCameraOpen, setIsCameraOpen] = useState(false);
  const [imageSrc, setImageSrc] = useState(null);
  const [cameraError, setCameraError] = useState('');
  const webcamRef = useRef(null);

  // Function to capture screenshot from webcam
  const capture = useCallback(() => {
    if (webcamRef.current) {
      const image = webcamRef.current.getScreenshot();
      if (image) {
        setImageSrc(image); // Set the captured image
      } else {
        console.error("Failed to capture image");
      }
    }
  }, [webcamRef]);

  // Handle Camera Errors
  const handleUserMediaError = (error) => {
    setCameraError("Error accessing the camera. Please allow camera permissions.");
    console.error("Camera error:", error);
  };

  // Handle Successful Camera Access
  const handleUserMedia = () => {
    setCameraError(""); // Reset error if camera works
    console.log("Camera accessed successfully");
  };

  // Function to reset and retake the picture
  const retakePicture = () => {
    setImageSrc(null);
  };

  // Close the camera and keep the image
  const keepPicture = () => {
    setIsCameraOpen(false);
  };

  return (
    <div className={`App ${isCameraOpen ? 'fullscreen' : ''}`}>
      <h2>Capture ID Card Image</h2>

      {!isCameraOpen && !imageSrc && (
        <button onClick={() => setIsCameraOpen(true)} style={{ marginBottom: '10px' }}>
          Start Camera
        </button>
      )}

      {/* Conditionally render the Webcam component based on isCameraOpen */}
      {isCameraOpen && !imageSrc && (
        <>
          <Webcam
            audio={false}
            ref={webcamRef}
            screenshotFormat="image/jpeg"
            className="webcam-view"
            videoConstraints={{
              facingMode: "environment", // Use rear camera if available
            }}
            onUserMedia={handleUserMedia}
            onUserMediaError={handleUserMediaError}
          />

          {/* Take Picture Button */}
          <button onClick={capture} className="capture-button">
            Take Picture
          </button>
        </>
      )}

      {/* Display Camera Error */}
      {cameraError && <p style={{ color: 'red' }}>{cameraError}</p>}

      {/* Display the captured image with Keep and Retake options */}
      {imageSrc && (
        <div className="image-preview-container">
          <h3>Captured Image</h3>
          <img src={imageSrc} alt="Captured ID" className="captured-image" />
          <div className="button-group">
            <button onClick={keepPicture} className="keep-button">
              Keep Picture
            </button>
            <button onClick={retakePicture} className="retake-button">
              Retake Picture
            </button>
          </div>
        </div>
      )}
    </div>
  );
}

export default App;
