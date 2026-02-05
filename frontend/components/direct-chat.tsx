'use client'

import { useState, useEffect, useRef } from 'react'
import { Send, ArrowLeft, User, Loader2, MessageSquare } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { cn } from '@/lib/utils'

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

interface Message {
  id: number
  sender_id: number
  sender_type: 'user' | 'lawyer'
  sender_name: string
  content: string
  is_read: boolean
  created_at: string
}

interface Conversation {
  id: number
  other_party_name: string
  other_party_id: number
  other_party_type: 'user' | 'lawyer'
  last_message: string | null
  last_message_at: string | null
  unread_count: number
  status: string
  created_at: string
}

interface ConversationDetail {
  id: number
  other_party_name: string
  other_party_id: number
  case_summary: string | null
  status: string
  messages: Message[]
}

interface DirectChatProps {
  userType: 'user' | 'lawyer'
}

export function DirectChat({ userType }: DirectChatProps) {
  const [conversations, setConversations] = useState<Conversation[]>([])
  const [selectedConversation, setSelectedConversation] = useState<ConversationDetail | null>(null)
  const [loading, setLoading] = useState(true)
  const [loadingMessages, setLoadingMessages] = useState(false)
  const [newMessage, setNewMessage] = useState('')
  const [sending, setSending] = useState(false)
  const messagesEndRef = useRef<HTMLDivElement>(null)

  const getAuthHeader = (): Record<string, string> => {
    const token = localStorage.getItem('justiciaai_token')
    return token ? { Authorization: `Bearer ${token}` } : {}
  }

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  useEffect(() => {
    scrollToBottom()
  }, [selectedConversation?.messages])

  // Fetch conversations
  useEffect(() => {
    const fetchConversations = async () => {
      try {
        const response = await fetch(`${API_URL}/api/chat/direct/conversations`, {
          headers: getAuthHeader()
        })
        if (response.ok) {
          const data = await response.json()
          setConversations(data)
        }
      } catch (error) {
        console.error('Error fetching conversations:', error)
      } finally {
        setLoading(false)
      }
    }

    fetchConversations()
    // Poll for new messages
    const interval = setInterval(fetchConversations, 10000)
    return () => clearInterval(interval)
  }, [])

  const openConversation = async (conversationId: number) => {
    setLoadingMessages(true)
    try {
      const response = await fetch(`${API_URL}/api/chat/direct/conversations/${conversationId}`, {
        headers: getAuthHeader()
      })
      if (response.ok) {
        const data = await response.json()
        setSelectedConversation(data)
        // Update unread count in list
        setConversations(prev => prev.map(c =>
          c.id === conversationId ? { ...c, unread_count: 0 } : c
        ))
      }
    } catch (error) {
      console.error('Error fetching conversation:', error)
    } finally {
      setLoadingMessages(false)
    }
  }

  const sendMessage = async () => {
    if (!newMessage.trim() || !selectedConversation || sending) return

    setSending(true)
    try {
      const response = await fetch(
        `${API_URL}/api/chat/direct/conversations/${selectedConversation.id}/messages`,
        {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            ...getAuthHeader()
          },
          body: JSON.stringify({ content: newMessage })
        }
      )

      if (response.ok) {
        const message = await response.json()
        setSelectedConversation(prev => prev ? {
          ...prev,
          messages: [...prev.messages, message]
        } : null)
        setNewMessage('')
      }
    } catch (error) {
      console.error('Error sending message:', error)
    } finally {
      setSending(false)
    }
  }

  const formatTime = (dateString: string) => {
    const date = new Date(dateString)
    const now = new Date()
    const diffDays = Math.floor((now.getTime() - date.getTime()) / (1000 * 60 * 60 * 24))

    if (diffDays === 0) {
      return date.toLocaleTimeString('es-CL', { hour: '2-digit', minute: '2-digit' })
    } else if (diffDays === 1) {
      return 'Ayer'
    } else if (diffDays < 7) {
      return date.toLocaleDateString('es-CL', { weekday: 'short' })
    } else {
      return date.toLocaleDateString('es-CL', { day: '2-digit', month: 'short' })
    }
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center h-96">
        <Loader2 className="h-8 w-8 animate-spin text-pacific-500" />
      </div>
    )
  }

  return (
    <div className="h-[600px] flex rounded-2xl overflow-hidden border border-slate-200 bg-white">
      {/* Conversations List */}
      <div className={cn(
        "w-full md:w-80 border-r border-slate-200 flex flex-col",
        selectedConversation && "hidden md:flex"
      )}>
        <div className="p-4 border-b border-slate-200">
          <h2 className="font-semibold text-slate-800">Mensajes</h2>
        </div>

        <div className="flex-1 overflow-y-auto">
          {conversations.length === 0 ? (
            <div className="flex flex-col items-center justify-center h-full text-center p-6">
              <MessageSquare className="h-12 w-12 text-slate-300 mb-3" />
              <p className="text-slate-500 text-sm">
                {userType === 'user'
                  ? 'Aun no tienes conversaciones con abogados'
                  : 'Aun no tienes mensajes de clientes'}
              </p>
            </div>
          ) : (
            conversations.map((conv) => (
              <div
                key={conv.id}
                onClick={() => openConversation(conv.id)}
                className={cn(
                  "p-4 border-b border-slate-100 cursor-pointer transition-colors hover:bg-slate-50",
                  selectedConversation?.id === conv.id && "bg-pacific-50"
                )}
              >
                <div className="flex items-start gap-3">
                  <div className="w-10 h-10 rounded-full bg-gradient-to-br from-pacific-400 to-pacific-600 flex items-center justify-center text-white font-semibold flex-shrink-0">
                    {conv.other_party_name.charAt(0)}
                  </div>
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center justify-between">
                      <h3 className="font-medium text-slate-800 truncate">
                        {conv.other_party_name}
                      </h3>
                      {conv.last_message_at && (
                        <span className="text-xs text-slate-400">
                          {formatTime(conv.last_message_at)}
                        </span>
                      )}
                    </div>
                    <p className="text-sm text-slate-500 truncate">
                      {conv.last_message || 'Sin mensajes'}
                    </p>
                  </div>
                  {conv.unread_count > 0 && (
                    <span className="w-5 h-5 rounded-full bg-pacific-500 text-white text-xs flex items-center justify-center">
                      {conv.unread_count}
                    </span>
                  )}
                </div>
              </div>
            ))
          )}
        </div>
      </div>

      {/* Chat Area */}
      <div className={cn(
        "flex-1 flex flex-col",
        !selectedConversation && "hidden md:flex"
      )}>
        {selectedConversation ? (
          <>
            {/* Chat Header */}
            <div className="p-4 border-b border-slate-200 flex items-center gap-3">
              <button
                onClick={() => setSelectedConversation(null)}
                className="md:hidden p-2 hover:bg-slate-100 rounded-lg"
              >
                <ArrowLeft className="h-5 w-5" />
              </button>
              <div className="w-10 h-10 rounded-full bg-gradient-to-br from-pacific-400 to-pacific-600 flex items-center justify-center text-white font-semibold">
                {selectedConversation.other_party_name.charAt(0)}
              </div>
              <div>
                <h3 className="font-semibold text-slate-800">
                  {selectedConversation.other_party_name}
                </h3>
                <p className="text-xs text-slate-500">
                  {userType === 'user' ? 'Abogado' : 'Cliente'}
                </p>
              </div>
            </div>

            {/* Messages */}
            <div className="flex-1 overflow-y-auto p-4 space-y-4 bg-slate-50">
              {loadingMessages ? (
                <div className="flex items-center justify-center h-full">
                  <Loader2 className="h-6 w-6 animate-spin text-pacific-500" />
                </div>
              ) : (
                <>
                  {selectedConversation.case_summary && (
                    <div className="p-3 bg-pacific-50 rounded-xl border border-pacific-100 text-sm text-pacific-700">
                      <p className="font-medium mb-1">Resumen del caso:</p>
                      <p>{selectedConversation.case_summary}</p>
                    </div>
                  )}

                  {selectedConversation.messages.map((message) => {
                    const isOwn = message.sender_type === userType
                    return (
                      <div
                        key={message.id}
                        className={cn(
                          "flex",
                          isOwn ? "justify-end" : "justify-start"
                        )}
                      >
                        <div className={cn(
                          "max-w-[75%] p-3 rounded-2xl",
                          isOwn
                            ? "bg-pacific-500 text-white rounded-br-md"
                            : "bg-white border border-slate-200 rounded-bl-md"
                        )}>
                          <p className="text-sm">{message.content}</p>
                          <p className={cn(
                            "text-xs mt-1",
                            isOwn ? "text-pacific-100" : "text-slate-400"
                          )}>
                            {formatTime(message.created_at)}
                          </p>
                        </div>
                      </div>
                    )
                  })}
                  <div ref={messagesEndRef} />
                </>
              )}
            </div>

            {/* Input */}
            <div className="p-4 border-t border-slate-200 bg-white">
              <form
                onSubmit={(e) => {
                  e.preventDefault()
                  sendMessage()
                }}
                className="flex gap-2"
              >
                <input
                  type="text"
                  value={newMessage}
                  onChange={(e) => setNewMessage(e.target.value)}
                  placeholder="Escribe un mensaje..."
                  className="flex-1 px-4 py-2 rounded-xl border border-slate-200 focus:border-pacific-500 focus:ring-2 focus:ring-pacific-500/20 outline-none"
                />
                <Button
                  type="submit"
                  disabled={!newMessage.trim() || sending}
                  className="bg-pacific-500 hover:bg-pacific-600"
                >
                  {sending ? (
                    <Loader2 className="h-5 w-5 animate-spin" />
                  ) : (
                    <Send className="h-5 w-5" />
                  )}
                </Button>
              </form>
            </div>
          </>
        ) : (
          <div className="flex-1 flex items-center justify-center text-center p-6">
            <div>
              <MessageSquare className="h-16 w-16 text-slate-200 mx-auto mb-4" />
              <h3 className="text-lg font-medium text-slate-600 mb-2">
                Selecciona una conversacion
              </h3>
              <p className="text-sm text-slate-400">
                Elige un chat de la lista para ver los mensajes
              </p>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}
