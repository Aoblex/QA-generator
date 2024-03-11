from openai import OpenAI
from .prompts import CHAT_HISTORY, INPUT_TEMPLATE
import logging
from openai.types.chat import ChatCompletion

class QAModel():

    api_key="sk-egkbiFTEc8E2FDN2Ec1470B3AdDc4d25B6417d8d75E9BaE7"
    base_url = "https://api.132999.xyz/v1"
    client = OpenAI(api_key=api_key, base_url=base_url)

    @classmethod
    def generate(self, context,
                 model="gpt-3.5-turbo-1106",
                 temperature=0.5,
                 frequency_penalty=0.08,
                 presence_penalty=0.08,) -> dict:
        logging.info(f"Generating response for '{context[:50]}...'")
        messages = CHAT_HISTORY.copy()
        messages.append({
            'role': 'user',
            'content': INPUT_TEMPLATE.format(context=context)
        })
        response: ChatCompletion = self.client.chat.completions.create(
            model=model,
            response_format={"type": "json_object"},
            temperature=temperature, # [0, 2.0]
            frequency_penalty=frequency_penalty, # [-2.0, 2.0] 减少重复内容
            presence_penalty=presence_penalty, # [-2.0, 2.0] 增加新主题可能性
            messages=messages,
        )
        return response.model_dump()