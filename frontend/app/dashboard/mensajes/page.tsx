'use client'

import { MessageSquare } from 'lucide-react'
import { PageHeader } from '@/components/dashboard'
import { DirectChat } from '@/components/direct-chat'
import { useEffect, useState } from 'react'

export default function MensajesPage() {
  const [userType, setUserType] = useState<'user' | 'lawyer'>('user')

  useEffect(() => {
    // Check user role from token or localStorage
    const userData = localStorage.getItem('justiciaai_user')
    if (userData) {
      try {
        const user = JSON.parse(userData)
        setUserType(user.role === 'lawyer' ? 'lawyer' : 'user')
      } catch (e) {
        console.error('Error parsing user data')
      }
    }
  }, [])

  return (
    <div>
      <PageHeader
        title="Mensajes"
        description="Conversaciones con tus abogados"
        icon={MessageSquare}
      />

      <DirectChat userType={userType} />
    </div>
  )
}
