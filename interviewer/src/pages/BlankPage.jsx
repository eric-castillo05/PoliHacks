import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import CameraPanel from '../components/CameraPanel.jsx'


const INITIAL_SECONDS = 15

function BlankPage() {
    const [secondsLeft, setSecondsLeft] = useState(INITIAL_SECONDS)
    const [isRunning, setIsRunning] = useState(false)
    const navigate = useNavigate()
    const [agentMessage, setAgentMessage] = useState("")

    useEffect(() => {
        const interval = setInterval(() => {
            if (customElements.get("elevenlabs-convai")) {
                console.log("Widget detectado");
                clearInterval(interval)

                const container = document.getElementById("widgetArea")

                if (!container) return

                container.innerHTML = ""

                const widget = document.createElement("elevenlabs-convai")
                widget.setAttribute("agent-id", "agent_2601kar32vt7eb288b41ttpb0fvp")
                widget.setAttribute("style", "position:absolute; top: 300px; right: 100px; width:300px; height:400px; ")

                widget.addEventListener("ready", () => {
                    console.log("Widget listo!");
                });

                widget.addEventListener("conversation-item-added", (event) => {
                    const text = event.detail?.output?.formatted?.text;

                    if (text) {
                        console.log("🟢 Texto en tiempo real:", text);
                        setAgentMessage(text);
                    }
                });


                container.appendChild(widget)
            }
        }, 500)

        return () => clearInterval(interval)
    }, [])

    useEffect(() => {
        if (!isRunning) return
        if (secondsLeft <= 0) {
            setIsRunning(false)
            setSecondsLeft(INITIAL_SECONDS)
            return
        }

        const id = setInterval(() => {
            setSecondsLeft(prev => prev - 1)
        }, 1000)

        return () => clearInterval(id)
    }, [isRunning, secondsLeft])

    const handleStartClick = () => {
        setSecondsLeft(INITIAL_SECONDS)
        setIsRunning(true)
    }

    const progress = secondsLeft / INITIAL_SECONDS

    return (
        <div className="w-screen min-h-screen flex flex-col bg-gradient-to-br from-slate-50 via-white to-emerald-50 text-black overflow-hidden">
            
            {/* TOP PROGRESS BAR */}
            <div className="w-full px-6 pt-6">
                <div className="max-w-7xl mx-auto">
                    <div className="w-full h-3 rounded-full bg-gray-200/60 overflow-hidden shadow-sm border border-gray-200/40">
                        <div
                            className="h-full bg-gradient-to-r from-emerald-400 via-emerald-500 to-emerald-600 rounded-full transition-all duration-1000 ease-linear shadow-lg"
                            style={{ transform: `scaleX(${progress})`, transformOrigin: 'left' }}
                        />
                    </div>
                </div>
            </div>

            {/* MAIN AREA */}
            <div className="flex px-6 py-4">
                <div className="w-full max-w-7xl mx-auto">
                    <div className="w-full bg-white rounded-3xl shadow-xl border border-gray-100/50 overflow-hidden relative backdrop-blur-sm">
                        
                        {/* Decorative gradient corners */}
                        <div className="absolute top-0 right-0 w-96 h-96 bg-gradient-to-bl from-emerald-100/30 to-transparent rounded-full blur-3xl -z-10" />
                        <div className="absolute bottom-0 left-0 w-80 h-80 bg-gradient-to-tr from-blue-100/20 to-transparent rounded-full blur-3xl -z-10" />

                        <div className="relative z-10 flex flex-col p-8 md:p-12">
                            
                            {/* HEADER SECTION */}
                            <div className="mb-6">
                               
                            </div>

                            {/* CONTENT GRID */}
                            <div className="flex-1 grid grid-cols-1 lg:grid-cols-3 gap-6 mb-6">
                                
                                {/* LEFT - Widget & Message */}
                                <div className="lg:col-span-2 space-y-4">
                                    {/* Agent Message Display */}
                                    {agentMessage && (
                                        <div className="rounded-2xl bg-gradient-to-br from-emerald-50 to-emerald-100/50 p-6 border border-emerald-200/60 shadow-sm hover:shadow-md transition">
                                            <p className="text-sm font-semibold text-emerald-700 mb-3 uppercase tracking-wide">Respuesta del Agente</p>
                                            <p className="text-lg text-slate-700 leading-relaxed font-medium">
                                                {agentMessage}
                                            </p>
                                        </div>
                                    )}

                                    {/* Widget Area */}
                                    <div className="rounded-2xl bg-gradient-to-br from-slate-100/50 to-slate-50/50 p-6 border border-slate-200/50 shadow-sm">
                                         <h2 className="text-4xl md:text-5xl font-bold bg-gradient-to-r from-slate-900 to-emerald-700 bg-clip-text text-transparent mb-2 px-9 py-3">
                                    ¿Qué algoritmo te gusta?
                                    </h2>
                                    
                                    <div className="h-1 w-180 bg-gradient-to-r from-emerald-400 to-emerald-600 rounded-full" />
                                            
                                        </div>
                                </div>

                                {/* RIGHT - Camera */}
                                <div className="flex flex-col items-center justify-center">
                                    <div className="w-full rounded-2xl overflow-hidden shadow-lg border-4 border-emerald-500/20 bg-gradient-to-br from-emerald-500/10 to-blue-500/10">
                                        <CameraPanel />
                                    </div>
                                    <p className="text-xs text-slate-500 mt-4 text-center">Cámara en vivo</p>
                                    <div id="widgetArea" className="flex justify-center" />
                                </div>

                            </div>

                            {/* INFO CARDS */}
                            <div className="grid grid-cols-1 md:grid-cols-3 gap-4 pt-35">
                                <div className="rounded-xl bg-gradient-to-br from-emerald-50 to-emerald-100/30 p-4 border border-emerald-200/40">
                                    <h4 className="font-semibold text-emerald-700 mb-1 text-sm">Conversación en vivo</h4>
                                    <p className="text-xs text-emerald-600">Interactúa con IA mediante voz</p>
                                </div>
                                <div className="rounded-xl bg-gradient-to-br from-blue-50 to-blue-100/30 p-4 border border-blue-200/40">
                                    <h4 className="font-semibold text-blue-700 mb-1 text-sm">Feedback instantáneo</h4>
                                    <p className="text-xs text-blue-600">Respuestas en tiempo real</p>
                                </div>
                                <div className="rounded-xl bg-gradient-to-br from-purple-50 to-purple-100/30 p-4 border border-purple-200/40">
                                    <h4 className="font-semibold text-purple-700 mb-1 text-sm">Cronometrado</h4>
                                    <p className="text-xs text-purple-600">{INITIAL_SECONDS} segundos por sesión</p>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            {/* BOTTOM BAR */}
            <div className="border-t border-gray-200/50 bg-white/80 backdrop-blur-md">
                <div className="max-w-7xl mx-auto px-6 py-4 flex items-center justify-between gap-4">
                    <button
                        type="button"
                        onClick={() => navigate('/')}
                        className="inline-flex items-center justify-center rounded-lg border-2 border-slate-900 px-5 py-2.5 text-sm font-bold bg-white text-slate-900 hover:bg-slate-900 hover:text-white transition shadow-sm"
                    >
                        Home
                    </button>

                    <div className="flex-1 flex justify-center items-center">
                        <button
                            type="button"
                            onClick={handleStartClick}
                            className="w-16 h-16 flex items-center justify-center rounded-full bg-gradient-to-br from-emerald-400 to-emerald-600 text-white text-2xl font-bold shadow-xl hover:shadow-2xl hover:from-emerald-500 hover:to-emerald-700 transition disabled:opacity-50 disabled:cursor-not-allowed border-2 border-emerald-300/50"
                            disabled={isRunning}
                        >
                            {secondsLeft}
                        </button>
                    </div>

                    <button
                        type="button"
                        onClick={() => navigate('/next')}
                        className="inline-flex items-center justify-center rounded-lg border-2 border-slate-900 px-5 py-2.5 text-sm font-bold bg-white text-slate-900 hover:bg-slate-900 hover:text-white transition shadow-sm"
                    >
                        Next
                    </button>
                </div>
            </div>
        </div>
    )
}

export default BlankPage