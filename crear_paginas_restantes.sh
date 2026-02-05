#!/bin/bash

# Script para crear las últimas 3 páginas del MVP

echo "Creando páginas restantes..."

# Página Privacy
cat > /Users/RobertoArcos/suite/justiciaai-mvp/frontend/app/privacy/page.tsx << 'EOF'
import Link from 'next/link'
import { Button } from '@/components/ui/button'
import { Scale, ArrowLeft } from 'lucide-react'

export default function PrivacyPage() {
  return (
    <div className="flex flex-col min-h-screen">
      <header className="border-b">
        <div className="container flex h-16 items-center justify-between">
          <Link href="/" className="flex items-center gap-2">
            <Scale className="h-6 w-6 text-primary-600" />
            <span className="font-bold text-xl">JusticiaAI</span>
          </Link>
          <Button variant="outline" asChild>
            <Link href="/"><ArrowLeft className="h-4 w-4 mr-2" />Volver</Link>
          </Button>
        </div>
      </header>

      <main className="flex-1 py-12 px-4">
        <div className="container max-w-4xl mx-auto prose prose-lg">
          <h1>Política de Privacidad</h1>
          <p className="text-muted-foreground">Última actualización: Noviembre 2024</p>

          <h2>1. Información que Recopilamos</h2>
          <p>En JusticiaAI recopilamos la siguiente información:</p>
          <ul>
            <li><strong>Información personal:</strong> Nombre, email, teléfono cuando te registras</li>
            <li><strong>Información de uso:</strong> Cómo interactúas con nuestro chatbot y plataforma</li>
            <li><strong>Información legal:</strong> Consultas que haces a nuestro asistente de IA (anonimizadas)</li>
          </ul>

          <h2>2. Cómo Usamos Tu Información</h2>
          <p>Utilizamos tu información para:</p>
          <ul>
            <li>Proporcionar orientación legal a través de nuestro chatbot</li>
            <li>Conectarte con abogados verificados</li>
            <li>Mejorar nuestros servicios y algoritmos de IA</li>
            <li>Comunicarnos contigo sobre tu cuenta y servicios</li>
          </ul>

          <h2>3. Compartir Información</h2>
          <p><strong>NO vendemos tu información personal.</strong> Solo compartimos información cuando:</p>
          <ul>
            <li>Solicitas conectarte con un abogado (compartimos tu consulta con ese abogado específico)</li>
            <li>Es requerido por ley o autoridades judiciales</li>
            <li>Es necesario para procesar pagos (con procesadores de pago seguros)</li>
          </ul>

          <h2>4. Seguridad de Datos</h2>
          <p>Implementamos medidas de seguridad industry-standard incluyendo:</p>
          <ul>
            <li>Encriptación SSL/TLS para todas las comunicaciones</li>
            <li>Almacenamiento seguro en servidores con certificación ISO 27001</li>
            <li>Acceso restringido a información personal</li>
            <li>Auditorías de seguridad regulares</li>
          </ul>

          <h2>5. Cookies</h2>
          <p>Usamos cookies para mejorar tu experiencia. Puedes desactivarlas en tu navegador, pero algunas funciones podrían no funcionar correctamente.</p>

          <h2>6. Tus Derechos (Ley 19.628 Chile)</h2>
          <p>Bajo la Ley de Protección de Datos de Chile, tienes derecho a:</p>
          <ul>
            <li>Acceder a tu información personal</li>
            <li>Rectificar información incorrecta</li>
            <li>Solicitar eliminación de tu cuenta</li>
            <li>Oponerte al procesamiento de tu información</li>
            <li>Portar tu información a otro servicio</li>
          </ul>

          <h2>7. Retención de Datos</h2>
          <p>Mantenemos tu información mientras tu cuenta esté activa. Si eliminas tu cuenta, borraremos tu información personal en 90 días, excepto lo requerido por ley.</p>

          <h2>8. Cambios a esta Política</h2>
          <p>Podemos actualizar esta política ocasionalmente. Te notificaremos de cambios significativos por email.</p>

          <h2>9. Contacto</h2>
          <p>Para preguntas sobre privacidad: <a href="mailto:privacidad@justiciaai.cl">privacidad@justiciaai.cl</a></p>

          <div className="mt-8 p-4 bg-primary/5 rounded-lg border border-primary/20">
            <p className="text-sm"><strong>Importante:</strong> JusticiaAI proporciona orientación legal general, NO asesoría legal formal. Para representación legal, consulta con un abogado licenciado.</p>
          </div>
        </div>
      </main>

      <footer className="border-t py-8 px-4">
        <div className="container flex flex-col md:flex-row justify-between items-center gap-4">
          <div className="flex items-center gap-2">
            <Scale className="h-5 w-5 text-primary-600" />
            <span className="font-semibold">JusticiaAI</span>
          </div>
          <p className="text-sm text-muted-foreground">© 2024 JusticiaAI</p>
          <div className="flex gap-4">
            <Link href="/terms" className="text-sm text-muted-foreground hover:text-foreground">Términos</Link>
            <Link href="/contact" className="text-sm text-muted-foreground hover:text-foreground">Contacto</Link>
          </div>
        </div>
      </footer>
    </div>
  )
}
EOF

# Página Terms
cat > /Users/RobertoArcos/suite/justiciaai-mvp/frontend/app/terms/page.tsx << 'EOF'
import Link from 'next/link'
import { Button } from '@/components/ui/button'
import { Scale, ArrowLeft } from 'lucide-react'

export default function TermsPage() {
  return (
    <div className="flex flex-col min-h-screen">
      <header className="border-b">
        <div className="container flex h-16 items-center justify-between">
          <Link href="/" className="flex items-center gap-2">
            <Scale className="h-6 w-6 text-primary-600" />
            <span className="font-bold text-xl">JusticiaAI</span>
          </Link>
          <Button variant="outline" asChild>
            <Link href="/"><ArrowLeft className="h-4 w-4 mr-2" />Volver</Link>
          </Button>
        </div>
      </header>

      <main className="flex-1 py-12 px-4">
        <div className="container max-w-4xl mx-auto prose prose-lg">
          <h1>Términos y Condiciones de Uso</h1>
          <p className="text-muted-foreground">Última actualización: Noviembre 2024</p>

          <h2>1. Aceptación de Términos</h2>
          <p>Al usar JusticiaAI, aceptas estos términos. Si no estás de acuerdo, no uses nuestros servicios.</p>

          <h2>2. Descripción del Servicio</h2>
          <p>JusticiaAI es una plataforma que proporciona:</p>
          <ul>
            <li><strong>Orientación legal general</strong> mediante inteligencia artificial</li>
            <li><strong>Marketplace</strong> para conectar con abogados verificados</li>
            <li><strong>Servicios automatizados</strong> de documentos legales básicos</li>
          </ul>

          <div className="bg-red-50 border-2 border-red-200 rounded-lg p-4 my-6">
            <h3 className="text-red-900 mt-0">⚠️ DISCLAIMER IMPORTANTE</h3>
            <p className="text-red-800 mb-0"><strong>JusticiaAI NO es un abogado y NO proporciona asesoría legal formal.</strong> Nuestro chatbot ofrece orientación general sobre leyes chilenas, pero NO reemplaza la consulta con un abogado licenciado. Para casos específicos, SIEMPRE consulta con un profesional del derecho.</p>
          </div>

          <h2>3. Elegibilidad</h2>
          <p>Para usar JusticiaAI debes:</p>
          <ul>
            <li>Tener al menos 18 años</li>
            <li>Residir en Chile (para servicios legales específicos)</li>
            <li>Proporcionar información verdadera y actualizada</li>
          </ul>

          <h2>4. Cuenta de Usuario</h2>
          <ul>
            <li>Eres responsable de mantener tu contraseña segura</li>
            <li>NO compartas tu cuenta con terceros</li>
            <li>Notifícanos inmediatamente de cualquier uso no autorizado</li>
            <li>Podemos suspender cuentas que violen estos términos</li>
          </ul>

          <h2>5. Uso Aceptable</h2>
          <p><strong>NO puedes:</strong></p>
          <ul>
            <li>Usar el servicio para actividades ilegales</li>
            <li>Acosar, amenazar o difamar a otros usuarios o abogados</li>
            <li>Intentar hackear o comprometer la seguridad de la plataforma</li>
            <li>Hacer reverse engineering de nuestro código o IA</li>
            <li>Usar bots o scripts automatizados sin autorización</li>
          </ul>

          <h2>6. Servicios de Abogados</h2>
          <ul>
            <li>Los abogados en nuestro marketplace son profesionales independientes</li>
            <li>JusticiaAI NO es responsable por el trabajo de los abogados</li>
            <li>Los contratos son directamente entre tú y el abogado</li>
            <li>Verificamos licencias, pero NO garantizamos resultados</li>
          </ul>

          <h2>7. Pagos y Facturación</h2>
          <ul>
            <li><strong>Comisiones:</strong> Cobramos 25% de honorarios en casos conectados vía plataforma</li>
            <li><strong>Suscripciones abogados:</strong> Se cobran mensualmente, renovación automática</li>
            <li><strong>Reembolsos:</strong> Ver nuestra política de reembolsos específica</li>
            <li>Todos los precios en CLP incluyen IVA cuando aplique</li>
          </ul>

          <h2>8. Propiedad Intelectual</h2>
          <p>Todo el contenido de JusticiaAI (código, diseño, textos, IA) es propiedad de JusticiaAI SpA. NO puedes copiar, modificar o distribuir sin autorización escrita.</p>

          <h2>9. Limitación de Responsabilidad</h2>
          <p><strong>JUSTICIAAI NO ES RESPONSABLE POR:</strong></p>
          <ul>
            <li>Resultados de casos legales</li>
            <li>Decisiones tomadas basándose en orientación de IA</li>
            <li>Errores u omisiones en información proporcionada</li>
            <li>Daños indirectos o consecuenciales</li>
            <li>Pérdidas financieras derivadas del uso del servicio</li>
          </ul>
          <p>Nuestra responsabilidad máxima está limitada al monto pagado por servicios en los últimos 12 meses.</p>

          <h2>10. Modificaciones del Servicio</h2>
          <p>Podemos modificar, suspender o descontinuar cualquier parte del servicio en cualquier momento. Intentaremos notificar cambios significativos con 30 días de anticipación.</p>

          <h2>11. Terminación</h2>
          <ul>
            <li>Puedes cancelar tu cuenta en cualquier momento</li>
            <li>Podemos terminar cuentas que violen estos términos</li>
            <li>Al terminar, pierdes acceso a tu cuenta y datos</li>
          </ul>

          <h2>12. Ley Aplicable y Jurisdicción</h2>
          <p>Estos términos se rigen por las leyes de Chile. Cualquier disputa será resuelta en los tribunales de Santiago, Chile.</p>

          <h2>13. Contacto Legal</h2>
          <p>Para asuntos legales: <a href="mailto:legal@justiciaai.cl">legal@justiciaai.cl</a></p>

          <div className="mt-8 p-4 bg-blue-50 rounded-lg border border-blue-200">
            <p className="text-sm mb-2"><strong>Al usar JusticiaAI, confirmas que:</strong></p>
            <ul className="text-sm space-y-1 mb-0">
              <li>✓ Has leído y entendido estos términos</li>
              <li>✓ Comprendes que NO proporcionamos asesoría legal formal</li>
              <li>✓ Consultarás con un abogado para casos importantes</li>
              <li>✓ Usarás el servicio de buena fe y dentro de la ley</li>
            </ul>
          </div>
        </div>
      </main>

      <footer className="border-t py-8 px-4">
        <div className="container flex flex-col md:flex-row justify-between items-center gap-4">
          <div className="flex items-center gap-2">
            <Scale className="h-5 w-5 text-primary-600" />
            <span className="font-semibold">JusticiaAI</span>
          </div>
          <p className="text-sm text-muted-foreground">© 2024 JusticiaAI</p>
          <div className="flex gap-4">
            <Link href="/privacy" className="text-sm text-muted-foreground hover:text-foreground">Privacidad</Link>
            <Link href="/contact" className="text-sm text-muted-foreground hover:text-foreground">Contacto</Link>
          </div>
        </div>
      </footer>
    </div>
  )
}
EOF

# Página Dashboard (simple placeholder para post-login)
cat > /Users/RobertoArcos/suite/justiciaai-mvp/frontend/app/dashboard/page.tsx << 'EOF'
'use client'

import { useEffect } from 'react'
import { useRouter } from 'next/navigation'
import Link from 'next/link'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Scale, MessageSquare, Users, FileText, Settings, LogOut } from 'lucide-react'

export default function DashboardPage() {
  const router = useRouter()

  // En producción, verificarías si el usuario está autenticado
  // Por ahora, es una página de demostración

  return (
    <div className="flex flex-col min-h-screen bg-muted/30">
      {/* Header */}
      <header className="border-b bg-white">
        <div className="container flex h-16 items-center justify-between">
          <Link href="/" className="flex items-center gap-2">
            <Scale className="h-6 w-6 text-primary-600" />
            <span className="font-bold text-xl">JusticiaAI</span>
          </Link>
          <div className="flex items-center gap-4">
            <span className="text-sm text-muted-foreground">Usuario Demo</span>
            <Button variant="ghost" size="sm" onClick={() => router.push('/')}>
              <LogOut className="h-4 w-4 mr-2" />
              Salir
            </Button>
          </div>
        </div>
      </header>

      <main className="flex-1 py-8 px-4">
        <div className="container max-w-6xl">
          <div className="mb-8">
            <h1 className="text-3xl font-bold mb-2">Mi Dashboard</h1>
            <p className="text-muted-foreground">Bienvenido a tu panel de control</p>
          </div>

          {/* Stats Cards */}
          <div className="grid md:grid-cols-4 gap-4 mb-8">
            <Card>
              <CardHeader className="pb-2">
                <CardDescription>Consultas con IA</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">12</div>
                <p className="text-xs text-muted-foreground">+3 esta semana</p>
              </CardContent>
            </Card>

            <Card>
              <CardHeader className="pb-2">
                <CardDescription>Casos Activos</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">1</div>
                <p className="text-xs text-muted-foreground">Con María González</p>
              </CardContent>
            </Card>

            <Card>
              <CardHeader className="pb-2">
                <CardDescription>Documentos</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">5</div>
                <p className="text-xs text-muted-foreground">3 pendientes</p>
              </CardContent>
            </Card>

            <Card>
              <CardHeader className="pb-2">
                <CardDescription>Ahorro Estimado</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">$250K</div>
                <p className="text-xs text-muted-foreground">vs. abogado tradicional</p>
              </CardContent>
            </Card>
          </div>

          {/* Quick Actions */}
          <div className="grid md:grid-cols-2 gap-6">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <MessageSquare className="h-5 w-5" />
                  Acciones Rápidas
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-2">
                <Button className="w-full justify-start" variant="outline" asChild>
                  <Link href="/chat">
                    <MessageSquare className="h-4 w-4 mr-2" />
                    Nueva consulta con IA
                  </Link>
                </Button>
                <Button className="w-full justify-start" variant="outline" asChild>
                  <Link href="/abogados">
                    <Users className="h-4 w-4 mr-2" />
                    Buscar abogado
                  </Link>
                </Button>
                <Button className="w-full justify-start" variant="outline">
                  <FileText className="h-4 w-4 mr-2" />
                  Crear documento
                </Button>
                <Button className="w-full justify-start" variant="outline">
                  <Settings className="h-4 w-4 mr-2" />
                  Configuración
                </Button>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle>Historial Reciente</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  <div className="flex items-start gap-3 pb-3 border-b">
                    <div className="w-2 h-2 mt-2 rounded-full bg-green-500"></div>
                    <div className="flex-1">
                      <p className="text-sm font-medium">Consulta sobre finiquito</p>
                      <p className="text-xs text-muted-foreground">Hace 2 horas • IA Legal</p>
                    </div>
                  </div>
                  <div className="flex items-start gap-3 pb-3 border-b">
                    <div className="w-2 h-2 mt-2 rounded-full bg-blue-500"></div>
                    <div className="flex-1">
                      <p className="text-sm font-medium">Caso laboral con María González</p>
                      <p className="text-xs text-muted-foreground">Hace 3 días • En progreso</p>
                    </div>
                  </div>
                  <div className="flex items-start gap-3">
                    <div className="w-2 h-2 mt-2 rounded-full bg-gray-300"></div>
                    <div className="flex-1">
                      <p className="text-sm font-medium">Carta de reclamo SERNAC</p>
                      <p className="text-xs text-muted-foreground">Hace 1 semana • Completado</p>
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>

          {/* Banner Info */}
          <Card className="mt-6 bg-primary/5 border-primary/20">
            <CardContent className="py-4">
              <div className="flex items-center justify-between">
                <div>
                  <p className="font-medium">Esta es una vista demo del dashboard</p>
                  <p className="text-sm text-muted-foreground">En producción, aquí verás tu información real</p>
                </div>
                <Button asChild>
                  <Link href="/">Volver al Inicio</Link>
                </Button>
              </div>
            </CardContent>
          </Card>
        </div>
      </main>

      <footer className="border-t py-6 px-4 bg-white">
        <div className="container flex flex-col md:flex-row justify-between items-center gap-4 text-sm text-muted-foreground">
          <div className="flex items-center gap-2">
            <Scale className="h-4 w-4" />
            <span>© 2024 JusticiaAI</span>
          </div>
          <div className="flex gap-4">
            <Link href="/privacy" className="hover:text-foreground">Privacidad</Link>
            <Link href="/terms" className="hover:text-foreground">Términos</Link>
            <Link href="/contact" className="hover:text-foreground">Soporte</Link>
          </div>
        </div>
      </footer>
    </div>
  )
}
EOF

echo "✅ Todas las páginas creadas exitosamente!"
echo ""
echo "Páginas creadas:"
echo "  - /app/privacy/page.tsx"
echo "  - /app/terms/page.tsx"
echo "  - /app/dashboard/page.tsx"
EOF

chmod +x /Users/RobertoArcos/suite/justiciaai-mvp/crear_paginas_restantes.sh
bash /Users/RobertoArcos/suite/justiciaai-mvp/crear_paginas_restantes.sh
