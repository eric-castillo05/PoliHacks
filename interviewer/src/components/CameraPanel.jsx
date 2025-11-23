import { useEffect, useRef, useState } from 'react'

function CameraPanel() {
  const videoRef = useRef(null)
  const [error, setError] = useState(null)
  const [isStreaming, setIsStreaming] = useState(false)

  useEffect(() => {
    let stream

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
}
        }
      } catch (err) {
  console.error("REAL ERROR:", err.name, err.message);
  setError(`Error: ${err.name} - ${err.message}`);
}
    }

    startCamera()

    return () => {
      if (stream) {
        stream.getTracks().forEach((track) => track.stop())
      }
    }
  }, [])

  return (
    <div className="flex flex-col gap-4 md:flex-row md:gap-6 w-full">
      {/* Local camera preview */}
      <div className="flex-1 rounded-2xl border border-slate-800 bg-green-600/60 p-4">
        <h2 className="text-sm font-semibold mb-2 text-slate-100">
          Camera Preview
        </h2>
        <p className="text-xs text-white text-slate-400 mb-3">
          This preview uses your local webcam via the browser. Make sure you
          accept the permission prompt.
        </p>
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