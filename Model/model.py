
from transformers import AutoTokenizer, AutoModelForQuestionAnswering, Trainer, TrainingArguments
from datasets import load_dataset
import torch

# Load the pretrained model and tokenizer
model_name = "deepset/bert-base-cased-squad2"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForQuestionAnswering.from_pretrained(model_name)

# Load the SQuAD dataset
dataset = load_dataset("squad")

# Tokenize the dataset
def tokenize_function(example):
    return tokenizer(
        example["question"],
        example["context"],
        truncation=True,
        padding="max_length",
        max_length=384,
        return_tensors="pt"
    )

tokenized_dataset = dataset.map(tokenize_function, batched=True)

# Define training arguments
training_args = TrainingArguments(
    output_dir="./fine_tuned_model",  # Output directory
    num_train_epochs=3,  # Number of epochs
    per_device_train_batch_size=4,  # Training batch size
    per_device_eval_batch_size=4,  # Evaluation batch size
    learning_rate=3e-5,  # Learning rate
    weight_decay=0.01,  # Weight decay
    evaluation_strategy="epoch",  # Evaluate after each epoch
    save_strategy="epoch",  # Save after each epoch
    load_best_model_at_end=True,  # Load best model at end of training
    metric_for_best_model="f1",  # Metric to track best model
    report_to="none"  # No reporting
)

# Define the compute_loss function
def compute_loss(model, inputs):
    # Extract labels from inputs
    labels_start = inputs.pop("start_positions", None)
    labels_end = inputs.pop("end_positions", None)
    
    # Forward pass
    outputs = model(**inputs)
    
    # Compute loss using CrossEntropyLoss
    loss_fct = torch.nn.CrossEntropyLoss()
    start_loss = loss_fct(outputs.start_logits, labels_start)
    end_loss = loss_fct(outputs.end_logits, labels_end)
    
    # Total loss
    return start_loss + end_loss

# Create the Trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_dataset["train"],
    eval_dataset=tokenized_dataset["validation"],
    tokenizer=tokenizer,
    compute_loss=compute_loss  # Setting the custom loss function
)

# Start training
trainer.train()

# Save the fine-tuned model
trainer.save_model()

# Load the fine-tuned model for inference
fine_tuned_model = AutoModelForQuestionAnswering.from_pretrained("./fine_tuned_model")
fine_tuned_tokenizer = AutoTokenizer.from_pretrained("./fine_tuned_model")

# Example inference
context = "Your text context here"
question = "Your question here"
inputs = fine_tuned_tokenizer(question, context, return_tensors="pt")
outputs = fine_tuned_model(**inputs)
answer_start = outputs.start_logits.argmax()
answer_end = outputs.end_logits.argmax()
answer = fine_tuned_tokenizer.convert_tokens_to_string(
    fine_tuned_tokenizer.convert_ids_to_tokens(inputs["input_ids"][0][answer_start:answer_end + 1])
)
print("Answer:", answer)
