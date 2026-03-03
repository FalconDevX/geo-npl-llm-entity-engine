import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from peft import PeftModel

base_model_name = "Qwen/Qwen2.5-3B-Instruct"
lora_path = "./qwen-gis-lora"

device = "cuda" if torch.cuda.is_available() else "cpu"

tokenizer = AutoTokenizer.from_pretrained(base_model_name)

base_model = AutoModelForCausalLM.from_pretrained(
    base_model_name,
    torch_dtype=torch.float16 if device == "cuda" else torch.float32
).to(device)

model = PeftModel.from_pretrained(base_model, lora_path)
model.eval()

def qwen_generate(user_input: str) -> str:

    messages = [
        {"role": "user", "content": user_input}
    ]

    text = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True
    )

    inputs = tokenizer(text, return_tensors="pt").to(device)

    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=300,
            temperature=0.7,
            top_p=0.9,
            do_sample=True
        )

    response = tokenizer.decode(outputs[0], skip_special_tokens=True)

    # opcjonalnie usuń prompt z odpowiedzi
    response = response.split("assistant")[-1].strip()

    return response