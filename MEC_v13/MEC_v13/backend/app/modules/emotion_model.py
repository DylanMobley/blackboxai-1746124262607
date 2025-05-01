import torch
from transformers import AutoModelForSequenceClassification, AutoTokenizer, AutoConfig
from transformers import AutoModel
from typing import Tuple
import numpy as np

# Optional LoRA/PEFT if enabled
try:
    from peft import PeftModel
    peft_available = True
except ImportError:
    peft_available = False

DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

class EmotionModel:
    def __init__(self, model_path="pretrained/emotion_model", use_peft=True):
        self.use_peft = use_peft and peft_available

        config = AutoConfig.from_pretrained(model_path)
        self.label_map = config.id2label if hasattr(config, "id2label") else {
            0: "joy", 1: "sadness", 2: "anger", 3: "fear", 4: "guilt", 5: "shame", 6: "neutral"
        }

        # Load base classifier
        base_model = AutoModelForSequenceClassification.from_pretrained(model_path)
        self.model = PeftModel.from_pretrained(base_model, model_path).to(DEVICE) if self.use_peft else base_model.to(DEVICE)
        self.tokenizer = AutoTokenizer.from_pretrained(model_path)

        # Load raw DistilBERT for embeddings
        self.encoder = AutoModel.from_pretrained("distilbert-base-uncased").to(DEVICE)
        self.encoder.eval()

    def classify(self, text: str) -> Tuple[str, float]:
        """ Returns predicted emotion label + confidence score """
        inputs = self.tokenizer(text, return_tensors="pt", truncation=True, padding=True).to(DEVICE)
        with torch.no_grad():
            outputs = self.model(**inputs)
            probs = torch.softmax(outputs.logits, dim=1).squeeze()
            label_id = int(torch.argmax(probs).cpu().item())
            label = self.label_map[label_id]
            confidence = round(probs[label_id].cpu().item(), 4)
            return label, confidence

    def embed(self, text: str) -> np.ndarray:
        """ Returns a pooled embedding vector (CLS) """
        inputs = self.tokenizer(text, return_tensors="pt", truncation=True, padding=True).to(DEVICE)
        with torch.no_grad():
            output = self.encoder(**inputs).last_hidden_state[:, 0, :]  # CLS token
        return output.squeeze().cpu().numpy()
