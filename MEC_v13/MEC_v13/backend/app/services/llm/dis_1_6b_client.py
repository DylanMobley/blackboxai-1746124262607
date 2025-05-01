import logging
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
from backend.model_loader.hot_swapper import ModelHotSwapper

logger = logging.getLogger("Dis1.6bClient")

class Dis1_6bClient:
    def __init__(self, model_name: str = "dis/1.6b", device: str = "cpu"):
        """
        Initialize Dis 1.6b LLM model with hot swapper support.
        """
        self.model_name = model_name
        self.device = device
        self.hot_swapper = ModelHotSwapper()
        self.model = None
        self.tokenizer = None
        self.load_model()

    def load_model(self):
        """
        Load the Dis 1.6b LLM model using the hot swapper.
        """
        try:
            logger.info(f"Loading Dis 1.6b LLM model via hot swapper: {self.model_name}")
            self.hot_swapper.load_model(
                model_name=self.model_name,
                module_path="transformers",
                loader_function="from_pretrained",
                pretrained_model_name_or_path=self.model_name
            )
            model_instance = self.hot_swapper.get_model(self.model_name)
            if model_instance:
                self.model = model_instance
                self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
                self.model.to(self.device)
                self.model.eval()
                logger.info("Dis 1.6b LLM model loaded successfully via hot swapper")
            else:
                logger.error("Failed to get model instance from hot swapper")
        except Exception as e:
            logger.error(f"Failed to load Dis 1.6b LLM model via hot swapper: {e}")
            self.model = None
            self.tokenizer = None

    def query(self, prompt: str, max_length: int = 256) -> str:
        """
        Query the Dis 1.6b LLM with a prompt.
        
        Args:
            prompt (str): Input prompt string.
            max_length (int): Maximum length of generated response.
        
        Returns:
            str: Generated response from the model.
        """
        if self.model is None or self.tokenizer is None:
            logger.warning("Dis 1.6b LLM model/tokenizer not loaded, returning placeholder response")
            return "[Dis 1.6b LLM response placeholder]"
        try:
            inputs = self.tokenizer(prompt, return_tensors="pt").to(self.device)
            outputs = self.model.generate(**inputs, max_length=max_length, do_sample=True, top_p=0.9, temperature=0.8)
            response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            return response
        except Exception as e:
            logger.error(f"Error querying Dis 1.6b LLM model: {e}")
            return "[Dis 1.6b LLM response error]"

# Example usage:
# client = Dis1_6bClient(model_name="dis/1.6b")
# response = client.query("Hello, how are you?")
