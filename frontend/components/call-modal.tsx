'use client'

import { useState, useEffect, useRef } from 'react'
import { useAuth } from '@/lib/auth'
import { Button } from '@/components/ui/button'
import {
  Phone,
  PhoneOff,
  Video,
  VideoOff,
  Mic,
  MicOff,
  X,
  Loader2,
  User
} from 'lucide-react'
import { cn } from '@/lib/utils'

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

interface CallModalProps {
  isOpen: boolean
  onClose: () => void
  transferId: number
  callType: 'voice' | 'video'
  participantName?: string
  isIncoming?: boolean
  callId?: number
}

type CallStatus = 'initiating' | 'ringing' | 'connecting' | 'connected' | 'ended' | 'failed'

export function CallModal({
  isOpen,
  onClose,
  transferId,
  callType,
  participantName,
  isIncoming = false,
  callId: incomingCallId
}: CallModalProps) {
  const { token } = useAuth()
  const [status, setStatus] = useState<CallStatus>('initiating')
  const [callId, setCallId] = useState<number | null>(incomingCallId || null)
  const [roomUrl, setRoomUrl] = useState<string | null>(null)
  const [callDuration, setCallDuration] = useState(0)
  const [isMuted, setIsMuted] = useState(false)
  const [isVideoOff, setIsVideoOff] = useState(callType === 'voice')
  const [error, setError] = useState<string | null>(null)

  const durationIntervalRef = useRef<NodeJS.Timeout | null>(null)

  // Format duration as MM:SS
  const formatDuration = (seconds: number) => {
    const mins = Math.floor(seconds / 60)
    const secs = seconds % 60
    return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`
  }

  // Start duration counter
  const startDurationCounter = () => {
    durationIntervalRef.current = setInterval(() => {
      setCallDuration(prev => prev + 1)
    }, 1000)
  }

  // Stop duration counter
  const stopDurationCounter = () => {
    if (durationIntervalRef.current) {
      clearInterval(durationIntervalRef.current)
      durationIntervalRef.current = null
    }
  }

  // Initiate call (for outgoing calls)
  const initiateCall = async () => {
    if (!token) return

    try {
      const response = await fetch(`${API_URL}/api/calls/transfers/${transferId}/request`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ call_type: callType })
      })

      if (response.ok) {
        const data = await response.json()
        setCallId(data.id)
        setRoomUrl(data.room_url)
        setStatus('ringing')
      } else {
        const errorData = await response.json()
        setError(errorData.detail || 'No se pudo iniciar la llamada')
        setStatus('failed')
      }
    } catch (err) {
      setError('Error de conexión')
      setStatus('failed')
    }
  }

  // Accept incoming call
  const acceptCall = async () => {
    if (!token || !callId) return

    try {
      const response = await fetch(`${API_URL}/api/calls/${callId}/accept`, {
        method: 'POST',
        headers: { 'Authorization': `Bearer ${token}` }
      })

      if (response.ok) {
        const data = await response.json()
        setRoomUrl(data.room_url)
        setStatus('connecting')
        // In real implementation, connect to Daily.co room here
        setTimeout(() => {
          setStatus('connected')
          startDurationCounter()
        }, 1000)
      } else {
        const errorData = await response.json()
        setError(errorData.detail || 'No se pudo aceptar la llamada')
        setStatus('failed')
      }
    } catch (err) {
      setError('Error de conexión')
      setStatus('failed')
    }
  }

  // Reject/End call
  const endCall = async () => {
    if (!token || !callId) {
      handleClose()
      return
    }

    stopDurationCounter()

    try {
      if (status === 'ringing' && isIncoming) {
        // Reject incoming call
        await fetch(`${API_URL}/api/calls/${callId}/reject`, {
          method: 'POST',
          headers: { 'Authorization': `Bearer ${token}` }
        })
      } else {
        // End active call
        await fetch(`${API_URL}/api/calls/${callId}/end`, {
          method: 'POST',
          headers: { 'Authorization': `Bearer ${token}` }
        })
      }
    } catch (err) {
      console.error('Error ending call:', err)
    }

    setStatus('ended')
    setTimeout(handleClose, 1000)
  }

  const handleClose = () => {
    stopDurationCounter()
    setStatus('initiating')
    setCallId(null)
    setRoomUrl(null)
    setCallDuration(0)
    setError(null)
    onClose()
  }

  // Initialize call on open
  useEffect(() => {
    if (isOpen && !isIncoming) {
      initiateCall()
    } else if (isOpen && isIncoming) {
      setStatus('ringing')
    }

    return () => {
      stopDurationCounter()
    }
  }, [isOpen])

  // Simulate call being answered (for demo purposes)
  useEffect(() => {
    if (status === 'ringing' && !isIncoming) {
      // Auto-connect after 3 seconds for demo
      const timeout = setTimeout(() => {
        setStatus('connecting')
        setTimeout(() => {
          setStatus('connected')
          startDurationCounter()
        }, 1000)
      }, 3000)

      return () => clearTimeout(timeout)
    }
  }, [status, isIncoming])

  if (!isOpen) return null

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/80">
      <div className="w-full max-w-md bg-slate-900 rounded-2xl overflow-hidden">
        {/* Video area (placeholder) */}
        <div className="relative aspect-video bg-slate-800 flex items-center justify-center">
          {callType === 'video' && status === 'connected' ? (
            <div className="text-white text-center">
              {/* In real implementation, Daily.co video would be here */}
              <div className="w-24 h-24 mx-auto mb-4 rounded-full bg-slate-700 flex items-center justify-center">
                <User className="h-12 w-12 text-slate-500" />
              </div>
              <p className="text-sm text-slate-400">Video conectado</p>
            </div>
          ) : (
            <div className="text-center">
              <div className="w-24 h-24 mx-auto mb-4 rounded-full bg-slate-700 flex items-center justify-center">
                <User className="h-12 w-12 text-slate-500" />
              </div>
              <p className="text-lg font-medium text-white mb-1">
                {participantName || 'Participante'}
              </p>
              <p className="text-sm text-slate-400">
                {status === 'initiating' && 'Iniciando llamada...'}
                {status === 'ringing' && (isIncoming ? 'Llamada entrante...' : 'Llamando...')}
                {status === 'connecting' && 'Conectando...'}
                {status === 'connected' && formatDuration(callDuration)}
                {status === 'ended' && 'Llamada finalizada'}
                {status === 'failed' && (error || 'Error en la llamada')}
              </p>
            </div>
          )}

          {/* Call type indicator */}
          <div className="absolute top-4 left-4 flex items-center gap-2 px-3 py-1 bg-black/50 rounded-full">
            {callType === 'video' ? (
              <Video className="h-4 w-4 text-white" />
            ) : (
              <Phone className="h-4 w-4 text-white" />
            )}
            <span className="text-sm text-white">
              {callType === 'video' ? 'Videollamada' : 'Llamada de voz'}
            </span>
          </div>

          {/* Close button */}
          <button
            onClick={handleClose}
            className="absolute top-4 right-4 p-2 text-white/70 hover:text-white transition-colors"
          >
            <X className="h-5 w-5" />
          </button>

          {/* Ringing animation */}
          {(status === 'ringing' || status === 'connecting') && (
            <div className="absolute inset-0 flex items-center justify-center">
              <div className="absolute w-32 h-32 rounded-full border-4 border-pacific-500/30 animate-ping" />
            </div>
          )}
        </div>

        {/* Controls */}
        <div className="p-6 bg-slate-900">
          {/* Incoming call buttons */}
          {status === 'ringing' && isIncoming && (
            <div className="flex items-center justify-center gap-6">
              <Button
                onClick={endCall}
                className="w-16 h-16 rounded-full bg-red-500 hover:bg-red-600"
              >
                <PhoneOff className="h-6 w-6" />
              </Button>
              <Button
                onClick={acceptCall}
                className="w-16 h-16 rounded-full bg-green-500 hover:bg-green-600"
              >
                <Phone className="h-6 w-6" />
              </Button>
            </div>
          )}

          {/* Connected call controls */}
          {(status === 'connected' || (status === 'ringing' && !isIncoming) || status === 'connecting') && (
            <div className="flex items-center justify-center gap-4">
              <Button
                variant="ghost"
                onClick={() => setIsMuted(!isMuted)}
                className={cn(
                  'w-14 h-14 rounded-full',
                  isMuted ? 'bg-red-500/20 text-red-500' : 'bg-white/10 text-white'
                )}
              >
                {isMuted ? <MicOff className="h-6 w-6" /> : <Mic className="h-6 w-6" />}
              </Button>

              {callType === 'video' && (
                <Button
                  variant="ghost"
                  onClick={() => setIsVideoOff(!isVideoOff)}
                  className={cn(
                    'w-14 h-14 rounded-full',
                    isVideoOff ? 'bg-red-500/20 text-red-500' : 'bg-white/10 text-white'
                  )}
                >
                  {isVideoOff ? <VideoOff className="h-6 w-6" /> : <Video className="h-6 w-6" />}
                </Button>
              )}

              <Button
                onClick={endCall}
                className="w-14 h-14 rounded-full bg-red-500 hover:bg-red-600"
              >
                <PhoneOff className="h-6 w-6" />
              </Button>
            </div>
          )}

          {/* Failed state */}
          {status === 'failed' && (
            <div className="text-center">
              <p className="text-red-400 mb-4">{error || 'No se pudo conectar la llamada'}</p>
              <Button variant="outline" onClick={handleClose}>
                Cerrar
              </Button>
            </div>
          )}

          {/* Initiating state */}
          {status === 'initiating' && (
            <div className="flex items-center justify-center">
              <Loader2 className="h-8 w-8 animate-spin text-pacific-500" />
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
