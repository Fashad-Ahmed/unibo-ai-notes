## Messages and Special Tokens


Q: When, I’m interacting with ChatGPT/Hugging Chat, I’m having a conversation using chat Messages, not a single prompt sequence

A: That’s correct! But this is in fact a UI abstraction. Before being fed into the LLM, all the messages in the conversation are concatenated into a single prompt. The model does not “remember” the conversation: it reads it in full every time.


Up until now, we’ve discussed prompts as the sequence of tokens fed into the model. But when you chat with systems like ChatGPT or HuggingChat, you’re actually exchanging messages. Behind the scenes, these messages are concatenated and formatted into a prompt that the model can understand.


![alt text](image-34.png)

This is where chat templates come in. They act as the bridge between conversational messages (user and assistant turns) and the specific formatting requirements of your chosen LLM. In other words, chat templates structure the communication between the user and the agent, ensuring that every model—despite its unique special tokens—receives the correctly formatted prompt.

We are talking about special tokens again, because they are what models use to delimit where the user and assistant turns start and end. Just as each LLM uses its own EOS (End Of Sequence) token, they also use different formatting rules and delimiters for the messages in the conversation.




