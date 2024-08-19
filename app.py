import requests
from bs4 import BeautifulSoup
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain.chains import RetrievalQA
from flask import Flask, request, Response
from langchain_core.messages import HumanMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda, RunnablePassthrough
from langchain.memory import ConversationBufferWindowMemory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from operator import itemgetter
from config import (
    PROVIDER,
    MAX_TOKENS,
    PROMPT_CHAT,
    PROMPT_VISUAL_CHAT,
    MEMORY_SIZE,
    CHUNCK_SIZE,
    CHUNK_OVERLAP,
)

app = Flask(__name__)


class AIProvider:
    def __init__(self, provider_name):
        self.provider_name = provider_name
        self.model = None
        self.vmodel = None
        self.embeddings = None
        self.setup_provider()

    def setup_provider(self):
        if self.provider_name == "ollama":
            from config import (
                OLLAMA_CHAT,
                OLLAMA_VISUAL_CHAT,
                OLLAMA_EMBEDDINGS_MODEL,
            )
            from langchain_community.chat_models import ChatOllama
            from langchain_community.embeddings import OllamaEmbeddings

            self.EMBEDDINGS_MODEL = OLLAMA_EMBEDDINGS_MODEL

            self.model = ChatOllama(model=OLLAMA_CHAT)
            self.vmodel = ChatOllama(model=OLLAMA_VISUAL_CHAT)
            self.embeddings = OllamaEmbeddings(model=OLLAMA_EMBEDDINGS_MODEL)

        elif self.provider_name == "fireworks":
            from config import (
                FIREWORKS_CHAT,
                FIREWORKS_VISUAL_CHAT,
                FIREWORKS_API_KEY,
                FIREWORKS_EMBEDDINGS_MODEL,
            )
            from langchain_fireworks import ChatFireworks, FireworksEmbeddings

            self.model = ChatFireworks(model=FIREWORKS_CHAT, api_key=FIREWORKS_API_KEY)
            self.vmodel = ChatFireworks(
                model=FIREWORKS_VISUAL_CHAT, api_key=FIREWORKS_API_KEY
            )
            self.embeddings = FireworksEmbeddings(
                model=FIREWORKS_EMBEDDINGS_MODEL, fireworks_api_key=FIREWORKS_API_KEY
            )
        else:
            raise ValueError("Invalid provider")


class AIChat:
    def __init__(self, provider):
        self.provider = provider
        self.memory = ConversationBufferWindowMemory(
            k=MEMORY_SIZE, return_messages=True
        )
        self.setup_chains()
        self.vectorstore = None

    def setup_chains(self):
        self.text_prompt = ChatPromptTemplate.from_messages(
            [
                ("system", PROMPT_CHAT),
                MessagesPlaceholder(variable_name="history"),
                ("human", "{input}"),
            ]
        )
        self.visual_prompt = ChatPromptTemplate.from_messages(
            [
                ("system", PROMPT_VISUAL_CHAT),
                MessagesPlaceholder(variable_name="history"),
                ("human", "{input}"),
            ]
        )

        self.create_chain(is_visual=False)

    def create_chain(self, is_visual=False):
        model = self.provider.vmodel if is_visual else self.provider.model
        prompt = self.visual_prompt if is_visual else self.text_prompt

        self.initial_chain = self.image_prompt | model | StrOutputParser()
        self.conversation_chain = (
            RunnablePassthrough.assign(
                history=RunnableLambda(self.memory.load_memory_variables)
                | itemgetter("history")
            )
            | prompt
            | model
            | StrOutputParser()
        )

    def image_prompt(self, data):
        image_part = {
            "type": "image_url",
            "image_url": {"url": data["img"]},
        }
        if "ChatOllama" in str(type(self.provider.model)):
            image_part = {
                "type": "image_url",
                "image_url": data["img"],
            }
        text_part = {
            "type": "text",
            "text": "What is this image? Give a detailed description of it. Don't leave any detail out. You will be asked about it.",
        }
        return [HumanMessage(content=[image_part]), HumanMessage(content=[text_part])]

    def generate(self, user_input, max_tokens=None):
        if not user_input:
            return "End of conversation"
        inputs = {"input": user_input}

        if self.vectorstore:
            qa_chain = RetrievalQA.from_chain_type(
                self.provider.model, retriever=self.vectorstore.as_retriever()
            )
            response = qa_chain.invoke({"query": user_input, "max_tokens": max_tokens})
            response = response["result"]
        else:
            response = self.conversation_chain.invoke(inputs)

        self.memory.save_context(inputs, {"output": response})
        return response

    def reset(self):
        self.create_chain(is_visual=False)
        self.memory.clear()
        self.vectorstore = None

    def process_image(self, image):
        self.create_chain(is_visual=True)
        response = self.initial_chain.invoke({"img": image})
        self.memory.save_context({"input": "Describe the image"}, {"output": response})
        return response

    def process_url(self, url):
        text = self.extract_text_from_url(url)
        self.create_vectorstore(text)
        return f"Processed URL: {url}. Ready for questions about its content."

    def extract_text_from_url(self, url):
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        return soup.get_text()

    def create_vectorstore(self, text):
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=CHUNCK_SIZE, chunk_overlap=CHUNK_OVERLAP
        )
        splits = text_splitter.split_text(text)
        print("Creating vectorstore")
        self.vectorstore = Chroma.from_texts(splits, self.provider.embeddings)


ai_provider = AIProvider(PROVIDER)
ai_chat = AIChat(ai_provider)


@app.route("/", methods=["POST"])
def generate_route():
    data = request.json
    prompt = data.get("prompt", "")
    image = data.get("image", "")
    url = data.get("url", "")
    reset = data.get("reset", False)

    if reset:
        ai_chat.reset()

    if url != "":
        response = ai_chat.process_url(url)
    if image != "":
        image = f"data:image/jpeg;base64,{image}"
        response = ai_chat.process_image(image)
    else:
        response = ai_chat.generate(prompt, max_tokens=MAX_TOKENS)

    return Response(response, content_type="text/plain; charset=utf-8")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
