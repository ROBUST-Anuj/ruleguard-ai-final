import { CheckCircle } from 'lucide-react';
import { QueryResponse } from '../types';
import EvidenceDrawer from './EvidenceDrawer';
import CitationBadge from './CitationBadge';

interface Props {
  response: QueryResponse;
}

export default function SupportedResponse({ response }: Props) {
  const renderAnswerWithCitations = () => {
    const text = response.answer;
    // Match both [SRC-001] and [1] style citations
    const parts = text.split(/(\[SRC-\d+\]|\[\d+\])/g);
    
    return parts.map((part, index) => {
      const srcMatch = part.match(/\[SRC-(\d+)\]/);
      const numMatch = part.match(/\[(\d+)\]/);
      
      if (srcMatch || numMatch) {
        const citationIdx = parseInt((srcMatch?.[1] || numMatch?.[1])!) - 1;
        const citation = response.citations?.[citationIdx];
        
        if (citation) {
          return (
            <CitationBadge
              key={index}
              id={citation.id || `${citationIdx + 1}`}
              document={citation.document}
              section={citation.section}
              onClick={() => {
                const el = document.getElementById('evidence-drawer');
                el?.scrollIntoView({ behavior: 'smooth' });
              }}
            />
          );
        }
      }
      return <span key={index}>{part}</span>;
    });
  };

  return (
    <div className="space-y-4">
      <div className="flex items-center space-x-2 text-emerald-600 bg-emerald-50 px-3 py-1.5 rounded-full w-fit">
        <CheckCircle className="w-4 h-4" />
        <span className="text-sm font-semibold tracking-wide">SUPPORTED</span>
      </div>
      
      <div className="prose prose-slate max-w-none text-slate-800 leading-relaxed">
        <p>{renderAnswerWithCitations()}</p>
      </div>

      <EvidenceDrawer evidence={response.evidence} />
    </div>
  );
}
