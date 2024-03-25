<div align = "center">
<h1>
    <img src = "https://github.com/0ssamaak0/SiriLLama/blob/master/icon.png?raw=true" width = 200 height = 200>
<br>

</h1>

<h3>
Siri LLama
</h3>

Siri LLama is apple shortcut that access locally running LLMs through Siri or the shortcut UI on any apple device connected to the same network of your host machine. It uses Langchain and Ollama

# Installation
1. Install [Ollama](https://ollama.com/) for your machine, you have to run `ollama serve` in the terminal to start the server
2. Install Langchain and Flask
```
pip install --upgrade --quiet  langchain langchain-openai
pip install flask
```
3. Download the shortcut from [here](https://www.icloud.com/shortcuts/4dd1bb0d7bda4314926adcd3ffdfd80d)

4. Enter your local IP address and the Flask port in the shortcut

5. Run the shortcut through Siri or the shortcut UI

# Note
**SiriLLama** is the most simple langchain chatbot, there's huge room for improvement and customization, including model selection (even through APIs), RAG Applications or better LLM Memory options, etc.

# Common Issues
- Even we access the flask app (not Ollama server directly), Some windows users who have Ollama installed via `WSL` have to make sure **ollama servere** is exposed to the network, [Check this issue for more details](https://github.com/ollama/ollama/issues/1431)


