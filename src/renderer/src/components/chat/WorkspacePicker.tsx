import { useState, useEffect } from 'react'
import { FolderSync, Check, ChevronDown, X } from 'lucide-react'
import { Button } from '@/components/ui/button'
import {
  Popover,
  PopoverContent,
  PopoverTrigger
} from '@/components/ui/popover'
import { useAppStore } from '@/lib/store'
import { cn } from '@/lib/utils'

export function WorkspacePicker(): React.JSX.Element {
  const { workspacePath, currentThreadId, setWorkspacePath, setWorkspaceFiles } = useAppStore()
  const [open, setOpen] = useState(false)
  const [loading, setLoading] = useState(false)

  // Load workspace path and files for current thread
  useEffect(() => {
    async function loadWorkspace(): Promise<void> {
      if (currentThreadId) {
        const path = await window.api.workspace.get(currentThreadId)
        setWorkspacePath(path)

        // If a folder is linked, load files from disk
        if (path) {
          const result = await window.api.workspace.loadFromDisk(currentThreadId)
          if (result.success && result.files) {
            setWorkspaceFiles(result.files)
          }
        }
      }
    }
    loadWorkspace()
  }, [currentThreadId, setWorkspacePath, setWorkspaceFiles])

  async function handleSelectFolder(): Promise<void> {
    if (!currentThreadId) return
    setLoading(true)
    try {
      const path = await window.api.workspace.select(currentThreadId)
      if (path) {
        setWorkspacePath(path)
        // Load files from the newly selected folder
        const result = await window.api.workspace.loadFromDisk(currentThreadId)
        if (result.success && result.files) {
          setWorkspaceFiles(result.files)
        }
      }
      setOpen(false)
    } catch (e) {
      console.error('[WorkspacePicker] Select folder error:', e)
    } finally {
      setLoading(false)
    }
  }

  async function handleClearFolder(): Promise<void> {
    if (!currentThreadId) return
    try {
      await window.api.workspace.set(currentThreadId, null)
      setWorkspacePath(null)
      setWorkspaceFiles([])
      setOpen(false)
    } catch (e) {
      console.error('[WorkspacePicker] Clear folder error:', e)
    }
  }

  const folderName = workspacePath?.split('/').pop()

  return (
    <Popover open={open} onOpenChange={setOpen}>
      <PopoverTrigger asChild>
        <Button
          variant="ghost"
          size="sm"
          className={cn(
            'h-7 px-2 text-xs gap-1.5',
            workspacePath ? 'text-foreground' : 'text-muted-foreground'
          )}
          disabled={!currentThreadId}
        >
          <FolderSync className="size-3.5" />
          <span className="max-w-[120px] truncate">
            {workspacePath ? folderName : 'Link folder'}
          </span>
          <ChevronDown className="size-3 opacity-50" />
        </Button>
      </PopoverTrigger>
      <PopoverContent className="w-64 p-3" align="start">
        <div className="space-y-3">
          <div className="text-xs font-medium text-muted-foreground uppercase tracking-wider">
            Workspace Folder
          </div>

          {workspacePath ? (
            <div className="space-y-2">
              <div className="flex items-center gap-2 p-2 rounded-md bg-background-secondary border border-border">
                <Check className="size-3.5 text-status-nominal shrink-0" />
                <span className="text-sm truncate flex-1" title={workspacePath}>
                  {folderName}
                </span>
              </div>
              <p className="text-[11px] text-muted-foreground leading-relaxed">
                Files created by the agent will be synced to this folder.
              </p>
              <div className="flex gap-2">
                <Button
                  variant="outline"
                  size="sm"
                  className="flex-1 h-8 text-xs"
                  onClick={handleSelectFolder}
                  disabled={loading}
                >
                  Change
                </Button>
                <Button
                  variant="ghost"
                  size="sm"
                  className="h-8 px-2"
                  onClick={handleClearFolder}
                >
                  <X className="size-3.5" />
                </Button>
              </div>
            </div>
          ) : (
            <div className="space-y-2">
              <p className="text-[11px] text-muted-foreground leading-relaxed">
                Link a folder to sync files created by the agent to your filesystem.
              </p>
              <Button
                variant="outline"
                size="sm"
                className="w-full h-8 text-xs"
                onClick={handleSelectFolder}
                disabled={loading}
              >
                <FolderSync className="size-3.5 mr-1.5" />
                Select Folder
              </Button>
            </div>
          )}
        </div>
      </PopoverContent>
    </Popover>
  )
}
