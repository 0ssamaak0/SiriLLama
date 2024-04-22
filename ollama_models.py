from langchain_community.chat_models import ChatOllama

# define your models here
chat_model = "llama3:latest"
vchat_model = "llava:7b"

model = ChatOllama(
    model=chat_model,
)
vmodel = ChatOllama(
    model=vchat_model,
)
