from langchain_ollama import ChatOllama

from backend.ai.prompts import (
    SYSTEM_PROMPT,
    RISK_ANALYSIS_PROMPT
)

class CyberLLM:

    def __init__(self):

        self.llm = ChatOllama(

            model="llama3.1:8b",

            temperature=0.2
        )

    def ask(self, context, question):

        prompt = RISK_ANALYSIS_PROMPT.format(

            context=context,

            question=question

        )

        messages = [

            ("system", SYSTEM_PROMPT),

            ("human", prompt)

        ]

        response = self.llm.invoke(messages)

        return response.content