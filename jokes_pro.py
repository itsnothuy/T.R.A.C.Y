import requests

def get_joke_api():
    joke_api = "https://official-joke-api.appspot.com/random_joke"
    r = requests.get(joke_api)
    if r.status_code == 200:
        data = r.json()
        return f"{data['setup']} ... {data['punchline']}"
    return "No jokes available at the moment."
