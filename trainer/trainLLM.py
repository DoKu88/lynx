import json
from datasets import Dataset
from transformers import T5Tokenizer, T5ForConditionalGeneration, TrainingArguments, Trainer

# Load your custom dataset
with open('data.json') as f:
    data = json.load(f)

# Convert to Hugging Face Dataset
dataset = Dataset.from_dict({"text": [item["text"] for item in data], "summary": [item["summary"] for item in data]})

# Split into train and validation sets
split_datasets = dataset.train_test_split(test_size=0.1)
train_dataset = split_datasets['train']
val_dataset = split_datasets['test']

# Initialize the tokenizer
model_name = 't5-small'
tokenizer = T5Tokenizer.from_pretrained(model_name)

# Preprocess the dataset
def preprocess_function(examples):
    inputs = [doc for doc in examples['text']]
    model_inputs = tokenizer(inputs, max_length=512, truncation=True, padding="max_length")

    # Setup the tokenizer for targets
    with tokenizer.as_target_tokenizer():
        labels = tokenizer(examples['summary'], max_length=150, truncation=True, padding="max_length")

    model_inputs["labels"] = labels["input_ids"]
    return model_inputs

# Tokenize the datasets
tokenized_train_dataset = train_dataset.map(preprocess_function, batched=True)
tokenized_val_dataset = val_dataset.map(preprocess_function, batched=True)

# Load the T5 model
model = T5ForConditionalGeneration.from_pretrained(model_name)

# Define the training arguments
training_args = TrainingArguments(
    output_dir='./results',
    evaluation_strategy="epoch",
    learning_rate=5e-5,
    per_device_train_batch_size=8,
    per_device_eval_batch_size=8,
    num_train_epochs=3,
    weight_decay=0.01,
)

# Initialize the Trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_train_dataset,
    eval_dataset=tokenized_val_dataset,
)

# Train the model
trainer.train()

# Save the model and tokenizer
model.save_pretrained('./fine-tuned-t5')
tokenizer.save_pretrained('./fine-tuned-t5')
