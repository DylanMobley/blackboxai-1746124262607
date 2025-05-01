# backend/core/emotion_core.py

import logging
from transformers import BertForSequenceClassification, BertTokenizer
from transformers import Trainer, TrainingArguments
import torch
from emotion_core.llm_reranker import select_best_response
from emotion_core.modifier_engine import apply_modifiers
from emotion_core.filter_engine import apply_response_filters

logger = logging.getLogger("EmotionCore")

class EmotionRecognitionModel:
    """
    A class to handle emotion recognition and fine-tuning of models for emotional context.
    """
    def __init__(self, model_name="bert-base-uncased", num_labels=6):
        self.model = BertForSequenceClassification.from_pretrained(model_name, num_labels=num_labels)
        self.tokenizer = BertTokenizer.from_pretrained(model_name)
    
    def predict_emotion(self, text: str) -> str:
        """
        Predict the emotion from the given text.
        """
        inputs = self.tokenizer(text, return_tensors="pt", padding=True, truncation=True)
        with torch.no_grad():
            outputs = self.model(**inputs)
        logits = outputs.logits
        predicted_class = torch.argmax(logits, dim=-1).item()
        
        return self.get_emotion_label(predicted_class)
    
    def get_emotion_label(self, predicted_class: int) -> str:
        """
        Map the prediction class to an emotion label.
        """
        emotion_labels = ["joy", "anger", "sadness", "fear", "surprise", "neutral"]
        return emotion_labels[predicted_class]
    
    def fine_tune(self, train_dataset, eval_dataset):
        """
        Fine-tune the model with emotion-specific datasets.
        """
        training_args = TrainingArguments(
            output_dir="./results", 
            num_train_epochs=3, 
            per_device_train_batch_size=16,
            per_device_eval_batch_size=64,
            warmup_steps=500,
            weight_decay=0.01,
            logging_dir="./logs",
        )

        trainer = Trainer(
            model=self.model,
            args=training_args,
            train_dataset=train_dataset,
            eval_dataset=eval_dataset,
        )

        trainer.train()


def generate_emotionally_fused_response(user_input: str, esil: dict, persona: dict) -> str:
    """
    Central fusion function combining:
    - Empathy-LLM generation
    - Reranking of candidates
    - Modifier-based persona alignment
    - Filtered safety enforcement

    Args:
        user_input (str): Text from user
        esil (dict): Emotional vector/context
        persona (dict): Persona intent/style config

    Returns:
        str: Final response ready for frontend
    """
    logger.info("[Fusion] Initiating emotional fusion")

    # Build base prompt
    prompt = build_prompt(user_input, esil, persona)

    # Step 1: Generate candidates using the Empathy LLM
    candidates = []
    for i in range(3):  # Generate multiple response candidates
        try:
            completion = query_empathy_llm(prompt)
            candidates.append(completion.strip())
        except Exception as e:
            logger.warning(f"[Fusion] Generation error: {e}")

    if not candidates:
        return "[⚠️] No responses generated."

    # Step 2: Rerank and choose the best response
    best = select_best_response(candidates, esil, persona)

    # Step 3: Apply emotional tone modifier based on persona
    persona_label = persona.get("label", "soothing_ally")  # Default persona if not found
    softened = apply_modifiers(best, persona_label, esil, options=persona)

    # Step 4: Final filtering to ensure response safety and context-appropriate tone
    dominant_emotion = esil.get("dominant_emotion", "neutral")
    safe_output = apply_response_filters(softened, dominant_emotion)

    logger.info(f"[Fusion] Completed fusion pipeline for emotion='{dominant_emotion}'")
    return safe_output


def build_prompt(user_input: str, esil: dict, persona: dict) -> str:
    """
    Constructs a rich context prompt using user input, ESIL, and persona hints.

    Args:
        user_input (str): The input string
        esil (dict): ESIL vector (Emotion State Inference Layer)
        persona (dict): Persona details (tone, goal, etc.)

    Returns:
        str: LLM-friendly prompt
    """
    emotion = esil.get("dominant_emotion", "neutral")  # Default to neutral if emotion is not found
    tone = persona.get("tone", "compassionate and steady")  # Default tone
    instruction = persona.get("prompt", "Respond with care, empathy, and helpful intent.")
    
    # Add emotion-specific context to the prompt to guide the LLM in generating empathetic responses
    emotion_context = f"Emotion: {emotion}"
    if emotion == "sadness":
        emotion_context += " | Provide a calming and empathetic response to help soothe the user."
    elif emotion == "happiness":
        emotion_context += " | Respond with joy and excitement to match the user's mood."
    elif emotion == "anger":
        emotion_context += " | Respond with neutral tone to defuse tension and offer guidance."

    # Construct the full prompt that will be fed into the empathy LLM
    prompt = f"""
User Emotion: {emotion}
Tone: {tone}

Instruction: {instruction}

Emotion Context: {emotion_context}

User Input:
\"\"\"{user_input}\"\"\"
"""
    return prompt.strip()
