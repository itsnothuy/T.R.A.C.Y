# tracy.py

from stt import recognize_speech
from intent_recognition import identify_intent
from weather import get_weather
from jokes_pro import get_joke_api
from tts import speak_text

# NEW: RAG imports
from rag_utils import (
    load_and_chunk_squad_dataset,
    build_vectorstore_from_contexts,
    create_rag_chain,
    get_rag_answer
)

def main():
    # 1) Greet user
    speak_text("Hello! I'm Tracy, your voice assistant with RAG capabilities. How can I help you today?")

    # 2) Load some QA data (SQuAD) & build a RAG pipeline (this can be done once at startup)
    # contexts = load_and_chunk_squad_dataset()
    # vectorstore = build_vectorstore_from_contexts(contexts, "squad_collection")
    # rag_chain = create_rag_chain(vectorstore)

    # 3) Listen for user input
    user_input = recognize_speech()  # from stt.py
    if user_input.lower() in ["exit", "quit", "bye"]:
        speak_text("Goodbye! Have a great day.")
            

    # 4) Identify intent
    intent = identify_intent(user_input)  # from intent_recognition.py

    # 5) Route to correct function based on intent
    if intent == "weather":
        lat, lon = 40.7128, -74.0060  # Example: NYC coordinates
        weather_info = get_weather(lat, lon)
        speak_text(weather_info)
    elif intent == "joke":
        joke = get_joke_api()
        speak_text(joke)
    else:
        # If not recognized, try RAG QA
        speak_text("Let me check my knowledge base...")

        # 6) Use the RAG chain to answer user queries
        # answer = get_rag_answer(user_input, rag_chain)
        # speak_text(answer)

if __name__ == "__main__":
    main()
