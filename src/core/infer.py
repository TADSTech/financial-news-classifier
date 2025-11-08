import torch
import pickle
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from huggingface_hub import hf_hub_download

# ----- Config -----
HF_MODEL_ID = "TADSTech/financial-news-classifier"

# ----- Load Model & Tokenizer ----
tokenizer = AutoTokenizer.from_pretrained(HF_MODEL_ID)
model = AutoModelForSequenceClassification.from_pretrained(HF_MODEL_ID)
model.eval()
label_encoder_path = hf_hub_download(repo_id=HF_MODEL_ID, filename="label_encoder.pkl")
with open(label_encoder_path, "rb") as f:
    label_encoder = pickle.load(f)

def predict(text: str):
    """
    Predict the sentiment of a single text input.
    
    Returns:
        label (str): Sentiment label (Bullish/Bearish/Neutral)
        confidence (float): Probability of predicted class [0.0, 1.0]
    """
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True)

    with torch.no_grad():
        outputs = model(**inputs)
        probs = torch.nn.functional.softmax(outputs.logits, dim=-1)

    pred_idx = torch.argmax(probs, dim=-1).item()
    pred_label = label_encoder.inverse_transform([pred_idx])[0]
    confidence = probs[0][pred_idx].item()

    return pred_label, confidence
