import { useEffect, useRef, useState } from 'react'

// Siri-like circular visualizer that reacts to microphone input
function VoiceOrb() {
  const [level, setLevel] = useState(0)
  const audioContextRef = useRef(null)
  const analyserRef = useRef(null)
  const dataArrayRef = useRef(null)
  const rafIdRef = useRef(null)
  const streamRef = useRef(null)

  useEffect(() => {
    let isMounted = true

    async function setupAudio() {
      try {
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true })
        streamRef.current = stream

        const AudioContextClass = window.AudioContext || window.webkitAudioContext
        const audioContext = new AudioContextClass()
        audioContextRef.current = audioContext

        const source = audioContext.createMediaStreamSource(stream)
        const analyser = audioContext.createAnalyser()
        analyser.fftSize = 512
        source.connect(analyser)

        const bufferLength = analyser.frequencyBinCount
        const dataArray = new Uint8Array(bufferLength)
        dataArrayRef.current = dataArray
        analyserRef.current = analyser

        const updateLevel = () => {
          if (!isMounted || !analyserRef.current || !dataArrayRef.current) return

          analyserRef.current.getByteFrequencyData(dataArrayRef.current)

          let sum = 0
          for (let i = 0; i < dataArrayRef.current.length; i++) {
            sum += dataArrayRef.current[i]
          }
          const avg = sum / dataArrayRef.current.length || 0

          // Normalize roughly into 0–1 range
          const normalized = Math.min(1, avg / 128)
          setLevel(normalized)

          rafIdRef.current = requestAnimationFrame(updateLevel)
        }

        updateLevel()
      } catch (err) {
        console.error('Error accessing microphone', err)
      }
    }

    setupAudio()

    return () => {
      isMounted = false
      if (rafIdRef.current) cancelAnimationFrame(rafIdRef.current)
      if (audioContextRef.current) audioContextRef.current.close()
      if (streamRef.current) {
        streamRef.current.getTracks().forEach((track) => track.stop())
      }
    }
  }, [])

  const scale = 1 + level * 0.6
  const glow = 18 + level * 40
  const outerOpacity = 0.25 + level * 0.35

  return (
    <div className="flex flex-col items-center justify-center">
      <div className="relative flex items-center justify-center">
        {/* Outer soft glow */}
        <div
          className="absolute rounded-full bg-emerald-400/40 blur-3xl transition-opacity duration-150 ease-out"
          style={{
            width: '7rem',
            height: '7rem',
            opacity: outerOpacity,
          }}
        />

        {/* Main orb */}
        <div
          className="relative flex items-center justify-center rounded-full bg-gradient-to-br from-emerald-400 via-emerald-500 to-blue-500 transition-transform duration-100 ease-out py-6"
          style={{
            width: '5rem',
            height: '5rem',
            transform: `scale(${scale})`,
            boxShadow: `0 0 ${glow}px rgba(16,185,129,0.7), 0 0 ${glow / 2}px rgba(59,130,246,0.6)`,
          }}
        >
          {/* Inner core */}
          <div className="w-10 h-10 rounded-full bg-slate-950/90 border border-emerald-200/70 shadow-inner" />
        </div>
      </div>

    </div>
  )
}

export default VoiceOrb
