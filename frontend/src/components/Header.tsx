import { BookOpen } from 'lucide-react';

export default function Header() {
  return (
    <header className="bg-primary text-white py-4 px-6 shadow-md">
      <div className="max-w-5xl mx-auto flex items-center space-x-3">
        <BookOpen className="w-8 h-8 text-white" />
        <div>
          <h1 className="text-2xl font-bold tracking-tight">RuleGuard</h1>
          <p className="text-sm text-slate-300 font-medium">University Regulation Assistant</p>
        </div>
      </div>
    </header>
  );
}
