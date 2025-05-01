# model_loader/hot_swapper.py

import os
import threading
import importlib
import logging
from typing import Dict, Any

logger = logging.getLogger("ModelHotSwapper")
logger.setLevel(logging.INFO)

class ModelHotSwapper:
    """
    Dynamically load and swap models at runtime without restarting system.
    """

    def __init__(self):
        self.models: Dict[str, Any] = {}
        self.locks: Dict[str, threading.Lock] = {}

    def load_model(self, model_name: str, module_path: str, loader_function: str = "load_model", **kwargs):
        """
        Load a model from specified module path dynamically.
        :param model_name: Unique identifier (e.g., "empathy-llm")
        :param module_path: Python import path (e.g., "microservices.empathy-llm.model")
        :param loader_function: Function inside module that returns the model
        :param kwargs: Extra params to pass to loader function
        """
        try:
            logger.info(f"🧠 Loading model [{model_name}] from [{module_path}]...")
            mod = importlib.import_module(module_path)
            model_loader = getattr(mod, loader_function)
            model_instance = model_loader(**kwargs)

            self.models[model_name] = model_instance
            self.locks[model_name] = threading.Lock()

            logger.info(f"✅ Model [{model_name}] loaded successfully!")

        except Exception as e:
            logger.error(f"❌ Failed to load model [{model_name}]", exc_info=True)
            raise e

    def get_model(self, model_name: str):
        """
        Thread-safe access to a model instance.
        """
        if model_name not in self.models:
            logger.error(f"❌ Model [{model_name}] not found!")
            return None
        
        with self.locks[model_name]:
            return self.models[model_name]

    def reload_model(self, model_name: str, module_path: str, loader_function: str = "load_model", **kwargs):
        """
        Hot-swap a model by reloading it dynamically.
        """
        logger.info(f"♻️ Reloading model [{model_name}]...")
        self.load_model(model_name, module_path, loader_function, **kwargs)

