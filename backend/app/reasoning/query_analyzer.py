import json
from openai import OpenAI
from backend.app.config import settings

class QueryAnalyzer:
    def __init__(self):
        self.client = OpenAI(api_key=settings.LLM_API_KEY, base_url=settings.LLM_BASE_URL)
        self.model = settings.LLM_MODEL

    def analyze(self, query: str) -> dict:
        prompt = f"Analyze this question: {query}\nExtract topic, entities, conditions, numbers, dates, requested_action as JSON."
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                response_format={ "type": "json_object" }
            )
            return json.loads(response.choices[0].message.content)
        except Exception:
            return {"topic": query}
