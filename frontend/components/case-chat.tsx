'use client'

import { useState, useEffect, useRef, useCallback } from 'react'
import { useAuth } from '@/lib/auth'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import {
  Send,
  Paperclip,
  Phone,
  Video,
  Check,
  CheckCheck,
  Loader2,
  FileText,
  Image as ImageIcon,
  File
} from 'lucide-react'
import { cn } from '@/lib/utils'

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

interface Message {
  id: number
  transfer_id: number
  sender_id: number
  sender_type: 'user' | 'lawyer'
  sender_name?: string
  content: string
  message_type: 'text' | 'file' | 'call_request' | 'system'
  file_path?: string
  file_name?: string
  file_size?: number
  is_read: boolean
  read_at?: string
  created_at: string
}

interface CommunicationSettings {
  chat_enabled: boolean
  voice_enabled: boolean
  video_enabled: boolean
}

interface CaseChatProps {
  transferId: number
  caseNumber?: string
  participantType: 'user' | 'lawyer'
  participantName?: string
  communicationSettings?: CommunicationSettings
  onCallRequest?: (callType: 'voice' | 'video') => void
}

export function CaseChat({
  transferId,
  caseNumber,
  participantType,
  participantName,
  communicationSettings,
  onCallRequest
}: CaseChatProps) {
  const { token } = useAuth()
  const [messages, setMessages] = useState<Message[]>([])
  const [newMessage, setNewMessage] = useState('')
  const [isLoading, setIsLoading] = useState(true)
  const [isSending, setIsSending] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const messagesEndRef = useRef<HTMLDivElement>(null)
  const fileInputRef = useRef<HTMLInputElement>(null)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  const fetchMessages = useCallback(async () => {
    if (!token) return

    try {
      const response = await fetch(
        `${API_URL}/api/messages/transfers/${transferId}/messages`,
        {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        }
      )

      if (response.ok) {
        const data = await response.json()
        setMessages(data)
        setError(null)
      } else {
        setError('Error al cargar mensajes')
      }
    } catch (err) {
      setError('Error de conexión')
    } finally {
      setIsLoading(false)
    }
  }, [token, transferId])

  const markAsRead = useCallback(async () => {
    if (!token) return

    try {
      await fetch(
        `${API_URL}/api/messages/transfers/${transferId}/messages/read`,
        {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${token}`
          }
        }
      )
    } catch (err) {
      console.error('Error marking messages as read:', err)
    }
  }, [token, transferId])

  useEffect(() => {
    fetchMessages()
    markAsRead()

    // Poll for new messages every 10 seconds
    const interval = setInterval(() => {
      fetchMessages()
    }, 10000)

    return () => clearInterval(interval)
  }, [fetchMessages, markAsRead])

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  const sendMessage = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!newMessage.trim() || !token || isSending) return

    setIsSending(true)

    try {
      const response = await fetch(
        `${API_URL}/api/messages/transfers/${transferId}/messages`,
        {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            content: newMessage.trim(),
            message_type: 'text'
          })
        }
      )

      if (response.ok) {
        const message = await response.json()
        setMessages(prev => [...prev, message])
        setNewMessage('')
        setError(null)
      } else {
        const data = await response.json()
        setError(data.detail || 'Error al enviar mensaje')
      }
    } catch (err) {
      setError('Error de conexión')
    } finally {
      setIsSending(false)
    }
  }

  const sendFileMessage = async (file: File) => {
    if (!token) return

    setIsSending(true)

    try {
      const formData = new FormData()
      formData.append('file', file)
      formData.append('message', `Archivo: ${file.name}`)

      const response = await fetch(
        `${API_URL}/api/messages/transfers/${transferId}/messages/file`,
        {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${token}`
          },
          body: formData
        }
      )

      if (response.ok) {
        const message = await response.json()
        setMessages(prev => [...prev, message])
        setError(null)
      } else {
        const data = await response.json()
        setError(data.detail || 'Error al enviar archivo')
      }
    } catch (err) {
      setError('Error de conexión')
    } finally {
      setIsSending(false)
    }
  }

  const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0]
    if (file) {
      if (file.size > 10 * 1024 * 1024) {
        setError('El archivo excede el tamaño máximo de 10MB')
        return
      }
      sendFileMessage(file)
    }
    e.target.value = ''
  }

  const formatTime = (dateString: string) => {
    const date = new Date(dateString)
    return date.toLocaleTimeString('es-CL', {
      hour: '2-digit',
      minute: '2-digit'
    })
  }

  const formatDate = (dateString: string) => {
    const date = new Date(dateString)
    const today = new Date()
    const yesterday = new Date(today)
    yesterday.setDate(yesterday.getDate() - 1)

    if (date.toDateString() === today.toDateString()) {
      return 'Hoy'
    } else if (date.toDateString() === yesterday.toDateString()) {
      return 'Ayer'
    } else {
      return date.toLocaleDateString('es-CL', {
        day: 'numeric',
        month: 'short'
      })
    }
  }

  const getFileIcon = (fileName?: string) => {
    if (!fileName) return <File className="h-4 w-4" />
    const ext = fileName.split('.').pop()?.toLowerCase()
    if (['jpg', 'jpeg', 'png', 'gif', 'webp'].includes(ext || '')) {
      return <ImageIcon className="h-4 w-4" />
    }
    if (ext === 'pdf') {
      return <FileText className="h-4 w-4" />
    }
    return <File className="h-4 w-4" />
  }

  const formatFileSize = (bytes?: number) => {
    if (!bytes) return ''
    if (bytes < 1024) return `${bytes} B`
    if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`
    return `${(bytes / (1024 * 1024)).toFixed(1)} MB`
  }

  // Group messages by date
  const groupedMessages: { date: string; messages: Message[] }[] = []
  let currentDate = ''

  messages.forEach(message => {
    const messageDate = new Date(message.created_at).toDateString()
    if (messageDate !== currentDate) {
      currentDate = messageDate
      groupedMessages.push({
        date: message.created_at,
        messages: [message]
      })
    } else {
      groupedMessages[groupedMessages.length - 1].messages.push(message)
    }
  })

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-64">
        <Loader2 className="h-8 w-8 animate-spin text-pacific-500" />
      </div>
    )
  }

  return (
    <div className="flex flex-col h-full bg-white rounded-xl border border-slate-200 overflow-hidden">
      {/* Header */}
      <div className="flex items-center justify-between px-4 py-3 border-b border-slate-200 bg-slate-50">
        <div>
          <h3 className="font-medium text-slate-900">
            Chat {participantType === 'user' ? 'con tu abogado' : 'con cliente'}
          </h3>
          {participantName && (
            <p className="text-sm text-slate-500">{participantName}</p>
          )}
          {caseNumber && (
            <p className="text-xs text-slate-400">Caso: {caseNumber}</p>
          )}
        </div>
        <div className="flex items-center gap-2">
          {communicationSettings?.voice_enabled && (
            <Button
              variant="ghost"
              size="sm"
              onClick={() => onCallRequest?.('voice')}
              className="text-slate-600 hover:text-pacific-600"
            >
              <Phone className="h-4 w-4" />
            </Button>
          )}
          {communicationSettings?.video_enabled && (
            <Button
              variant="ghost"
              size="sm"
              onClick={() => onCallRequest?.('video')}
              className="text-slate-600 hover:text-pacific-600"
            >
              <Video className="h-4 w-4" />
            </Button>
          )}
        </div>
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4 min-h-[300px] max-h-[500px]">
        {messages.length === 0 ? (
          <div className="flex flex-col items-center justify-center h-full text-slate-500">
            <p>No hay mensajes aún</p>
            <p className="text-sm">Envía un mensaje para iniciar la conversación</p>
          </div>
        ) : (
          groupedMessages.map((group, groupIndex) => (
            <div key={groupIndex}>
              {/* Date separator */}
              <div className="flex items-center justify-center my-4">
                <span className="px-3 py-1 text-xs text-slate-500 bg-slate-100 rounded-full">
                  {formatDate(group.date)}
                </span>
              </div>

              {/* Messages for this date */}
              {group.messages.map((message) => {
                const isOwn = message.sender_type === participantType
                return (
                  <div
                    key={message.id}
                    className={cn(
                      'flex mb-2',
                      isOwn ? 'justify-end' : 'justify-start'
                    )}
                  >
                    <div
                      className={cn(
                        'max-w-[70%] rounded-2xl px-4 py-2',
                        isOwn
                          ? 'bg-pacific-500 text-white rounded-br-md'
                          : 'bg-slate-100 text-slate-900 rounded-bl-md'
                      )}
                    >
                      {message.message_type === 'file' && message.file_name && (
                        <div className={cn(
                          'flex items-center gap-2 mb-1 p-2 rounded-lg',
                          isOwn ? 'bg-pacific-600' : 'bg-slate-200'
                        )}>
                          {getFileIcon(message.file_name)}
                          <div className="flex-1 min-w-0">
                            <p className="text-sm font-medium truncate">
                              {message.file_name}
                            </p>
                            <p className={cn(
                              'text-xs',
                              isOwn ? 'text-pacific-200' : 'text-slate-500'
                            )}>
                              {formatFileSize(message.file_size)}
                            </p>
                          </div>
                        </div>
                      )}

                      <p className="text-sm whitespace-pre-wrap break-words">
                        {message.content}
                      </p>

                      <div className={cn(
                        'flex items-center justify-end gap-1 mt-1',
                        isOwn ? 'text-pacific-200' : 'text-slate-400'
                      )}>
                        <span className="text-xs">
                          {formatTime(message.created_at)}
                        </span>
                        {isOwn && (
                          message.is_read ? (
                            <CheckCheck className="h-3 w-3" />
                          ) : (
                            <Check className="h-3 w-3" />
                          )
                        )}
                      </div>
                    </div>
                  </div>
                )
              })}
            </div>
          ))
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* Error */}
      {error && (
        <div className="px-4 py-2 text-sm text-red-600 bg-red-50 border-t border-red-100">
          {error}
        </div>
      )}

      {/* Input */}
      <form onSubmit={sendMessage} className="p-4 border-t border-slate-200 bg-slate-50">
        <div className="flex items-center gap-2">
          <input
            type="file"
            ref={fileInputRef}
            onChange={handleFileSelect}
            className="hidden"
            accept=".pdf,.doc,.docx,.xls,.xlsx,.jpg,.jpeg,.png,.gif"
          />
          <Button
            type="button"
            variant="ghost"
            size="icon"
            onClick={() => fileInputRef.current?.click()}
            disabled={isSending}
            className="text-slate-500 hover:text-pacific-600"
          >
            <Paperclip className="h-5 w-5" />
          </Button>

          <Input
            value={newMessage}
            onChange={(e) => setNewMessage(e.target.value)}
            placeholder="Escribe un mensaje..."
            disabled={isSending}
            className="flex-1"
          />

          <Button
            type="submit"
            size="icon"
            disabled={!newMessage.trim() || isSending}
            className="bg-pacific-500 hover:bg-pacific-600"
          >
            {isSending ? (
              <Loader2 className="h-4 w-4 animate-spin" />
            ) : (
              <Send className="h-4 w-4" />
            )}
          </Button>
        </div>
      </form>
    </div>
  )
}
