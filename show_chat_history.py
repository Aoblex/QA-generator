from qa_generator.prompts import AI_PROMPT, HUMAN_PROMPT, SYSTEM_PROMPT, INPUT_TEMPLATE
print(SYSTEM_PROMPT, "\n", "="*40)
print(HUMAN_PROMPT, "\n", "="*40)
print(AI_PROMPT, "\n", "="*40)
print(INPUT_TEMPLATE.format(context="Some context"), "\n", "="*40)
