from langchain_fireworks import ChatFireworks

# fireworks API KEY
api_key = None
with open("fireworks_api.txt") as f:
    api_key = f.read().strip()

# define your models here
chat_model = "accounts/fireworks/models/llama-v3-70b-instruct"
vchat_model = "accounts/fireworks/models/llava-yi-34b"

model = ChatFireworks(model=chat_model, api_key=api_key)

vmodel = ChatFireworks(model=vchat_model, api_key=api_key)
