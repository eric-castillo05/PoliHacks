import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import CameraPanel from '../components/CameraPanel.jsx'

const INITIAL_SECONDS = 15

function BlankPage() {
  const [secondsLeft, setSecondsLeft] = useState(INITIAL_SECONDS)
  const [isRunning, setIsRunning] = useState(false)
  const navigate = useNavigate()

  useEffect(() => {
    if (!isRunning) return
    if (secondsLeft <= 0) {
      setIsRunning(false)
      setSecondsLeft(INITIAL_SECONDS)
      return
    }

    const id = setInterval(() => {
      setSecondsLeft((prev) => prev - 1)
    }, 1000)

    return () => clearInterval(id)
  }, [isRunning, secondsLeft])

  const handleStartClick = () => {
    setSecondsLeft(INITIAL_SECONDS)
    setIsRunning(true)
  }

  const progress = secondsLeft / INITIAL_SECONDS

  return (
    <div className="w-screen h-screen flex flex-col bg-white text-black overflow-hidden ">
      {/* TOP PROGRESS BAR */}
      <div className="w-full px-4 pt-4">
        <div className="max-w-5xl mx-auto flex flex-col items-center">
          <div className="w-full max-w-1500 h-8 rounded-full bg-gray-200 overflow-hidden shadow-inner relative ease-linear">
            <div
              className="h-full bg-emerald-500 origin-center rounded-full transition-transform duration-1000 ease-linear"
              style={{
                transform: `scaleX(${progress})`,
              }}
            />
          </div>
        </div>
      </div>

      {/* MAIN AREA */}
      <div className="flex-1 flex">
        <div className="w-full h-full p-8 relative">
          <div className="w-full h-full bg-gray-300 rounded-2xl shadow-inner relative">
            <div className="absolute bottom-4 right-4 w-[340px]">
              <CameraPanel />
            </div>
          </div>
        </div>
      </div>

      {/* BOTTOM BAR WITH BUTTONS */}
      <div className="border-t border-gray-200 bg-white">
        <div className="max-w-2xl mx-auto px-4 py-3 flex items-center justify-between gap-4">
          {/* Home button (left) */}
          <button
  type="button"
  onClick={() => navigate('/')}
  className="inline-flex items-center justify-center rounded-xl border border-black px-4 py-2 text-sm font-semibold bg-black text-white hover:bg-neutral-800 transition"
>
  Home
</button>

          {/* Center Start / countdown button */}
          <div className="flex-1 flex justify-center items-center">
            <button
              type="button"
              onClick={handleStartClick}
              className="w-12 h-12 flex items-center justify-center rounded-full bg-green-500 text-white text-lg font-semibold shadow-sm hover:bg-green-600 transition disabled:opacity-60"
              disabled={isRunning}
            >
              {secondsLeft}
            </button>
          </div>

          {/* Next button (right) */}
          <button
  type="button"
  onClick={() => navigate('/next')}
  className="inline-flex items-center justify-center rounded-xl border border-black px-4 py-2 text-sm font-semibold bg-black text-white hover:bg-neutral-800 transition"
>
  Next
</button>
        </div>
      </div>
    </div>
  )
}

export default BlankPage