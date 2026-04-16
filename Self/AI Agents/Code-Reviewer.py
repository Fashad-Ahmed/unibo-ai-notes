from langchain.chat_models import init_chat_model
from langchain_core.prompts import PromptTemplate
import gradio as gr

# Model: gpt-4o-mini | Provider: openai

# Step 1: Create prompt template
prompt_template_str = """
You are a senior software engineer reviewing code.

Analyze the following code snippet and respond in this structure:

1. What the code does (1–2 sentences)

2. Potential Issues
- List any bugs, inefficiencies, or bad practices

3. Improvements
- Suggest clearer, more efficient, or more maintainable approaches

4. Optimized Version
Provide an improved version of the code

Code:
{code_snippet}
"""

# Step 2: Create template object
prompt_template = PromptTemplate.from_template(prompt_template_str)

# Step 3: Initialize model
model = init_chat_model("gpt-4o-mini", model_provider="openai")

# Step 4: Define function
def review_code(code_snippet):
    prompt = prompt_template.format(code_snippet=code_snippet)
    response = model.invoke(prompt)
    return response.content



demo = gr.Interface(
    fn=review_code,
    inputs=[gr.Textbox(label="Code Snippet", lines=10)],
    outputs=[gr.Textbox(label="Code Review", lines=15)],
    flagging_mode="never",
    title="AI Code Reviewer",
    description="Get senior engineer feedback on your code"
)

demo.launch()