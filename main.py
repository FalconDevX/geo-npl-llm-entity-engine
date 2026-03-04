import json
import requests
from functions import search_place_by_name
from qwen_chat import qwen_generate
import re

tools = [
    {
        "type": "function",
        "function": {
            "name": "search_place_by_name",
            "description": "Wyszukuje kod terytorialny (kod TERYT) dla podanej nazwy miejscowości lub miejsca - stosuj zawsze gdy jest pytanie o jakiekolwiek miejsce.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Nazwa miejscowości, np. Warszawa"}
                },
                "required": ["query"]
            }
        }
    }
]

while True:
    user_input = input("Enter your message: ")

    if user_input.lower() in ["exit", "quit"]:
        break

    response = qwen_generate(user_input)

    try:
        match = re.search(r'(\{.*\})', response, re.DOTALL)
        if match:
            data = json.loads(match.group(1))

            if "name" in data:       
                for tool in tools:
                    if data["name"] == tool["function"]["name"]:
                        teryt = search_place_by_name(data["arguments"]["query"])

                        print(f" Asystent: {response}")
                        print(f"Kod TERYT: {teryt}")
                        break
                else:
                    print(f" Asystent: {response}")
            else:
                print(f" Asystent: {response}")
        else:
            print(f" Asystent: {response}")

    except json.JSONDecodeError as e:
        print(f"JSON decode error: {e}")
        print(f" Asystent: {response}")