interface Props {
  id: string;
  document: string;
  section: string | null;
  onClick: () => void;
}

export default function CitationBadge({ id, document, section, onClick }: Props) {
  return (
    <button
      onClick={onClick}
      className="inline-flex items-center justify-center px-1.5 py-0.5 ml-1 text-xs font-semibold bg-blue-100 text-blue-700 hover:bg-blue-200 hover:text-blue-800 rounded transition-colors group relative"
      title={`${document}${section ? ` - ${section}` : ''}`}
    >
      [{id}]
    </button>
  );
}
