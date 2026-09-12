import { Loader2 } from 'lucide-react';

export default function LoadingState() {
  return (
    <div className="flex flex-col items-center justify-center p-8 space-y-4">
      <Loader2 className="w-8 h-8 text-primary animate-spin" />
      <div className="text-center space-y-1">
        <p className="text-lg font-medium text-slate-800">Analyzing university regulations...</p>
        <div className="text-sm text-slate-500 flex items-center justify-center space-x-2">
          <span className="animate-pulse">Retrieving</span>
          <span>→</span>
          <span className="animate-pulse delay-75">Analyzing</span>
          <span>→</span>
          <span className="animate-pulse delay-150">Generating</span>
        </div>
      </div>
    </div>
  );
}
