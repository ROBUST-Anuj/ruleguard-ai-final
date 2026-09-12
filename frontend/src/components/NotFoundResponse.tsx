import { SearchX } from 'lucide-react';
import { QueryResponse } from '../types';

interface Props {
  response: QueryResponse;
}

export default function NotFoundResponse({ response }: Props) {
  return (
    <div className="space-y-4">
      <div className="flex items-center space-x-2 text-amber-600 bg-amber-50 px-3 py-1.5 rounded-full w-fit">
        <SearchX className="w-4 h-4" />
        <span className="text-sm font-semibold tracking-wide">NOT FOUND</span>
      </div>
      
      <div className="text-slate-800 leading-relaxed">
        <p>{response.answer}</p>
      </div>
      
      {response.query_analysis && (
        <div className="mt-6 bg-slate-50 border border-slate-200 rounded-lg p-4">
          <h4 className="text-sm font-semibold text-slate-700 mb-2">We searched for:</h4>
          <ul className="list-disc list-inside text-sm text-slate-600 space-y-1">
            <li><span className="font-medium">Topic:</span> {response.query_analysis.topic}</li>
            {response.query_analysis.entities.length > 0 && (
              <li><span className="font-medium">Entities:</span> {response.query_analysis.entities.join(', ')}</li>
            )}
            {response.query_analysis.conditions.length > 0 && (
              <li><span className="font-medium">Conditions:</span> {response.query_analysis.conditions.join(', ')}</li>
            )}
          </ul>
        </div>
      )}
    </div>
  );
}
