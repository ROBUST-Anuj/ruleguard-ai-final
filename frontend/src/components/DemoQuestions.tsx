import { HelpCircle } from 'lucide-react';

interface Props {
  onSelect: (question: string) => void;
}

const DEMO_QUESTIONS = [
  { text: "What is the minimum attendance required for semester examinations?", type: "supported" },
  { text: "What happens if I miss the examination because of a family wedding?", type: "not_found" },
  { text: "Can I appear for the examination with 68% attendance if I have a medical exemption?", type: "contradiction" }
];

export default function DemoQuestions({ onSelect }: Props) {
  return (
    <div className="w-full mt-4">
      <div className="flex items-center text-slate-500 mb-3 space-x-2">
        <HelpCircle className="w-4 h-4" />
        <span className="text-sm font-medium">Try these examples:</span>
      </div>
      <div className="flex flex-col space-y-2">
        {DEMO_QUESTIONS.map((q, idx) => (
          <button
            key={idx}
            onClick={() => onSelect(q.text)}
            className="text-left bg-white px-4 py-3 rounded-lg border border-slate-200 hover:border-primary hover:bg-slate-50 transition-colors text-sm text-slate-700 shadow-sm flex items-center justify-between group"
          >
            <span>"{q.text}"</span>
            <span className="text-xs font-mono text-slate-400 group-hover:text-primary capitalize opacity-50">
              {q.type.replace('_', ' ')} test
            </span>
          </button>
        ))}
      </div>
    </div>
  );
}
