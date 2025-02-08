def identify_intent(user_input):
    user_input_lower = user_input.lower()
    if "weather" in user_input_lower:
        return "weather"
    elif "joke" in user_input_lower:
        return "joke"
    elif "timer" in user_input_lower:
        return "timer"
    elif "exit" in user_input_lower or "quit" in user_input_lower:
        return "exit"
    else:
        return "general"
