"use client"

import * as React from "react"
import Link from "next/link"
import { Header } from "@/components/layout/Header"
import { Button } from "@/components/ui/button"
import { RegistrationModal } from "@/components/ui/registration-modal"
import {
  Check,
  Users,
  TrendingUp,
  Shield,
  Briefcase,
  FileText,
  Calendar,
  BarChart3,
  Zap,
  Star,
  ArrowRight,
  Bot,
  Gavel,
  BadgeCheck,
  Clock,
  DollarSign,
  Building2,
} from "lucide-react"
import { LeiaLogo } from "@/components/ui/leia-logo"
import { cn } from "@/lib/utils"

const benefits = [
  {
    icon: Users,
    title: "Capta más clientes",
    description: "Accede a miles de personas buscando asesoría legal en Chile cada mes.",
  },
  {
    icon: BadgeCheck,
    title: "Perfil verificado",
    description: "Destaca con un badge de verificación que genera confianza en los usuarios.",
  },
  {
    icon: Bot,
    title: "LEIA Escritos",
    description: "IA que te ayuda a generar borradores de escritos judiciales y contratos.",
  },
  {
    icon: Gavel,
    title: "Conexión Poder Judicial",
    description: "Consulta causas del PJUD y recibe alertas de actualizaciones automáticas.",
  },
  {
    icon: Briefcase,
    title: "CRM Legal completo",
    description: "Gestiona clientes, casos, documentos y fechas importantes en un solo lugar.",
  },
  {
    icon: BarChart3,
    title: "Métricas y reportes",
    description: "Analiza tu práctica con estadísticas de casos, ingresos y rendimiento.",
  },
]

const testimonials = [
  {
    name: "María González",
    role: "Abogada Laboral",
    location: "Santiago",
    quote: "LEIA me ha permitido captar clientes que antes no llegaban a mi oficina. El CRM es excelente para llevar el control de mis casos.",
    rating: 5,
  },
  {
    name: "Carlos Muñoz",
    role: "Estudio Jurídico Muñoz & Asociados",
    location: "Valparaíso",
    quote: "La conexión con el Poder Judicial me ahorra horas de trabajo. Las alertas de actualizaciones son invaluables.",
    rating: 5,
  },
  {
    name: "Ana Martínez",
    role: "Procuradora",
    location: "Concepción",
    quote: "Como procuradora, LEIA Escritos me ayuda a generar borradores rápidamente. Mis clientes están muy satisfechos.",
    rating: 5,
  },
]

const steps = [
  {
    number: 1,
    title: "Crea tu perfil",
    description: "Completa tu información profesional y áreas de especialización.",
  },
  {
    number: 2,
    title: "Verifica tu identidad",
    description: "Sube tu carnet de abogado o documentos que acrediten tu profesión.",
  },
  {
    number: 3,
    title: "Comienza a recibir clientes",
    description: "Tu perfil estará visible y podrás recibir consultas de inmediato.",
  },
]

export default function UnirsePage() {
  const [isModalOpen, setIsModalOpen] = React.useState(false)

  return (
    <div className="flex flex-col min-h-screen bg-mesh">
      <Header />

      {/* Registration Modal */}
      <RegistrationModal
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
        type="profesional"
      />

      {/* Hero */}
      <section className="relative pt-28 lg:pt-36 pb-16">
        <div className="absolute top-20 left-1/4 w-96 h-96 bg-pacific-400/20 rounded-full blur-3xl animate-pulse-glow" />
        <div className="absolute bottom-0 right-1/4 w-80 h-80 bg-terracota-400/10 rounded-full blur-3xl animate-pulse-glow" style={{ animationDelay: '1s' }} />

        <div className="container relative">
          <div className="max-w-4xl mx-auto text-center">
            <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-pacific-100/50 text-pacific-700 text-sm font-medium mb-6">
              <Building2 className="h-4 w-4" />
              Para Abogados, Procuradores y Estudios Jurídicos
            </div>

            <h1 className="text-4xl lg:text-5xl font-semibold text-slate-900 mb-6">
              Haz crecer tu práctica legal con <span className="text-gradient">LEIA</span>
            </h1>
            <p className="text-lg text-slate-600 mb-8 max-w-2xl mx-auto">
              Únete a la red de profesionales legales más grande de Chile. Capta clientes,
              gestiona tu práctica y automatiza tu trabajo con inteligencia artificial.
            </p>

            <div className="flex flex-col sm:flex-row gap-4 justify-center mb-10">
              <Button
                size="lg"
                variant="pacific"
                className="shadow-lg shadow-pacific-500/25"
                onClick={() => setIsModalOpen(true)}
              >
                Crear mi perfil gratis
                <ArrowRight className="ml-2 h-5 w-5" />
              </Button>
              <Button size="lg" variant="outline" asChild>
                <Link href="/precios">Ver planes y precios</Link>
              </Button>
            </div>

            <div className="flex flex-wrap justify-center gap-6 text-sm text-slate-500">
              <span className="flex items-center gap-2">
                <Check className="h-4 w-4 text-green-500" />
                Sin costo de inscripción
              </span>
              <span className="flex items-center gap-2">
                <Check className="h-4 w-4 text-green-500" />
                500+ profesionales ya confían en LEIA
              </span>
              <span className="flex items-center gap-2">
                <Check className="h-4 w-4 text-green-500" />
                Cancela cuando quieras
              </span>
            </div>
          </div>
        </div>
      </section>

      {/* Benefits */}
      <section className="py-20">
        <div className="container">
          <div className="max-w-5xl mx-auto">
            <div className="text-center mb-12">
              <h2 className="text-3xl font-semibold text-slate-900 mb-4">
                Todo lo que necesitas para tu práctica
              </h2>
              <p className="text-slate-600 max-w-xl mx-auto">
                Herramientas diseñadas para abogados, procuradores y estudios jurídicos en Chile
              </p>
            </div>

            <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
              {benefits.map((benefit, index) => (
                <div
                  key={index}
                  className="glass-card-hover rounded-2xl p-6"
                >
                  <div className="h-12 w-12 rounded-xl bg-gradient-to-br from-pacific-100 to-pacific-50 flex items-center justify-center mb-4">
                    <benefit.icon className="h-6 w-6 text-pacific-600" />
                  </div>
                  <h3 className="font-semibold text-slate-900 mb-2">{benefit.title}</h3>
                  <p className="text-sm text-slate-600">{benefit.description}</p>
                </div>
              ))}
            </div>
          </div>
        </div>
      </section>

      {/* How it works */}
      <section className="py-20 relative">
        <div className="absolute inset-0 bg-gradient-to-b from-transparent via-pacific-50/30 to-transparent" />

        <div className="container relative">
          <div className="max-w-4xl mx-auto">
            <div className="text-center mb-12">
              <h2 className="text-3xl font-semibold text-slate-900 mb-4">
                Comienza en 3 simples pasos
              </h2>
            </div>

            <div className="grid md:grid-cols-3 gap-8">
              {steps.map((step, index) => (
                <div key={index} className="relative text-center">
                  <div className="inline-flex items-center justify-center h-14 w-14 rounded-full bg-gradient-to-br from-pacific-500 to-pacific-600 text-white text-xl font-bold mb-4 shadow-lg shadow-pacific-500/25">
                    {step.number}
                  </div>
                  {index < steps.length - 1 && (
                    <div className="hidden md:block absolute top-7 left-[60%] w-[80%] h-0.5 bg-gradient-to-r from-pacific-300 to-pacific-100" />
                  )}
                  <h3 className="font-semibold text-slate-900 mb-2">{step.title}</h3>
                  <p className="text-sm text-slate-600">{step.description}</p>
                </div>
              ))}
            </div>

            {/* CTA in steps */}
            <div className="text-center mt-12">
              <Button
                size="lg"
                variant="pacific"
                className="shadow-lg shadow-pacific-500/25"
                onClick={() => setIsModalOpen(true)}
              >
                Comenzar ahora
                <ArrowRight className="ml-2 h-5 w-5" />
              </Button>
            </div>
          </div>
        </div>
      </section>

      {/* Testimonials */}
      <section className="py-20">
        <div className="container">
          <div className="max-w-5xl mx-auto">
            <div className="text-center mb-12">
              <h2 className="text-3xl font-semibold text-slate-900 mb-4">
                Lo que dicen nuestros profesionales
              </h2>
            </div>

            <div className="grid md:grid-cols-3 gap-6">
              {testimonials.map((testimonial, index) => (
                <div
                  key={index}
                  className="glass-card rounded-2xl p-6"
                >
                  <div className="flex gap-1 mb-4">
                    {[...Array(testimonial.rating)].map((_, i) => (
                      <Star key={i} className="h-4 w-4 fill-amber-400 text-amber-400" />
                    ))}
                  </div>
                  <p className="text-slate-700 mb-4 italic">"{testimonial.quote}"</p>
                  <div>
                    <p className="font-semibold text-slate-900">{testimonial.name}</p>
                    <p className="text-sm text-slate-500">{testimonial.role} • {testimonial.location}</p>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </section>

      {/* Final CTA */}
      <section className="py-20">
        <div className="container">
          <div className="max-w-4xl mx-auto">
            <div className="relative rounded-3xl overflow-hidden">
              <div className="absolute inset-0 bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900" />
              <div className="absolute top-0 left-0 w-96 h-96 bg-pacific-500/20 rounded-full blur-3xl" />
              <div className="absolute bottom-0 right-0 w-80 h-80 bg-terracota-500/10 rounded-full blur-3xl" />

              <div className="relative p-10 lg:p-14 text-center">
                <h2 className="text-3xl font-semibold text-white mb-4">
                  ¿Listo para hacer crecer tu práctica?
                </h2>
                <p className="text-lg text-white/70 mb-8 max-w-xl mx-auto">
                  Únete a cientos de abogados, procuradores y estudios jurídicos que ya confían en LEIA.
                </p>

                <div className="flex flex-col sm:flex-row gap-4 justify-center">
                  <Button
                    size="lg"
                    variant="white"
                    onClick={() => setIsModalOpen(true)}
                  >
                    Crear perfil gratis
                    <ArrowRight className="ml-2 h-5 w-5" />
                  </Button>
                  <Button size="lg" variant="glass" className="text-white border-white/20 hover:bg-white/10" asChild>
                    <Link href="/precios">Ver planes</Link>
                  </Button>
                </div>

                <div className="flex flex-wrap justify-center gap-6 mt-8 text-sm text-white/60">
                  <span className="flex items-center gap-2">
                    <Check className="h-4 w-4 text-pacific-400" />
                    Gratis para comenzar
                  </span>
                  <span className="flex items-center gap-2">
                    <Check className="h-4 w-4 text-pacific-400" />
                    Sin compromisos
                  </span>
                  <span className="flex items-center gap-2">
                    <Check className="h-4 w-4 text-pacific-400" />
                    Soporte incluido
                  </span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="py-16 border-t border-slate-200/50">
        <div className="container">
          <div className="max-w-5xl mx-auto">
            <div className="flex flex-col lg:flex-row justify-between items-center gap-8">
              <Link href="/">
                <LeiaLogo size="md" />
              </Link>

              <div className="flex flex-wrap justify-center gap-8 text-sm">
                <Link href="/chat" className="text-slate-600 hover:text-slate-900 transition-colors">Asistente IA</Link>
                <Link href="/abogados" className="text-slate-600 hover:text-slate-900 transition-colors">Abogados</Link>
                <Link href="/precios" className="text-slate-600 hover:text-slate-900 transition-colors">Precios</Link>
                <Link href="/terminos" className="text-slate-600 hover:text-slate-900 transition-colors">Términos</Link>
                <Link href="/privacidad" className="text-slate-600 hover:text-slate-900 transition-colors">Privacidad</Link>
              </div>

              <p className="text-sm text-slate-500 flex items-center gap-2">
                © 2025 LEIA. Hecho en Chile
                <svg viewBox="0 0 30 20" className="h-4 w-6 rounded shadow-sm" aria-label="Chile">
                  <rect x="0" y="0" width="10" height="10" fill="#0039A6" />
                  <polygon points="5,2 6.2,5.5 9.5,5.5 6.8,7.5 7.8,11 5,8.5 2.2,11 3.2,7.5 0.5,5.5 3.8,5.5" fill="white" transform="scale(0.7) translate(2.1, 1.4)" />
                  <rect x="10" y="0" width="20" height="10" fill="white" />
                  <rect x="0" y="10" width="30" height="10" fill="#D52B1E" />
                </svg>
              </p>
            </div>
          </div>
        </div>
      </footer>
    </div>
  )
}
