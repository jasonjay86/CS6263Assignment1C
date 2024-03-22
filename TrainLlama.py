import os
from dataclasses import dataclass, field
from typing import Optional

import torch
from datasets import load_dataset
from datasets import load_from_disk
from peft import LoraConfig, get_peft_model
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    BitsAndBytesConfig,
    HfArgumentParser,
    AutoTokenizer,
    TrainingArguments,
)
from tqdm.notebook import tqdm

from trl import SFTTrainer
from huggingface_hub import interpreter_login
from accelerate import Accelerator

modelpath ="meta-llama/Llama-2-7b-hf"
accelerator = Accelerator()
interpreter_login()
torch.cuda.empty_cache() 
compute_dtype = getattr(torch, "float16")
bnb_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_quant_type='nf4',
        bnb_4bit_compute_dtype='float16',
        bnb_4bit_use_double_quant=False,
    )
device_map = "auto"

#Download model
model = AutoModelForCausalLM.from_pretrained(
        modelpath, 
        # quantization_config=bnb_config,
        device_map=device_map,
        trust_remote_code=True,
        use_auth_token=True
    )
print (model)
# model.config.pretraining_tp = 1
# #gradient checkpointing to save memory
# model.gradient_checkpointing_enable()

# peft_config = LoraConfig(
#     r=32,
#     lora_alpha=16,
#     target_modules=[
#     'q_proj',
#     'k_proj',
#     'v_proj',
#     'dense',
#     'fc1',
#     'fc2',
#     ],#"all-linear",
#     bias="none",
#     lora_dropout=0.05, # Conventional
#     task_type="CAUSAL_LM",
# )

# lora_model = get_peft_model(model, peft_config)

# lora_model = accelerator.prepare_model(lora_model)

# tokenizer = AutoTokenizer.from_pretrained("microsoft/phi-2", trust_remote_code=True)
# tokenizer.pad_token = tokenizer.eos_token

# training_arguments = TrainingArguments(
#     output_dir="./results",
#     per_device_train_batch_size=2,
#     per_device_eval_batch_size=2,
#     prediction_loss_only=True,
#     # gradient_accumulation_steps=4,
#     # optim="paged_adamw_32bit",
#     # save_steps=500, #CHANGE THIS IF YOU WANT IT TO SAVE LESS OFTEN. I WOULDN'T SAVE MORE OFTEN BECAUSE OF SPACE
#     # logging_steps=10,
#     # learning_rate=2e-4,
#     # fp16=False,
#     # bf16=True,
#     # max_grad_norm=.3,
#     # max_steps=10000,
#     # warmup_ratio=.03,
#     # group_by_length=True,
#     # lr_scheduler_type="constant",
# )

# lora_model.config.use_cache = False

# dataset = load_dataset("flytech/python-codes-25k", split='train').train_test_split(test_size=.001,train_size=.01)

# trainer = SFTTrainer(
#     model=lora_model,
#     # train_dataset=dataset,
#     train_dataset=dataset["train"],
#     eval_dataset=dataset["test"],
#     # peft_config=peft_config,
#     dataset_text_field="text",
#     max_seq_length=2048,
#     tokenizer=tokenizer,
#     args=training_arguments,
#     packing=False,
# )

# trainer.train()

# trainer.save_model("./FTPhi2_dev")