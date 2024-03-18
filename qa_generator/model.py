from openai import OpenAI
from .prompts import CHAT_HISTORY, INPUT_TEMPLATE
import logging
from openai.types.chat import ChatCompletion

class QAModel():

    api_key="sk-n4wVb574XCbb0p3SFbF7547e4a484b3d82640c8dCe553e20"
    base_url = "https://api.132999.xyz/v1"
    client = OpenAI(api_key=api_key, base_url=base_url)

    @classmethod
    def generate(self, context, model_configs: dict) -> dict:
        logging.info(f"Context length = {len(context)}")
        messages = CHAT_HISTORY.copy()
        messages.append({
            'role': 'user',
            'content': INPUT_TEMPLATE.format(context=context)
        })
        response: ChatCompletion = self.client.chat.completions.create(
            messages=messages,
            response_format={"type": "json_object"},
            **model_configs,
        )
        response_dict = response.model_dump()
        response_dict["parameters"] = model_configs 
        return response_dict