import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from peft import PeftModel
from tools_def import tools


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

def qwen_generate(user_input: str):
    messages = [
        {"role": "system", "content": "Jesteś pomocnikiem GIS. Masz dostęp do narzędzi. Jeśli użytkownik pyta o miejsce, użyj funkcji."},
        {"role": "user", "content": user_input}
    ]

    text = tokenizer.apply_chat_template(
        messages,
        tools=tools, 
        tokenize=False,
        add_generation_prompt=True
    )

    inputs = tokenizer(text, return_tensors="pt").to(device)

    outputs = model.generate(
        **inputs,
        max_new_tokens=512,
        temperature=0.1, 
        do_sample=False 
    )

    generated_ids = [
        output_ids[len(input_ids):] for input_ids, output_ids in zip(inputs.input_ids, outputs)
    ]
    response = tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]
    
    return response