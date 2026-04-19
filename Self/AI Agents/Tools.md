A good tool should be something that complements the power of an LLM.

For instance, if you need to perform arithmetic, giving a calculator tool to your LLM will provide better results than relying on the native capabilities of the model.

Furthermore, LLMs predict the completion of a prompt based on their training data, which means that their internal knowledge only includes events prior to their training. Therefore, if your agent needs up-to-date data you must provide it through some tool.

For instance, if you ask an LLM directly (without a search tool) for today’s weather, the LLM will potentially hallucinate random weather.


A Tool should contain:

- A textual description of what the function does.
- A Callable (something to perform an action).
- Arguments with typings.
- (Optional) Outputs with typings.