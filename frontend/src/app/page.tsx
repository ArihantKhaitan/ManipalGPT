'use client'

import { useState, useRef, useEffect } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { Send, Bot, User, Menu, X, Sparkles, Square, MessageSquare, Settings, LogOut } from 'lucide-react'
import { ScrollArea } from '@/components/ui/scroll-area'
import { cn } from '@/lib/utils'

interface Message {
  id: string
  type: 'user' | 'ai'
  content: string
  timestamp: string
}

interface QuickAction {
  id: string
  label: string
  query: string
}

const quickActions: QuickAction[] = [
  { id: '1', label: 'Course Information', query: 'Tell me about available courses' },
  { id: '2', label: 'Exam Schedule', query: 'When are the upcoming exams?' },
  { id: '3', label: 'Library Hours', query: 'What are the library timings?' },
  { id: '4', label: 'Campus Events', query: 'What events are happening on campus?' },
  { id: '5', label: 'Hostel Info', query: 'Tell me about hostel facilities' },
  { id: '6', label: 'Academic Calendar', query: 'Show me the academic calendar' },
]

function MessageTimestamp({ timestamp, align }: { timestamp: string; align: 'left' | 'right' }) {
  const [timeString, setTimeString] = useState<string>('')

  useEffect(() => {
    const date = new Date(timestamp)
    setTimeString(date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }))
  }, [timestamp])

  if (!timeString) return null

  return (
    <p className={cn(
      "text-[10px] opacity-40 mt-1.5 px-2",
      align === 'right' ? "text-right text-white/60" : "text-left text-black/40"
    )}>
      {timeString}
    </p>
  )
}

export default function ChatInterface() {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: '1',
      type: 'ai',
      content: 'Hello! I\'m your MIT Manipal AI Assistant. I can help you with course information, exam schedules, campus facilities, and much more. How can I assist you today?',
      timestamp: new Date().toISOString(),
    },
  ])
  const [inputValue, setInputValue] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [isSidebarOpen, setIsSidebarOpen] = useState(false)
  const [abortController, setAbortController] = useState<AbortController | null>(null)
  const messagesEndRef = useRef<HTMLDivElement>(null)
  const inputRef = useRef<HTMLTextAreaElement>(null)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  useEffect(() => {
    if (!isLoading && inputRef.current) {
      inputRef.current.focus()
    }
  }, [isLoading])

  const handleSendMessage = async (content: string) => {
    if (!content.trim() || isLoading) return

    const userMessage: Message = {
      id: Date.now().toString(),
      type: 'user',
      content: content.trim(),
      timestamp: new Date().toISOString(),
    }

    setMessages(prev => [...prev, userMessage])
    setInputValue('')
    
    const controller = new AbortController()
    setAbortController(controller)
    setIsLoading(true)

    try {
      const response = await fetch('/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: content.trim() }),
        signal: controller.signal,
      })

      if (!response.ok) throw new Error('Failed to get response')

      const data = await response.json()
      
      const aiMessage: Message = {
        id: (Date.now() + 1).toString(),
        type: 'ai',
        content: data.response || 'I apologize, but I encountered an error. Please try again.',
        timestamp: new Date().toISOString(),
      }

      setMessages(prev => [...prev, aiMessage])
    } catch (error: any) {
      if (error.name === 'AbortError') {
        const stopMessage: Message = {
          id: (Date.now() + 1).toString(),
          type: 'ai',
          content: 'Response generation stopped.',
          timestamp: new Date().toISOString(),
        }
        setMessages(prev => [...prev, stopMessage])
      } else {
        console.error('Error:', error)
        const errorMessage: Message = {
          id: (Date.now() + 1).toString(),
          type: 'ai',
          content: 'I apologize, but I\'m currently experiencing technical difficulties. Please try again later.',
          timestamp: new Date().toISOString(),
        }
        setMessages(prev => [...prev, errorMessage])
      }
    } finally {
      setIsLoading(false)
      setAbortController(null)
      inputRef.current?.focus()
    }
  }

  const handleStop = () => {
    if (abortController) {
      abortController.abort()
      setIsLoading(false)
      setAbortController(null)
      inputRef.current?.focus()
    }
  }

  const handleQuickAction = (query: string) => {
    handleSendMessage(query)
    setIsSidebarOpen(false)
  }

  const handleNewChat = () => {
    setMessages([{
      id: '1',
      type: 'ai',
      content: 'Hello! I\'m your MIT Manipal AI Assistant. How can I help you today?',
      timestamp: new Date().toISOString(),
    }])
    setInputValue('')
    setIsSidebarOpen(false)
  }

  const handleKeyPress = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSendMessage(inputValue)
    }
  }

  return (
    <div className="h-screen w-screen flex relative overflow-hidden font-sans bg-black">
      {/* Animated gradient background */}
      <div className="absolute inset-0 overflow-hidden">
        <div 
          className="absolute inset-0"
          style={{
            background: 'linear-gradient(135deg, #0a0a0a 0%, #1a0a0a 25%, #0f0a0a 50%, #1a0a0a 75%, #0a0a0a 100%)',
            backgroundSize: '400% 400%',
            animation: 'gradientShift 30s ease infinite'
          }}
        />
        {/* Orange accent blobs */}
        <div 
          className="absolute top-0 right-0 w-[700px] h-[700px] rounded-full opacity-25"
          style={{
            background: 'radial-gradient(circle, rgba(255, 107, 53, 0.5) 0%, transparent 70%)',
            filter: 'blur(140px)',
            animation: 'float 25s ease-in-out infinite',
            transform: 'translate(25%, -25%)'
          }}
        />
        <div 
          className="absolute bottom-0 left-0 w-[600px] h-[600px] rounded-full opacity-20"
          style={{
            background: 'radial-gradient(circle, rgba(255, 140, 66, 0.4) 0%, transparent 70%)',
            filter: 'blur(120px)',
            animation: 'float 30s ease-in-out infinite reverse',
            transform: 'translate(-25%, 25%)'
          }}
        />
      </div>

      {/* Sidebar */}
      <aside 
        className={cn(
          "fixed lg:static inset-y-0 left-0 z-50 w-72 h-screen transition-transform duration-300 ease-out",
          isSidebarOpen ? "translate-x-0" : "-translate-x-full lg:translate-x-0"
        )}
        style={{
          background: 'rgba(0, 0, 0, 0.5)',
          backdropFilter: 'blur(50px) saturate(200%)',
          WebkitBackdropFilter: 'blur(50px) saturate(200%)',
          borderRight: '1px solid rgba(255, 107, 53, 0.1)',
          boxShadow: '4px 0 40px rgba(0, 0, 0, 0.3)'
        }}
      >
        <div className="flex flex-col h-full">
          {/* Sidebar Header */}
          <div className="px-6 py-8 border-b border-white/5">
            <div className="flex items-center justify-between">
              <div>
                <h1 className="text-white font-semibold text-xl tracking-tight mb-1">
                  MIT Manipal
                </h1>
                <p className="text-white/40 text-xs font-light">AI Assistant</p>
              </div>
              <button
                onClick={() => setIsSidebarOpen(false)}
                className="lg:hidden p-1.5 rounded-lg hover:bg-white/5 transition-colors text-white/40 hover:text-white/80"
              >
                <X className="w-4 h-4" />
              </button>
            </div>
          </div>
          
          {/* Navigation */}
          <div className="flex-1 overflow-y-auto py-6">
            <nav className="px-4 space-y-2">
              <button
                onClick={handleNewChat}
                className="w-full flex items-center gap-3 px-4 py-3 rounded-xl transition-all duration-200 text-sm font-medium text-white/70 hover:text-white hover:bg-white/5 border border-transparent hover:border-white/10"
              >
                <MessageSquare className="w-4 h-4 shrink-0" />
                <span>New Chat</span>
              </button>
              <button
                className="w-full flex items-center gap-3 px-4 py-3 rounded-xl transition-all duration-200 text-sm font-medium text-white/70 hover:text-white hover:bg-white/5 border border-transparent hover:border-white/10"
              >
                <Settings className="w-4 h-4 shrink-0" />
                <span>Settings</span>
              </button>
            </nav>

            {/* Quick Actions */}
            <div className="mt-8 px-4">
              <div className="flex items-center gap-2 px-4 mb-4">
                <Sparkles className="w-3.5 h-3.5 text-white/40 shrink-0" />
                <h3 className="text-[10px] font-medium text-white/40 uppercase tracking-wider">
                  Quick Actions
                </h3>
              </div>
              <div className="space-y-1.5">
                {quickActions.map((action) => (
                  <button
                    key={action.id}
                    onClick={() => handleQuickAction(action.query)}
                    className="w-full text-left px-4 py-2.5 rounded-lg transition-all duration-200 text-white/50 hover:text-white/90 hover:bg-white/5 text-xs font-normal border border-transparent hover:border-white/5"
                  >
                    {action.label}
                  </button>
                ))}
              </div>
            </div>
          </div>

          {/* Footer */}
          <div className="p-4 border-t border-white/5 shrink-0">
            <button className="w-full flex items-center gap-3 px-4 py-3 rounded-xl text-white/40 hover:text-white/70 hover:bg-white/5 transition-all duration-200 text-sm font-normal border border-transparent hover:border-white/5">
              <LogOut className="w-4 h-4 shrink-0" />
              <span>Sign Out</span>
            </button>
          </div>
        </div>
      </aside>

      {/* Mobile Overlay */}
      {isSidebarOpen && (
        <div 
          className="fixed inset-0 bg-black/50 z-40 lg:hidden backdrop-blur-sm"
          onClick={() => setIsSidebarOpen(false)}
        />
      )}

      {/* Main Content */}
      <main className="flex-1 flex flex-col min-w-0 h-screen relative z-10">
        {/* Header */}
        <header 
          className="h-20 flex items-center justify-between px-8 shrink-0"
          style={{
            background: 'rgba(0, 0, 0, 0.4)',
            backdropFilter: 'blur(50px) saturate(200%)',
            WebkitBackdropFilter: 'blur(50px) saturate(200%)',
            borderBottom: '1px solid rgba(255, 107, 53, 0.1)',
          }}
        >
          <button 
            onClick={() => setIsSidebarOpen(!isSidebarOpen)}
            className="lg:hidden p-2 rounded-lg hover:bg-white/5 transition-colors text-white/60 hover:text-white/90"
          >
            <Menu className="w-5 h-5" />
          </button>
          
          <div className="flex-1" />
          
          <div 
            className="w-9 h-9 rounded-xl flex items-center justify-center cursor-pointer hover:bg-white/5 transition-colors shrink-0"
            style={{
              background: 'rgba(255, 255, 255, 0.05)',
              border: '1px solid rgba(255, 107, 53, 0.2)',
            }}
          >
            <User className="w-4 h-4 text-white/50" />
          </div>
        </header>

        {/* Chat Messages Area */}
        <div className="flex-1 overflow-hidden min-h-0">
          <ScrollArea className="h-full">
            <div className="max-w-4xl mx-auto px-8 py-12 space-y-8">
              <AnimatePresence>
                {messages.map((message) => (
                  <motion.div
                    key={message.id}
                    initial={{ opacity: 0, y: 10 }}
                    animate={{ opacity: 1, y: 0 }}
                    exit={{ opacity: 0, y: -10 }}
                    transition={{ duration: 0.25 }}
                    className={cn(
                      "flex items-start gap-4",
                      message.type === 'user' ? "justify-end" : "justify-start"
                    )}
                  >
                    {message.type === 'ai' && (
                      <div 
                        className="w-8 h-8 rounded-xl flex items-center justify-center shrink-0 mt-1"
                        style={{
                          background: 'rgba(255, 255, 255, 0.1)',
                          border: '1px solid rgba(255, 255, 255, 0.15)',
                          boxShadow: '0 4px 12px rgba(0, 0, 0, 0.2)'
                        }}
                      >
                        <Bot className="w-4 h-4 text-white/70" />
                      </div>
                    )}
                    <div className={cn(
                      "flex flex-col",
                      message.type === 'user' ? "items-end" : "items-start",
                      "max-w-[78%]"
                    )}>
                      <div
                        className={cn(
                          "px-6 py-4 rounded-3xl",
                          message.type === 'user' ? "rounded-br-lg" : "rounded-bl-lg"
                        )}
                        style={
                          message.type === 'user'
                            ? {
                                background: 'linear-gradient(135deg, rgba(255, 107, 53, 0.95) 0%, rgba(196, 69, 54, 0.95) 100%)',
                                backdropFilter: 'blur(30px)',
                                border: '1px solid rgba(255, 255, 255, 0.15)',
                                color: '#ffffff',
                                boxShadow: '0 8px 32px rgba(255, 107, 53, 0.3), inset 0 1px 0 rgba(255, 255, 255, 0.2)'
                              }
                            : {
                                background: 'rgba(255, 255, 255, 0.98)',
                                backdropFilter: 'blur(30px)',
                                border: '1px solid rgba(0, 0, 0, 0.06)',
                                color: '#1a1a1a',
                                boxShadow: '0 8px 32px rgba(0, 0, 0, 0.1), inset 0 1px 0 rgba(255, 255, 255, 0.8)'
                              }
                        }
                      >
                        <p className="text-[15.5px] leading-relaxed whitespace-pre-wrap font-normal">
                          {message.content}
                        </p>
                      </div>
                      <MessageTimestamp 
                        timestamp={message.timestamp} 
                        align={message.type === 'user' ? 'right' : 'left'} 
                      />
                    </div>
                    {message.type === 'user' && (
                      <div 
                        className="w-8 h-8 rounded-xl flex items-center justify-center shrink-0 mt-1"
                        style={{
                          background: 'linear-gradient(135deg, rgba(255, 107, 53, 0.95) 0%, rgba(196, 69, 54, 0.95) 100%)',
                          boxShadow: '0 4px 12px rgba(255, 107, 53, 0.3)'
                        }}
                      >
                        <User className="w-4 h-4 text-white" />
                      </div>
                    )}
                  </motion.div>
                ))}
              </AnimatePresence>

              {isLoading && (
                <motion.div
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                  className="flex items-start gap-4"
                >
                  <div 
                    className="w-8 h-8 rounded-xl flex items-center justify-center shrink-0 mt-1"
                    style={{
                      background: 'rgba(255, 255, 255, 0.1)',
                      border: '1px solid rgba(255, 255, 255, 0.15)',
                      boxShadow: '0 4px 12px rgba(0, 0, 0, 0.2)'
                    }}
                  >
                    <Bot className="w-4 h-4 text-white/70" />
                  </div>
                  <div
                    className="rounded-3xl rounded-bl-lg px-6 py-4"
                    style={{
                      background: 'rgba(255, 255, 255, 0.98)',
                      backdropFilter: 'blur(30px)',
                      border: '1px solid rgba(0, 0, 0, 0.06)',
                      boxShadow: '0 8px 32px rgba(0, 0, 0, 0.1)'
                    }}
                  >
                    <div className="flex gap-2">
                      <div className="w-2.5 h-2.5 bg-black/30 rounded-full animate-bounce" />
                      <div 
                        className="w-2.5 h-2.5 bg-black/30 rounded-full animate-bounce" 
                        style={{ animationDelay: '0.15s' }}
                      />
                      <div 
                        className="w-2.5 h-2.5 bg-black/30 rounded-full animate-bounce" 
                        style={{ animationDelay: '0.3s' }}
                      />
                    </div>
                  </div>
                </motion.div>
              )}
              <div ref={messagesEndRef} />
            </div>
          </ScrollArea>
        </div>

        {/* Input Area */}
        <div 
          className="shrink-0 px-8 py-6"
          style={{
            background: 'rgba(0, 0, 0, 0.4)',
            backdropFilter: 'blur(50px) saturate(200%)',
            WebkitBackdropFilter: 'blur(50px) saturate(200%)',
            borderTop: '1px solid rgba(255, 107, 53, 0.1)',
          }}
        >
          <div className="max-w-4xl mx-auto">
            <div
              className="flex items-end gap-3 p-4 rounded-2xl"
              style={{
                background: 'rgba(255, 255, 255, 0.98)',
                backdropFilter: 'blur(30px)',
                border: '1px solid rgba(255, 107, 53, 0.15)',
                boxShadow: '0 8px 32px rgba(0, 0, 0, 0.15), inset 0 1px 0 rgba(255, 255, 255, 0.9)'
              }}
            >
              <textarea
                ref={inputRef}
                value={inputValue}
                onChange={(e) => setInputValue(e.target.value)}
                onKeyPress={handleKeyPress}
                placeholder="Ask me about MIT Manipal..."
                className="flex-1 bg-transparent border-none outline-none resize-none text-[15.5px] placeholder:text-gray-400 text-gray-900 max-h-32 py-1.5 font-normal scrollbar-hide min-h-[28px]"
                rows={1}
                disabled={isLoading}
                autoFocus
                style={{ color: '#1a1a1a' }}
              />
              
              {isLoading ? (
                <button
                  onClick={handleStop}
                  className="shrink-0 w-11 h-11 rounded-xl flex items-center justify-center transition-all duration-200 hover:opacity-80 active:scale-95"
                  style={{
                    background: '#ef4444',
                    boxShadow: '0 4px 16px rgba(239, 68, 68, 0.4)'
                  }}
                  title="Stop generating"
                >
                  <Square className="w-4 h-4 text-white" />
                </button>
              ) : (
                <button
                  onClick={() => handleSendMessage(inputValue)}
                  disabled={!inputValue.trim()}
                  className={cn(
                    "shrink-0 w-11 h-11 rounded-xl flex items-center justify-center transition-all duration-200",
                    inputValue.trim() ? "hover:opacity-90 active:scale-95" : "",
                    "disabled:opacity-30 disabled:cursor-not-allowed"
                  )}
                  style={{
                    background: inputValue.trim() 
                      ? 'linear-gradient(135deg, #FF6B35 0%, #C44536 100%)'
                      : 'rgba(0, 0, 0, 0.1)',
                    boxShadow: inputValue.trim() 
                      ? '0 4px 16px rgba(255, 107, 53, 0.4), inset 0 1px 0 rgba(255, 255, 255, 0.2)' 
                      : 'none'
                  }}
                >
                  <Send className="w-4 h-4 text-white" />
                </button>
              )}
            </div>
            
            <p className="text-[11px] text-white/40 text-center mt-4 font-light">
              Responses can be wrong, please check • Press Enter to send
            </p>
          </div>
        </div>
      </main>
    </div>
  )
}
