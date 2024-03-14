from openai import OpenAI
from .prompts import CHAT_HISTORY, INPUT_TEMPLATE
import logging
from openai.types.chat import ChatCompletion
from configs.model_config import (
    MODEL, TEMPERATURE,
    FREQUENCY_PENALTY, PRESENCE_PENALTY,
)

class QAModel():

    api_key="sk-egkbiFTEc8E2FDN2Ec1470B3AdDc4d25B6417d8d75E9BaE7"
    base_url = "https://api.132999.xyz/v1"
    client = OpenAI(api_key=api_key, base_url=base_url)

    @classmethod
    def generate(self, context) -> dict:
        logging.info(f"Context length = {len(context)}")
        messages = CHAT_HISTORY.copy()
        messages.append({
            'role': 'user',
            'content': INPUT_TEMPLATE.format(context=context)
        })
        response: ChatCompletion = self.client.chat.completions.create(
            model=MODEL,
            temperature=TEMPERATURE, # [0, 2.0]
            frequency_penalty=FREQUENCY_PENALTY, # [-2.0, 2.0] 减少重复内容
            presence_penalty=PRESENCE_PENALTY, # [-2.0, 2.0] 增加新主题可能性
            messages=messages,
            response_format={"type": "json_object"},
        )
        return response.model_dump()