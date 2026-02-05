'use client'

import { useState, useEffect } from 'react'
import Link from 'next/link'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { Star, MapPin, Briefcase, ArrowLeft, MessageSquare, Search, Loader2, Sparkles, CheckCircle } from 'lucide-react'
import { LeiaLogo } from '@/components/ui/leia-logo'
import { ConsultationModal } from '@/components/ui/consultation-modal'
import { cn } from '@/lib/utils'

// API URL from environment variable with fallback
const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

// Specialties and locations for filters
const SPECIALTIES = [
  "Todas las especialidades",
  "Derecho Laboral",
  "Derecho de Familia",
  "Deudas y Cobranzas",
  "Derecho del Consumidor",
  "Arriendos",
  "Herencias"
]

const LOCATIONS = [
  "Todas las ubicaciones",
  "Santiago Centro",
  "Las Condes",
  "Providencia",
  "Maipu",
  "Nunoa"
]

interface Lawyer {
  id: number
  name: string
  specialty: string
  experience: string | null
  rating: number
  reviews: number
  location: string | null
  price_min: number | null
  price_max: number | null
  price: string | null
  image: string | null
  cases: number
  success_rate: number | null
  description: string | null
  is_verified: boolean
}

interface LawyerListResponse {
  lawyers: Lawyer[]
  total: number
  page: number
  page_size: number
}

export default function AbogadosPage() {
  const [lawyers, setLawyers] = useState<Lawyer[]>([])
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [selectedSpecialty, setSelectedSpecialty] = useState("Todas las especialidades")
  const [selectedLocation, setSelectedLocation] = useState("Todas las ubicaciones")
  const [searchTerm, setSearchTerm] = useState("")
  const [debouncedSearch, setDebouncedSearch] = useState("")
  const [selectedLawyer, setSelectedLawyer] = useState<Lawyer | null>(null)
  const [isModalOpen, setIsModalOpen] = useState(false)
  const [totalLawyers, setTotalLawyers] = useState(0)
  const [searchFocused, setSearchFocused] = useState(false)

  // Debounce search input
  useEffect(() => {
    const timer = setTimeout(() => {
      setDebouncedSearch(searchTerm)
    }, 300)
    return () => clearTimeout(timer)
  }, [searchTerm])

  // Fetch lawyers when filters change
  useEffect(() => {
    const fetchLawyers = async () => {
      setIsLoading(true)
      setError(null)

      try {
        const params = new URLSearchParams()
        if (selectedSpecialty !== "Todas las especialidades") {
          params.append('specialty', selectedSpecialty)
        }
        if (selectedLocation !== "Todas las ubicaciones") {
          params.append('location', selectedLocation)
        }
        if (debouncedSearch) {
          params.append('search', debouncedSearch)
        }

        const url = `${API_URL}/api/lawyers${params.toString() ? `?${params.toString()}` : ''}`
        const response = await fetch(url)

        if (!response.ok) {
          throw new Error('Error al cargar los abogados')
        }

        const data: LawyerListResponse = await response.json()
        setLawyers(data.lawyers)
        setTotalLawyers(data.total)
      } catch (err) {
        console.error('Error fetching lawyers:', err)
        setError('No se pudieron cargar los abogados. Verifica que el servidor este corriendo.')
      } finally {
        setIsLoading(false)
      }
    }

    fetchLawyers()
  }, [selectedSpecialty, selectedLocation, debouncedSearch])

  const handleConsultationClick = (lawyer: Lawyer) => {
    setSelectedLawyer(lawyer)
    setIsModalOpen(true)
  }

  const handleModalClose = () => {
    setIsModalOpen(false)
    setSelectedLawyer(null)
  }

  return (
    <div className="flex flex-col min-h-screen bg-mesh">
      {/* Ambient background blobs */}
      <div className="fixed top-20 left-1/4 w-96 h-96 bg-pacific-400/10 rounded-full blur-3xl pointer-events-none" />
      <div className="fixed bottom-40 right-1/3 w-80 h-80 bg-terracota-400/5 rounded-full blur-3xl pointer-events-none" />

      {/* Glass Header */}
      <header className="glass-heavy shadow-glass sticky top-0 z-10">
        <div className="container flex h-16 items-center justify-between">
          <Link href="/">
            <LeiaLogo size="md" />
          </Link>
          <div className="flex items-center gap-3">
            <Button variant="glass" size="sm" asChild>
              <Link href="/chat">
                <Sparkles className="h-4 w-4 mr-2" />
                Asistente IA
              </Link>
            </Button>
            <Button variant="glass" size="sm" asChild>
              <Link href="/">
                <ArrowLeft className="h-4 w-4 mr-2" />
                Volver
              </Link>
            </Button>
          </div>
        </div>
      </header>

      <main className="flex-1 relative">
        {/* Hero Section */}
        <section className="py-16 px-4 relative">
          <div className="container">
            <div className="max-w-3xl mx-auto text-center">
              <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full glass-button mb-6">
                <CheckCircle className="h-4 w-4 text-pacific-500" />
                <span className="text-sm font-medium text-slate-700">Abogados Verificados</span>
              </div>

              <h1 className="text-4xl lg:text-5xl font-semibold text-slate-900 mb-4">
                Encuentra el abogado
                <br />
                <span className="text-gradient">perfecto para tu caso</span>
              </h1>
              <p className="text-lg text-slate-600 mb-8 max-w-xl mx-auto">
                Profesionales verificados, precios transparentes y contacto directo
              </p>

              {/* Glass Search and Filters */}
              <div className="max-w-2xl mx-auto">
                <div
                  className={cn(
                    "glass-card rounded-2xl p-4 transition-all duration-300 mb-4",
                    searchFocused && "shadow-glass-lg glow-pacific"
                  )}
                >
                  <div className="relative">
                    <Search className="absolute left-4 top-1/2 transform -translate-y-1/2 h-5 w-5 text-slate-400" />
                    <input
                      type="text"
                      placeholder="Buscar por nombre..."
                      value={searchTerm}
                      onChange={(e) => setSearchTerm(e.target.value)}
                      onFocus={() => setSearchFocused(true)}
                      onBlur={() => setSearchFocused(false)}
                      className="w-full pl-12 pr-4 py-3 bg-transparent border-0 text-slate-800 placeholder:text-slate-400 focus:outline-none focus:ring-0 text-base"
                    />
                  </div>
                </div>

                {/* Filter Dropdowns */}
                <div className="flex flex-col sm:flex-row gap-3 justify-center">
                  <select
                    className="px-4 py-2.5 glass-button rounded-xl text-slate-700 focus:outline-none focus:ring-2 focus:ring-pacific-400 appearance-none cursor-pointer"
                    value={selectedSpecialty}
                    onChange={(e) => setSelectedSpecialty(e.target.value)}
                  >
                    {SPECIALTIES.map((specialty) => (
                      <option key={specialty} value={specialty}>
                        {specialty}
                      </option>
                    ))}
                  </select>

                  <select
                    className="px-4 py-2.5 glass-button rounded-xl text-slate-700 focus:outline-none focus:ring-2 focus:ring-pacific-400 appearance-none cursor-pointer"
                    value={selectedLocation}
                    onChange={(e) => setSelectedLocation(e.target.value)}
                  >
                    {LOCATIONS.map((location) => (
                      <option key={location} value={location}>
                        {location}
                      </option>
                    ))}
                  </select>
                </div>
              </div>

              <div className="flex flex-wrap items-center justify-center gap-6 mt-8 text-sm text-slate-500">
                <div className="flex items-center gap-2">
                  <Star className="h-4 w-4 fill-amber-400 text-amber-400" />
                  <span>Todos verificados</span>
                </div>
                <div className="flex items-center gap-2">
                  <Briefcase className="h-4 w-4 text-pacific-500" />
                  <span>{totalLawyers > 0 ? `${totalLawyers} abogados disponibles` : 'Cargando...'}</span>
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* Lista de Abogados */}
        <section className="py-12 px-4">
          <div className="container">
            {/* Loading State */}
            {isLoading && (
              <div className="flex flex-col items-center justify-center py-12">
                <div className="glass-card p-6 rounded-2xl">
                  <Loader2 className="h-8 w-8 animate-spin text-pacific-600 mb-4 mx-auto" />
                  <p className="text-slate-600">Cargando abogados...</p>
                </div>
              </div>
            )}

            {/* Error State */}
            {error && !isLoading && (
              <div className="flex flex-col items-center justify-center py-12">
                <div className="glass-card p-6 rounded-2xl text-center">
                  <p className="text-terracota-600 mb-4">{error}</p>
                  <Button variant="pacific" onClick={() => window.location.reload()}>
                    Reintentar
                  </Button>
                </div>
              </div>
            )}

            {/* Empty State */}
            {!isLoading && !error && lawyers.length === 0 && (
              <div className="flex flex-col items-center justify-center py-12">
                <div className="glass-card p-8 rounded-2xl text-center max-w-md">
                  <p className="text-slate-600 mb-4">
                    No se encontraron abogados con los filtros seleccionados.
                  </p>
                  <Button
                    variant="glass"
                    onClick={() => {
                      setSelectedSpecialty("Todas las especialidades")
                      setSelectedLocation("Todas las ubicaciones")
                      setSearchTerm("")
                    }}
                  >
                    Limpiar filtros
                  </Button>
                </div>
              </div>
            )}

            {/* Lawyers Grid */}
            {!isLoading && !error && lawyers.length > 0 && (
              <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3 max-w-6xl mx-auto">
                {lawyers.map((lawyer) => (
                  <div
                    key={lawyer.id}
                    className="glass-card-hover rounded-2xl overflow-hidden transition-all duration-300"
                  >
                    <div className="p-6">
                      {/* Header */}
                      <div className="flex items-start gap-4 mb-4">
                        <img
                          src={lawyer.image || 'https://via.placeholder.com/64'}
                          alt={lawyer.name}
                          className="w-16 h-16 rounded-xl object-cover shadow-lg"
                        />
                        <div className="flex-1 min-w-0">
                          <h3 className="font-semibold text-lg text-slate-900 mb-1 truncate">{lawyer.name}</h3>
                          <Badge variant="pacific" className="mb-2">
                            {lawyer.specialty}
                          </Badge>
                          <div className="flex items-center gap-1 text-sm">
                            <Star className="h-4 w-4 fill-amber-400 text-amber-400" />
                            <span className="font-semibold text-slate-900">{lawyer.rating.toFixed(1)}</span>
                            <span className="text-slate-500">({lawyer.reviews})</span>
                          </div>
                        </div>
                      </div>

                      {/* Description */}
                      <p className="text-sm text-slate-600 mb-4 line-clamp-2">{lawyer.description}</p>

                      {/* Details */}
                      <div className="space-y-2 text-sm mb-4">
                        <div className="flex items-center gap-2 text-slate-500">
                          <MapPin className="h-4 w-4 text-pacific-500" />
                          <span>{lawyer.location || 'No especificada'}</span>
                        </div>
                        <div className="flex items-center gap-2 text-slate-500">
                          <Briefcase className="h-4 w-4 text-pacific-500" />
                          <span>{lawyer.experience || 'No especificada'}</span>
                        </div>
                      </div>

                      {/* Stats */}
                      <div className="flex items-center justify-between py-3 border-t border-slate-200/50">
                        <div>
                          <div className="text-xs text-slate-500">Honorarios</div>
                          <div className="font-semibold text-slate-900">{lawyer.price || 'Consultar'}</div>
                        </div>
                        <div className="text-right">
                          <div className="text-xs text-slate-500">Tasa de exito</div>
                          <div className="font-semibold text-green-600">
                            {lawyer.success_rate ? `${lawyer.success_rate}%` : 'N/A'}
                          </div>
                        </div>
                      </div>

                      {/* CTA */}
                      <Button
                        className="w-full mt-4 shadow-lg shadow-pacific-500/25"
                        variant="pacific"
                        onClick={() => handleConsultationClick(lawyer)}
                      >
                        Solicitar Consulta
                      </Button>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        </section>

        {/* CTA Section */}
        <section className="py-16 px-4">
          <div className="container">
            <div className="max-w-3xl mx-auto">
              <div className="relative rounded-3xl overflow-hidden">
                {/* Background */}
                <div className="absolute inset-0 bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900" />
                <div className="absolute top-0 left-0 w-64 h-64 bg-pacific-500/20 rounded-full blur-3xl" />
                <div className="absolute bottom-0 right-0 w-48 h-48 bg-terracota-500/10 rounded-full blur-3xl" />

                {/* Content */}
                <div className="relative p-10 lg:p-14 text-center">
                  <h2 className="text-2xl lg:text-3xl font-semibold text-white mb-4">
                    ¿No encuentras lo que buscas?
                  </h2>
                  <p className="text-white/70 mb-8 max-w-md mx-auto">
                    Habla con LEIA, nuestra IA legal, y te ayudara a encontrar el abogado perfecto para tu caso
                  </p>
                  <Button size="lg" variant="white" className="shadow-xl" asChild>
                    <Link href="/chat">
                      <Sparkles className="h-5 w-5 mr-2" />
                      Hablar con LEIA
                    </Link>
                  </Button>
                </div>
              </div>
            </div>
          </div>
        </section>
      </main>

      {/* Glass Footer */}
      <footer className="glass-heavy py-8 px-4">
        <div className="container">
          <div className="flex flex-col md:flex-row justify-between items-center gap-4">
            <Link href="/">
              <LeiaLogo size="sm" />
            </Link>
            <p className="text-sm text-slate-500">
              © 2025 LEIA. Hecho en Chile.
            </p>
            <div className="flex gap-6">
              <Link href="/privacy" className="text-sm text-slate-500 hover:text-slate-900 transition-colors">
                Privacidad
              </Link>
              <Link href="/terms" className="text-sm text-slate-500 hover:text-slate-900 transition-colors">
                Terminos
              </Link>
            </div>
          </div>
        </div>
      </footer>

      {/* Consultation Modal */}
      <ConsultationModal
        isOpen={isModalOpen}
        onClose={handleModalClose}
        lawyer={selectedLawyer}
      />
    </div>
  )
}
