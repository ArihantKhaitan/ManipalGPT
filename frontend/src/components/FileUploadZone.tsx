import { useState, useCallback } from 'react'
import { useDropzone } from 'react-dropzone'
import { Upload, File, X, AlertCircle, CheckCircle2 } from 'lucide-react'
import { motion, AnimatePresence } from 'framer-motion'

interface FileUploadZoneProps {
  onFileProcess: (content: string) => void
}

export default function FileUploadZone({ onFileProcess }: FileUploadZoneProps) {
  const [files, setFiles] = useState<File[]>([])
  const [processing, setProcessing] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [success, setSuccess] = useState(false)

  const onDrop = useCallback(async (acceptedFiles: File[]) => {
    setError(null)
    setSuccess(false)
    setFiles(acceptedFiles)

    for (const file of acceptedFiles) {
      try {
        setProcessing(true)
        const content = await readFileContent(file)
        onFileProcess(content)
        setSuccess(true)
      } catch (err) {
        setError('Failed to process file. Please try again.')
        console.error('File processing error:', err)
      } finally {
        setProcessing(false)
      }
    }
  }, [onFileProcess])

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'application/pdf': ['.pdf'],
      'application/msword': ['.doc'],
      'application/vnd.openxmlformats-officedocument.wordprocessingml.document': ['.docx'],
      'text/plain': ['.txt']
    },
    maxFiles: 1
  })

  const readFileContent = (file: File): Promise<string> => {
    return new Promise((resolve, reject) => {
      const reader = new FileReader()

      reader.onload = () => {
        resolve(reader.result as string)
      }

      reader.onerror = () => {
        reject(new Error('Failed to read file'))
      }

      reader.readAsText(file)
    })
  }

  const removeFile = (index: number) => {
    setFiles(files => files.filter((_, i) => i !== index))
    setError(null)
    setSuccess(false)
  }

  return (
    <div className="w-full space-y-4">
      <div
        {...getRootProps()}
        className={`dropzone h-32 ${
          isDragActive ? 'dropzone-active' : 'border-muted-foreground/20'
        }`}
      >
        <input {...getInputProps()} />
        <div className="flex flex-col items-center justify-center text-muted-foreground">
          <Upload className="w-8 h-8 mb-2" />
          <p className="text-sm text-center">
            {isDragActive
              ? 'Drop your file here...'
              : 'Drag & drop a file here, or click to select'}
          </p>
          <p className="text-xs mt-1 text-muted-foreground/60">
            Supported: PDF, DOC, DOCX, TXT
          </p>
        </div>
      </div>

      {/* File List */}
      <AnimatePresence>
        {files.map((file, index) => (
          <motion.div
            key={file.name}
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -10 }}
            className="premium-card p-3 rounded-lg flex items-center justify-between"
          >
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-lg bg-primary/10 flex items-center justify-center">
                <File className="w-5 h-5 text-primary" />
              </div>
              <div>
                <p className="text-sm font-medium truncate max-w-[200px]">
                  {file.name}
                </p>
                <p className="text-xs text-muted-foreground">
                  {(file.size / 1024).toFixed(1)} KB
                </p>
              </div>
            </div>
            <div className="flex items-center gap-2">
              {processing && (
                <div className="flex gap-2 items-center text-muted-foreground">
                  <div className="w-4 h-4 rounded-full border-2 border-primary/30 border-t-primary animate-spin" />
                  <span className="text-xs">Processing...</span>
                </div>
              )}
              {error && (
                <div className="flex items-center gap-1.5 text-destructive">
                  <AlertCircle className="w-4 h-4" />
                  <span className="text-xs">{error}</span>
                </div>
              )}
              {success && (
                <div className="flex items-center gap-1.5 text-green-500">
                  <CheckCircle2 className="w-4 h-4" />
                  <span className="text-xs">Processed successfully</span>
                </div>
              )}
              <button
                onClick={() => removeFile(index)}
                className="p-1 hover:bg-muted rounded-md transition-colors"
              >
                <X className="w-4 h-4 text-muted-foreground" />
              </button>
            </div>
          </motion.div>
        ))}
      </AnimatePresence>
    </div>
  )
}