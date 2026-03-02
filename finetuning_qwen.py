import torch
from datasets import load_dataset
from transformers import AutoTokenizer, AutoModelForCausalLM, TrainingArguments
from peft import LoraConfig, get_peft_model
from trl import SFTTrainer

model_name = "Qwen/Qwen2.5-7B-Instruct"

#tokenizer
tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)

#model
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    torch_dtype=torch.float16
).cuda()

#lora config
peft_config = LoraConfig(
    r=16,
    lora_alpha=32,
    target_modules=["q_proj", "v_proj"],
    lora_dropout=0.05,
    bias="none",
    task_type="CAUSAL_LM"
)

model = get_peft_model(model, peft_config)

# dataset
dataset = load_dataset("json", data_files="train.json")

# messages to text conversion
def format_chat(example):
    example["text"] = tokenizer.apply_chat_template(
        example["messages"],
        tokenize=False
    )
    return example

dataset = dataset.map(format_chat)

training_args = TrainingArguments(
    output_dir="./qwen-gis-lora",
    per_device_train_batch_size=2,
    gradient_accumulation_steps=4,
    num_train_epochs=3,
    learning_rate=2e-4,
    fp16=True,
    logging_steps=10,
    save_strategy="epoch"
)

trainer = SFTTrainer(
    model=model,
    train_dataset=dataset["train"],
    args=training_args,
    processing_class=tokenizer,
)

trainer.train()
trainer.save_model("./qwen-gis-lora")