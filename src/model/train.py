from sklearn.preprocessing import LabelEncoder
from tqdm.auto import tqdm
import os
import pandas as pd
from sklearn.model_selection import train_test_split
import torch
from torch.utils.data import Dataset, DataLoader
from transformers import DistilBertTokenizerFast, DistilBertForSequenceClassification, Trainer, TrainingArguments

# --------- Config ---------
CSV_PATH = "data/processed/train.csv"  # path to processed CSV
MODEL_SAVE_PATH = "src/model/saved/finbert"
MAX_LEN = 64
BATCH_SIZE = 32
EPOCHS = 3
# -------------------------

# Load CSV
df = pd.read_csv(CSV_PATH)
texts = df["text"].tolist()
labels = df["label_name"].tolist()

# Encode labels to integers
le = LabelEncoder()
labels_enc = le.fit_transform(labels)

# Save label encoder for inference
import pickle
os.makedirs(MODEL_SAVE_PATH, exist_ok=True)
with open(os.path.join(MODEL_SAVE_PATH, "label_encoder.pkl"), "wb") as f:
    pickle.dump(le, f)

# Split train/validation
train_texts, val_texts, train_labels, val_labels = train_test_split(
    texts, labels_enc, test_size=0.2, random_state=42, stratify=labels_enc
)

# Tokenizer
tokenizer = DistilBertTokenizerFast.from_pretrained("distilbert-base-uncased")

# Function to tokenize a list of texts and show progress with tqdm
def tokenize_and_encode(texts, tokenizer, max_len, desc):
    """Tokenizes text list and returns input_ids and attention_mask lists."""
    tokenized_data = {'input_ids': [], 'attention_mask': []}
    
    # Use tqdm to show a progress bar for the tokenization process
    for text in tqdm(texts, desc=desc):
        encoding = tokenizer(
            str(text),
            truncation=True,
            padding="max_length",
            max_length=max_len,
        )
        # Store as lists of integers, which will be converted to tensors in Dataset
        tokenized_data['input_ids'].append(encoding['input_ids'])
        tokenized_data['attention_mask'].append(encoding['attention_mask'])
        
    return tokenized_data

# ----------------------------------------------------
# Pre-tokenize all data using the new function with tqdm
# ----------------------------------------------------

print("Tokenizing Training Data...")
train_encodings = tokenize_and_encode(
    train_texts, tokenizer, MAX_LEN, desc="Tokenizing Train Data"
)
print("Tokenizing Validation Data...")
val_encodings = tokenize_and_encode(
    val_texts, tokenizer, MAX_LEN, desc="Tokenizing Val Data"
)


class FinanceDataset(Dataset):
    # Updated to accept pre-tokenized inputs
    def __init__(self, encodings, labels):
        self.encodings = encodings
        self.labels = labels

    def __len__(self):
        return len(self.labels)

    def __getitem__(self, idx):
        # Access pre-tokenized inputs and convert to PyTorch tensors
        return {
            "input_ids": torch.tensor(self.encodings["input_ids"][idx], dtype=torch.long),
            "attention_mask": torch.tensor(self.encodings["attention_mask"][idx], dtype=torch.long),
            "labels": torch.tensor(self.labels[idx], dtype=torch.long)
        }

# Create datasets (passing encodings directly)
train_dataset = FinanceDataset(train_encodings, train_labels)
val_dataset = FinanceDataset(val_encodings, val_labels)

# Load model
model = DistilBertForSequenceClassification.from_pretrained(
    "distilbert-base-uncased",
    num_labels=len(le.classes_)
)

# Training arguments
training_args = TrainingArguments(
    output_dir=MODEL_SAVE_PATH,
    num_train_epochs=EPOCHS,
    per_device_train_batch_size=BATCH_SIZE,
    per_device_eval_batch_size=BATCH_SIZE,
    eval_strategy="steps",      # <-- Renamed from evaluation_strategy
    save_strategy="steps",      # <-- Renamed from save_strategy
    eval_steps=100,
    save_steps=100,
    save_total_limit=2,
    logging_dir=f"{MODEL_SAVE_PATH}/logs",
    logging_steps=50,
    load_best_model_at_end=True,
    metric_for_best_model="accuracy",
    report_to="none",
)

# Metrics
import numpy as np
from sklearn.metrics import accuracy_score, f1_score

def compute_metrics(pred):
    labels = pred.label_ids
    preds = np.argmax(pred.predictions, axis=1)
    acc = accuracy_score(labels, preds)
    f1 = f1_score(labels, preds, average="weighted")
    return {"accuracy": acc, "f1": f1}

# Trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=val_dataset,
    tokenizer=tokenizer,
    compute_metrics=compute_metrics
)

# Train
model.gradient_checkpointing_enable()
model.is_parallelizable = True
model.model_parallel = True
trainer.train()


# Save model + tokenizer
trainer.save_model(MODEL_SAVE_PATH)
tokenizer.save_pretrained(MODEL_SAVE_PATH)

print(f"✅ Model trained and saved to {MODEL_SAVE_PATH}")