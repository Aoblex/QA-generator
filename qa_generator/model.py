from openai import OpenAI
from .prompts import CHAT_HISTORY, INPUT_TEMPLATE
import logging

class QAModel():

    api_key="sk-egkbiFTEc8E2FDN2Ec1470B3AdDc4d25B6417d8d75E9BaE7"
    base_url = "https://api.132999.xyz/v1"
    client = OpenAI(api_key=api_key, base_url=base_url)

    @classmethod
    def generate(self, context):
        logging.info(f"Generating response for '{context[:50]}...'")
        messages = CHAT_HISTORY.copy()
        messages.append({
            'role': 'user',
            'content': INPUT_TEMPLATE.format(context=context)
        })
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo-1106",
            response_format={"type": "json_object"},
            temperature=1.5, # [0, 2.0]
            frequency_penalty=1.5, # [-2.0, 2.0] 减少重复内容
            presence_penalty=1.5, # [-2.0, 2.0] 增加新主题可能性
            messages=messages,
        )
        result = response.choices[0].message.content
        return result