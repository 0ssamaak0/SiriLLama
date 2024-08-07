from flask import Flask, request, Response

from langchain_core.messages import HumanMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda, RunnablePassthrough
from langchain.memory import ConversationBufferWindowMemory

from langchain_core.messages import SystemMessage
from langchain_core.prompts import (
    ChatPromptTemplate,
    MessagesPlaceholder,
)

from operator import itemgetter

from config import PROMPT_CHAT, PROMPT_VISUAL_CHAT, MEMORY_SIZE, ANSWER_SIZE_TOKENS

# ---------------- select your provider here ----------------
provider = "fireworks"  # or provider = "ollama"

if provider == "ollama":
    from config import OLLAMA_CHAT, OLLAMA_VISUAL_CHAT
    from langchain_community.chat_models import ChatOllama

    model = ollama_model = ChatOllama(model=OLLAMA_CHAT)
    vmodel = ollama_vmodel = ChatOllama(model=OLLAMA_VISUAL_CHAT)

elif provider == "fireworks":
    from config import FIREWORKS_CHAT, FIREWORKS_VISUAL_CHAT, FIREWORKS_API_KEY
    from langchain_fireworks import ChatFireworks

    model = ChatFireworks(model=FIREWORKS_CHAT, api_key=FIREWORKS_API_KEY)
    vmodel = ChatFireworks(model=FIREWORKS_VISUAL_CHAT, api_key=FIREWORKS_API_KEY)

# add any other provider here
# elif ...
else:
    raise ValueError("Invalid provider")
# ----------------------------------------------------------

app = Flask(__name__)

description_prompt = "What is this image? give detailed description of it. don't leave any detail. you will be asked about it"


# image prompt (for vChat)
def image_prompt(data):
    """
    This function takes a dictionary 'data' as input which should contain keys 'image' and 'text'.
    It tries to encode the image if it's not already encoded. If the image is already encoded, it uses the encoded image.
    It then creates a 'HumanMessage' which is a list containing two dictionaries - 'text_part' and 'image_part'.
    'text_part' is a dictionary with 'type' as 'text' and 'text' as the text from the input data.
    'image_part' is a dictionary with 'type' as 'image_url' and 'image_url' as a dictionary containing 'url' as the encoded image.
    The function returns the 'HumanMessage'.

    Parameters:
    data (dict): A dictionary containing 'image' and 'text'. 'image' could be a local image or an already encoded image.

    Returns:
    list: A list containing two dictionaries - 'text_part' and 'image_part'.
    """
    # try:
    #     image = data["img"]
    #     encoded_image = encode_image(image)
    # except:
    #     encoded_image = data["img"]

    image_part = {
        "type": "image_url",
        "image_url": {
            "url": data["img"],
        },
    }
    if "ChatOllama" in str(type(model)):
        image_part = {
            "type": "image_url",
            "image_url": data["img"],
        }

    text_part = {"type": "text", "text": description_prompt}

    return [HumanMessage(content=[image_part]), HumanMessage(content=[text_part])]


# Prompt for chat
prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            PROMPT_CHAT,
        ),
        MessagesPlaceholder(variable_name="history"),
        ("human", "{input}"),
    ]
)

# Prompt for vchat
vprompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            PROMPT_VISUAL_CHAT,
        ),
        MessagesPlaceholder(variable_name="history"),
        ("human", "{input}"),
    ]
)

# define memory and chains for chat model
memory = ConversationBufferWindowMemory(k=MEMORY_SIZE, return_messages=True)

chain1 = image_prompt | model | StrOutputParser()

chain2 = (
    RunnablePassthrough.assign(
        history=RunnableLambda(memory.load_memory_variables) | itemgetter("history")
    )
    | prompt
    | model
    | StrOutputParser()
)

vchain1 = image_prompt | vmodel | StrOutputParser()

vchain2 = (
    RunnablePassthrough.assign(
        history=RunnableLambda(memory.load_memory_variables) | itemgetter("history")
    )
    | vprompt
    | vmodel
    | StrOutputParser()
)

# main chains are chat chains by default
main_chain1 = chain1
main_chain2 = chain2


def generate(user_input="Test"):
    print(f'current memory:\n{memory.load_memory_variables({""})}')
    if user_input == "":
        return "End of conversation"
    inputs = {"input": f"{user_input}"}
    response = main_chain2.invoke({"input": user_input})
    memory.save_context(inputs, {"output": response})
    return response


@app.route("/", methods=["POST"])
def generate_route():
    global main_chain1, main_chain2
    data = request.json
    prompt = data.get("prompt", "")
    image = data.get("image", "")
    reset = data.get("reset", False)

    if reset:
        main_chain1 = chain1
        main_chain2 = chain2

    # first time only (vChat)
    if image != "":
        image = f"data:image/jpeg;base64,{image}"
        main_chain1 = vchain1
        main_chain2 = vchain2
        response = main_chain1.invoke(
            {
                "img": image,
            }
        )
        memory.save_context({"input": description_prompt}, {"output": response})
        return response

    generated_response = generate(prompt)

    resp = Response(generated_response)
    resp.headers['content-type'] = 'text/plain; charset=utf-8'
    return resp


if __name__ == "__main__":
    app.run(host="0.0.0.0")
