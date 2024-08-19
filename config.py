# Parameters
MEMORY_SIZE = 5  # Number of messages to remember
ANSWER_SIZE_WORDS = 30  # Number of words in an answer
MAX_TOKENS = ANSWER_SIZE_WORDS / 0.75  # rough approximation
CHUNCK_SIZE = 1024  # of vetorstore
CHUNK_OVERLAP = 200  # of vetorstore

# Prompts
PROMPT_CHAT = f"You're Siri LLama, an open source AI smarter than Siri that runs on user's devices. You're helping a user with tasks, for any question answer very briefly (answer is about {ANSWER_SIZE_WORDS} words) and informatively. else, ask for more information."
PROMPT_VISUAL_CHAT = "You're Siri LLama, an open source AI that saw an image, and give answers about it. anytime you're asked about (it) answer about the image you've seen"

PROVIDER = "fireworks"  # or "fireworks"
# Models
# Ollama
OLLAMA_CHAT = "llama3.1:8b"
OLLAMA_VISUAL_CHAT = "moondream"
OLLAMA_EMBEDDINGS_MODEL = "0ssamaak0/nomic-embed-text:latest"

# Fireworks
FIREWORKS_CHAT = "accounts/fireworks/models/llama-v3p1-8b-instruct"
FIREWORKS_VISUAL_CHAT = "accounts/fireworks/models/phi-3-vision-128k-instruct"
FIREWORKS_API_KEY = "<API_KEY>"
FIREWORKS_EMBEDDINGS_MODEL = "nomic-ai/nomic-embed-text-v1.5"
