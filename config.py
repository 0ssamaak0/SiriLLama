# Parameters
MEMORY_SIZE = 5  # Number of messages to remember
ANSWER_SIZE_WORDS = 30  # Number of words in an answer
ANSWER_SIZE_TOKENS = ANSWER_SIZE_WORDS / 0.75  # rough approximation

# Prompts
PROMPT_CHAT = f"You're Siri LLama, an open source AI smarter than Siri that runs on user's devices. You're helping a user with tasks, for any question answer very briefly (answer is about {ANSWER_SIZE_WORDS} words) and informatively. else, ask for more information."
PROMPT_VISUAL_CHAT = "You're Siri LLama, an open source AI that saw an image, and give answers about it. anytime you're asked about (it) answer about the image you've seen"

# Models
# Ollama
OLLAMA_CHAT = "llama3:8b"
OLLAMA_VISUAL_CHAT = "llava:7b"

# Fireworks
FIREWORKS_CHAT = "accounts/fireworks/models/llama-v3-70b-instruct"
FIREWORKS_VISUAL_CHAT = "accounts/fireworks/models/llava-yi-34b"
FIREWORKS_API_KEY = "GOtyI1w6nujfkksUvHvCiFHnDaAVP2HkTiDIxo4jwXALLZLo"
