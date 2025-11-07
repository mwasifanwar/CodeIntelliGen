import ast
from typing import List, Dict, Any
from ..core.code_generator import CodeGenerator

class DocumentationGenerator:
    def __init__(self, model_path: str = None):
        self.generator = CodeGenerator(model_path)
    
    def generate_docstring(self, code: str, language: str = "python") -> str:
        if language == "python":
            return self._generate_python_docstring(code)
        else:
            return self._generate_generic_docstring(code, language)
    
    def _generate_python_docstring(self, code: str) -> str:
        try:
            tree = ast.parse(code)
            
            for node in ast.walk(tree):
                if isinstance(node, (ast.FunctionDef, ast.ClassDef, ast.Module)):
                    prompt = f"Generate a comprehensive docstring for this Python code:\n\n{ast.get_docstring(node) or code}\n\nDocstring:"
                    
                    docstring = self.generator.generate_code(prompt, max_length=200, temperature=0.1)
                    return docstring.strip()
        
        except:
            pass
        
        prompt = f"Generate a docstring for this code:\n\n{code}\n\nDocstring:"
        docstring = self.generator.generate_code(prompt, max_length=200, temperature=0.1)
        return docstring.strip()
    
    def _generate_generic_docstring(self, code: str, language: str) -> str:
        prompt = f"Generate documentation comments for this {language} code:\n\n{code}\n\nDocumentation:"
        
        documentation = self.generator.generate_code(prompt, max_length=200, temperature=0.1)
        return documentation.strip()
    
    def generate_readme(self, project_structure: Dict[str, Any], language: str = "python") -> str:
        structure_str = "\n".join([f"- {item}" for item in project_structure.get('files', [])])
        
        prompt = f"""Generate a comprehensive README.md file for a {language} project with the following structure:

{structure_str}

Project description: {project_structure.get('description', 'A software project')}

Include sections for:
- Installation
- Usage
- Features
- Configuration
- Contributing
- License

README.md:"""
        
        readme = self.generator.generate_code(prompt, max_length=500, temperature=0.1)
        return readme
    
    def generate_api_documentation(self, code: str, language: str = "python") -> str:
        prompt = f"""Generate API documentation for this {language} code:

{code}

Include:
- Endpoint descriptions
- Request/Response formats
- Parameters
- Examples

API Documentation:"""
        
        api_docs = self.generator.generate_code(prompt, max_length=400, temperature=0.1)
        return api_docs