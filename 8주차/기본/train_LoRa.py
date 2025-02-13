import os
import sys
import math
import torch
import wandb
import logging
import datasets
import argparse
import evaluate
import transformers
import time

from typing import Optional
from itertools import chain
from dataclasses import dataclass, field
from datasets import load_dataset
from trl import SFTConfig, SFTTrainer, DataCollatorForCompletionOnlyLM
from transformers import (
    AutoConfig,
    AutoModelForCausalLM,
    AutoTokenizer,
    HfArgumentParser,
    Trainer,
    TrainingArguments,
    TrainerCallback,
    default_data_collator
)

from peft import get_peft_config, get_peft_model, LoraConfig, TaskType

from transformers.trainer_utils import get_last_checkpoint


def formatting_prompts_func(example):
    output_texts = []
    for i in range(len(example['instruction'])):
        text = f"### Question: {example['instruction'][i]}\n ### Answer: {example['output'][i]}"
        output_texts.append(text)
    return output_texts


# WandB 콜백 클래스 생성
class WandbLoggingCallback(TrainerCallback):
    def on_train_begin(self, args, state, control, **kwargs):
        self.start_time = time.time()  # 학습 시작 시간 기록
        print("Training Started...")

    def on_train_end(self, args, state, control, **kwargs):
        total_time = time.time() - self.start_time
        wandb.log({"Train Time (s)": total_time})
        print(f"Training Completed! Total Time: {total_time:.2f} seconds")

    def on_evaluate(self, args, state, control, metrics, **kwargs):
        if metrics:
            wandb.log({"Eval Loss": metrics.get("eval_loss", None)})

    def on_log(self, args, state, control, logs=None, **kwargs):
        if logs:
            wandb.log({
                "Train Loss": logs.get("loss", None),
                "Learning Rate": logs.get("learning_rate", None),
                "Step": state.global_step
            })
            

wandb.init(project='Hanghae99-8_basic')
wandb.run.name = 'new lora_r 256'



lora_r: int = 256
lora_dropout: float = 0.1
lora_alpha: int = 32




dataset = load_dataset("sahil2801/CodeAlpaca-20k", split="train")
split_dataset = dataset.train_test_split(test_size=0.2)

train_dataset = split_dataset['train']
val_dataset = split_dataset['test']

tokenizer = AutoTokenizer.from_pretrained("facebook/opt-350m")
model = AutoModelForCausalLM.from_pretrained("facebook/opt-350m", device_map="auto")

response_template = " ### Answer:"
collator = DataCollatorForCompletionOnlyLM(response_template, tokenizer=tokenizer)

target_modules = set()


for name, module in model.named_modules():
    if isinstance(module, torch.nn.Linear):
        names = name.split('.')
        target_modules.add(names[0] if len(names) == 1 else names[-1])

if "lm_head" in target_modules:  # needed for 16-bit
    target_modules.remove("lm_head")

target_modules = list(target_modules)

peft_config = LoraConfig(
    task_type=TaskType.CAUSAL_LM,
    inference_mode=False,
    r=lora_r,
    lora_alpha=lora_alpha,
    lora_dropout=lora_dropout,
    target_modules=target_modules
)
model = get_peft_model(model, peft_config)


training_arguments = TrainingArguments(
    output_dir="/tmp/rora_sft_result_256",
    save_total_limit=1,
    logging_steps=500,
    eval_steps=500,
    do_train=True,
    do_eval=True,
    per_device_train_batch_size=8,
    per_device_eval_batch_size=8,
    logging_strategy="steps",
    eval_strategy="steps",
    overwrite_output_dir=True,
    num_train_epochs=1
)


trainer = SFTTrainer(
    model,
    train_dataset=train_dataset,
    eval_dataset=val_dataset,
    args=SFTConfig(output_dir=training_arguments.output_dir, max_seq_length=128),
    formatting_func=formatting_prompts_func,
    data_collator=collator,
    callbacks=[WandbLoggingCallback()],
)

checkpoint = None
last_checkpoint = get_last_checkpoint(training_arguments.output_dir)  
if training_arguments.resume_from_checkpoint is not None: 
    checkpoint = training_arguments.resume_from_checkpoint
else:  
    checkpoint = last_checkpoint

train_result = trainer.train(resume_from_checkpoint=checkpoint)

trainer.save_model()

metrics = train_result.metrics
trainer.log_metrics("train", metrics)
trainer.save_metrics("train", metrics)
trainer.save_state()

# Max Alloc 값 계산 및 출력
max_alloc = round(torch.cuda.max_memory_allocated(0) / 1024**3, 1)
print('Max Alloc:', max_alloc, 'GB')

# WandB에 Max Alloc 기록
wandb.log({"Max Alloc (GB)": max_alloc})

# Max Alloc 값을 metrics에 추가 후 저장
metrics["max_alloc_gb"] = max_alloc
trainer.save_metrics("train", metrics)