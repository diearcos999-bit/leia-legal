'use client'

import { cn } from '@/lib/utils'

interface LeiaLogoProps {
  size?: 'sm' | 'md' | 'lg'
  className?: string
  showText?: boolean
}

export function LeiaLogo({ size = 'md', className, showText = true }: LeiaLogoProps) {
  const sizeClasses = {
    sm: 'h-7 w-7',
    md: 'h-9 w-9',
    lg: 'h-11 w-11'
  }

  const textSizes = {
    sm: 'text-lg',
    md: 'text-xl',
    lg: 'text-2xl'
  }

  return (
    <div className={cn('flex items-center gap-2.5 group', className)}>
      {/* Logo icon - mini LEIA face */}
      <div className="relative">
        <div className="absolute inset-0 bg-pacific-500/20 rounded-xl blur-lg group-hover:bg-pacific-500/30 transition-colors" />
        <div className={cn(
          'relative rounded-xl bg-gradient-to-br from-pacific-500 to-pacific-600 flex items-center justify-center shadow-lg shadow-pacific-500/25 overflow-hidden',
          sizeClasses[size]
        )}>
          <svg
            viewBox="0 0 40 40"
            fill="none"
            xmlns="http://www.w3.org/2000/svg"
            className="w-full h-full"
          >
            {/* Background circle - face */}
            <circle cx="20" cy="20" r="16" fill="white" />

            {/* Hair */}
            <ellipse cx="20" cy="8" rx="10" ry="4" fill="#60A5FA" />
            <ellipse cx="18" cy="7" rx="6" ry="2.5" fill="#93C5FD" opacity="0.5" />

            {/* Left eye */}
            <ellipse cx="15" cy="18" rx="3.5" ry="4" fill="white" />
            <circle cx="15.5" cy="19" r="2" fill="#1E40AF" />
            <circle cx="16" cy="18" r="0.7" fill="white" />

            {/* Right eye */}
            <ellipse cx="25" cy="18" rx="3.5" ry="4" fill="white" />
            <circle cx="25.5" cy="19" r="2" fill="#1E40AF" />
            <circle cx="26" cy="18" r="0.7" fill="white" />

            {/* Eyebrows */}
            <path
              d="M11 15 Q15 13.5 19 15"
              stroke="#64748B"
              strokeWidth="1"
              strokeLinecap="round"
              fill="none"
            />
            <path
              d="M21 15 Q25 13.5 29 15"
              stroke="#64748B"
              strokeWidth="1"
              strokeLinecap="round"
              fill="none"
            />

            {/* Smile */}
            <path
              d="M14 26 Q20 30 26 26"
              stroke="#2563EB"
              strokeWidth="1.5"
              strokeLinecap="round"
              fill="none"
            />

            {/* Cheeks */}
            <ellipse cx="10" cy="23" rx="2" ry="1.2" fill="#FCA5A5" opacity="0.4" />
            <ellipse cx="30" cy="23" rx="2" ry="1.2" fill="#FCA5A5" opacity="0.4" />
          </svg>
        </div>
      </div>

      {/* Text with Chilean flag */}
      {showText && (
        <div className="flex items-center gap-1.5">
          <span className={cn(
            'font-semibold text-slate-800 tracking-tight',
            textSizes[size]
          )}>
            LEIA
          </span>
          {/* Mini Chilean flag */}
          <svg
            viewBox="0 0 30 20"
            className="h-3 w-4 rounded-sm opacity-80 group-hover:opacity-100 transition-opacity"
            aria-label="Chile"
          >
            <rect x="0" y="0" width="10" height="10" fill="#0039A6" />
            <polygon
              points="5,2 6.2,5.5 9.5,5.5 6.8,7.5 7.8,11 5,8.5 2.2,11 3.2,7.5 0.5,5.5 3.8,5.5"
              fill="white"
              transform="scale(0.7) translate(2.1, 1.4)"
            />
            <rect x="10" y="0" width="20" height="10" fill="white" />
            <rect x="0" y="10" width="30" height="10" fill="#D52B1E" />
          </svg>
        </div>
      )}
    </div>
  )
}
