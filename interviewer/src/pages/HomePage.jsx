import { Link } from 'react-router-dom'

function HomePage() {
    return (
        <div className="relative min-h-screen bg-white text-slate-900 flex items-center justify-center px-4 overflow-hidden">

            <div className="max-w-8xl w-full space-y-8 text-center z-10">
                <header className="space-y-2">
                    <p className="inline-flex items-center rounded-full bg-green-100 px-3 py-1 text-xs font-medium text-green-600 ring-1 ring-green-300">
                        Elevate al siguiente nivel
                    </p>
                    <h1 className="text-4xl md:text-5xl font-bold tracking-tight">
                        HireLabs: optimiza tus entrevistas técnicas.
                    </h1>
                    <p className="text-slate-600 text-sm md:text-base max-w-2xl mx-auto">
                        Interviewer ayuda a los equipos a realizar entrevistas técnicas consistentes, justas y basadas en datos.
                        Prepara conjuntos de preguntas, toma notas estructuradas y comparte retroalimentación con tu equipo en minutos.
                    </p>
                </header>

                <section className="grid gap-6 md:grid-cols-3">
                    <div className="rounded-2xl bg-green-50 p-4 border border-green-200">
                        <h2 className="text-sm font-semibold mb-1 text-green-800">Sesiones estructuradas</h2>
                        <p className="text-xs text-green-700">
                            Mantén cada entrevista en orden con plantillas de preguntas y rúbricas de evaluación prediseñadas.
                        </p>
                    </div>

                    <div className="rounded-2xl bg-green-50 p-4 border border-green-200">
                        <h2 className="text-sm font-semibold mb-1 text-green-800">Retroalimentación colaborativa</h2>
                        <p className="text-xs text-green-700">
                            Comparte notas con tu panel de contratación y toma decisiones basadas en señales, no en memoria.
                        </p>
                    </div>

                    <div className="rounded-2xl bg-green-50 p-4 border border-green-200">
                        <h2 className="text-sm font-semibold mb-1 text-green-800">Amigable para candidatos</h2>
                        <p className="text-xs text-green-700">
                            Brinda a los candidatos expectativas claras y una experiencia fluida y agradable.
                        </p>
                    </div>
                </section>

                <div className="flex items-center justify-center gap-4">
                    <Link
                        to="/blank"
                        className="inline-flex items-center rounded-lg bg-green-500 px-5 py-3.5 text-sm font-bold text-white shadow-lg shadow-green-500 hover:bg-green-600 transition"
                    >
                        Pruébalo ahora
                    </Link>
                </div>

            </div>


            <div className="absolute bottom-0 left-0 w-full h-60 pointer-events-none">
                <div className="w-full h-full bg-gradient-to-t from-green-700/70 to-transparent rounded-t-full blur-2xl" />
            </div>

        </div>
    )
}

export default HomePage;
