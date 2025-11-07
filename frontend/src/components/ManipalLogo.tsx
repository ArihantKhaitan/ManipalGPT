import React from 'react'

interface ManipalLogoProps {
  className?: string
  variant?: 'full' | 'icon'
}

const ManipalLogo: React.FC<ManipalLogoProps> = ({ className = "w-6 h-6", variant = 'icon' }) => {
  if (variant === 'full') {
    return (
      <div className={`flex flex-col items-center ${className}`}>
        <svg 
          viewBox="0 0 140 140" 
          className="w-32 h-32 max-w-full max-h-full"
          fill="none" 
          xmlns="http://www.w3.org/2000/svg"
          preserveAspectRatio="xMidYMid meet"
        >
          <defs>
            <linearGradient id="logoGradient" x1="0%" y1="0%" x2="0%" y2="100%">
              <stop offset="0%" stopColor="#FF8C42" />
              <stop offset="50%" stopColor="#FF6B35" />
              <stop offset="100%" stopColor="#C44536" />
            </linearGradient>
          </defs>
          
          <ellipse cx="70" cy="40" rx="9" ry="14" fill="url(#logoGradient)" />
          
          <path 
            d="M 52 58 Q 52 63 54 68 L 54 85 Q 54 90 57 90 L 60 90 Q 63 90 63 85 L 63 68 Q 63 63 70 59 Q 77 63 77 68 L 77 85 Q 77 90 80 90 L 83 90 Q 86 90 86 85 L 86 68 Q 86 63 88 58 Z" 
            fill="url(#logoGradient)" 
          />
          
          <path 
            d="M 35 90 Q 28 78 28 65 Q 28 52 35 42 Q 42 32 52 28 Q 58 24 62 26 Q 66 28 70 35" 
            stroke="#8B4513" 
            strokeWidth="2.5" 
            fill="none"
            strokeLinecap="round"
          />
          
          {[38, 43, 48, 53, 58, 63].map((y, i) => (
            <ellipse 
              key={i} 
              cx={30 + i * 3} 
              cy={y} 
              rx="4" 
              ry="6" 
              fill="#8B4513" 
              transform={`rotate(-${15 + i * 4} ${30 + i * 3} ${y})`} 
            />
          ))}
          
          <path 
            d="M 105 90 Q 112 78 112 65 Q 112 52 105 42 Q 98 32 88 28 Q 82 24 78 26 Q 74 28 70 35" 
            stroke="#8B4513" 
            strokeWidth="2.5" 
            fill="none"
            strokeLinecap="round"
          />
          
          {[38, 43, 48, 53, 58, 63].map((y, i) => (
            <ellipse 
              key={i} 
              cx={110 - i * 3} 
              cy={y} 
              rx="4" 
              ry="6" 
              fill="#8B4513" 
              transform={`rotate(${15 + i * 4} ${110 - i * 3} ${y})`} 
            />
          ))}
          
          <path 
            d="M 62 90 L 78 90 M 70 82 L 70 98" 
            stroke="#8B4513" 
            strokeWidth="3" 
            strokeLinecap="round"
          />
          
          <text 
            x="70" 
            y="115" 
            textAnchor="middle" 
            fontSize="10" 
            fill="#8B4513"
            fontFamily="serif"
            fontWeight="600"
            letterSpacing="1"
          >
            INSPIRED BY LIFE
          </text>
        </svg>
        <div className="mt-3 text-center">
          <div className="text-xl font-bold text-gray-800" style={{ fontFamily: 'serif', letterSpacing: '1px' }}>
            MANIPAL
          </div>
          <div 
            className="text-xs text-gray-700 mt-1 border-t border-gray-400 pt-1" 
            style={{ fontFamily: 'sans-serif', letterSpacing: '0.5px' }}
          >
            INSTITUTE OF TECHNOLOGY
          </div>
          <div className="text-[10px] text-gray-600 italic mt-1">
            (A constituent unit of MAHE, Manipal)
          </div>
        </div>
      </div>
    )
  }

  // Icon variant - properly sized and constrained
  return (
    <svg 
      viewBox="0 0 100 100" 
      className={className}
      fill="none" 
      xmlns="http://www.w3.org/2000/svg"
      preserveAspectRatio="xMidYMid meet"
      style={{ maxWidth: '100%', maxHeight: '100%', width: '100%', height: '100%' }}
    >
      <defs>
        <linearGradient id="iconGradient" x1="0%" y1="0%" x2="0%" y2="100%">
          <stop offset="0%" stopColor="#FF8C42" />
          <stop offset="50%" stopColor="#FF6B35" />
          <stop offset="100%" stopColor="#C44536" />
        </linearGradient>
      </defs>
      
      <ellipse cx="50" cy="30" rx="7" ry="11" fill="url(#iconGradient)" />
      
      <path 
        d="M 38 43 Q 38 47 40 51 L 40 63 Q 40 67 42.5 67 L 45 67 Q 47.5 67 47.5 63 L 47.5 51 Q 47.5 47 50 45 Q 52.5 47 52.5 51 L 52.5 63 Q 52.5 67 55 67 L 57.5 67 Q 60 67 60 63 L 60 51 Q 60 47 62 43 Z" 
        fill="url(#iconGradient)" 
      />
      
      <path 
        d="M 25 68 Q 20 58 20 48 Q 20 38 25 30 Q 30 22 38 19 Q 42 17 45 18 Q 48 19 50 24" 
        stroke="#8B4513" 
        strokeWidth="2.5" 
        fill="none"
        strokeLinecap="round"
      />
      
      {[32, 38, 44, 50, 56, 62].map((y, i) => (
        <ellipse 
          key={i} 
          cx={22 + i * 2.5} 
          cy={y} 
          rx="3" 
          ry="4.5" 
          fill="#8B4513" 
          transform={`rotate(-${12 + i * 3} ${22 + i * 2.5} ${y})`} 
        />
      ))}
      
      <path 
        d="M 75 68 Q 80 58 80 48 Q 80 38 75 30 Q 70 22 62 19 Q 58 17 55 18 Q 52 19 50 24" 
        stroke="#8B4513" 
        strokeWidth="2.5" 
        fill="none"
        strokeLinecap="round"
      />
      
      {[32, 38, 44, 50, 56, 62].map((y, i) => (
        <ellipse 
          key={i} 
          cx={78 - i * 2.5} 
          cy={y} 
          rx="3" 
          ry="4.5" 
          fill="#8B4513" 
          transform={`rotate(${12 + i * 3} ${78 - i * 2.5} ${y})`} 
        />
      ))}
      
      <path 
        d="M 47 68 L 53 68 M 50 64 L 50 72" 
        stroke="#8B4513" 
        strokeWidth="2.5" 
        strokeLinecap="round"
      />
    </svg>
  )
}

export default ManipalLogo
