# tracy.py

# from stt import recognize_speech
# from intent_recognition import identify_intent
# from weather import get_weather
# from jokes_pro import get_joke_api
# from tts import speak_text_cli

# NEW: RAG imports
from rag_utils import (
    load_and_chunk_squad_dataset,
    build_vectorstore_from_contexts,
    create_rag_chain,
    get_rag_answer
)

# def main():
#     # 1) Greet user
#     speak_text("Hello! I'm Tracy, your voice assistant with RAG capabilities. How can I help you today?")

#     # 2) Load some QA data (SQuAD) & build a RAG pipeline (this can be done once at startup)
#     # contexts = load_and_chunk_squad_dataset()
#     # vectorstore = build_vectorstore_from_contexts(contexts, "squad_collection")
#     # rag_chain = create_rag_chain(vectorstore)

#     # 3) Listen for user input
#     user_input = recognize_speech()  # from stt.py
#     if user_input.lower() in ["exit", "quit", "bye"]:
#         speak_text("Goodbye! Have a great day.")
            

#     # 4) Identify intent
#     intent = identify_intent(user_input)  # from intent_recognition.py

#     # 5) Route to correct function based on intent
#     if intent == "weather":
#         lat, lon = 40.7128, -74.0060  # Example: NYC coordinates
#         weather_info = get_weather(lat, lon)
#         speak_text(weather_info)
#     elif intent == "joke":
#         joke = get_joke_api()
#         speak_text(joke)
#     else:
#         # If not recognized, try RAG QA
#         speak_text("Let me check my knowledge base...")

#         # 6) Use the RAG chain to answer user queries
#         # answer = get_rag_answer(user_input, rag_chain)
#         # speak_text(answer)

# tracy.py
# tracy.py
from stt import recognize_speech
from intent_recognition import identify_intent
from weather import get_weather
from jokes_pro import get_joke_api
# Import CLI-based function
from tts import speak_text_cli

def main():
    # Suppose we place your absolute paths in one place:
    model_cfg = "/Users/huy/Desktop/training/F5-TTS/src/f5_tts/configs/F5TTS_Base_train.yaml"
    ckpt_file = "/Users/huy/Desktop/training/F5-TTS/ckpts/F5TTS_Base_vocos_custom_my_speak_custom/model_last.pt"
    vocab_file = "/Users/huy/Desktop/training/F5-TTS/data/my_speak_custom_custom/vocab.txt"

    speak_text_cli(
        "Hello! I'm Tracy, your voice assistant. How can I help you today?",
        model_name="F5-TTS",
        model_cfg=model_cfg,
        ckpt_file=ckpt_file,
        vocab_file=vocab_file
    )

    user_input = recognize_speech()
    if user_input.lower() in ["exit", "quit", "bye"]:
        speak_text_cli("Goodbye!", model_cfg=model_cfg, ckpt_file=ckpt_file, vocab_file=vocab_file)
        return

    intent = identify_intent(user_input)

    if intent == "weather":
        info = get_weather(40.7128, -74.0060)
        speak_text_cli(info, model_cfg=model_cfg, ckpt_file=ckpt_file, vocab_file=vocab_file)
    elif intent == "joke":
        speak_text_cli(get_joke_api(), model_cfg=model_cfg, ckpt_file=ckpt_file, vocab_file=vocab_file)
    else:
        speak_text_cli("Let me check my knowledge base...", model_cfg=model_cfg, ckpt_file=ckpt_file, vocab_file=vocab_file)

if __name__ == "__main__":
    main()


# from stt import recognize_speech
# from intent_recognition import identify_intent
# from weather import get_weather
# from jokes_pro import get_joke_api
# from tts import MyDirectTTS

# def main():
#     tts = MyDirectTTS(
#         ckpt_file="/Users/huy/Desktop/training/F5-TTS/ckpts/F5TTS_Base_vocos_custom_my_speak_custom/model_last.pt",
#         vocab_file="/Users/huy/Desktop/training/F5-TTS/data/my_speak_custom_custom/vocab.txt",
#         device="cpu"
#     )

#     tts.speak_text_direct("Hello! I'm Tracy, your direct-load TTS. How can I help you?")

#     user_input = recognize_speech()
#     if user_input.lower() in ["exit", "quit", "bye"]:
#         tts.speak_text_direct("Goodbye!")
#         return

#     intent = identify_intent(user_input)
#     if intent == "weather":
#         info = get_weather(40.7128, -74.0060)
#         tts.speak_text_direct(info)
#     elif intent == "joke":
#         tts.speak_text_direct(get_joke_api())
#     else:
#         tts.speak_text_direct("Let me check my knowledge base...")

# if __name__ == "__main__":
#     main()