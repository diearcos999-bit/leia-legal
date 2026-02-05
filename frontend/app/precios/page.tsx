"use client"

import Link from "next/link"
import { Header } from "@/components/layout/Header"
import { Button } from "@/components/ui/button"
import {
  Check,
  MessageSquare,
  Users,
  Shield,
  Briefcase,
  FileText,
  Calendar,
  BarChart3,
  Zap,
  Building2,
  Star,
  ArrowRight,
  Bot,
  Gavel,
} from "lucide-react"
import { LeiaLogo } from "@/components/ui/leia-logo"
import { cn } from "@/lib/utils"

const userPlans = [
  {
    name: "Gratis",
    price: "$0",
    period: "siempre",
    description: "Orientación legal con IA para resolver tus dudas",
    features: [
      "Consultas ilimitadas con LEIA",
      "Orientación legal básica",
      "Ver perfiles de abogados",
      "Información sobre tus derechos",
    ],
    cta: "Comenzar Gratis",
    href: "/chat",
    highlighted: false,
  },
  {
    name: "Premium",
    price: "$9.990",
    period: "/mes",
    description: "Conecta directamente con abogados verificados",
    features: [
      "Todo lo del plan Gratis",
      "Contactar abogados directamente",
      "Respuesta prioritaria de abogados",
      "Documentos legales básicos",
      "Historial de consultas guardado",
      "Soporte prioritario",
    ],
    cta: "Obtener Premium",
    href: "/registro?plan=premium",
    highlighted: true,
  },
]

const professionalPlans = [
  {
    name: "Starter",
    price: "$0",
    period: "siempre",
    description: "Comienza a captar clientes en LEIA",
    features: [
      "Perfil básico en directorio",
      "Hasta 3 consultas por mes",
      "Sistema de reputación",
      "Notificaciones de consultas",
    ],
    cta: "Crear Perfil Gratis",
    href: "/unirse?plan=starter",
    highlighted: false,
  },
  {
    name: "Profesional",
    price: "$29.990",
    period: "/mes",
    description: "Todo lo que necesitas para tu práctica legal",
    features: [
      "Perfil destacado + Badge Verificado",
      "Consultas ilimitadas",
      "CRM Legal: gestión de clientes y casos",
      "Conexión Poder Judicial (PJUD)",
      "LEIA Escritos: IA para borradores",
      "Calendario legal con alertas",
      "Estadísticas y reportes",
    ],
    cta: "Comenzar Profesional",
    href: "/unirse?plan=profesional",
    highlighted: true,
    badge: "Más Popular",
  },
  {
    name: "Firma",
    price: "$79.990",
    period: "/mes",
    description: "Para estudios jurídicos y equipos legales",
    features: [
      "Todo lo de Profesional",
      "Hasta 10 usuarios por firma",
      "Página de firma personalizada",
      "Leads prioritarios",
      "Gestión de roles y permisos",
      "API para integraciones",
      "Soporte dedicado",
    ],
    cta: "Contactar Ventas",
    href: "/contacto?plan=firma",
    highlighted: false,
  },
]

const features = [
  {
    icon: Bot,
    title: "LEIA Escritos",
    description: "IA que genera borradores de escritos judiciales, contratos y cartas basados en la legislación chilena vigente.",
  },
  {
    icon: Gavel,
    title: "Conexión Poder Judicial",
    description: "Consulta automática de causas en el PJUD con alertas de actualizaciones en tiempo real.",
  },
  {
    icon: Briefcase,
    title: "CRM Legal",
    description: "Gestiona clientes, casos, documentos, fechas importantes y recordatorios en un solo lugar.",
  },
  {
    icon: Calendar,
    title: "Calendario Legal",
    description: "Plazos, audiencias y vencimientos sincronizados con notificaciones automáticas.",
  },
  {
    icon: BarChart3,
    title: "Reportes y Métricas",
    description: "Analiza el rendimiento de tu práctica: casos, ingresos, tiempo por cliente.",
  },
  {
    icon: Shield,
    title: "Seguridad y Privacidad",
    description: "Datos encriptados, cumplimiento normativo y respaldo automático de información.",
  },
]

export default function PreciosPage() {
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
              Planes para cada necesidad
            </h1>
            <p className="text-lg text-slate-600">
              Ya sea que busques asesoría legal o quieras hacer crecer tu práctica profesional, tenemos un plan para ti.
            </p>
          </div>
        </div>
      </section>

      {/* User Plans */}
      <section className="py-16">
        <div className="container">
          <div className="max-w-5xl mx-auto">
            <div className="text-center mb-12">
              <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-pacific-100/50 text-pacific-700 text-sm font-medium mb-4">
                <Users className="h-4 w-4" />
                Para Usuarios
              </div>
              <h2 className="text-3xl font-semibold text-slate-900 mb-3">
                ¿Buscas orientación legal?
              </h2>
              <p className="text-slate-600 max-w-xl mx-auto">
                Consulta gratis con nuestra IA o conecta con abogados verificados
              </p>
            </div>

            <div className="grid md:grid-cols-2 gap-6 max-w-3xl mx-auto">
              {userPlans.map((plan, index) => (
                <div
                  key={index}
                  className={cn(
                    "relative rounded-2xl p-8 transition-all duration-300",
                    plan.highlighted
                      ? "glass-card shadow-glass-lg ring-2 ring-pacific-500/20"
                      : "glass-card-hover"
                  )}
                >
                  {plan.highlighted && (
                    <div className="absolute -top-3 left-1/2 -translate-x-1/2">
                      <span className="px-3 py-1 rounded-full bg-gradient-to-r from-pacific-500 to-pacific-600 text-white text-xs font-medium shadow-lg">
                        Recomendado
                      </span>
                    </div>
                  )}

                  <div className="mb-6">
                    <h3 className="text-xl font-semibold text-slate-900 mb-2">{plan.name}</h3>
                    <p className="text-sm text-slate-600">{plan.description}</p>
                  </div>

                  <div className="mb-6">
                    <span className="text-4xl font-bold text-slate-900">{plan.price}</span>
                    <span className="text-slate-500">{plan.period}</span>
                  </div>

                  <ul className="space-y-3 mb-8">
                    {plan.features.map((feature, i) => (
                      <li key={i} className="flex items-start gap-3 text-sm text-slate-700">
                        <Check className="h-5 w-5 text-pacific-500 flex-shrink-0" />
                        {feature}
                      </li>
                    ))}
                  </ul>

                  <Button
                    variant={plan.highlighted ? "pacific" : "outline"}
                    className="w-full"
                    asChild
                  >
                    <Link href={plan.href}>{plan.cta}</Link>
                  </Button>
                </div>
              ))}
            </div>
          </div>
        </div>
      </section>

      {/* Professional Plans */}
      <section className="py-16 relative">
        <div className="absolute inset-0 bg-gradient-to-b from-transparent via-pacific-50/30 to-transparent" />

        <div className="container relative">
          <div className="max-w-6xl mx-auto">
            <div className="text-center mb-12">
              <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-terracota-100/50 text-terracota-700 text-sm font-medium mb-4">
                <Briefcase className="h-4 w-4" />
                Para Profesionales
              </div>
              <h2 className="text-3xl font-semibold text-slate-900 mb-3">
                ¿Eres abogado, procurador o estudio jurídico?
              </h2>
              <p className="text-slate-600 max-w-xl mx-auto">
                Capta clientes, gestiona tu práctica y automatiza tu trabajo con IA
              </p>
            </div>

            <div className="grid md:grid-cols-3 gap-6">
              {professionalPlans.map((plan, index) => (
                <div
                  key={index}
                  className={cn(
                    "relative rounded-2xl p-8 transition-all duration-300",
                    plan.highlighted
                      ? "glass-card shadow-glass-lg ring-2 ring-pacific-500/20 md:-mt-4 md:mb-4"
                      : "glass-card-hover"
                  )}
                >
                  {plan.badge && (
                    <div className="absolute -top-3 left-1/2 -translate-x-1/2">
                      <span className="px-3 py-1 rounded-full bg-gradient-to-r from-pacific-500 to-pacific-600 text-white text-xs font-medium shadow-lg flex items-center gap-1">
                        <Star className="h-3 w-3" />
                        {plan.badge}
                      </span>
                    </div>
                  )}

                  <div className="mb-6">
                    <h3 className="text-xl font-semibold text-slate-900 mb-2">{plan.name}</h3>
                    <p className="text-sm text-slate-600">{plan.description}</p>
                  </div>

                  <div className="mb-6">
                    <span className="text-4xl font-bold text-slate-900">{plan.price}</span>
                    <span className="text-slate-500">{plan.period}</span>
                  </div>

                  <ul className="space-y-3 mb-8">
                    {plan.features.map((feature, i) => (
                      <li key={i} className="flex items-start gap-3 text-sm text-slate-700">
                        <Check className="h-5 w-5 text-pacific-500 flex-shrink-0" />
                        {feature}
                      </li>
                    ))}
                  </ul>

                  <Button
                    variant={plan.highlighted ? "pacific" : "outline"}
                    className="w-full"
                    asChild
                  >
                    <Link href={plan.href}>{plan.cta}</Link>
                  </Button>
                </div>
              ))}
            </div>
          </div>
        </div>
      </section>

      {/* Features for Professionals */}
      <section className="py-16">
        <div className="container">
          <div className="max-w-5xl mx-auto">
            <div className="text-center mb-12">
              <h2 className="text-3xl font-semibold text-slate-900 mb-3">
                Herramientas para profesionales
              </h2>
              <p className="text-slate-600 max-w-xl mx-auto">
                Todo lo que necesitas para modernizar tu práctica legal
              </p>
            </div>

            <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
              {features.map((feature, index) => (
                <div
                  key={index}
                  className="glass-card-hover rounded-2xl p-6"
                >
                  <div className="h-12 w-12 rounded-xl bg-gradient-to-br from-pacific-100 to-pacific-50 flex items-center justify-center mb-4">
                    <feature.icon className="h-6 w-6 text-pacific-600" />
                  </div>
                  <h3 className="font-semibold text-slate-900 mb-2">{feature.title}</h3>
                  <p className="text-sm text-slate-600">{feature.description}</p>
                </div>
              ))}
            </div>
          </div>
        </div>
      </section>

      {/* Legal Disclaimer */}
      <section className="py-12">
        <div className="container">
          <div className="max-w-4xl mx-auto">
            <div className="glass-card rounded-2xl p-6 border-l-4 border-pacific-500">
              <div className="flex gap-4">
                <Shield className="h-6 w-6 text-pacific-600 flex-shrink-0 mt-0.5" />
                <div>
                  <h3 className="font-semibold text-slate-900 mb-2">Aviso Legal</h3>
                  <p className="text-sm text-slate-600 leading-relaxed">
                    Las respuestas generadas por LEIA son orientativas y no constituyen asesoría legal profesional.
                    Los documentos generados son borradores que deben ser revisados por un profesional habilitado
                    antes de su uso. LEIA SpA no se hace responsable por decisiones tomadas en base a la información
                    proporcionada. El uso de esta plataforma implica la aceptación de nuestros{" "}
                    <Link href="/terminos" className="text-pacific-600 hover:underline">Términos de Servicio</Link>.
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* CTA */}
      <section className="py-16">
        <div className="container">
          <div className="max-w-4xl mx-auto">
            <div className="relative rounded-3xl overflow-hidden">
              <div className="absolute inset-0 bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900" />
              <div className="absolute top-0 left-0 w-96 h-96 bg-pacific-500/20 rounded-full blur-3xl" />
              <div className="absolute bottom-0 right-0 w-80 h-80 bg-terracota-500/10 rounded-full blur-3xl" />

              <div className="relative p-10 lg:p-14 text-center">
                <h2 className="text-3xl font-semibold text-white mb-4">
                  ¿Tienes dudas sobre qué plan elegir?
                </h2>
                <p className="text-lg text-white/70 mb-8 max-w-xl mx-auto">
                  Conversemos. Te ayudamos a encontrar la mejor opción para ti.
                </p>

                <div className="flex flex-col sm:flex-row gap-4 justify-center">
                  <Button size="lg" variant="white" asChild>
                    <Link href="/contacto">
                      Contactar
                      <ArrowRight className="ml-2 h-5 w-5" />
                    </Link>
                  </Button>
                  <Button size="lg" variant="glass" className="text-white border-white/20 hover:bg-white/10" asChild>
                    <Link href="/chat">Probar LEIA Gratis</Link>
                  </Button>
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
