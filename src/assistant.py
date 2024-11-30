from src.memory import create_memory, create_context, create_history
from src.embedding import load_and_embedd, encode
from src.args import Args

from langchain.prompts import PromptTemplate
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()


class Assistant:

    def __init__(self):
        self.g_vars = {}
        self.client = OpenAI()
        self.memo = []

    def get_the_prompt(self, question):
        results = self.g_vars['dp'].max_marginal_relevance_search(
            question, k=1, fetch_metadata=True)
        
        template = self.g_vars['config']['prompts']['system_propmt']
        context, sources = create_context(results)
        history = create_history(self.g_vars['memory'].chat_memory.messages)

        new_template = template.format(
            context=context,
            history=history,
            question=question
        )
        prompt = PromptTemplate(
            input_variables=["context", "history", "question"],
            template=new_template
        )
        
        self.sources = sources
        
        print(results)

        return prompt

    def stream_text(self, question):
        prompt = self.get_the_prompt(question)
        return self.openai_llm(prompt, question)

    def openai_llm(self, prompt, question):

        messages = [
            {"role": "system", "content": prompt.template}
        ]

        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            temperature=0,
            messages=messages,
            stream=True,
        )

        res = ""

        for chunk in response:
            txt = chunk.choices[0].delta.content
            if txt:
                res += txt

                yield txt
                
        yield f"\n\n **the source of the data is {self.sources}**"

        self.g_vars['memory'].chat_memory.messages = []
        self.g_vars['memory'].save_context(
            {"input": question}, {"output": res})
