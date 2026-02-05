'use client'

import { cn } from '@/lib/utils'

interface LeiaAvatarProps {
  size?: 'sm' | 'md' | 'lg' | 'xl'
  className?: string
  animated?: boolean
}

export function LeiaAvatar({ size = 'lg', className, animated = true }: LeiaAvatarProps) {
  const sizeClasses = {
    sm: 'w-16 h-16',
    md: 'w-24 h-24',
    lg: 'w-32 h-32',
    xl: 'w-40 h-40'
  }

  const scaleClasses = {
    sm: 'scale-[0.4]',
    md: 'scale-[0.6]',
    lg: 'scale-[0.8]',
    xl: 'scale-100'
  }

  return (
    <div className={cn('relative flex items-center justify-center', sizeClasses[size], className)}>
      {/* Glow effect behind avatar */}
      <div className="absolute inset-0 bg-pacific-400/20 rounded-full blur-2xl animate-pulse" />

      {/* Main avatar container */}
      <div className={cn('relative', scaleClasses[size])}>
        <svg
          width="160"
          height="180"
          viewBox="0 0 160 180"
          fill="none"
          xmlns="http://www.w3.org/2000/svg"
          className={cn(animated && 'animate-float')}
        >
          <defs>
            {/* Suit gradient - dark navy */}
            <linearGradient id="suitGradient" x1="0%" y1="0%" x2="100%" y2="100%">
              <stop offset="0%" stopColor="#1E3A5F" />
              <stop offset="100%" stopColor="#0F172A" />
            </linearGradient>
            {/* Suit highlight */}
            <linearGradient id="suitHighlight" x1="0%" y1="0%" x2="100%" y2="0%">
              <stop offset="0%" stopColor="#2D4A6F" />
              <stop offset="50%" stopColor="#1E3A5F" />
              <stop offset="100%" stopColor="#2D4A6F" />
            </linearGradient>
            {/* Face gradient */}
            <linearGradient id="faceGradient" x1="0%" y1="0%" x2="0%" y2="100%">
              <stop offset="0%" stopColor="#FFFFFF" />
              <stop offset="100%" stopColor="#F1F5F9" />
            </linearGradient>
            {/* Tie gradient */}
            <linearGradient id="tieGradient" x1="0%" y1="0%" x2="0%" y2="100%">
              <stop offset="0%" stopColor="#3B82F6" />
              <stop offset="100%" stopColor="#1D4ED8" />
            </linearGradient>
            {/* Hair gradient */}
            <linearGradient id="hairGradient" x1="0%" y1="0%" x2="100%" y2="100%">
              <stop offset="0%" stopColor="#60A5FA" />
              <stop offset="100%" stopColor="#2563EB" />
            </linearGradient>
            <filter id="shadow" x="-20%" y="-20%" width="140%" height="140%">
              <feDropShadow dx="0" dy="4" stdDeviation="8" floodOpacity="0.15"/>
            </filter>
            <filter id="innerShadow" x="-50%" y="-50%" width="200%" height="200%">
              <feDropShadow dx="0" dy="2" stdDeviation="2" floodOpacity="0.1"/>
            </filter>
          </defs>

          {/* === SUIT/BODY === */}

          {/* Shoulders - wider suit shape */}
          <ellipse
            cx="80"
            cy="155"
            rx="58"
            ry="30"
            fill="url(#suitGradient)"
            filter="url(#shadow)"
          />

          {/* Suit body */}
          <path
            d="M22 155
               Q22 135 40 125
               L55 118
               L80 130
               L105 118
               L120 125
               Q138 135 138 155
               L138 180
               L22 180
               Z"
            fill="url(#suitGradient)"
          />

          {/* Left lapel */}
          <path
            d="M55 118
               L48 125
               L52 155
               L68 155
               L75 130
               L80 130
               L55 118
               Z"
            fill="url(#suitHighlight)"
          />

          {/* Right lapel */}
          <path
            d="M105 118
               L112 125
               L108 155
               L92 155
               L85 130
               L80 130
               L105 118
               Z"
            fill="url(#suitHighlight)"
          />

          {/* Lapel inner edge - left */}
          <path
            d="M68 128 L60 155"
            stroke="#0F172A"
            strokeWidth="1"
            opacity="0.3"
          />

          {/* Lapel inner edge - right */}
          <path
            d="M92 128 L100 155"
            stroke="#0F172A"
            strokeWidth="1"
            opacity="0.3"
          />

          {/* White shirt visible */}
          <path
            d="M68 125
               L80 140
               L92 125
               L90 160
               L70 160
               Z"
            fill="white"
          />

          {/* Shirt collar left */}
          <path
            d="M58 120 L72 130 L68 118 Z"
            fill="white"
          />

          {/* Shirt collar right */}
          <path
            d="M102 120 L88 130 L92 118 Z"
            fill="white"
          />

          {/* Tie knot */}
          <path
            d="M76 125 L80 120 L84 125 L80 130 Z"
            fill="#1E40AF"
          />

          {/* Tie body */}
          <path
            d="M77 130
               L76 140
               L74 160
               L80 168
               L86 160
               L84 140
               L83 130
               Z"
            fill="url(#tieGradient)"
            className={cn(animated && 'origin-top animate-swing')}
          />

          {/* Tie stripe detail */}
          <path
            d="M79 135 L79 158 M81 135 L81 158"
            stroke="#1E40AF"
            strokeWidth="0.5"
            opacity="0.3"
          />

          {/* Suit buttons */}
          <circle cx="80" cy="162" r="2.5" fill="#CBD5E1" />
          <circle cx="80" cy="172" r="2.5" fill="#CBD5E1" />

          {/* Pocket square hint - left */}
          <path
            d="M52 138 Q54 134 58 136"
            stroke="#60A5FA"
            strokeWidth="2"
            fill="none"
            strokeLinecap="round"
          />

          {/* === HEAD === */}

          {/* Neck */}
          <ellipse cx="80" cy="115" rx="18" ry="10" fill="url(#faceGradient)" />

          {/* Head */}
          <circle
            cx="80"
            cy="70"
            r="50"
            fill="url(#faceGradient)"
            filter="url(#shadow)"
          />

          {/* Hair - friendly rounded style */}
          {/* Main top hair - soft rounded */}
          <ellipse
            cx="80"
            cy="28"
            rx="35"
            ry="15"
            fill="url(#hairGradient)"
          />

          {/* Hair highlight */}
          <ellipse
            cx="75"
            cy="25"
            rx="20"
            ry="8"
            fill="#93C5FD"
            opacity="0.4"
          />

          {/* Left eye white */}
          <ellipse cx="62" cy="65" rx="12" ry="14" fill="white" />
          {/* Right eye white */}
          <ellipse cx="98" cy="65" rx="12" ry="14" fill="white" />

          {/* Left pupil */}
          <circle
            cx="64"
            cy="67"
            r="6"
            fill="#1E40AF"
            className={cn(animated && 'animate-look')}
          />
          {/* Right pupil */}
          <circle
            cx="100"
            cy="67"
            r="6"
            fill="#1E40AF"
            className={cn(animated && 'animate-look')}
          />

          {/* Left eye shine */}
          <circle cx="66" cy="64" r="2" fill="white" />
          {/* Right eye shine */}
          <circle cx="102" cy="64" r="2" fill="white" />

          {/* Eyebrows */}
          <path
            d="M50 52 Q62 48 74 52"
            stroke="#64748B"
            strokeWidth="3"
            strokeLinecap="round"
            fill="none"
          />
          <path
            d="M86 52 Q98 48 110 52"
            stroke="#64748B"
            strokeWidth="3"
            strokeLinecap="round"
            fill="none"
          />

          {/* Smile */}
          <path
            d="M60 88 Q80 102 100 88"
            stroke="#2563EB"
            strokeWidth="4"
            strokeLinecap="round"
            fill="none"
            className={cn(animated && 'animate-smile')}
          />

          {/* Cheeks blush */}
          <ellipse cx="45" cy="80" rx="8" ry="5" fill="#FCA5A5" opacity="0.4" />
          <ellipse cx="115" cy="80" rx="8" ry="5" fill="#FCA5A5" opacity="0.4" />

          {/* === DECORATIONS === */}

          {/* Legal pin on lapel */}
          <circle cx="56" cy="140" r="5" fill="#FBBF24" />
          <text x="56" y="143" textAnchor="middle" fill="#1E40AF" fontSize="7" fontWeight="bold">§</text>

          {/* Sparkles around head */}
          <g className={cn(animated && 'animate-sparkle')}>
            <path d="M20 40 L22 45 L27 47 L22 49 L20 54 L18 49 L13 47 L18 45 Z" fill="#FBBF24" />
          </g>
          <g className={cn(animated && 'animate-sparkle')} style={{ animationDelay: '0.5s' }}>
            <path d="M140 35 L142 40 L147 42 L142 44 L140 49 L138 44 L133 42 L138 40 Z" fill="#FBBF24" />
          </g>
          <g className={cn(animated && 'animate-sparkle')} style={{ animationDelay: '1s' }}>
            <path d="M145 75 L146 78 L149 79 L146 80 L145 83 L144 80 L141 79 L144 78 Z" fill="#60A5FA" />
          </g>
        </svg>
      </div>
    </div>
  )
}
