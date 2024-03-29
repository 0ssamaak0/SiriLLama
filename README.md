<div align = "center">
<h1>
    <img src = "https://github.com/0ssamaak0/SiriLLama/blob/main/assets/icon.png?raw=true" width = 200 height = 200>
<br>

</h1>

<h3>
Siri LLama
</h3>
</div>

Siri LLama is apple shortcut that access locally running LLMs through Siri or the shortcut UI on any apple device connected to the same network of your host machine. It uses Langchain and Ollama

[Demo Video🎬](https://twitter.com/0ssamaak0/status/1772356905064665530)

# Installation
1. Install [Ollama](https://ollama.com/) for your machine, you have to run `ollama serve` in the terminal to start the server
2. Install Langchain and Flask & Run the app
```
pip install --upgrade --quiet  langchain langchain-openai
pip install flask
```
run the flask app on your machine
```
python3 app.py
```
3. On your Apple device, Download the shortcut from [here](https://www.icloud.com/shortcuts/3bf9c6400e5049dd81b2df1e16754d3a)

4. Run the shortcut through Siri or the shortcut UI, in first time you run the shortcut you will be asked to enter your [IP address](https://stackoverflow.com/a/15864222) and the port number 

# Note
**SiriLLama** is the most simple langchain chatbot, there's huge room for improvement and customization, including model selection (even through OpenAI, Anthropic API), RAG Applications or better LLM Memory options, etc.

# Common Issues
- Even we access the flask app (not Ollama server directly), Some windows users who have Ollama installed via `WSL` have to make sure **ollama servere** is exposed to the network, [Check this issue for more details](https://github.com/ollama/ollama/issues/1431)


