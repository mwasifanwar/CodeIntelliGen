from typing import List, Dict, Any
from ..core.code_generator import CodeGenerator

class CodeCompleter:
    def __init__(self, model_path: str = None):
        self.generator = CodeGenerator(model_path)
        self.context_window = 1000
    
    def complete_line(self, partial_code: str, language: str = "python") -> List[str]:
        prompts = [
            f"Complete this {language} code:\n{partial_code}",
            f"Finish this {language} line:\n{partial_code}",
            f"Continue writing {language} code:\n{partial_code}"
        ]
        
        completions = []
        for prompt in prompts:
            completion = self.generator.generate_code(prompt, max_length=50, temperature=0.3)
            completions.append(completion.replace(prompt, "").strip())
        
        return completions
    
    def suggest_imports(self, code: str, language: str = "python") -> List[str]:
        prompt = f"Based on this {language} code, what imports are needed?\n{code}\n\nImports:"
        
        response = self.generator.generate_code(prompt, max_length=100, temperature=0.1)
        imports = [imp.strip() for imp in response.split('\n') if imp.strip()]
        
        return imports
    
    def refactor_code(self, code: str, language: str = "python") -> str:
        prompt = f"Refactor this {language} code to be more efficient and readable:\n\n{code}\n\nRefactored code:"
        
        refactored = self.generator.generate_code(prompt, max_length=500, temperature=0.2)
        return refactored
    
    def generate_boilerplate(self, project_type: str, language: str = "python") -> str:
        prompt = f"Generate {language} boilerplate code for a {project_type} project. Include proper structure and comments."
        
        boilerplate = self.generator.generate_code(prompt, max_length=300, temperature=0.1)
        return boilerplate