import { QueryResponse } from '../types';
import SupportedResponse from './SupportedResponse';
import NotFoundResponse from './NotFoundResponse';
import ContradictionResponse from './ContradictionResponse';

interface Props {
  response: QueryResponse;
}

export default function ResponseCard({ response }: Props) {
  return (
    <div className="bg-white rounded-xl shadow-md border border-slate-200 p-6 w-full">
      {response.state === 'SUPPORTED' && <SupportedResponse response={response} />}
      {response.state === 'NOT_FOUND' && <NotFoundResponse response={response} />}
      {response.state === 'CONTRADICTION' && <ContradictionResponse response={response} />}
    </div>
  );
}
