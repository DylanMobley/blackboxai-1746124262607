import logging
import torch
import cv2
import numpy as np
import io

logger = logging.getLogger("VideoAdapter")

from backend.model_loader.hot_swapper import ModelHotSwapper

class VideoFeatureExtractor:
    def __init__(self, model_path: str = None, device: str = "cpu"):
        """
        Initialize video feature extraction model with hot swapper.
        """
        self.model_path = model_path
        self.device = device
        self.hot_swapper = ModelHotSwapper()
        self.model = None
        self.load_model()

    def load_model(self):
        """
        Load the video feature extraction model from the specified path using hot swapper.
        """
        try:
            logger.info(f"Loading video feature extraction model from {self.model_path} via hot swapper")
            self.hot_swapper.load_model(
                model_name="video_feature_extractor_model",
                module_path="path.to.video.feature.module",  # Replace with actual module path
                loader_function="load_model",  # Replace with actual loader function
                model_path=self.model_path,
                device=self.device
            )
            model_instance = self.hot_swapper.get_model("video_feature_extractor_model")
            if model_instance:
                self.model = model_instance
                self.model.to(self.device)
                self.model.eval()
                logger.info("Video feature extraction model loaded successfully via hot swapper")
            else:
                logger.error("Failed to get video feature extraction model instance from hot swapper")
        except Exception as e:
            logger.error(f"Failed to load video feature extraction model: {e}")
            self.model = None

    def extract_features(self, video_data: bytes) -> dict:
        """
        Extract video features from raw video data.
        
        Args:
            video_data (bytes): Raw video bytes (e.g., mp4 or avi).
        
        Returns:
            dict: Extracted video features such as facial_expression, eye_gaze, movement_intensity, affective_signal.
        """
        if self.model is None:
            logger.warning("Video model not loaded, returning default features")
            return {
                "facial_expression": "neutral",
                "eye_gaze": "center",
                "movement_intensity": 0.0,
                "affective_signal": "neutral"
            }
        try:
            # Convert bytes to numpy array for OpenCV
            video_array = np.frombuffer(video_data, np.uint8)
            cap = cv2.VideoCapture(io.BytesIO(video_data))
            frames = []
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                frames.append(frame)
            cap.release()
            # Preprocess frames as needed for model input
            # Example: take average frame or sample frames
            if not frames:
                logger.warning("No frames extracted from video data")
                return {
                    "facial_expression": "neutral",
                    "eye_gaze": "center",
                    "movement_intensity": 0.0,
                    "affective_signal": "neutral"
                }
            avg_frame = np.mean(frames, axis=0).astype(np.uint8)
            # Convert to tensor
            input_tensor = torch.from_numpy(avg_frame).permute(2, 0, 1).unsqueeze(0).float().to(self.device)
            with torch.no_grad():
                features = self.model(input_tensor)
            # Example postprocessing - adapt as per actual model output
            facial_expression = features.get("facial_expression", "neutral") if isinstance(features, dict) else "neutral"
            eye_gaze = features.get("eye_gaze", "center") if isinstance(features, dict) else "center"
            movement_intensity = features.get("movement_intensity", 0.0) if isinstance(features, dict) else 0.0
            affective_signal = features.get("affective_signal", "neutral") if isinstance(features, dict) else "neutral"
            return {
                "facial_expression": facial_expression,
                "eye_gaze": eye_gaze,
                "movement_intensity": movement_intensity,
                "affective_signal": affective_signal
            }
        except Exception as e:
            logger.error(f"Error extracting video features: {e}")
            return {
                "facial_expression": "neutral",
                "eye_gaze": "center",
                "movement_intensity": 0.0,
                "affective_signal": "neutral"
            }

# Example usage:
# extractor = VideoFeatureExtractor(model_path="path/to/video/model.pt")
# features = extractor.extract_features(video_bytes)
