"use client"

import * as React from "react"
import Link from "next/link"
import { useSearchParams } from "next/navigation"
import { Header } from "@/components/layout/Header"
import { Button } from "@/components/ui/button"
import { LeiaAvatar } from "@/components/ui/leia-avatar"
import { RegistrationModal } from "@/components/ui/registration-modal"
import {
  Check,
  Shield,
  ArrowRight,
  MessageSquare,
  Users,
  Sparkles,
} from "lucide-react"
import { Suspense } from "react"

function RegistroContent() {
  const searchParams = useSearchParams()
  const plan = searchParams.get("plan") || "gratis"
  const isPremium = plan === "premium"
  const [isModalOpen, setIsModalOpen] = React.useState(false)

  // Auto-open modal on page load
  React.useEffect(() => {
    const timer = setTimeout(() => setIsModalOpen(true), 300)
    return () => clearTimeout(timer)
  }, [])

  return (
    <div className="flex flex-col min-h-screen bg-mesh">
      <Header />

      {/* Registration Modal */}
      <RegistrationModal
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
        type="usuario"
        plan={plan}
      />

      <section className="relative pt-28 lg:pt-36 pb-16 flex-1 flex items-center">
        <div className="absolute top-20 left-1/4 w-96 h-96 bg-pacific-400/20 rounded-full blur-3xl animate-pulse-glow" />
        <div className="absolute bottom-0 right-1/4 w-80 h-80 bg-terracota-400/10 rounded-full blur-3xl animate-pulse-glow" style={{ animationDelay: '1s' }} />

        <div className="container relative">
          <div className="max-w-2xl mx-auto text-center">
            {/* Avatar */}
            <div className="flex justify-center mb-8">
              <LeiaAvatar size="xl" />
            </div>

            <h1 className="text-4xl lg:text-5xl font-semibold text-slate-900 mb-6">
              {isPremium ? "Obtén LEIA Premium" : "Únete a LEIA"}
            </h1>
            <p className="text-lg text-slate-600 mb-8 max-w-xl mx-auto">
              {isPremium
                ? "Conecta directamente con abogados verificados y obtén asesoría legal personalizada."
                : "Accede a orientación legal gratuita con inteligencia artificial."}
            </p>

            {/* Benefits */}
            <div className="grid sm:grid-cols-3 gap-6 mb-10">
              {isPremium ? (
                <>
                  <div className="glass-card rounded-2xl p-5 text-center">
                    <Users className="h-8 w-8 text-pacific-600 mx-auto mb-3" />
                    <p className="font-medium text-slate-900 text-sm">Contacta abogados directamente</p>
                  </div>
                  <div className="glass-card rounded-2xl p-5 text-center">
                    <Shield className="h-8 w-8 text-pacific-600 mx-auto mb-3" />
                    <p className="font-medium text-slate-900 text-sm">Documentos legales básicos</p>
                  </div>
                  <div className="glass-card rounded-2xl p-5 text-center">
                    <Sparkles className="h-8 w-8 text-pacific-600 mx-auto mb-3" />
                    <p className="font-medium text-slate-900 text-sm">Historial guardado</p>
                  </div>
                </>
              ) : (
                <>
                  <div className="glass-card rounded-2xl p-5 text-center">
                    <MessageSquare className="h-8 w-8 text-pacific-600 mx-auto mb-3" />
                    <p className="font-medium text-slate-900 text-sm">Consultas ilimitadas con IA</p>
                  </div>
                  <div className="glass-card rounded-2xl p-5 text-center">
                    <Users className="h-8 w-8 text-pacific-600 mx-auto mb-3" />
                    <p className="font-medium text-slate-900 text-sm">Directorio de abogados</p>
                  </div>
                  <div className="glass-card rounded-2xl p-5 text-center">
                    <Shield className="h-8 w-8 text-pacific-600 mx-auto mb-3" />
                    <p className="font-medium text-slate-900 text-sm">100% confidencial</p>
                  </div>
                </>
              )}
            </div>

            {isPremium && (
              <div className="inline-block mb-8 p-4 rounded-xl bg-pacific-50/50 border border-pacific-100">
                <div className="flex items-center gap-4">
                  <div>
                    <p className="text-sm text-slate-600">Plan Premium</p>
                    <p className="text-2xl font-bold text-slate-900">$9.990<span className="text-sm font-normal text-slate-500">/mes</span></p>
                  </div>
                  <Sparkles className="h-8 w-8 text-pacific-500" />
                </div>
              </div>
            )}

            {/* CTA */}
            <Button
              size="lg"
              variant="pacific"
              className="shadow-lg shadow-pacific-500/25"
              onClick={() => setIsModalOpen(true)}
            >
              {isPremium ? "Continuar con Premium" : "Crear cuenta gratis"}
              <ArrowRight className="ml-2 h-5 w-5" />
            </Button>

            <p className="text-sm text-slate-500 mt-6">
              ¿Ya tienes cuenta?{" "}
              <Link href="/login" className="text-pacific-600 hover:underline">
                Inicia sesión
              </Link>
            </p>

            <p className="text-sm text-slate-500 mt-2">
              ¿Eres abogado, procurador o estudio jurídico?{" "}
              <Link href="/unirse" className="text-pacific-600 hover:underline">
                Únete como profesional
              </Link>
            </p>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="py-8 border-t border-slate-200/50">
        <div className="container">
          <div className="flex flex-col md:flex-row justify-between items-center gap-4">
            <p className="text-sm text-slate-500 flex items-center gap-2">
              © 2025 LEIA. Hecho en Chile
              <svg viewBox="0 0 30 20" className="h-4 w-6 rounded shadow-sm" aria-label="Chile">
                <rect x="0" y="0" width="10" height="10" fill="#0039A6" />
                <polygon points="5,2 6.2,5.5 9.5,5.5 6.8,7.5 7.8,11 5,8.5 2.2,11 3.2,7.5 0.5,5.5 3.8,5.5" fill="white" transform="scale(0.7) translate(2.1, 1.4)" />
                <rect x="10" y="0" width="20" height="10" fill="white" />
                <rect x="0" y="10" width="30" height="10" fill="#D52B1E" />
              </svg>
            </p>
            <div className="flex gap-6 text-sm">
              <Link href="/terminos" className="text-slate-600 hover:text-slate-900 transition-colors">Términos</Link>
              <Link href="/privacidad" className="text-slate-600 hover:text-slate-900 transition-colors">Privacidad</Link>
            </div>
          </div>
        </div>
      </footer>
    </div>
  )
}

export default function RegistroPage() {
  return (
    <Suspense fallback={<div className="min-h-screen bg-mesh" />}>
      <RegistroContent />
    </Suspense>
  )
}
