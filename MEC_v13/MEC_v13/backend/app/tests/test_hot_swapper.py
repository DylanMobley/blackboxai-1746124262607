import pytest
from backend.model_loader.hot_swapper import ModelHotSwapper

def test_load_and_get_model():
    hot_swapper = ModelHotSwapper()
    # Use a simple module for testing, e.g., math
    hot_swapper.load_model("math_model", "math", "sqrt")
    model = hot_swapper.get_model("math_model")
    assert model is not None
    assert callable(model)

def test_reload_model():
    hot_swapper = ModelHotSwapper()
    hot_swapper.load_model("math_model", "math", "sqrt")
    hot_swapper.reload_model("math_model", "math", "sqrt")
    model = hot_swapper.get_model("math_model")
    assert model is not None
    assert callable(model)
