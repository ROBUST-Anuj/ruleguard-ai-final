import { useState } from 'react';
import { ChevronDown, FileText, ChevronRight } from 'lucide-react';
import { Evidence } from '../types';

interface Props {
  evidence: Evidence[];
}

export default function EvidenceDrawer({ evidence }: Props) {
  const [isOpen, setIsOpen] = useState(false);

  if (!evidence || evidence.length === 0) return null;

  return (
    <div className="mt-6 border-t border-slate-200 pt-4">
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="flex items-center space-x-2 text-sm font-medium text-slate-600 hover:text-primary transition-colors"
      >
        {isOpen ? <ChevronDown className="w-4 h-4" /> : <ChevronRight className="w-4 h-4" />}
        <span>View Source Evidence ({evidence.length})</span>
      </button>
      
      {isOpen && (
        <div className="mt-4 space-y-4">
          {evidence.map((item, idx) => (
            <div key={idx} className="bg-slate-50 rounded-lg p-4 border border-slate-200 text-sm">
              <div className="flex items-center space-x-2 mb-2 text-slate-700 font-semibold">
                <FileText className="w-4 h-4 text-slate-400" />
                <span>{item.document}</span>
                {item.section && (
                  <>
                    <span className="text-slate-300">•</span>
                    <span className="text-slate-600">{item.section}</span>
                  </>
                )}
                {item.page && (
                  <>
                    <span className="text-slate-300">•</span>
                    <span className="text-slate-500 font-normal">Page {item.page}</span>
                  </>
                )}
              </div>
              <p className="text-slate-600 pl-6 border-l-2 border-slate-300 leading-relaxed italic">
                "{item.text}"
              </p>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
