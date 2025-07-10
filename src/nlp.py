def generateResponse(text):
    #only for testing so no actual integration for now
    if "cupcake" in text.lower():
        return "I love cupcakes too! They're delicious and fun to decorate."
    elif "weather" in text.lower():
        return "The weather is always changing, isn't it? Do you prefer sunny days or rainy ones?"
    elif "music" in text.lower():
        return "Music is a universal language! What genre do you enjoy the most?"
    elif "movies" in text.lower():
        return "Movies are a great way to tell stories. Do you have a favorite genre or director?"
    elif "hello" in text.lower():
        return "Hello! This is Veena from CareSecure Insurance. How can I assist you today?"
    else:
        return "I'm not sure how to respond to that. Can you tell me more about what you're interested in?"