#change from train.json all function to name
import json

with open('train.json', 'r') as f:
    data = json.load(f)

for item in data:
    for message in item['messages']:
        if message['role'] == 'assistant' and 'function' in message['content']:
            message['content'] = message['content'].replace('function', 'name')

with open('train.json', 'w') as f:
    json.dump(data, f, indent=4)