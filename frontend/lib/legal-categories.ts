/**
 * Categorías legales para LEIA
 * Define las áreas de práctica y subcategorías
 */

import {
  Briefcase,
  Users,
  FileText,
  Home,
  CreditCard,
  ShoppingBag,
  Shield,
  Globe,
  Building,
  Calculator,
  Lightbulb,
  Stamp,
  Scroll,
  Landmark,
  Umbrella,
  Scale,
  LucideIcon
} from 'lucide-react'

export interface LegalCategory {
  id: string
  name: string
  description: string
  icon: LucideIcon
  color: string
  subcategories: string[]
}

export const LEGAL_CATEGORIES: LegalCategory[] = [
  {
    id: 'laboral',
    name: 'Laboral',
    description: 'Despidos, finiquitos, contratos de trabajo',
    icon: Briefcase,
    color: 'bg-blue-500',
    subcategories: [
      'Despido',
      'Finiquito',
      'Autodespido',
      'Nulidad del despido',
      'Tutela laboral',
      'Accidentes del trabajo',
      'Licencias médicas',
      'Remuneraciones y horas extra'
    ]
  },
  {
    id: 'familia',
    name: 'Familia',
    description: 'Pensión, divorcio, custodia, VIF',
    icon: Users,
    color: 'bg-pink-500',
    subcategories: [
      'Pensión de alimentos',
      'Relación directa y regular',
      'Cuidado personal',
      'Divorcio',
      'Compensación económica',
      'Violencia intrafamiliar',
      'Adopción'
    ]
  },
  {
    id: 'civil',
    name: 'Civil y Contratos',
    description: 'Contratos, indemnizaciones, cobros',
    icon: FileText,
    color: 'bg-slate-500',
    subcategories: [
      'Incumplimiento contractual',
      'Indemnización de perjuicios',
      'Cobro de pesos',
      'Responsabilidad civil',
      'Promesas y compraventas',
      'Servicios'
    ]
  },
  {
    id: 'arriendos',
    name: 'Arriendos',
    description: 'Contratos, desahucio, garantías',
    icon: Home,
    color: 'bg-amber-500',
    subcategories: [
      'Término de arriendo',
      'Desahucio',
      'No pago de arriendo',
      'Garantía y mes de garantía',
      'Daños a la propiedad',
      'Copropiedad y administración',
      'Compraventa de inmuebles'
    ]
  },
  {
    id: 'deudas',
    name: 'Deudas y Cobranza',
    description: 'Embargos, DICOM, prescripción',
    icon: CreditCard,
    color: 'bg-red-500',
    subcategories: [
      'Pagaré, letra y cheque',
      'Embargo',
      'Prescripción de deudas',
      'Repactaciones',
      'Cobranza extrajudicial',
      'DICOM y boletín comercial'
    ]
  },
  {
    id: 'consumidor',
    name: 'Consumidor',
    description: 'SERNAC, garantías, reclamos',
    icon: ShoppingBag,
    color: 'bg-green-500',
    subcategories: [
      'Garantía legal',
      'Derecho a retracto',
      'Incumplimiento de compra o servicio',
      'Estafas comerciales',
      'Pasajes y viajes',
      'Telecomunicaciones',
      'Reclamos SERNAC'
    ]
  },
  {
    id: 'penal',
    name: 'Penal',
    description: 'Denuncias, querellas, defensa',
    icon: Shield,
    color: 'bg-purple-500',
    subcategories: [
      'Denuncias',
      'Querellas',
      'Citaciones',
      'Medidas cautelares',
      'Delitos económicos simples'
    ]
  },
  {
    id: 'migracion',
    name: 'Migración',
    description: 'Visas, permisos, extranjería',
    icon: Globe,
    color: 'bg-cyan-500',
    subcategories: [
      'Visas',
      'Prórrogas',
      'Permanencia definitiva',
      'Rechazos migratorios',
      'Recursos administrativos'
    ]
  },
  {
    id: 'administrativo',
    name: 'Administrativo',
    description: 'Municipalidades, permisos, multas',
    icon: Building,
    color: 'bg-gray-500',
    subcategories: [
      'Municipalidades',
      'Sumarios administrativos',
      'Permisos',
      'Sanciones',
      'Reclamos ante servicios públicos',
      'Recursos administrativos'
    ]
  },
  {
    id: 'tributario',
    name: 'Tributario',
    description: 'SII, impuestos, fiscalizaciones',
    icon: Calculator,
    color: 'bg-emerald-500',
    subcategories: [
      'SII y fiscalizaciones',
      'RAV',
      'Reposición administrativa',
      'Reclamación en TTA',
      'Multas tributarias',
      'IVA y boletas'
    ]
  },
  {
    id: 'societario',
    name: 'Empresas',
    description: 'Sociedades, socios, contratos',
    icon: Users,
    color: 'bg-indigo-500',
    subcategories: [
      'Constitución de sociedades',
      'Pactos de socios',
      'Contratos comerciales',
      'Términos y condiciones',
      'Políticas de privacidad'
    ]
  },
  {
    id: 'propiedad_intelectual',
    name: 'Marcas y Patentes',
    description: 'Registro, oposiciones, licencias',
    icon: Lightbulb,
    color: 'bg-yellow-500',
    subcategories: [
      'Registro de marca',
      'Oposición a marca',
      'Infracciones',
      'Uso indebido',
      'Licencias'
    ]
  },
  {
    id: 'notarial',
    name: 'Notarial',
    description: 'Escrituras, poderes, trámites',
    icon: Stamp,
    color: 'bg-orange-500',
    subcategories: [
      'Escrituras simples',
      'Poderes',
      'Autorizaciones',
      'Herencias simples',
      'Posesión efectiva'
    ]
  },
  {
    id: 'sucesiones',
    name: 'Herencias',
    description: 'Testamentos, partición, posesión',
    icon: Scroll,
    color: 'bg-stone-500',
    subcategories: [
      'Posesión efectiva',
      'Partición de bienes',
      'Testamentos',
      'Deudas hereditarias'
    ]
  },
  {
    id: 'bancario',
    name: 'Bancario',
    description: 'Créditos, fraudes, renegociación',
    icon: Landmark,
    color: 'bg-teal-500',
    subcategories: [
      'Créditos',
      'Cláusulas abusivas',
      'Renegociación de deudas',
      'Fraudes bancarios',
      'Seguros asociados'
    ]
  },
  {
    id: 'seguros',
    name: 'Seguros',
    description: 'Siniestros, rechazos, coberturas',
    icon: Umbrella,
    color: 'bg-sky-500',
    subcategories: [
      'Rechazo de cobertura',
      'Siniestros',
      'Seguros de auto',
      'Seguros de salud',
      'Seguros de vida'
    ]
  }
]

// Categorías principales para mostrar en home (las más comunes)
export const MAIN_CATEGORIES = LEGAL_CATEGORIES.filter(cat =>
  ['laboral', 'familia', 'civil', 'arriendos', 'deudas', 'consumidor', 'penal', 'migracion'].includes(cat.id)
)

// Helper para obtener una categoría por ID
export function getCategoryById(id: string): LegalCategory | undefined {
  return LEGAL_CATEGORIES.find(cat => cat.id === id)
}

// Helper para obtener el ícono por nombre (para datos del backend)
export function getCategoryIcon(categoryName: string): LucideIcon {
  const category = LEGAL_CATEGORIES.find(
    cat => cat.name.toLowerCase() === categoryName.toLowerCase() ||
           cat.id === categoryName.toLowerCase()
  )
  return category?.icon || Scale
}
