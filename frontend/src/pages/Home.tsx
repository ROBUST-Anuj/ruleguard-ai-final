import { useState, useRef, useEffect } from 'react';
import Header from '../components/Header';
import QueryInput from '../components/QueryInput';
import DemoQuestions from '../components/DemoQuestions';
import ResponseCard from '../components/ResponseCard';
import LoadingState from '../components/LoadingState';
import ErrorState from '../components/ErrorState';
import { ChatMessage } from '../types';
import { apiClient } from '../api/client';
import { User, ShieldCheck } from 'lucide-react';

export default function Home() {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSearch = async (query: string) => {
    const userMsgId = Date.now().toString();
    const systemMsgId = (Date.now() + 1).toString();

    // Add user message and initial loading system message
    setMessages(prev => [
      ...prev,
      { id: userMsgId, type: 'user', question: query, timestamp: new Date() },
      { id: systemMsgId, type: 'system', isLoading: true, timestamp: new Date() }
    ]);

    setIsLoading(true);

    try {
      const response = await apiClient.query(query);
      
      setMessages(prev => prev.map(msg => 
        msg.id === systemMsgId 
          ? { ...msg, isLoading: false, response } 
          : msg
      ));
    } catch (error) {
      setMessages(prev => prev.map(msg => 
        msg.id === systemMsgId 
          ? { ...msg, isLoading: false, error: 'Failed to communicate with the RuleGuard API. Please ensure the backend is running.' } 
          : msg
      ));
    } finally {
      setIsLoading(false);
    }
  };

  const handleRetry = (index: number) => {
    // Find the user message right before this error message
    const userMsg = messages[index - 1];
    if (userMsg && userMsg.type === 'user' && userMsg.question) {
      // Remove the error message and retry
      setMessages(prev => prev.filter((_, i) => i !== index));
      handleSearch(userMsg.question);
    }
  };

  return (
    <div className="flex flex-col h-screen bg-slate-50">
      <Header />
      
      <main className="flex-1 overflow-y-auto px-4 py-8">
        <div className="max-w-4xl mx-auto space-y-8 pb-32">
          {messages.length === 0 ? (
            <div className="mt-12 text-center space-y-6">
              <div className="w-20 h-20 bg-primary/10 rounded-full flex items-center justify-center mx-auto mb-4">
                <ShieldCheck className="w-10 h-10 text-primary" />
              </div>
              <h2 className="text-3xl font-bold text-slate-800">Academic Policy QA System</h2>
              <p className="text-lg text-slate-600 max-w-2xl mx-auto">
                Ask questions about university regulations. RuleGuard cross-references policies to provide accurate answers and automatically detects contradictory rules.
              </p>
              
              <div className="max-w-2xl mx-auto text-left mt-12 bg-white p-6 rounded-xl shadow-sm border border-slate-200">
                <DemoQuestions onSelect={handleSearch} />
              </div>
            </div>
          ) : (
            <div className="space-y-6">
              {messages.map((msg, index) => (
                <div key={msg.id} className={`flex ${msg.type === 'user' ? 'justify-end' : 'justify-start'}`}>
                  {msg.type === 'user' ? (
                    <div className="flex items-start max-w-[80%]">
                      <div className="bg-primary text-white rounded-2xl rounded-tr-sm px-5 py-3 shadow-sm">
                        <p className="text-[15px] leading-relaxed">{msg.question}</p>
                      </div>
                      <div className="w-8 h-8 rounded-full bg-slate-200 ml-3 flex items-center justify-center shrink-0 border border-slate-300">
                        <User className="w-5 h-5 text-slate-500" />
                      </div>
                    </div>
                  ) : (
                    <div className="flex items-start w-full max-w-3xl">
                      <div className="w-8 h-8 rounded-full bg-primary/10 border border-primary/20 mr-3 flex items-center justify-center shrink-0">
                        <ShieldCheck className="w-5 h-5 text-primary" />
                      </div>
                      <div className="flex-1">
                        {msg.isLoading ? (
                          <div className="bg-white rounded-2xl rounded-tl-sm shadow-sm border border-slate-200 w-full overflow-hidden">
                            <LoadingState />
                          </div>
                        ) : msg.error ? (
                          <ErrorState message={msg.error} onRetry={() => handleRetry(index)} />
                        ) : msg.response ? (
                          <ResponseCard response={msg.response} />
                        ) : null}
                      </div>
                    </div>
                  )}
                </div>
              ))}
              <div ref={messagesEndRef} />
            </div>
          )}
        </div>
      </main>

      <div className="fixed bottom-0 left-0 right-0 bg-gradient-to-t from-slate-50 via-slate-50 to-transparent pt-6 pb-6 px-4">
        <div className="max-w-4xl mx-auto">
          <QueryInput onSearch={handleSearch} isLoading={isLoading} />
        </div>
      </div>
    </div>
  );
}
