from langchain.chat_models import init_chat_model
from langchain_core.prompts import PromptTemplate
import gradio as gr

# Prompt template stays outside the function
prompt_template_str = """
Your task is to explain the concept of **{concept}** to me in a way that is:

1. Clear and intuitive
2. Concise (in under 100 words)
3. Tailored specifically to me and what I already know

Use the following information about me to personalize your explanations:

- Background: Software Engineer with 3.5 years full-stack development experience, currently pursuing Master's in AI
- Professional Goals: Transitioning from full-stack development to AI/LLM application development
- Technical Context: Comfortable with Python, classes, and package usage

The personalization should be subtle and natural. Avoid forced references to my background that don't genuinely enhance understanding of the concept.
"""

prompt_template = PromptTemplate.from_template(prompt_template_str)

# Model initialization stays outside the function
model = init_chat_model("gpt-4o-mini", model_provider="openai")


def generate_explanation(input_text):
    prompt = prompt_template.format(concept=input_text)
    response = model.invoke(prompt)
    return response.content


demo = gr.Interface(
    fn=generate_explanation,
    inputs=[gr.Textbox(label="Enter a concept", lines=1)],
    outputs=[gr.Textbox(label="Explanation", lines=5)],
    flagging_mode="never",
    title="Concept Explainer",
    description="Get personalized explanations for any concept"
)

demo.launch()