import json
from datasets import Dataset
from transformers import T5Tokenizer, T5ForConditionalGeneration, TrainingArguments, Trainer
import torch

# Load your custom dataset
with open('data.json') as f:
    data = json.load(f)

# Convert to Hugging Face Dataset

# Define the dataset
dataset = Dataset.from_dict({
                            "user": [item["user"] for item in data],
                            "text": [item["text"] for item in data], 
                            "summary": [item["summary"] for item in data]})

# Split into train and validation sets
split_datasets = dataset.train_test_split(test_size=0.1)
train_dataset = split_datasets['train']
val_dataset = split_datasets['test']

# Initialize the tokenizer
model_name = 't5-small'
tokenizer = T5Tokenizer.from_pretrained(model_name)

# Preprocess the dataset
# Add a delimiter between the user and the text and tokenize the inputs
# Delimiter added for ease of training to denote users and the text we want 
def preprocess_function(examples):
    users = [doc for doc in examples['user']]
    text = [doc for doc in examples['text']]

    userTokens = tokenizer(users, max_length=512, truncation=True, padding="max_length", return_tensors='pt')
    textTokens = tokenizer(text, max_length=512, truncation=True, padding="max_length", return_tensors='pt')

    delimiter_token = '[DELIMITER]'
    tokenizer.add_tokens([delimiter_token])
    delimiter_token_id = tokenizer.convert_tokens_to_ids(delimiter_token)

    # Concatenate user and question encodings with the delimiter token in between
    input_ids = [torch.cat([user, torch.tensor([delimiter_token_id]), text]) for user, text in zip(userTokens['input_ids'], textTokens['input_ids'])]
    attention_mask = [torch.cat([user, torch.tensor([1]), text]) for user, text in zip(userTokens['attention_mask'], textTokens['attention_mask'])]

    # The final encodings that can be used as input to the model
    final_encodings = {'input_ids': torch.stack(input_ids), 'attention_mask': torch.stack(attention_mask)}

    # Setup the tokenizer for targets
    with tokenizer.as_target_tokenizer():
        labels = tokenizer(examples['summary'], max_length=150, truncation=True, padding="max_length")

    final_encodings["labels"] = labels["input_ids"]
    return final_encodings

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
