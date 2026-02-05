"use client"

import * as React from "react"
import Link from "next/link"
import { Menu, X } from "lucide-react"
import { Button } from "@/components/ui/button"
import { LeiaLogo } from "@/components/ui/leia-logo"
import { cn } from "@/lib/utils"

export function Header() {
  const [isScrolled, setIsScrolled] = React.useState(false)
  const [isMobileMenuOpen, setIsMobileMenuOpen] = React.useState(false)

  React.useEffect(() => {
    const handleScroll = () => {
      setIsScrolled(window.scrollY > 10)
    }
    window.addEventListener("scroll", handleScroll)
    return () => window.removeEventListener("scroll", handleScroll)
  }, [])

  return (
    <header
      className={cn(
        "fixed top-0 left-0 right-0 z-50 transition-all duration-500",
        isScrolled
          ? "glass-heavy shadow-glass"
          : "bg-transparent"
      )}
    >
      <div className="container">
        <nav className="flex h-16 items-center justify-between">
          {/* Logo */}
          <Link href="/">
            <LeiaLogo size="md" />
          </Link>

          {/* Desktop Navigation */}
          <div className="hidden md:flex items-center gap-1">
            <Link
              href="/chat"
              className="px-4 py-2 text-sm font-medium text-slate-600 hover:text-slate-900 hover:bg-white/50 rounded-xl transition-all duration-200"
            >
              Asistente IA
            </Link>
            <Link
              href="/abogados"
              className="px-4 py-2 text-sm font-medium text-slate-600 hover:text-slate-900 hover:bg-white/50 rounded-xl transition-all duration-200"
            >
              Abogados
            </Link>
            <Link
              href="/precios"
              className="px-4 py-2 text-sm font-medium text-slate-600 hover:text-slate-900 hover:bg-white/50 rounded-xl transition-all duration-200"
            >
              Precios
            </Link>
            <Link
              href="/unirse"
              className="px-4 py-2 text-sm font-medium text-slate-600 hover:text-slate-900 hover:bg-white/50 rounded-xl transition-all duration-200"
            >
              Trabaja con nosotros
            </Link>
          </div>

          {/* CTA Buttons */}
          <div className="hidden md:flex items-center gap-3">
            <Button variant="ghost" size="sm" className="text-slate-600" asChild>
              <Link href="/login">Ingresar</Link>
            </Button>
            <Button variant="pacific" size="sm" className="shadow-lg shadow-pacific-500/25" asChild>
              <Link href="/registro">Registrarse</Link>
            </Button>
          </div>

          {/* Mobile Menu Button */}
          <button
            onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}
            className="md:hidden p-2 text-slate-700 hover:bg-white/50 rounded-xl transition-colors"
            aria-label={isMobileMenuOpen ? "Cerrar menu" : "Abrir menu"}
          >
            {isMobileMenuOpen ? (
              <X className="h-6 w-6" />
            ) : (
              <Menu className="h-6 w-6" />
            )}
          </button>
        </nav>

        {/* Mobile Menu */}
        <div
          className={cn(
            "md:hidden overflow-hidden transition-all duration-300",
            isMobileMenuOpen ? "max-h-[400px] pb-4" : "max-h-0"
          )}
        >
          <nav className="flex flex-col gap-1 pt-4 border-t border-white/20">
            <Link
              href="/chat"
              onClick={() => setIsMobileMenuOpen(false)}
              className="px-4 py-3 text-sm font-medium text-slate-700 hover:bg-white/50 rounded-xl transition-colors"
            >
              Asistente IA
            </Link>
            <Link
              href="/abogados"
              onClick={() => setIsMobileMenuOpen(false)}
              className="px-4 py-3 text-sm font-medium text-slate-700 hover:bg-white/50 rounded-xl transition-colors"
            >
              Abogados
            </Link>
            <Link
              href="/precios"
              onClick={() => setIsMobileMenuOpen(false)}
              className="px-4 py-3 text-sm font-medium text-slate-700 hover:bg-white/50 rounded-xl transition-colors"
            >
              Precios
            </Link>
            <Link
              href="/unirse"
              onClick={() => setIsMobileMenuOpen(false)}
              className="px-4 py-3 text-sm font-medium text-slate-700 hover:bg-white/50 rounded-xl transition-colors"
            >
              Trabaja con nosotros
            </Link>
            <div className="flex flex-col gap-2 mt-4 pt-4 border-t border-white/20">
              <Button variant="ghost" asChild className="w-full justify-center">
                <Link href="/login">Ingresar</Link>
              </Button>
              <Button variant="pacific" asChild className="w-full justify-center shadow-lg shadow-pacific-500/25">
                <Link href="/registro">Registrarse</Link>
              </Button>
            </div>
          </nav>
        </div>
      </div>
    </header>
  )
}
