"use client"

import Link from "next/link"
import { Header } from "@/components/layout/Header"
import { FileText, AlertTriangle, ChevronRight } from "lucide-react"
import { LeiaLogo } from "@/components/ui/leia-logo"

const sections = [
  {
    id: 1,
    title: "Aceptacion de los Terminos",
    content: `Al acceder y utilizar los servicios de LEIA SpA ("LEIA", "nosotros", "nuestro"), usted ("Usuario", "usted") acepta estos Terminos de Servicio en su totalidad. Si no esta de acuerdo con estos terminos, no debe utilizar nuestros servicios.`
  },
  {
    id: 2,
    title: "Descripcion del Servicio",
    content: `LEIA proporciona los siguientes servicios:`,
    list: [
      { bold: "Asistente Legal IA:", text: "Orientacion legal automatizada mediante inteligencia artificial especializada en derecho chileno." },
      { bold: "Directorio de Abogados:", text: "Plataforma para conectar usuarios con profesionales legales verificados." },
      { bold: "Herramientas para Profesionales:", text: "CRM legal, generacion de documentos y conexion con el Poder Judicial." }
    ]
  },
  {
    id: 3,
    title: "Naturaleza de la Informacion",
    highlight: "Las respuestas proporcionadas por LEIA son meramente orientativas y no constituyen asesoria legal profesional.",
    list: [
      { text: "La informacion generada por IA es de caracter general y educativo." },
      { text: "No se establece relacion abogado-cliente entre LEIA y el usuario." },
      { text: "Los documentos generados son borradores que requieren revision profesional." },
      { text: "Para casos especificos, recomendamos consultar con un abogado habilitado." }
    ]
  },
  {
    id: 4,
    title: "Limitacion de Responsabilidad",
    content: "LEIA SpA no sera responsable por:",
    list: [
      { text: "Decisiones tomadas en base a la informacion proporcionada por el servicio." },
      { text: "Resultados de procesos judiciales o administrativos." },
      { text: "Perdidas economicas, danos directos o indirectos derivados del uso del servicio." },
      { text: "Errores, omisiones o inexactitudes en la informacion generada." },
      { text: "Acciones u omisiones de los abogados listados en la plataforma." },
      { text: "Interrupciones o fallas tecnicas del servicio." }
    ],
    footer: "El usuario reconoce que utiliza LEIA bajo su propio riesgo y responsabilidad."
  },
  {
    id: 5,
    title: "Uso del Servicio",
    content: "El usuario se compromete a:",
    list: [
      { text: "Proporcionar informacion veraz y actualizada." },
      { text: "No utilizar el servicio para fines ilegales o fraudulentos." },
      { text: "No intentar vulnerar la seguridad de la plataforma." },
      { text: "No compartir su cuenta con terceros." },
      { text: "Mantener la confidencialidad de sus credenciales." }
    ]
  },
  {
    id: 6,
    title: "Propiedad Intelectual",
    content: "Todos los derechos de propiedad intelectual sobre LEIA, incluyendo software, diseno, marcas y contenido, pertenecen a LEIA SpA. El usuario no adquiere ningun derecho de propiedad sobre el servicio."
  },
  {
    id: 7,
    title: "Privacidad y Datos Personales",
    content: "El tratamiento de datos personales se rige por nuestra Politica de Privacidad, la cual forma parte integral de estos terminos. LEIA cumple con la Ley 19.628 sobre Proteccion de la Vida Privada de Chile.",
    link: { href: "/privacidad", text: "Ver Politica de Privacidad" }
  },
  {
    id: 8,
    title: "Planes y Pagos",
    list: [
      { text: "Los precios estan expresados en pesos chilenos e incluyen IVA." },
      { text: "Los pagos se procesan de forma segura a traves de proveedores certificados." },
      { text: "Las suscripciones se renuevan automaticamente salvo cancelacion previa." },
      { text: "No hay reembolsos por periodos parciales no utilizados." },
      { text: "LEIA se reserva el derecho de modificar precios con aviso previo de 30 dias." }
    ]
  },
  {
    id: 9,
    title: "Para Profesionales Legales",
    content: "Los abogados, procuradores y estudios juridicos que utilicen LEIA:",
    list: [
      { text: "Declaran estar habilitados para ejercer en Chile." },
      { text: "Son responsables de verificar y aprobar todo documento antes de su uso." },
      { text: "Mantienen su independencia profesional y responsabilidad etica." },
      { text: "Se comprometen a mantener actualizada su informacion de perfil." }
    ]
  },
  {
    id: 10,
    title: "Modificaciones",
    content: "LEIA se reserva el derecho de modificar estos terminos en cualquier momento. Los cambios seran notificados por correo electronico y/o mediante aviso en la plataforma. El uso continuado del servicio implica aceptacion de las modificaciones."
  },
  {
    id: 11,
    title: "Terminacion",
    content: "LEIA puede suspender o terminar el acceso al servicio por incumplimiento de estos terminos, sin previo aviso ni responsabilidad. El usuario puede cancelar su cuenta en cualquier momento desde su configuracion."
  },
  {
    id: 12,
    title: "Ley Aplicable y Jurisdiccion",
    content: "Estos terminos se rigen por las leyes de la Republica de Chile. Para cualquier controversia, las partes se someten a la jurisdiccion de los tribunales ordinarios de Santiago de Chile."
  },
  {
    id: 13,
    title: "Contacto",
    content: "Para consultas sobre estos terminos, puede contactarnos en:",
    list: [
      { bold: "Email:", text: "legal@leia.cl" },
      { bold: "Direccion:", text: "Santiago, Chile" }
    ]
  }
]

export default function TerminosPage() {
  return (
    <div className="flex flex-col min-h-screen bg-mesh">
      <Header />

      {/* Hero */}
      <section className="relative pt-28 lg:pt-36 pb-8">
        <div className="container">
          <div className="max-w-3xl mx-auto text-center">
            <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-pacific-100/50 text-pacific-700 text-sm font-medium mb-4">
              <FileText className="h-4 w-4" />
              Documento Legal
            </div>
            <h1 className="text-4xl font-semibold text-slate-900 mb-4">
              Terminos de Servicio
            </h1>
            <p className="text-slate-600">
              Ultima actualizacion: Febrero 2025
            </p>
          </div>
        </div>
      </section>

      {/* Aviso importante */}
      <section className="py-4">
        <div className="container">
          <div className="max-w-3xl mx-auto">
            <div className="p-5 rounded-2xl bg-amber-50 border border-amber-200">
              <div className="flex gap-4">
                <AlertTriangle className="h-6 w-6 text-amber-600 flex-shrink-0" />
                <div>
                  <p className="font-semibold text-amber-900 text-lg">Aviso Importante</p>
                  <p className="text-amber-800 mt-2 leading-relaxed">
                    LEIA es una herramienta de orientacion legal y <strong>no reemplaza la asesoria de un abogado</strong>.
                    Las respuestas generadas por inteligencia artificial son orientativas y no constituyen
                    asesoria legal profesional vinculante.
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Content */}
      <section className="py-8">
        <div className="container">
          <div className="max-w-3xl mx-auto space-y-6">
            {sections.map((section) => (
              <div key={section.id} className="glass-card rounded-2xl p-6 lg:p-8">
                <h2 className="text-xl font-semibold text-slate-900 mb-4 flex items-center gap-3">
                  <span className="flex items-center justify-center w-8 h-8 rounded-full bg-pacific-100 text-pacific-700 text-sm font-bold">
                    {section.id}
                  </span>
                  {section.title}
                </h2>

                {section.highlight && (
                  <p className="text-pacific-700 font-medium bg-pacific-50 p-4 rounded-xl mb-4">
                    {section.highlight}
                  </p>
                )}

                {section.content && (
                  <p className="text-slate-600 leading-relaxed mb-4">
                    {section.content}
                  </p>
                )}

                {section.list && (
                  <ul className="space-y-3">
                    {section.list.map((item, idx) => (
                      <li key={idx} className="flex items-start gap-3 text-slate-600">
                        <ChevronRight className="h-5 w-5 text-pacific-500 flex-shrink-0 mt-0.5" />
                        <span>
                          {'bold' in item && item.bold && <strong className="text-slate-800">{item.bold} </strong>}
                          {item.text}
                        </span>
                      </li>
                    ))}
                  </ul>
                )}

                {section.footer && (
                  <p className="text-slate-700 font-medium mt-4 pt-4 border-t border-slate-200">
                    {section.footer}
                  </p>
                )}

                {section.link && (
                  <Link
                    href={section.link.href}
                    className="inline-flex items-center gap-2 mt-4 text-pacific-600 hover:text-pacific-700 font-medium"
                  >
                    {section.link.text}
                    <ChevronRight className="h-4 w-4" />
                  </Link>
                )}
              </div>
            ))}

            {/* Final note */}
            <div className="text-center py-8">
              <p className="text-slate-500">
                Al utilizar LEIA, usted reconoce haber leido, entendido y aceptado estos
                Terminos de Servicio en su totalidad.
              </p>
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
