import { NextRequest, NextResponse } from 'next/server'

const BACKEND_URL = process.env.BACKEND_URL || 'http://localhost:8000'

export async function POST(request: NextRequest) {
  try {
    const { message } = await request.json()
    
    if (!message || typeof message !== 'string') {
      return NextResponse.json(
        { error: 'Message is required and must be a string' },
        { status: 400 }
      )
    }

    // Forward request to Python backend
    try {
      const response = await fetch(`${BACKEND_URL}/api/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message }),
      })

      if (!response.ok) {
        throw new Error(`Backend responded with status: ${response.status}`)
      }

      const data = await response.json()
      return NextResponse.json({ 
        response: data.response || 'I apologize, but I encountered an error. Please try again.',
        timestamp: data.timestamp || new Date().toISOString()
      })
    } catch (backendError) {
      console.error('Backend error:', backendError)
      // Fallback response if backend is not available
      return NextResponse.json({
        response: 'I apologize, but I\'m currently unable to connect to the AI service. Please make sure the backend server is running on port 8000. You can start it by running "python backend/main.py" in the project root.',
        timestamp: new Date().toISOString()
      })
    }
  } catch (error) {
    console.error('API Error:', error)
    return NextResponse.json(
      { 
        error: 'Internal server error',
        response: 'I apologize, but I encountered an error. Please try again later.'
      },
      { status: 500 }
    )
  }
}