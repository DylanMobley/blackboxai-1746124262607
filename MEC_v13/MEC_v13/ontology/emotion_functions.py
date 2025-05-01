import json

class EmotionFunctionMap:
    def __init__(self, json_path: str = "ontology/emotional_functions.json"):
        with open(json_path, "r") as f:
            self.function_map = json.load(f)

    def get_function_data(self, emotion: str) -> dict:
        return self.function_map.get(emotion.lower(), {
            "function": "observe",
            "subtypes": [],
            "needs": [],
            "example": ""
        })

    def get_function(self, emotion: str) -> str:
        return self.get_function_data(emotion).get("function", "observe")

    def get_needs(self, emotion: str) -> list:
        return self.get_function_data(emotion).get("needs", [])

    def get_example(self, emotion: str) -> str:
        return self.get_function_data(emotion).get("example", "")
