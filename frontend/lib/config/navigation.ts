import {
  MessageSquare,
  Bookmark,
  User,
  Scale,
  FileText,
  Bell,
  Search,
  Calendar,
  CreditCard,
  UserCircle,
  Inbox,
  BarChart3,
  Users,
  Briefcase,
  CalendarDays,
  Sparkles,
  Building2,
  Receipt,
  Settings,
  FolderOpen,
  Gavel,
  ClipboardList,
  type LucideIcon
} from 'lucide-react'

export interface NavItem {
  label: string
  href: string
  icon: LucideIcon
  badge?: number | string
  description?: string
}

// User (cliente) navigation
export const userNavigation: NavItem[] = [
  {
    label: 'Mis Casos',
    href: '/dashboard/usuario/mis-casos',
    icon: FolderOpen,
    description: 'Gestiona tus casos legales'
  },
  {
    label: 'Mis Conversaciones',
    href: '/dashboard/usuario/conversaciones',
    icon: MessageSquare,
    description: 'Historial de chats con LEIA'
  },
  {
    label: 'Consultas Guardadas',
    href: '/dashboard/usuario/consultas-guardadas',
    icon: Bookmark,
    description: 'Consultas y respuestas guardadas'
  },
  {
    label: 'Mi Perfil',
    href: '/dashboard/usuario/perfil',
    icon: User,
    description: 'Configuracion de tu cuenta'
  },
  {
    label: 'Consultas a Abogados',
    href: '/dashboard/usuario/consultas-abogados',
    icon: Scale,
    description: 'Consultas con profesionales'
  },
  {
    label: 'Documentos',
    href: '/dashboard/usuario/documentos',
    icon: FileText,
    description: 'Documentos generados'
  },
  {
    label: 'Notificaciones',
    href: '/dashboard/usuario/notificaciones',
    icon: Bell,
    description: 'Alertas y avisos'
  },
  {
    label: 'Seguimiento de Casos',
    href: '/dashboard/usuario/seguimiento-casos',
    icon: Search,
    description: 'Estado de tus casos'
  },
  {
    label: 'Causas Poder Judicial',
    href: '/dashboard/usuario/causas-pjud',
    icon: Gavel,
    description: 'Sincroniza tus causas del PJUD'
  },
  {
    label: 'Citas',
    href: '/dashboard/usuario/citas',
    icon: Calendar,
    description: 'Citas programadas'
  },
  {
    label: 'Pagos y Facturas',
    href: '/dashboard/usuario/pagos',
    icon: CreditCard,
    description: 'Historial de pagos'
  }
]

// Common navigation items for all lawyers (abogado, procurador, estudio)
const commonLawyerNavigation: NavItem[] = [
  {
    label: 'Mi Perfil Publico',
    href: '/dashboard/profesional/perfil-publico',
    icon: UserCircle,
    description: 'Tu perfil visible para clientes'
  },
  {
    label: 'Solicitudes',
    href: '/dashboard/profesional/solicitudes',
    icon: Inbox,
    description: 'Solicitudes de consulta'
  },
  {
    label: 'Estadisticas',
    href: '/dashboard/profesional/estadisticas',
    icon: BarChart3,
    description: 'Metricas y rendimiento'
  },
  {
    label: 'CRM Clientes',
    href: '/dashboard/profesional/crm',
    icon: Users,
    description: 'Gestion de clientes'
  },
  {
    label: 'Gestion de Casos',
    href: '/dashboard/profesional/casos',
    icon: Briefcase,
    description: 'Administra tus casos'
  },
  {
    label: 'Calendario',
    href: '/dashboard/profesional/calendario',
    icon: CalendarDays,
    description: 'Agenda y citas'
  },
  {
    label: 'Configuracion',
    href: '/dashboard/profesional/configuracion',
    icon: Settings,
    description: 'Ajustes de comunicacion'
  }
]

// Full lawyer navigation (abogado) - has all features
export const lawyerNavigation: NavItem[] = [
  ...commonLawyerNavigation,
  {
    label: 'LEIA Escritos',
    href: '/dashboard/profesional/leia-escritos',
    icon: Sparkles,
    description: 'IA para documentos legales'
  },
  {
    label: 'Poder Judicial',
    href: '/dashboard/profesional/poder-judicial',
    icon: Building2,
    description: 'Conexion con tribunales'
  },
  {
    label: 'Facturacion',
    href: '/dashboard/profesional/facturacion',
    icon: Receipt,
    description: 'Ingresos y facturas'
  }
]

// Procurador navigation - limited functions (court procedures only)
export const procuradorNavigation: NavItem[] = [
  {
    label: 'Mi Perfil Publico',
    href: '/dashboard/profesional/perfil-publico',
    icon: UserCircle,
    description: 'Tu perfil visible para clientes'
  },
  {
    label: 'Solicitudes',
    href: '/dashboard/profesional/solicitudes',
    icon: Inbox,
    description: 'Solicitudes de tramites'
  },
  {
    label: 'Tramites Activos',
    href: '/dashboard/profesional/tramites',
    icon: ClipboardList,
    description: 'Tramites en proceso'
  },
  {
    label: 'Poder Judicial',
    href: '/dashboard/profesional/poder-judicial',
    icon: Building2,
    description: 'Conexion con tribunales'
  },
  {
    label: 'Calendario',
    href: '/dashboard/profesional/calendario',
    icon: CalendarDays,
    description: 'Agenda de diligencias'
  },
  {
    label: 'Estadisticas',
    href: '/dashboard/profesional/estadisticas',
    icon: BarChart3,
    description: 'Metricas de tramites'
  },
  {
    label: 'Facturacion',
    href: '/dashboard/profesional/facturacion',
    icon: Receipt,
    description: 'Ingresos y facturas'
  },
  {
    label: 'Configuracion',
    href: '/dashboard/profesional/configuracion',
    icon: Settings,
    description: 'Ajustes de comunicacion'
  }
]

// Law firm (estudio juridico) navigation - management focus
export const estudioNavigation: NavItem[] = [
  {
    label: 'Perfil del Estudio',
    href: '/dashboard/profesional/perfil-publico',
    icon: Building2,
    description: 'Perfil visible del estudio'
  },
  {
    label: 'Solicitudes',
    href: '/dashboard/profesional/solicitudes',
    icon: Inbox,
    description: 'Solicitudes entrantes'
  },
  {
    label: 'Gestion de Casos',
    href: '/dashboard/profesional/casos',
    icon: Briefcase,
    description: 'Casos del estudio'
  },
  {
    label: 'Equipo',
    href: '/dashboard/profesional/equipo',
    icon: Users,
    description: 'Abogados y procuradores'
  },
  {
    label: 'CRM Clientes',
    href: '/dashboard/profesional/crm',
    icon: Users,
    description: 'Base de clientes'
  },
  {
    label: 'LEIA Escritos',
    href: '/dashboard/profesional/leia-escritos',
    icon: Sparkles,
    description: 'IA para documentos legales'
  },
  {
    label: 'Poder Judicial',
    href: '/dashboard/profesional/poder-judicial',
    icon: Building2,
    description: 'Conexion con tribunales'
  },
  {
    label: 'Calendario',
    href: '/dashboard/profesional/calendario',
    icon: CalendarDays,
    description: 'Agenda del estudio'
  },
  {
    label: 'Estadisticas',
    href: '/dashboard/profesional/estadisticas',
    icon: BarChart3,
    description: 'Metricas globales'
  },
  {
    label: 'Facturacion',
    href: '/dashboard/profesional/facturacion',
    icon: Receipt,
    description: 'Finanzas del estudio'
  },
  {
    label: 'Configuracion',
    href: '/dashboard/profesional/configuracion',
    icon: Settings,
    description: 'Ajustes del estudio'
  }
]

// Helper function to get navigation by professional type
export function getNavigationByProfessionalType(professionalType: string | null): NavItem[] {
  switch (professionalType) {
    case 'procurador':
      return procuradorNavigation
    case 'estudio':
      return estudioNavigation
    case 'abogado':
    default:
      return lawyerNavigation
  }
}

// Helper function to get role label by professional type
export function getProfessionalTypeLabel(professionalType: string | null): string {
  switch (professionalType) {
    case 'procurador':
      return 'Procurador/a'
    case 'estudio':
      return 'Estudio Juridico'
    case 'abogado':
    default:
      return 'Abogado/a'
  }
}
