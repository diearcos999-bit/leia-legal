"use client"

import Link from "next/link"
import { Header } from "@/components/layout/Header"
import { Shield, Lock, Eye, UserCheck, Database, ChevronRight } from "lucide-react"
import { LeiaLogo } from "@/components/ui/leia-logo"

const keyPoints = [
  { icon: Lock, title: "Datos encriptados", description: "Toda tu informacion viaja protegida" },
  { icon: Eye, title: "Transparencia total", description: "Sabes exactamente que recopilamos" },
  { icon: UserCheck, title: "Tu controlas", description: "Puedes acceder, modificar o eliminar tus datos" },
]

const sections = [
  {
    id: 1,
    title: "Informacion que Recopilamos",
    subsections: [
      {
        subtitle: "Informacion que nos proporcionas",
        list: [
          { bold: "Datos de registro:", text: "Nombre, correo electronico, telefono, contrasena." },
          { bold: "Perfil profesional (abogados):", text: "Especializacion, experiencia, documentos de verificacion." },
          { bold: "Consultas legales:", text: "Contenido de las conversaciones con el asistente IA." },
          { bold: "Informacion de pago:", text: "Procesada de forma segura por proveedores certificados (no almacenamos datos de tarjetas)." }
        ]
      },
      {
        subtitle: "Informacion recopilada automaticamente",
        list: [
          { bold: "Datos de uso:", text: "Paginas visitadas, funciones utilizadas, tiempo en la plataforma." },
          { bold: "Informacion del dispositivo:", text: "Tipo de navegador, sistema operativo, direccion IP." },
          { bold: "Cookies:", text: "Utilizamos cookies esenciales y de analisis." }
        ]
      }
    ]
  },
  {
    id: 2,
    title: "Como Utilizamos tu Informacion",
    content: "Utilizamos tus datos para:",
    list: [
      { text: "Proporcionar y mejorar nuestros servicios." },
      { text: "Personalizar tu experiencia con el asistente legal IA." },
      { text: "Conectarte con abogados relevantes para tu consulta." },
      { text: "Procesar pagos y gestionar suscripciones." },
      { text: "Enviarte comunicaciones sobre el servicio." },
      { text: "Cumplir con obligaciones legales." },
      { text: "Prevenir fraudes y proteger la seguridad de la plataforma." }
    ]
  },
  {
    id: 3,
    title: "Como Protegemos tu Informacion",
    list: [
      { bold: "Encriptacion:", text: "Toda la informacion se transmite mediante HTTPS/TLS." },
      { bold: "Almacenamiento seguro:", text: "Datos almacenados en servidores con certificacion de seguridad." },
      { bold: "Acceso restringido:", text: "Solo personal autorizado puede acceder a datos personales." },
      { bold: "Monitoreo continuo:", text: "Sistemas de deteccion de intrusiones y auditorias regulares." }
    ]
  },
  {
    id: 4,
    title: "Comparticion de Datos",
    highlight: "No vendemos tu informacion personal.",
    content: "Solo compartimos datos en los siguientes casos:",
    list: [
      { bold: "Con abogados:", text: "Cuando solicitas contactar a un profesional, compartimos informacion relevante de tu consulta." },
      { bold: "Proveedores de servicios:", text: "Procesadores de pago, servicios de hosting, analisis (bajo estrictos acuerdos de confidencialidad)." },
      { bold: "Requerimientos legales:", text: "Cuando sea requerido por ley, orden judicial o autoridad competente." },
      { bold: "Proteccion de derechos:", text: "Para proteger los derechos, seguridad o propiedad de LEIA o terceros." }
    ]
  },
  {
    id: 5,
    title: "Tus Derechos (Ley 19.628)",
    content: "De acuerdo con la legislacion chilena, tienes derecho a:",
    list: [
      { bold: "Acceso:", text: "Solicitar una copia de tus datos personales." },
      { bold: "Rectificacion:", text: "Corregir datos inexactos o incompletos." },
      { bold: "Cancelacion:", text: "Solicitar la eliminacion de tus datos." },
      { bold: "Oposicion:", text: "Oponerte al tratamiento de tus datos en ciertos casos." }
    ],
    footer: "Para ejercer estos derechos, contactanos en privacidad@leia.cl"
  },
  {
    id: 6,
    title: "Cookies",
    content: "Utilizamos los siguientes tipos de cookies:",
    list: [
      { bold: "Esenciales:", text: "Necesarias para el funcionamiento del sitio (sesion, autenticacion)." },
      { bold: "Analiticas:", text: "Para entender como usas la plataforma y mejorar el servicio." },
      { bold: "Preferencias:", text: "Para recordar tus configuraciones." }
    ],
    footer: "Puedes gestionar las cookies desde la configuracion de tu navegador."
  },
  {
    id: 7,
    title: "Retencion de Datos",
    list: [
      { bold: "Datos de cuenta:", text: "Mientras mantengas tu cuenta activa." },
      { bold: "Historial de consultas:", text: "2 anos desde la ultima actividad." },
      { bold: "Datos de facturacion:", text: "6 anos por obligaciones tributarias." },
      { bold: "Datos eliminados:", text: "Se eliminan de forma segura dentro de 30 dias." }
    ]
  },
  {
    id: 8,
    title: "Menores de Edad",
    content: "LEIA no esta dirigido a menores de 18 anos. No recopilamos intencionalmente informacion de menores. Si detectamos que hemos recopilado datos de un menor, los eliminaremos de inmediato."
  },
  {
    id: 9,
    title: "Transferencias Internacionales",
    content: "Tus datos pueden ser procesados en servidores ubicados fuera de Chile. En estos casos, nos aseguramos de que existan garantias adecuadas de proteccion de datos, como clausulas contractuales estandar o certificaciones."
  },
  {
    id: 10,
    title: "Cambios a esta Politica",
    content: "Podemos actualizar esta politica periodicamente. Te notificaremos de cambios significativos por correo electronico o mediante aviso en la plataforma. Te recomendamos revisar esta pagina regularmente."
  },
  {
    id: 11,
    title: "Contacto",
    content: "Si tienes preguntas sobre esta politica o el tratamiento de tus datos:",
    list: [
      { bold: "Email:", text: "privacidad@leia.cl" },
      { bold: "Responsable de datos:", text: "LEIA SpA" },
      { bold: "Direccion:", text: "Santiago, Chile" }
    ]
  }
]

export default function PrivacidadPage() {
  return (
    <div className="flex flex-col min-h-screen bg-mesh">
      <Header />

      {/* Hero */}
      <section className="relative pt-28 lg:pt-36 pb-8">
        <div className="container">
          <div className="max-w-3xl mx-auto text-center">
            <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-pacific-100/50 text-pacific-700 text-sm font-medium mb-4">
              <Shield className="h-4 w-4" />
              Tu privacidad importa
            </div>
            <h1 className="text-4xl font-semibold text-slate-900 mb-4">
              Politica de Privacidad
            </h1>
            <p className="text-slate-600">
              Ultima actualizacion: Febrero 2025
            </p>
          </div>
        </div>
      </section>

      {/* Key Points */}
      <section className="py-6">
        <div className="container">
          <div className="max-w-3xl mx-auto">
            <div className="grid md:grid-cols-3 gap-4">
              {keyPoints.map((point, idx) => (
                <div key={idx} className="glass-card rounded-2xl p-5 text-center">
                  <point.icon className="h-10 w-10 text-pacific-600 mx-auto mb-3" />
                  <p className="font-semibold text-slate-900">{point.title}</p>
                  <p className="text-sm text-slate-600 mt-1">{point.description}</p>
                </div>
              ))}
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
                  <p className="text-pacific-700 font-semibold bg-pacific-50 p-4 rounded-xl mb-4 text-lg">
                    {section.highlight}
                  </p>
                )}

                {section.content && (
                  <p className="text-slate-600 leading-relaxed mb-4">
                    {section.content}
                  </p>
                )}

                {section.subsections && section.subsections.map((sub, idx) => (
                  <div key={idx} className={idx > 0 ? "mt-6 pt-6 border-t border-slate-200" : ""}>
                    <h3 className="font-medium text-slate-800 mb-3">{sub.subtitle}</h3>
                    <ul className="space-y-3">
                      {sub.list.map((item, i) => (
                        <li key={i} className="flex items-start gap-3 text-slate-600">
                          <ChevronRight className="h-5 w-5 text-pacific-500 flex-shrink-0 mt-0.5" />
                          <span>
                            {item.bold && <strong className="text-slate-800">{item.bold} </strong>}
                            {item.text}
                          </span>
                        </li>
                      ))}
                    </ul>
                  </div>
                ))}

                {section.list && !section.subsections && (
                  <ul className="space-y-3">
                    {section.list.map((item, idx) => (
                      <li key={idx} className="flex items-start gap-3 text-slate-600">
                        <ChevronRight className="h-5 w-5 text-pacific-500 flex-shrink-0 mt-0.5" />
                        <span>
                          {item.bold && <strong className="text-slate-800">{item.bold} </strong>}
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
              </div>
            ))}

            {/* Final note */}
            <div className="text-center py-8">
              <p className="text-slate-500">
                Al utilizar LEIA, aceptas el tratamiento de tus datos personales conforme
                a esta Politica de Privacidad.
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
                <Link href="/terminos" className="text-slate-600 hover:text-slate-900 transition-colors">Terminos</Link>
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
