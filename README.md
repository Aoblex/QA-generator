# QA-generator

根据统计学语料生成高质量统计学知识问答。语料的获取方式是将教材转化为文本后分成小段。

## configs

参数配置

### converter_config.py

`CONVERTER_INPUT_DIR`: $\texttt{.pdf}$格式的英文书籍所在文件夹

`CONVERTER_OUTPUT_DIR`: 转化成$\texttt{.mmd}$的输出文件夹

### model_config.py

`MODEL`: 选用的模型名称

`TEMPERATURE`: 模型温度 $\in [0, 2.0]$

`FREQUENCY_PENALTY`: 重复token惩罚项 $\in [-2.0, 2.0]$

`PRESENCE_PENALTY`: 现有token惩罚项 $\in [-2.0, 2.0]$


### processor_config.py

`PROCESSOR_INPUT_DIR`: 需要处理的文本所在文件夹

`PROCESSOR_OUTPUT_BASE_DIR`: 经过处理的文本的输出文件夹

## qa_generator

问答生成模型

### model.py

`QAModel`: 使用OpenAI的API接口模型生成问答

### prompts.py

`SYSTEM_PROMPT`: 系统提示词

`HUMAN_PROMPT`: 第一轮对话的用户提示

`AI_PROMPT`: 第一轮对话的结果

`INPUT_TEMPLATE`: 第二轮对话中用户输入的模板

`CHAT_HISTORY`: 包含以上所有prompts的最终输入的模板

## text_processor

对文本进行分段，有若干分段策略供选择

### pieces.py

`ChunkPiece`: 固定长度段落

`SectionPiece`: 小节段落

### text.py

`Text`: 包含原始的文本，可以通过调用`segment`对其进行分段




