import json
import requests
from qwen_chat import qwen_generate

while True:
    user_input = input("Enter your message: ")
    response = qwen_generate(user_input)
    response_data = json.loads(response)

    print("Catched query: ", response_data["arguments"]["query"])

    query = response_data["arguments"]["query"]
    response = requests.get(f"http://localhost:8000/search?q={query}")
    data = response.json()


    print("Miejsce: ", query)
    print("Kod teryt : ", data[0]["kod"])

    if user_input.lower() in ["exit", "quit"]:
        print("bye")
        break