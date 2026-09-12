import { AlertTriangle, BookOpen, ChevronRight } from 'lucide-react';
import { QueryResponse } from '../types';
import EvidenceDrawer from './EvidenceDrawer';

interface Props {
  response: QueryResponse;
}

export default function ContradictionResponse({ response }: Props) {
  const conflicts = response.conflicts || [];

  return (
    <div className="space-y-6">
      <div className="flex items-center space-x-2 text-red-600 bg-red-50 px-3 py-1.5 rounded-full w-fit">
        <AlertTriangle className="w-4 h-4" />
        <span className="text-sm font-semibold tracking-wide">CONTRADICTION DETECTED</span>
      </div>
      
      <div className="text-slate-800 leading-relaxed">
        <p>{response.answer}</p>
      </div>

      {conflicts.map((conflict, idx) => (
        <div key={idx} className="mt-6 space-y-4 border-t border-slate-200 pt-6">
          <h4 className="text-sm font-semibold text-slate-800 flex items-center">
            <span className="bg-slate-200 w-6 h-6 rounded-full flex items-center justify-center mr-2 text-xs">
              {idx + 1}
            </span>
            Conflicting Provisions
          </h4>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {/* Provision A */}
            <div className="bg-red-50/50 border border-red-100 rounded-lg p-4 space-y-3">
              <div className="flex items-center justify-between text-xs font-semibold text-red-800 uppercase tracking-wider">
                <span>Provision A</span>
              </div>
              <p className="text-sm text-slate-700 italic border-l-2 border-red-300 pl-3">
                "{conflict.evidence_a}"
              </p>
              <div className="flex flex-col text-xs text-slate-500 mt-2 bg-white p-2 rounded border border-slate-100">
                <span className="font-medium flex items-center">
                  <BookOpen className="w-3 h-3 mr-1" /> 
                  {conflict.citation_a.document}
                </span>
                {conflict.citation_a.section && <span>Section: {conflict.citation_a.section}</span>}
              </div>
            </div>

            {/* Provision B */}
            <div className="bg-red-50/50 border border-red-100 rounded-lg p-4 space-y-3">
              <div className="flex items-center justify-between text-xs font-semibold text-red-800 uppercase tracking-wider">
                <span>Provision B</span>
              </div>
              <p className="text-sm text-slate-700 italic border-l-2 border-red-300 pl-3">
                "{conflict.evidence_b}"
              </p>
              <div className="flex flex-col text-xs text-slate-500 mt-2 bg-white p-2 rounded border border-slate-100">
                <span className="font-medium flex items-center">
                  <BookOpen className="w-3 h-3 mr-1" /> 
                  {conflict.citation_b.document}
                </span>
                {conflict.citation_b.section && <span>Section: {conflict.citation_b.section}</span>}
              </div>
            </div>
          </div>
          
          <div className="bg-slate-50 p-3 rounded-lg border border-slate-200 text-sm text-slate-700 flex items-start">
            <ChevronRight className="w-4 h-4 text-slate-400 mr-2 mt-0.5 shrink-0" />
            <p><span className="font-semibold text-slate-800">Conflict Reason:</span> {conflict.reason}</p>
          </div>
        </div>
      ))}

      <EvidenceDrawer evidence={response.evidence} />
    </div>
  );
}
