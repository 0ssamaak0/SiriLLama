<div align = "center">
<h1>
    <img src = "https://github.com/0ssamaak0/SiriLLama/blob/main/assets/icon.png?raw=true" width = 200 height = 200>
<br>

</h1>

<h3>
Siri LLama
</h3>
</div>

Siri LLama is apple shortcut that access locally running LLMs through Siri or the shortcut UI on any apple device connected to the same network of your host machine. It uses Langchain 🦜🔗 and supports open source models from both [Ollama](https://ollama.com/) 🦙 or [Fireworks AI](https://fireworks.ai/) 🎆

[Demo Video🎬](https://twitter.com/0ssamaak0/status/1772356905064665530)

[🆕 Multimodal support 🎬](https://twitter.com/0ssamaak0/status/1782462691291890148)

# Getting Started
## Requirements
### Ollama Installation🦙
1. Install [Ollama](https://ollama.com/) for your machine, you have to run `ollama serve` in the terminal to start the server

2. pull the models you want to use, for example
```bash
ollama run llama3 # chat model
ollama run llava # multimodal
```

3. Install Langchain and Flask
```bash
pip install --upgrade --quiet  langchain langchain-community
pip install flask
```

4. in `config.py` set `OLLAMA_CHAT` and `OLLAMA_VISUAL_CHAT` to the models you pulled from Ollama
### Fireworks AI Installation🎆

1.Install Langchain and Flask

```bash
pip install --upgrade --quiet  langchain langchain-fireworks
pip install flask
```

2. get your [Fireworks API Key](http://fireworks.ai/) and put it in `fireworks_models.py`

3. in `config.py` set `FIREWORKS_CHAT` and `vchat_model` to the models you want to use from Fireworks AI. and set your and `FIREWORKS_API_KEY` 

## Config
in `confing.py` set `MEMORY_SIZE` (How many previous messages to remember) and `ANSWER_SIZE_WORDS` (How many words to generate in the answer)

## Running SiriLlama 🟣🦙

1. [Download](https://github.com/0ssamaak0/SiriLLama/archive/refs/heads/main.zip) or clone the repo 

2. [set the provider (Ollama / Fireworks)](https://github.com/0ssamaak0/SiriLLama/blob/d07ff97a0eb07db08601e5e3fe0254c6f05aee50/app.py#L18) in `app.py` 

3. Run the flask app using
```bash
>>> python3 app.py
```

4. On your Apple device, Download the shortcut from [here](https://www.icloud.com/shortcuts/4a1c41c6f4ec49908d0cd67cab7860b7)

5. Run the shortcut through Siri or the shortcut UI, in first time you run the shortcut you will be asked to enter your [IP address](https://stackoverflow.com/a/15864222) and the port number showing in terminal
```bash
>>> python app.py
...
 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:5000
 * Running on http://192.168.1.134:5000
Press CTRL+C to quit
```
In the example above, the IP address is `192.168.1.134` and the port is `5000`



# Common Issues 🐞
- Even we access the flask app (not Ollama server directly), Some windows users who have Ollama installed using `WSL` have to make sure **ollama servere** is exposed to the network, [Check this issue for more details](https://github.com/ollama/ollama/issues/1431)
- Running the shortcut for the first time from Siri, will ask you to allow sending data to the server. it doesn't click in IOS 17.4, try to send any message from the shortcut UI to allow, then try again from Siri

# Other LLM Provider 🤖🤖
Supposedly SiriLLama should work with any LLMs that including OpenAI, Claude, etc. but make sure first you installed the corresponding Langchain packages and set the models in `config.py`

