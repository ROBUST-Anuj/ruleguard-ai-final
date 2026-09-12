import { AlertCircle, RefreshCw } from 'lucide-react';

interface Props {
  message: string;
  onRetry: () => void;
}

export default function ErrorState({ message, onRetry }: Props) {
  return (
    <div className="bg-red-50 border border-red-200 rounded-xl p-6 flex flex-col items-center justify-center text-center space-y-4">
      <div className="w-12 h-12 bg-red-100 rounded-full flex items-center justify-center">
        <AlertCircle className="w-6 h-6 text-red-600" />
      </div>
      <div>
        <h3 className="text-lg font-semibold text-red-800">Something went wrong</h3>
        <p className="text-sm text-red-600 mt-1 max-w-md">{message}</p>
      </div>
      <button
        onClick={onRetry}
        className="flex items-center space-x-2 px-4 py-2 bg-white border border-red-200 text-red-700 rounded-lg hover:bg-red-50 transition-colors"
      >
        <RefreshCw className="w-4 h-4" />
        <span>Try Again</span>
      </button>
    </div>
  );
}
