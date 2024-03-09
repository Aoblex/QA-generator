from openai import OpenAI


SYSTEM_PROMPT = """你是一名精通统计学的老师，你的任务是根据一段英文统计学教材中的文本，提出统计学相关问题，并自己给出详尽的答案。

    要求:
    1.这些问题必须完全不同，鼓励你从多角度提出多样性的问题；
    2.你的问题需要有一定的深度，需要基于你对文本作出深度思考来给出提问；
    3.问题的答案必须包含在文本中，或者可以根据文本推理出来；
    4.你给出的答案不能过短，必须给出充分的回答；
    5.鼓励你根据文章中的案例举一反三，提出自己的实际案例并用课本中的知识分析出来；
    6.你阅读的是英文教材，但回答必须是中文。
    7.你应当提出至少十对问答
    8.若需要引用文本中的内容，那么你的问题中应当包含文本的内容，而不是引用相应内容"""

HUMAN_PROMPT = r"""请你基于参考文本提出统计学相关问题，并给予解答，以下是参考文本:
    
    <context>
    **Definition 1.1.1**: **:** A collection of sets \(\mathcal{F}\subset\mathcal{P}(\Omega)\) is called an _algebra_ if
    (a) \(\Omega\in\mathcal{F}\),
    (b) \(A\in\mathcal{F}\) implies \(A^{c}\in\mathcal{F}\), and
    (c) \(A,B\in\mathcal{F}\) implies \(A\cup B\in\mathcal{F}\) (i.e., closure under pairwise unions).

    Thus, an algebra is a class of sets containing \(\Omega\) that is closed under complementation and pairwise (and hence finite) unions.
    It is easy to see that one can equivalently define an algebra by requiring that properties (a), (b) hold and that the property

    \[\left(\mathrm{c}\right)^{\prime}\quad A,B\in\mathcal{F}\Rightarrow A\cap B \in\mathcal{F}\]

    holds (i.e. closure under finite intersections).

    **Definition 1.1.2:** A class \({\cal F}\subset{\cal P}(\Omega)\) is called a \(\sigma\)-_algebra_ if it is an algebra and if it satisfies
    \[(d)\quad A_{n}\in{\cal F}\quad\mbox{for}\quad n\geq 1\Rightarrow\bigcup_{n\geq 1 }A_{n}\in{\cal F}.\]
    Thus, a \(\sigma\)-algebra is a class of subsets of \(\Omega\) that contains \(\Omega\) and is closed under complementation and countable unions. As pointed out in the introductory chapter, a \(\sigma\)-algebra can be alternatively defined as an algebra that is closed under monotone unions as the following shows.
    </context>

    你应当按照一问一答的格式输出你的结果，你可以参考给定的文本，但你的问答应该是自洽的，即不应提及对参考文本的引用。
"""

AI_PROMPT = \
  r"问题1: 什么是集合的代数（algebra）？集合的\(\sigma\)-代数又是什么？" + "\n" \
+ r"答案1: 集合的代数是指一个集合闭合于补集和有限并集的集合系统。具体来说，对于集合\(\Omega\)，如果一个集合\(\mathcal{F}\)满足以下条件：1）\(\Omega\)属于\(\mathcal{F}\)，2）若\(A\)属于\(\mathcal{F}\)，则\(A\)的补集\(A^{c}\)也属于\(\mathcal{F}\)，3）若\(A\)和\(B\)属于\(\mathcal{F}\)，则\(A\)和\(B\)的并集\(A\cup B\)也属于\(\mathcal{F}\)，那么\(\mathcal{F}\)就是\(\Omega\)的代数。而对于\(\sigma\)-代数，则在代数的基础上再加上一个性质：对于一个可数个集合\(A_{n}\)均属于\(\mathcal{F}\)，则它们的并集\(\bigcup_{n\geq 1 }A_{n}\)也属于\(\mathcal{F}\)。" + "\n" \
+ r"问题2: 给出一个例子，说明一个集合的代数不是\(\sigma\)-代数。" + "\n" \
+ r"答案2: 假设\(\Omega\)是一个非空集合，定义一个集合\(\mathcal{F}_{5}\)：\(\mathcal{F}_{5}=\{A\subset\Omega: |A|\)是有限或者\(|A^{c}|\)是有限\}。这里的\(|A|\)表示集合\(A\)中元素的个数。可以证明\(\mathcal{F}_{5}\)是一个代数，但如果\(\Omega\)的元素个数是无限的话，\(\mathcal{F}_{5}\)就不是\(\sigma\)-代数。因为在无限情况下，存在一列集合\(A_{n}=\{\omega_{n}\}\)，其中\(\omega_{n}\)是\(\Omega\)的元素，那么它们的并集\(\bigcup_{n\geq 1}A_{n}\)将包含无限个元素，从而不属于\(\mathcal{F}_{5}" + "\n" \
+ r"问题3: 什么是\(\sigma\)-代数（sigma-algebra）？它与代数（algebra）有何区别？" + "\n" \
+ r"答案3: \(\sigma\)-代数是集合的一个子集类，它包含了全集，对补集和可数并集都是封闭的。与代数相比，\(\sigma\)-代数除了满足代数的条件外，还需要满足对于可数并集的封闭性。" + "\n" \
+ r"问题4: 什么是可测函数（measurable function）和随机变量（random variable）？" + "\n" \
+ r"答案4: 引入可测函数的概念是为了可以对集合上的函数进行测度。对于测度空间\((\Omega, \mathcal{F}, \mu)\)，可测函数具有一些重要性质，例如可测函数的线性组合、积分和点态收敛等，这些性质使得我们能够对随机变量进行更深入的研究和分析。" + "\n"

INPUT_TEMPLATE = """请你基于参考文本提出统计学相关问题，并给予解答，以下是参考文本:

    <context>
    {context}
    </context>

    你应当按照一问一答的格式输出你的结果，你可以参考给定的文本，但你的问答应该是自洽的，即不应提及对参考文本的引用。至少输出十对问答。
"""

CHAT_HISTORY = [
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

class OpenAILLM():

    api_key="sk-egkbiFTEc8E2FDN2Ec1470B3AdDc4d25B6417d8d75E9BaE7"
    base_url = "https://api.132999.xyz/v1"

    def __init__(self):
        self.client = OpenAI(api_key=self.api_key,
                             base_url=self.base_url)

    def generate(self, context):
        messages = CHAT_HISTORY.copy()
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

openai = OpenAILLM()