import torch
import transformers
from transformers import AutoModel, AutoTokenizer
import os
import json

class ModelManager:
    def __init__(self, model_dir: str = "./models"):
        self.model_dir = model_dir
        self.loaded_models = {}
        os.makedirs(model_dir, exist_ok=True)
    
    def load_transformer_model(self, model_name: str, model_type: str = "codegen"):
        if model_name in self.loaded_models:
            return self.loaded_models[model_name]
        
        try:
            if model_type == "codegen":
                tokenizer = AutoTokenizer.from_pretrained(model_name)
                model = AutoModel.from_pretrained(model_name)
            else:
                tokenizer = AutoTokenizer.from_pretrained(model_name)
                model = AutoModel.from_pretrained(model_name)
            
            self.loaded_models[model_name] = {
                'model': model,
                'tokenizer': tokenizer,
                'type': model_type
            }
            
            return self.loaded_models[model_name]
        
        except Exception as e:
            print(f"Error loading model {model_name}: {str(e)}")
            return None
    
    def save_model(self, model_name: str, local_name: str):
        if model_name in self.loaded_models:
            model_info = self.loaded_models[model_name]
            save_path = os.path.join(self.model_dir, local_name)
            
            model_info['model'].save_pretrained(save_path)
            model_info['tokenizer'].save_pretrained(save_path)
            
            return save_path
        return None
    
    def get_available_models(self) -> List[str]:
        return list(self.loaded_models.keys())
    
    def unload_model(self, model_name: str):
        if model_name in self.loaded_models:
            del self.loaded_models[model_name]
            torch.cuda.empty_cache()
    
    def optimize_model(self, model_name: str, optimization_level: int = 1):
        if model_name not in self.loaded_models:
            return False
        
        model_info = self.loaded_models[model_name]
        model = model_info['model']
        
        if optimization_level >= 1:
            model.half()
        
        if optimization_level >= 2:
            model = torch.jit.script(model)
        
        model_info['model'] = model
        return True