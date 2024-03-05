from langchain_community.chat_models import ChatCohere
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import SystemMessage, HumanMessage, ChatMessage
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from openai import OpenAI
import os
import re
import json
import hashlib
import datetime


class ModelResponse:

    def __init__(self, context, response):
        self.context = context
        self.response = response

    @property
    def context_hash(self) -> str:
        return hashlib.sha1(self.context.encode()).hexdigest()


    @property
    def response_dict(self) -> dict:
        try:
            return json.loads(self.response)
        except:
            pattern = r'\[(.*)\]'
            match = re.search(pattern, self.response, flags=re.DOTALL)
            if match is None:
                return {}
            try:
                return json.loads(match.group(0))
            except:
                json_str = match.group(0).replace("{{", "{").replace("}}", "}")
                try:
                    return json.loads(json_str)
                except:
                    return {}
    
    def save_response(self, output_dir="./results", file_name="hash"):
        current_time = datetime.datetime.now()

        if file_name == "time":
            file_name = current_time.strftime("%Y-%m-%d_%H-%M-%S.json")
        elif file_name == "hash":
            file_name = f"{self.context_hash}.json"
        else:
            raise IndexError(f"Invalid file name type: {file_name}")

        output_dict = {
            "context": self.context,
            "raw_response": self.response,
            "response": self.response_dict,
        }
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        with open(os.path.join(output_dir, file_name), "w", encoding="utf-8") as json_file:
            json.dump(output_dict, json_file, indent=4, ensure_ascii=False)

SYSTEM_PROMPT = """你是一名初学统计学的学生，你的任务是根据一段统计学教材中的文本，向老师提出3个统计学相关的题目，并自己给出答案。

    要求:
    1.这些问题必须完全不同，鼓励你从多角度提出多样性的问题；
    2.你的问题需要有一定的深度，需要基于你对文本作出深度思考来给出提问；
    3.问题的答案必须包含在文本中，或者可以根据文本推理出来；
    4.你给出的答案不能过短，必须给出充分的回答；
    5.鼓励你根据文章中的案例举一反三，提出自己的实际案例并用课本中的知识分析出来；
    6.你不能使用课本中的图片或表格描述。"""
HUMAN_PROMPT = """根据文本，提出统计学相关问题，并给予解答，以下是参考文本:
    
    <context>
    1.2.1 分类数据、顺序数据、数值型数据按照所采用的计量尺度的不同①,可以将统计数据分为分类数据、顺序数据和数值型数据。
    分类数据(categorical data)是只能归于某一类别的非数字型数据，它是对事物进行分类的结果，数据表现为类别，是用文字来表述的。
    例如，人口按照性别分为男、女两①数据的测量尺度有四种:第一，分类尺度(nominal scale)。
    按照事物的某种属性对其进行的平行的分类，数据表现为类别。
    第二，顺序尺度(ordinal scale)。
    对事物类别顺序的测度，数据表现为有序的类别。
    第三，间隔尺度(interval scale),对事物类别或次序之间间距的测度，没有绝对零点，数据表现为数字。
    第四，比率尺度(ratioscale)。
    对事物类别或次序之间间距的测度，有绝对零点，数据表现为数字
    </context>

    你应当按照以下格式输出你的回答:
    [
        {{
            \"题目\":\"...\",
            \"答案\":\"...\"
        }},
        ...
        {{
            \"题目\":\"...\",
            \"答案\":\"...\"
        }}
    ]"""
AI_PROMPT = """[
        {{
            \"题目\": \"在统计学中，为什么要将数据按照计量尺度的不同进行分类，而不是简单地将所有数据都看作是数字型数据？\",
            \"答案\":\"在统计学中，将数据按照计量尺度的不同进行分类是为了更好地理解和分析数据的特性和可操作性。不同的计量尺度反映了数据所具有的不同属性和特征，例如分类数据、顺序数据和数值型数据，它们分别呈现出不同的统计特征和分析方法。通过这样的分类，我们可以针对不同类型的数据采用合适的统计技术和方法，从而更准确地描述数据的含义和进行推断分析。\"
        }},
        {{
            \"题目\":\"在分类数据、顺序数据和数值型数据中，有哪些具体的应用场景或案例可以帮助理解它们之间的差异？\",
            \"答案\":\"分类数据通常用于描述事物的属性或类别，例如性别、民族、学历等，其应用场景包括人口统计学、市场调查等领域；顺序数据则反映了事物的有序关系，如学生的成绩等级、产品的质量等，适用于评价和排序问题；而数值型数据则是以数值形式呈现的数据，可用于测量和计量，如温度、身高、收入等，广泛应用于自然科学、社会科学等各个领域。\"
        }},
        {{
            \"题目\":\"在实际统计分析中，如何确定采用何种计量尺度对数据进行分类，以及如何选择适当的统计方法进行分析？\",
            \"答案\":\"确定采用何种计量尺度对数据进行分类需要考虑数据的性质和研究目的。若数据仅涉及分类或标签，应选用分类尺度；若数据除了分类外还有明显的顺序关系，则选用顺序尺度；若数据是具有等距或等比关系的数值型数据，则可选用间隔尺度或比率尺度。在选择统计方法时，应结合数据类型和研究问题，选择适合的描述统计方法、推断统计方法或模型方法，以确保分析结果的准确性和可靠性。\"
        }}
    ]"""
INPUT_TEMPLATE = """根据文本，提出统计学相关问题，并给予解答，以下是参考文本:

    <context>
    {context}
    </context>

    你应当按照以下格式输出你的回答:
    [
        {{
            \"题目\":\"...\",
            \"答案\":\"...\"
        }},
        ...
        {{
            \"题目\":\"...\",
            \"答案\":\"...\"
        }}
    ]"""

CHATGLM_HISTORY = [
    {
        'role': 'system',
        'content': SYSTEM_PROMPT,
    },
    {
        'role': 'user',
        'content': HUMAN_PROMPT,
    },
    {
        'role': 'assistant',
        'content': AI_PROMPT,
    }
]

model = ChatCohere(cohere_api_key="A1c1O5tYigERdYOVc2ZRjvTYFoBbSZT8YfUgRFVM")
statistics_template = ChatPromptTemplate.from_messages([
    ("system", SYSTEM_PROMPT),
    ("human", HUMAN_PROMPT),
    ("ai", AI_PROMPT),
    ("human", INPUT_TEMPLATE),
])

cohere = statistics_template | model

# from transformers import AutoTokenizer, AutoModel
# tokenizer = AutoTokenizer.from_pretrained("THUDM/chatglm3-6b-32k", trust_remote_code=True)
# chatglm = AutoModel.from_pretrained("THUDM/chatglm3-6b-32k", trust_remote_code=True).half().cuda()
# chatglm = chatglm.eval()


class OpenAILLM():
    
    base_url = "https://api.132999.xyz/v1"
    def __init__(self, api_key):
        self.client = OpenAI(api_key=api_key, base_url=self.base_url)

    def generate(self, context):
        messages = CHATGLM_HISTORY.copy()
        messages.append(
            {
                'role': 'user',
                'content': INPUT_TEMPLATE.format(context=context)
            }
        )
        response = self.client.chat.completions.create(model="gpt-3.5-turbo-1106",
                                                       messages=messages)
        result = response.choices[0].message.content
        return result

openai = OpenAILLM(api_key="sk-C4GIY6tWzvgCLDie7326B17079554e70A9262b156fDc3b3b")