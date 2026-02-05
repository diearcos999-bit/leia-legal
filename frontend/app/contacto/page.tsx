"use client"

import Link from "next/link"
import { Header } from "@/components/layout/Header"
import { Button } from "@/components/ui/button"
import { LeiaLogo } from "@/components/ui/leia-logo"
import {
  Mail,
  Phone,
  MapPin,
  MessageSquare,
  Clock,
  ArrowRight,
  Scale,
} from "lucide-react"

export default function ContactoPage() {
  return (
    <div className="flex flex-col min-h-screen bg-mesh">
      <Header />

      {/* Hero */}
      <section className="relative pt-28 lg:pt-36 pb-16">
        <div className="absolute top-20 left-1/4 w-96 h-96 bg-pacific-400/20 rounded-full blur-3xl animate-pulse-glow" />
        <div className="absolute bottom-0 right-1/4 w-80 h-80 bg-terracota-400/10 rounded-full blur-3xl animate-pulse-glow" style={{ animationDelay: '1s' }} />

        <div className="container relative">
          <div className="text-center max-w-3xl mx-auto">
            <h1 className="text-4xl lg:text-5xl font-semibold text-slate-900 mb-4">
              Conversemos
            </h1>
            <p className="text-lg text-slate-600">
              ¿Tienes preguntas sobre nuestros planes o servicios? Estamos aquí para ayudarte.
            </p>
          </div>
        </div>
      </section>

      {/* Content */}
      <section className="py-16">
        <div className="container">
          <div className="max-w-5xl mx-auto">
            <div className="grid lg:grid-cols-2 gap-12">
              {/* Contact Info */}
              <div>
                <h2 className="text-2xl font-semibold text-slate-900 mb-6">
                  Información de contacto
                </h2>

                <div className="space-y-6">
                  <div className="flex items-start gap-4">
                    <div className="h-12 w-12 rounded-xl bg-pacific-100 flex items-center justify-center flex-shrink-0">
                      <Mail className="h-6 w-6 text-pacific-600" />
                    </div>
                    <div>
                      <p className="font-medium text-slate-900">Email</p>
                      <a href="mailto:contacto@leia.cl" className="text-pacific-600 hover:underline">
                        contacto@leia.cl
                      </a>
                    </div>
                  </div>

                  <div className="flex items-start gap-4">
                    <div className="h-12 w-12 rounded-xl bg-pacific-100 flex items-center justify-center flex-shrink-0">
                      <Phone className="h-6 w-6 text-pacific-600" />
                    </div>
                    <div>
                      <p className="font-medium text-slate-900">Teléfono</p>
                      <a href="tel:+56912345678" className="text-pacific-600 hover:underline">
                        +56 9 1234 5678
                      </a>
                    </div>
                  </div>

                  <div className="flex items-start gap-4">
                    <div className="h-12 w-12 rounded-xl bg-pacific-100 flex items-center justify-center flex-shrink-0">
                      <MapPin className="h-6 w-6 text-pacific-600" />
                    </div>
                    <div>
                      <p className="font-medium text-slate-900">Ubicación</p>
                      <p className="text-slate-600">Santiago, Chile</p>
                    </div>
                  </div>

                  <div className="flex items-start gap-4">
                    <div className="h-12 w-12 rounded-xl bg-pacific-100 flex items-center justify-center flex-shrink-0">
                      <Clock className="h-6 w-6 text-pacific-600" />
                    </div>
                    <div>
                      <p className="font-medium text-slate-900">Horario de atención</p>
                      <p className="text-slate-600">Lunes a Viernes: 9:00 - 18:00</p>
                      <p className="text-sm text-slate-500">El asistente IA está disponible 24/7</p>
                    </div>
                  </div>
                </div>

                {/* Quick links */}
                <div className="mt-10 p-6 glass-card rounded-2xl">
                  <h3 className="font-semibold text-slate-900 mb-4">Enlaces rápidos</h3>
                  <div className="space-y-3">
                    <Link href="/chat" className="flex items-center gap-2 text-pacific-600 hover:underline">
                      <MessageSquare className="h-4 w-4" />
                      Probar el asistente IA gratis
                    </Link>
                    <Link href="/precios" className="flex items-center gap-2 text-pacific-600 hover:underline">
                      <Scale className="h-4 w-4" />
                      Ver planes y precios
                    </Link>
                    <Link href="/unirse" className="flex items-center gap-2 text-pacific-600 hover:underline">
                      <ArrowRight className="h-4 w-4" />
                      Unirme como abogado
                    </Link>
                  </div>
                </div>
              </div>

              {/* Contact Form */}
              <div className="glass-panel rounded-3xl p-8">
                <h2 className="text-2xl font-semibold text-slate-900 mb-6">
                  Envíanos un mensaje
                </h2>

                <form className="space-y-4">
                  <div className="grid grid-cols-2 gap-4">
                    <div>
                      <label className="block text-sm font-medium text-slate-700 mb-1">
                        Nombre
                      </label>
                      <input
                        type="text"
                        className="w-full px-4 py-3 rounded-xl glass-input text-slate-800 placeholder:text-slate-400 focus:outline-none"
                        placeholder="Tu nombre"
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-slate-700 mb-1">
                        Apellido
                      </label>
                      <input
                        type="text"
                        className="w-full px-4 py-3 rounded-xl glass-input text-slate-800 placeholder:text-slate-400 focus:outline-none"
                        placeholder="Tu apellido"
                      />
                    </div>
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-slate-700 mb-1">
                      Email
                    </label>
                    <input
                      type="email"
                      className="w-full px-4 py-3 rounded-xl glass-input text-slate-800 placeholder:text-slate-400 focus:outline-none"
                      placeholder="tu@email.cl"
                    />
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-slate-700 mb-1">
                      Asunto
                    </label>
                    <select
                      className="w-full px-4 py-3 rounded-xl glass-input text-slate-800 focus:outline-none"
                    >
                      <option value="">Selecciona un tema</option>
                      <option value="planes">Consulta sobre planes</option>
                      <option value="firma">Plan Firma / Empresas</option>
                      <option value="abogado">Unirme como abogado</option>
                      <option value="soporte">Soporte técnico</option>
                      <option value="otro">Otro</option>
                    </select>
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-slate-700 mb-1">
                      Mensaje
                    </label>
                    <textarea
                      rows={5}
                      className="w-full px-4 py-3 rounded-xl glass-input text-slate-800 placeholder:text-slate-400 focus:outline-none resize-none"
                      placeholder="¿En qué podemos ayudarte?"
                    />
                  </div>

                  <Button type="submit" variant="pacific" size="lg" className="w-full">
                    Enviar mensaje
                    <ArrowRight className="ml-2 h-5 w-5" />
                  </Button>
                </form>

                <p className="text-sm text-slate-500 text-center mt-6">
                  Responderemos a tu mensaje dentro de 24 horas hábiles.
                </p>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="py-16 border-t border-slate-200/50 mt-auto">
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
