from typing import Dict, Any

class ModelConfig:
    DEFAULT_MODELS = {
        "codegen": {
            "name": "Salesforce/codegen-350M-mono",
            "type": "code_generation",
            "description": "Code generation model from Salesforce",
            "max_length": 512
        },
        "gpt2": {
            "name": "gpt2",
            "type": "general",
            "description": "General purpose GPT-2 model",
            "max_length": 1024
        }
    }
    
    MODEL_PARAMS = {
        "temperature_range": [0.1, 1.0],
        "max_length_range": [50, 2048],
        "default_max_length": 100,
        "default_temperature": 0.7
    }
    
    @classmethod
    def get_model_config(cls, model_name: str) -> Dict[str, Any]:
        return cls.DEFAULT_MODELS.get(model_name, {})
    
    @classmethod
    def get_available_models(cls) -> list:
        return list(cls.DEFAULT_MODELS.keys())