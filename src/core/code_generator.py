import torch
import transformers
from typing import List, Dict, Any
import json

class CodeGenerator:
    def __init__(self, model_path: str = None):
        self.model = None
        self.tokenizer = None
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.load_model(model_path)
    
    def load_model(self, model_path: str):
        if model_path:
            self.tokenizer = transformers.AutoTokenizer.from_pretrained(model_path)
            self.model = transformers.AutoModelForCausalLM.from_pretrained(model_path)
        else:
            self.tokenizer = transformers.GPT2Tokenizer.from_pretrained("gpt2")
            self.model = transformers.GPT2LMHeadModel.from_pretrained("gpt2")
        
        self.model.to(self.device)
        self.model.eval()
    
    def generate_code(self, prompt: str, max_length: int = 100, temperature: float = 0.7) -> str:
        inputs = self.tokenizer.encode(prompt, return_tensors="pt").to(self.device)
        
        with torch.no_grad():
            outputs = self.model.generate(
                inputs,
                max_length=max_length,
                temperature=temperature,
                num_return_sequences=1,
                pad_token_id=self.tokenizer.eos_token_id,
                do_sample=True
            )
        
        generated_code = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        return generated_code
    
    def complete_function(self, function_signature: str, context: str = "") -> str:
        prompt = f"{context}\n\n{function_signature}"
        return self.generate_code(prompt)
    
    def generate_from_template(self, template: str, variables: Dict[str, str]) -> str:
        for key, value in variables.items():
            template = template.replace(f"{{{key}}}", value)
        return self.generate_code(template)