import { useEffect, useRef, useState } from 'react'

function CameraPanel() {
  const videoRef = useRef(null)
  const [error, setError] = useState(null)
  const [isStreaming, setIsStreaming] = useState(false)
  const wsRef = useRef(null)

  useEffect(() => {
    let stream

    // Setup WebSocket connection
    wsRef.current = new WebSocket('ws://localhost:5000/ws'); // Update with backend WebSocket URL
    wsRef.current.onopen = () => {
      console.log('WebSocket connected');
    };
    wsRef.current.onerror = (e) => {
      console.error('WebSocket error', e);
    };
    wsRef.current.onclose = () => {
      console.log('WebSocket closed');
    };

    async function startCamera() {
      try {
        setError(null)
        stream = await navigator.mediaDevices.getUserMedia({
          video: { width: 1280, height: 720 },
          audio: false,
        })
        if (videoRef.current) {
          videoRef.current.srcObject = stream
          videoRef.current.onloadedmetadata = () => {
            videoRef.current.play()
            setIsStreaming(true)
            // Start sending frames
            startSendingFrames()
          }
        }
      } catch (err) {
        console.error("REAL ERROR:", err.name, err.message);
        setError(`Error: ${err.name} - ${err.message}`);
      }
    }

    // Function to send frames over WebSocket
    function startSendingFrames() {
      const canvas = document.createElement('canvas');
      canvas.width = 640;
      canvas.height = 360;
      const ctx = canvas.getContext('2d');

      function sendFrame() {
        if (videoRef.current && wsRef.current && wsRef.current.readyState === 1) {
          ctx.drawImage(videoRef.current, 0, 0, canvas.width, canvas.height);
          canvas.toBlob((blob) => {
            if (blob) {
              blob.arrayBuffer().then((buffer) => {
                wsRef.current.send(buffer);
              });
            }
          }, 'image/jpeg', 0.7);
        }
        requestAnimationFrame(sendFrame);
      }
      sendFrame();
    }

    startCamera()

    return () => {
      if (stream) {
        stream.getTracks().forEach((track) => track.stop())
      }
      if (wsRef.current) {
        wsRef.current.close();
      }
    }
  }, [])

  return (
    <div className="flex flex-col gap-4 md:flex-row md:gap-6 w-full">
      <div className="flex-1 rounded-2xl border border-slate-800 bg-green-600/60 p-4">
        <h2 className="text-sm font-semibold mb-2 text-slate-100">
          Camera Preview
        </h2>

<div className="relative h-32 md:h-40 overflow-hidden rounded-xl bg-slate-250 border border-slate-800">
  {error ? (
    <div className="flex h-full items-center justify-center px-4 text-center text-xs text-red-300">
      {error}
    </div>
  ) : (
    <>
      {!isStreaming && (
        <div className="absolute inset-0 flex items-center justify-center text-xs text-slate-400">
          Initializing camera…
        </div>
      )}
      <video
        ref={videoRef}
        className="h-full w-full object-cover"
        playsInline
        muted
      />
    </>
  )}
</div>
      </div>
    </div>
  )
}

export default CameraPanel