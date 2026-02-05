"use client"

import Link from "next/link"
import { Button } from "@/components/ui/button"
import { Header } from "@/components/layout/Header"
import { HeroSearch } from "@/components/ui/hero-search"
import { LeiaAvatar } from "@/components/ui/leia-avatar"
import { LeiaLogo } from "@/components/ui/leia-logo"
import {
  MessageSquare,
  Users,
  Brain,
  ArrowRight,
  Shield,
  CheckCircle,
  Sparkles,
  Briefcase,
  Heart,
  CreditCard,
  Home,
  ShoppingBag,
  Stethoscope,
  FileText,
  Scale,
  Zap,
  Clock,
  TrendingUp,
} from "lucide-react"
import { cn } from "@/lib/utils"

const suggestions = [
  "Me despidieron sin aviso",
  "Pension alimenticia",
  "Deudas impagas",
  "Problema con arriendo",
]

const areas = [
  { name: "Laboral", icon: Briefcase, href: "/chat?area=laboral", description: "Despidos, contratos, finiquitos" },
  { name: "Familia", icon: Heart, href: "/chat?area=familia", description: "Divorcios, custodia, pensiones" },
  { name: "Deudas", icon: CreditCard, href: "/chat?area=deudas", description: "Cobranzas, renegociacion" },
  { name: "Arriendos", icon: Home, href: "/chat?area=arriendos", description: "Contratos, desahucios" },
  { name: "Consumidor", icon: ShoppingBag, href: "/chat?area=consumidor", description: "Reclamos, garantias" },
  { name: "Salud", icon: Stethoscope, href: "/chat?area=salud", description: "ISAPRE, licencias, GES" },
  { name: "Herencias", icon: FileText, href: "/chat?area=herencias", description: "Testamentos, posesiones" },
  { name: "Penal", icon: Scale, href: "/chat?area=penal", description: "Defensas, querellas" },
]

const stats = [
  { value: "50K+", label: "Consultas resueltas", icon: MessageSquare },
  { value: "500+", label: "Abogados verificados", icon: Users },
  { value: "<60s", label: "Tiempo de respuesta", icon: Zap },
  { value: "24/7", label: "Disponibilidad", icon: Clock },
]

export default function HomePage() {
  return (
    <div className="flex flex-col min-h-screen bg-mesh">
      <Header />

      {/* Hero Section */}
      <section className="relative pt-28 lg:pt-40 pb-20 lg:pb-32 overflow-hidden">
        {/* Ambient background blobs */}
        <div className="absolute top-20 left-1/4 w-96 h-96 bg-pacific-400/20 rounded-full blur-3xl animate-pulse-glow" />
        <div className="absolute bottom-0 right-1/4 w-80 h-80 bg-terracota-400/10 rounded-full blur-3xl animate-pulse-glow" style={{ animationDelay: '1s' }} />

        <div className="container relative">
          <div className="max-w-4xl mx-auto">
            {/* Hero content with avatar */}
            <div className="flex flex-col lg:flex-row items-center justify-center gap-8 lg:gap-14 mb-12">
              {/* LEIA Avatar */}
              <div
                className="flex-shrink-0 animate-fade-in opacity-0"
                style={{ animationDelay: '0ms', animationFillMode: 'forwards' }}
              >
                <LeiaAvatar size="xl" animated />
              </div>

              {/* Text content - protagonist */}
              <div className="text-center lg:text-left">
                {/* Badge */}
                <div
                  className="inline-flex items-center gap-2 px-3 py-1.5 rounded-full bg-pacific-100 text-pacific-700 text-sm font-medium mb-4 animate-fade-in opacity-0"
                  style={{ animationDelay: '100ms', animationFillMode: 'forwards' }}
                >
                  <svg viewBox="0 0 30 20" className="h-4 w-6 rounded shadow-sm" aria-label="Chile">
                    <rect x="0" y="0" width="10" height="10" fill="#0039A6" />
                    <polygon points="5,2 6.2,5.5 9.5,5.5 6.8,7.5 7.8,11 5,8.5 2.2,11 3.2,7.5 0.5,5.5 3.8,5.5" fill="white" transform="scale(0.7) translate(2.1, 1.4)" />
                    <rect x="10" y="0" width="20" height="10" fill="white" />
                    <rect x="0" y="10" width="30" height="10" fill="#D52B1E" />
                  </svg>
                  Especializado en leyes de Chile
                </div>

                {/* Headline */}
                <h1
                  className="text-4xl sm:text-5xl lg:text-6xl font-semibold mb-3 animate-fade-in-up opacity-0"
                  style={{ animationDelay: '200ms', animationFillMode: 'forwards' }}
                >
                  <span className="text-slate-900">Hola, soy </span>
                  <span className="text-gradient">LEIA</span>
                </h1>

                <p
                  className="text-lg lg:text-xl text-slate-600 max-w-lg animate-fade-in-up opacity-0 mb-4"
                  style={{ animationDelay: '400ms', animationFillMode: 'forwards' }}
                >
                  Tu asistente legal con IA. Cuentame tu problema y te ayudo.
                </p>

                {/* Stats badge */}
                <div
                  className="inline-flex items-center gap-2 text-sm text-slate-500 animate-fade-in opacity-0"
                  style={{ animationDelay: '500ms', animationFillMode: 'forwards' }}
                >
                  <span className="flex items-center gap-1">
                    <span className="h-2 w-2 rounded-full bg-green-500 animate-pulse"></span>
                    <strong className="text-slate-700">2,847</strong> consultas esta semana
                  </span>
                </div>
              </div>
            </div>

            {/* Hero Search - menor peso visual inicial */}
            <div
              className="text-center animate-fade-in opacity-0"
              style={{ animationDelay: '700ms', animationFillMode: 'forwards' }}
            >
              <HeroSearch
                placeholder="Cuentame, ¿en que puedo ayudarte?"
                suggestions={suggestions}
              />
            </div>

            {/* Disclaimer + Trust indicators */}
            <div
              className="mt-8 animate-fade-in opacity-0"
              style={{ animationDelay: '900ms', animationFillMode: 'forwards' }}
            >
              {/* Disclaimer */}
              <div className="flex items-center justify-center gap-2 text-sm text-slate-500 mb-4">
                <Scale className="h-4 w-4 text-pacific-500" />
                <span>LEIA te orienta, pero <strong>no reemplaza</strong> a un abogado</span>
              </div>

              {/* Trust indicators */}
              <div className="flex flex-wrap justify-center gap-6">
                {[
                  { icon: CheckCircle, text: "Gratis", color: "text-green-500" },
                  { icon: Shield, text: "Confidencial", color: "text-pacific-500" },
                  { icon: Zap, text: "Respuesta inmediata", color: "text-amber-500" },
                ].map((item, index) => (
                  <div key={index} className="flex items-center gap-2 text-sm text-slate-500">
                    <item.icon className={cn("h-4 w-4", item.color)} />
                    <span>{item.text}</span>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* How it works */}
      <section className="py-24 relative">
        <div className="container">
          <div className="text-center mb-16">
            <h2 className="text-3xl lg:text-4xl font-semibold text-slate-900 mb-4">
              Asi de simple
            </h2>
            <p className="text-slate-600 max-w-xl mx-auto">
              Tres pasos para resolver tus dudas legales
            </p>
          </div>

          <div className="max-w-5xl mx-auto">
            <div className="grid md:grid-cols-3 gap-6">
              {[
                { number: 1, icon: MessageSquare, title: "Describe tu caso", description: "Cuentanos tu situacion con tus propias palabras" },
                { number: 2, icon: Brain, title: "IA te orienta", description: "Recibe informacion legal clara al instante" },
                { number: 3, icon: Users, title: "Conecta si necesitas", description: "Accede a abogados verificados" },
              ].map((step, index) => (
                <div
                  key={index}
                  className={cn(
                    "relative p-8 rounded-2xl transition-all duration-300",
                    "glass-card-hover"
                  )}
                >
                  {/* Step number */}
                  <div className="absolute -top-3 left-8">
                    <div className="h-6 w-6 rounded-full bg-gradient-to-br from-pacific-500 to-pacific-600 flex items-center justify-center text-white text-xs font-bold shadow-lg shadow-pacific-500/25">
                      {step.number}
                    </div>
                  </div>

                  {/* Icon */}
                  <div className="h-14 w-14 rounded-2xl bg-gradient-to-br from-slate-100 to-slate-50 flex items-center justify-center mb-5">
                    <step.icon className="h-7 w-7 text-pacific-600" />
                  </div>

                  <h3 className="text-lg font-semibold text-slate-900 mb-2">{step.title}</h3>
                  <p className="text-sm text-slate-600">{step.description}</p>
                </div>
              ))}
            </div>
          </div>
        </div>
      </section>

      {/* Legal Areas */}
      <section className="py-24 relative">
        {/* Background accent */}
        <div className="absolute inset-0 bg-gradient-to-b from-transparent via-pacific-50/30 to-transparent" />

        <div className="container relative">
          <div className="text-center mb-16">
            <h2 className="text-3xl lg:text-4xl font-semibold text-slate-900 mb-4">
              ¿En que te podemos ayudar?
            </h2>
            <p className="text-slate-600 max-w-xl mx-auto">
              Selecciona un area para iniciar tu consulta
            </p>
          </div>

          <div className="max-w-5xl mx-auto">
            <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
              {areas.map((area, index) => (
                <Link
                  key={index}
                  href={area.href}
                  className={cn(
                    "group relative p-5 rounded-2xl transition-all duration-300",
                    "glass-card-hover"
                  )}
                >
                  {/* Icon */}
                  <div className={cn(
                    "h-12 w-12 rounded-xl flex items-center justify-center mb-4 transition-all duration-300",
                    "bg-gradient-to-br from-pacific-100 to-pacific-50",
                    "group-hover:from-pacific-200 group-hover:to-pacific-100"
                  )}>
                    <area.icon className="h-6 w-6 text-pacific-600" />
                  </div>

                  <h3 className="font-semibold text-slate-900 mb-1">{area.name}</h3>
                  <p className="text-xs text-slate-500">{area.description}</p>

                  {/* Arrow on hover */}
                  <div className="absolute top-5 right-5 opacity-0 group-hover:opacity-100 transition-opacity">
                    <ArrowRight className="h-4 w-4 text-pacific-500" />
                  </div>
                </Link>
              ))}
            </div>
          </div>
        </div>
      </section>

      {/* Stats */}
      <section className="py-24">
        <div className="container">
          <div className="max-w-5xl mx-auto">
            <div className="glass-panel rounded-3xl p-10 lg:p-14">
              <div className="text-center mb-12">
                <p className="text-pacific-600 font-medium mb-2">Resultados</p>
                <h2 className="text-3xl font-semibold text-slate-900 flex items-center justify-center gap-3 flex-wrap">
                  Miles de chilenos ya resolvieron sus dudas
                  {/* Chilean Flag */}
                  <svg
                    viewBox="0 0 30 20"
                    className="h-6 w-9 rounded shadow-sm flex-shrink-0"
                    aria-label="Bandera de Chile"
                  >
                    {/* Blue canton */}
                    <rect x="0" y="0" width="10" height="10" fill="#0039A6" />
                    {/* White star */}
                    <polygon
                      points="5,2 6.2,5.5 9.5,5.5 6.8,7.5 7.8,11 5,8.5 2.2,11 3.2,7.5 0.5,5.5 3.8,5.5"
                      fill="white"
                      transform="scale(0.7) translate(2.1, 1.4)"
                    />
                    {/* White stripe */}
                    <rect x="10" y="0" width="20" height="10" fill="white" />
                    {/* Red stripe */}
                    <rect x="0" y="10" width="30" height="10" fill="#D52B1E" />
                  </svg>
                </h2>
              </div>

              <div className="grid grid-cols-2 lg:grid-cols-4 gap-8">
                {stats.map((stat, index) => (
                  <div key={index} className="text-center">
                    <div className="inline-flex items-center justify-center h-12 w-12 rounded-2xl bg-pacific-100/50 mb-4">
                      <stat.icon className="h-6 w-6 text-pacific-600" />
                    </div>
                    <div className="text-3xl lg:text-4xl font-semibold text-slate-900 mb-1">
                      {stat.value}
                    </div>
                    <div className="text-sm text-slate-600">{stat.label}</div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-24 relative overflow-hidden">
        {/* Glass dark panel */}
        <div className="container">
          <div className="max-w-5xl mx-auto">
            <div className="relative rounded-3xl overflow-hidden">
              {/* Background */}
              <div className="absolute inset-0 bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900" />
              <div className="absolute top-0 left-0 w-96 h-96 bg-pacific-500/20 rounded-full blur-3xl" />
              <div className="absolute bottom-0 right-0 w-80 h-80 bg-terracota-500/10 rounded-full blur-3xl" />

              {/* Content */}
              <div className="relative p-10 lg:p-16 text-center">
                <h2 className="text-3xl lg:text-4xl font-semibold text-white mb-4">
                  ¿Necesitas un abogado?
                </h2>
                <p className="text-lg text-white/70 mb-8 max-w-xl mx-auto">
                  Conecta con profesionales verificados. Precios transparentes y evaluaciones reales.
                </p>

                <div className="flex flex-col sm:flex-row gap-4 justify-center">
                  <Button size="lg" variant="white" className="shadow-xl" asChild>
                    <Link href="/abogados">
                      Ver Abogados
                      <ArrowRight className="ml-2 h-5 w-5" />
                    </Link>
                  </Button>
                  <Button size="lg" variant="glass" className="text-white border-white/20 hover:bg-white/10" asChild>
                    <Link href="/chat">Consultar Gratis</Link>
                  </Button>
                </div>

                {/* Trust badges */}
                <div className="flex flex-wrap justify-center gap-6 mt-10 text-sm text-white/60">
                  {[
                    "500+ abogados verificados",
                    "Precios transparentes",
                    "Evaluaciones reales"
                  ].map((text, index) => (
                    <div key={index} className="flex items-center gap-2">
                      <CheckCircle className="h-4 w-4 text-pacific-400" />
                      {text}
                    </div>
                  ))}
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
              {/* Logo */}
              <Link href="/">
                <LeiaLogo size="md" />
              </Link>

              {/* Links */}
              <div className="flex flex-wrap justify-center gap-8 text-sm">
                <Link href="/chat" className="text-slate-600 hover:text-slate-900 transition-colors">Asistente IA</Link>
                <Link href="/abogados" className="text-slate-600 hover:text-slate-900 transition-colors">Abogados</Link>
                <Link href="/precios" className="text-slate-600 hover:text-slate-900 transition-colors">Precios</Link>
                <Link href="/terminos" className="text-slate-600 hover:text-slate-900 transition-colors">Términos</Link>
                <Link href="/privacidad" className="text-slate-600 hover:text-slate-900 transition-colors">Privacidad</Link>
              </div>

              {/* Copyright */}
              <p className="text-sm text-slate-500 flex items-center gap-2">
                © 2025 LEIA. Hecho en Chile
                <svg
                  viewBox="0 0 30 20"
                  className="h-4 w-6 rounded shadow-sm"
                  aria-label="Bandera de Chile"
                >
                  <rect x="0" y="0" width="10" height="10" fill="#0039A6" />
                  <polygon
                    points="5,2 6.2,5.5 9.5,5.5 6.8,7.5 7.8,11 5,8.5 2.2,11 3.2,7.5 0.5,5.5 3.8,5.5"
                    fill="white"
                    transform="scale(0.7) translate(2.1, 1.4)"
                  />
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
