from flask import Flask, request, jsonify

from operator import itemgetter
from langchain.memory import ConversationBufferWindowMemory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnableLambda, RunnablePassthrough
from langchain_openai import ChatOpenAI

import requests

app = Flask(__name__)

# define the model (default: mistral:instruct)
model = ChatOpenAI(
    temperature=0,
    model_name="mistral:instruct",
    openai_api_base="http://localhost:11434/v1",
    openai_api_key="you own the model, server and data here!",
    max_tokens=80,
)

# define the prompt and system message
prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You're Siri LLama, an open source AI smarter than Siri that runs on user's devices. You're helping a user with tasks, for any question answer very briefly (answer is about 30 words) and informatively. else, ask for more information.",
        ),
        MessagesPlaceholder(variable_name="history"),
        ("human", "{input}"),
    ]
)
# define memory type
memory = ConversationBufferWindowMemory(k=5, return_messages=True)

# define the chain
chain = (
    RunnablePassthrough.assign(
        history=RunnableLambda(memory.load_memory_variables) | itemgetter("history")
    )
    | prompt
    | model
)


def generate(user_input="Test"):
    print(f'current memory:\n{memory.load_memory_variables({""})}')
    if user_input == "":
        return "End of conversation"
    inputs = {"input": f"{user_input}"}
    response = chain.invoke(inputs)
    memory.save_context(inputs, {"output": response.content})
    return response.content


@app.route("/", methods=["POST"])
def generate_route():
    prompt = request.json.get("prompt", "")
    response = generate(prompt)
    return response
    # return jsonify(response=response)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
