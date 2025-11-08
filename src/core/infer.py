import torch
import pickle
import logging
from typing import Tuple, List, Dict, Union
from pathlib import Path
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from huggingface_hub import hf_hub_download
import os

logger = logging.getLogger(__name__)

# ----- Config -----
HF_MODEL_ID = "TADSTech/financial-news-classifier"
LOCAL_MODEL_PATH = Path(__file__).parent.parent / "model" / "saved" / "finbert"
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
MAX_LENGTH = 512
BATCH_SIZE = 32


def check_local_model() -> bool:
    """
    Check if a local model is available at src/model/saved/finbert.
    
    Returns:
        bool: True if local model files exist, False otherwise
    """
    if not LOCAL_MODEL_PATH.exists():
        return False
    
    # Check for required model files
    required_files = ["config.json"]
    return all((LOCAL_MODEL_PATH / f).exists() for f in required_files)


def get_label_encoder_path() -> Path:
    """
    Get the path to label encoder, checking local first.
    
    Returns:
        Path: Path to label encoder file
    """
    local_encoder = LOCAL_MODEL_PATH / "label_encoder.pkl"
    if local_encoder.exists():
        return local_encoder
    return None


class ModelLoader:
    """Singleton model loader for efficiency."""
    _instance = None
    _model = None
    _tokenizer = None
    _label_encoder = None
    _device = DEVICE
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ModelLoader, cls).__new__(cls)
        return cls._instance
    
    @classmethod
    def load_model(cls, model_id: str = HF_MODEL_ID, device: str = None):
        """Load model, tokenizer, and label encoder."""
        if device:
            cls._device = torch.device(device)
        
        try:
            if cls._model is None:
                # Try to load from local path first
                use_local = False
                if check_local_model():
                    logger.info(f"Local model found at {LOCAL_MODEL_PATH}")
                    model_id = str(LOCAL_MODEL_PATH)
                    use_local = True
                else:
                    logger.info(f"Local model not found, using HuggingFace: {model_id}")
                
                logger.info(f"Loading model from {model_id} on {cls._device}")
                cls._tokenizer = AutoTokenizer.from_pretrained(model_id)
                cls._model = AutoModelForSequenceClassification.from_pretrained(model_id)
                cls._model.to(cls._device)
                cls._model.eval()
                
                # Load label encoder
                if use_local:
                    label_encoder_path = get_label_encoder_path()
                    if not label_encoder_path:
                        raise FileNotFoundError("label_encoder.pkl not found in local model directory")
                    logger.info(f"Loading label encoder from local: {label_encoder_path}")
                else:
                    label_encoder_path = hf_hub_download(
                        repo_id=model_id, 
                        filename="label_encoder.pkl"
                    )
                    logger.info(f"Downloaded label encoder from HuggingFace")
                
                with open(label_encoder_path, "rb") as f:
                    cls._label_encoder = pickle.load(f)
                
                logger.info("Model loaded successfully")
                
        except Exception as e:
            logger.error(f"Error loading model: {str(e)}")
            raise RuntimeError(f"Failed to load model: {str(e)}")
        
        return cls._model, cls._tokenizer, cls._label_encoder
    
    @classmethod
    def get_model(cls):
        """Get loaded model (lazy load if needed)."""
        if cls._model is None:
            cls.load_model()
        return cls._model, cls._tokenizer, cls._label_encoder, cls._device


def predict(text: str) -> Dict[str, Union[str, float]]:
    """
    Predict sentiment of a single text input.
    
    Args:
        text (str): Input text to classify
        
    Returns:
        Dict with keys:
            - 'sentiment': Sentiment label (str)
            - 'confidence': Confidence score (float, 0-1)
            - 'scores': Dict of all class probabilities
            
    Raises:
        ValueError: If text is empty or invalid
        RuntimeError: If model inference fails
    """
    # Validate input
    if not isinstance(text, str):
        raise ValueError("Text must be a string")
    
    text = text.strip()
    if not text:
        raise ValueError("Text cannot be empty")
    
    if len(text) > 5000:
        logger.warning(f"Text is very long ({len(text)} chars), may be truncated")
    
    try:
        model, tokenizer, label_encoder, device = ModelLoader.get_model()
        
        # Tokenize
        inputs = tokenizer(
            text,
            return_tensors="pt",
            truncation=True,
            padding=True,
            max_length=MAX_LENGTH
        )
        inputs = {k: v.to(device) for k, v in inputs.items()}
        
        # Inference
        with torch.no_grad():
            outputs = model(**inputs)
            probs = torch.nn.functional.softmax(outputs.logits, dim=-1)
        
        # Get predictions
        pred_idx = torch.argmax(probs, dim=-1).item()
        pred_label = label_encoder.inverse_transform([pred_idx])[0]
        confidence = probs[0][pred_idx].item()
        
        # Get all class probabilities
        all_probs = probs[0].cpu().numpy()
        scores = {
            label_encoder.inverse_transform([i])[0]: float(prob)
            for i, prob in enumerate(all_probs)
        }
        
        return {
            'sentiment': str(pred_label),
            'confidence': round(confidence, 4),
            'scores': scores
        }
        
    except Exception as e:
        logger.error(f"Error during inference: {str(e)}")
        raise RuntimeError(f"Prediction failed: {str(e)}")


def predict_batch(texts: List[str], batch_size: int = BATCH_SIZE) -> List[Dict]:
    """
    Predict sentiment for multiple texts efficiently.
    
    Args:
        texts (List[str]): List of texts to classify
        batch_size (int): Batch size for processing
        
    Returns:
        List[Dict]: List of prediction results
        
    Raises:
        ValueError: If texts list is empty
    """
    if not texts:
        raise ValueError("Texts list cannot be empty")
    
    if not isinstance(texts, list):
        raise ValueError("Texts must be a list")
    
    # Filter valid texts
    valid_texts = [str(t).strip() for t in texts if t]
    if not valid_texts:
        raise ValueError("No valid texts found")
    
    logger.info(f"Processing {len(valid_texts)} texts in batches of {batch_size}")
    
    try:
        model, tokenizer, label_encoder, device = ModelLoader.get_model()
        results = []
        
        # Process in batches
        for i in range(0, len(valid_texts), batch_size):
            batch = valid_texts[i:i + batch_size]
            
            # Tokenize batch
            inputs = tokenizer(
                batch,
                return_tensors="pt",
                truncation=True,
                padding=True,
                max_length=MAX_LENGTH
            )
            inputs = {k: v.to(device) for k, v in inputs.items()}
            
            # Inference
            with torch.no_grad():
                outputs = model(**inputs)
                probs = torch.nn.functional.softmax(outputs.logits, dim=-1)
            
            # Extract predictions
            pred_indices = torch.argmax(probs, dim=-1).cpu().numpy()
            confidences = torch.max(probs, dim=-1)[0].cpu().numpy()
            
            for j, (text, pred_idx, conf) in enumerate(zip(batch, pred_indices, confidences)):
                pred_label = label_encoder.inverse_transform([pred_idx])[0]
                results.append({
                    'text': text,
                    'sentiment': str(pred_label),
                    'confidence': round(float(conf), 4)
                })
        
        logger.info(f"Batch processing complete: {len(results)} predictions")
        return results
        
    except Exception as e:
        logger.error(f"Error during batch inference: {str(e)}")
        raise RuntimeError(f"Batch prediction failed: {str(e)}")


def predict_with_explanations(text: str) -> Dict:
    """
    Predict sentiment with detailed score breakdown.
    
    Args:
        text (str): Input text
        
    Returns:
        Dict with detailed prediction information
    """
    result = predict(text)
    
    return {
        'text': text[:100] + "..." if len(text) > 100 else text,
        'prediction': result['sentiment'],
        'confidence': result['confidence'],
        'all_scores': result['scores'],
        'model_id': HF_MODEL_ID,
        'device': str(DEVICE)
    }


def set_device(device: str) -> None:
    """
    Set the device for inference (cpu or cuda).
    
    Args:
        device (str): 'cpu' or 'cuda'
    """
    valid_devices = ['cpu', 'cuda']
    if device not in valid_devices:
        raise ValueError(f"Device must be one of {valid_devices}")
    
    ModelLoader._device = torch.device(device)
    logger.info(f"Device set to {device}")
